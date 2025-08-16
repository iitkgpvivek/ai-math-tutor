"""
Base agent class for the AI Math Tutor application.

This module defines the base Agent class that provides common functionality
for all agents in the system, including LLM integration, logging, and configuration.
"""

import logging
from typing import Dict, Any, Optional, List, Union, Callable, Awaitable
import json
import os
import asyncio
from dataclasses import dataclass
from enum import Enum
import aiohttp

class AgentRole(str, Enum):
    """Defines the role of the agent in the system."""
    STUDENT = "student"
    TUTOR = "tutor"
    EVALUATOR = "evaluator"
    GENERATOR = "generator"

@dataclass
class Message:
    """A message in the agent's conversation."""
    role: str  # 'user', 'assistant', 'system', etc.
    content: str
    metadata: Optional[Dict[str, Any]] = None

class Agent:
    """
    Base class for all agents in the AI Math Tutor system.
    
    This class provides common functionality and interface that all agents
    should implement.
    """
    
    def __init__(
        self, 
        agent_id: str, 
        role: AgentRole = AgentRole.STUDENT,
        config: Optional[Dict[str, Any]] = None,
        llm_endpoint: Optional[str] = None,
        llm_headers: Optional[Dict[str, str]] = None,
        **kwargs
    ):
        """
        Initialize the agent with a unique ID and optional configuration.
        
        Args:
            agent_id: A unique identifier for this agent instance
            config: Optional configuration dictionary for the agent
            role: The role of this agent in the system
            llm_endpoint: Optional custom LLM endpoint
            llm_headers: Optional headers for LLM API requests
        """
        self.agent_id = agent_id
        self.role = role
        self.config = config or {}
        self.logger = self._setup_logging()
        self.state = {}
        self.conversation_history: List[Message] = []
        
        # LLM configuration for local Ollama server
        self.llm_endpoint = llm_endpoint or "http://localhost:11434/api/generate"
        self.llm_headers = llm_headers or {"Content-Type": "application/json"}
        self.llm_model = self.config.get("llm_model", "mistral")
        self.llm_temperature = float(self.config.get("llm_temperature", 0.7))
        
        self.logger.info(f"Initialized {self.__class__.__name__} with ID: {agent_id}, Role: {role.value}")
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(f"{self.__class__.__name__}.{self.agent_id}")
        logger.setLevel(logging.DEBUG)
        
        # Create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        
        # Add the handler to the logger
        if not logger.handlers:
            logger.addHandler(ch)
        
        return logger
    
    async def process_message(self, message: Union[Dict[str, Any], Message]) -> Dict[str, Any]:
        """
        Process an incoming message and return a response.
        
        This method should be implemented by subclasses to define agent-specific
        message handling logic.
        
        Args:
            message: The incoming message to process (can be dict or Message object)
            
        Returns:
            A response message
        """
        # Convert dict to Message if needed
        if isinstance(message, dict):
            message = Message(
                role=message.get("role", "user"),
                content=message.get("content", ""),
                metadata=message.get("metadata")
            )
        
        # Add to conversation history
        self.conversation_history.append(message)
        
        # Let subclasses handle the actual processing
        response = await self._process_message_impl(message)
        
        # Add assistant response to history
        if response:
            response_msg = Message(
                role="assistant",
                content=response.get("content", ""),
                metadata=response.get("metadata")
            )
            self.conversation_history.append(response_msg)
        
        return response or {"content": "I'm not sure how to respond to that.", "status": "error"}
    
    async def _process_message_impl(self, message: Message) -> Dict[str, Any]:
        """
        Internal implementation of message processing.
        Subclasses should override this method instead of process_message.
        """
        raise NotImplementedError("Subclasses must implement _process_message_impl")
    
    async def generate_with_llm(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: int = 1000,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a response using the configured LLM.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to guide the LLM
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            json_mode: Whether to expect a JSON response
            
        Returns:
            Dictionary containing the generated response and metadata
        """
        if temperature is None:
            temperature = self.llm_temperature
            
        # Prepare the prompt with system message if provided
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        payload = {
            "model": self.llm_model,
            "prompt": full_prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        if json_mode:
            payload["format"] = "json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.llm_endpoint,
                    headers=self.llm_headers,
                    json=payload,
                    timeout=60
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    # Extract the response content from Ollama API
                    if 'response' in result:
                        return {
                            'content': result['response'],
                            'model': result.get('model', self.llm_model),
                            'usage': {
                                'prompt_tokens': result.get('prompt_eval_count', 0),
                                'completion_tokens': result.get('eval_count', 0),
                                'total_tokens': (result.get('prompt_eval_count', 0) + 
                                               result.get('eval_count', 0))
                            }
                        }
                    else:
                        self.logger.error(f"Unexpected response format: {result}")
                        return {'content': "I'm having trouble generating a response right now.", 'error': 'invalid_format'}
        except Exception as e:
            self.logger.error(f"Error generating with LLM: {str(e)}")
            return {
                "content": "I'm having trouble generating a response right now.",
                "error": str(e),
                "status": "error"
            }
    
    def save_state(self, file_path: str) -> None:
        """
        Save the agent's state to a file.
        
        Args:
            file_path: Path to save the state file
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(self.state, f, indent=2)
        self.logger.info(f"Saved state to {file_path}")
    
    def load_state(self, file_path: str) -> None:
        """
        Load the agent's state from a file.
        
        Args:
            file_path: Path to the state file to load
            
        Raises:
            FileNotFoundError: If the state file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"State file not found: {file_path}")
            
        with open(file_path, 'r') as f:
            self.state = json.load(f)
        self.logger.info(f"Loaded state from {file_path}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Return a dictionary describing the agent's capabilities.
        
        Subclasses should override this to provide specific capability information.
        """
        return {
            "agent_type": self.__class__.__name__,
            "capabilities": []
        }
    
    def __str__(self) -> str:
        """Return a string representation of the agent."""
        return f"{self.__class__.__name__}({self.agent_id})"
