"""
Agents package for the AI Math Tutor system.

This package contains different types of agents that can be used in the system.
"""

__all__ = [
    'Agent',
    'Message',
    'AgentRole',
    'StudentAgent',
    'ValidationResult',
    'ProblemReview',
    'TeacherAgent',
    'ProblemVariation'
]

# Import the base agent, student agent, and teacher agent modules
from . import base_agent
from . import student_agent
from . import teacher_agent

# Make the Agent, StudentAgent, and TeacherAgent classes available at the package level
from .base_agent import Agent, Message, AgentRole
from .student_agent import StudentAgent, ValidationResult, ProblemReview
from .teacher_agent import TeacherAgent, ProblemVariation
