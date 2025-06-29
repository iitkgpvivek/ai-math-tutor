import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict, field
import hashlib
from collections import defaultdict

@dataclass
class ProblemAttempt:
    problem_hash: str
    timestamp: str
    correct: bool
    time_taken: float  # in seconds
    difficulty: str
    topic: str
    subtopic: str
    problem_type: str

@dataclass
class StudentProgress:
    student_id: str
    name: str
    grade: str
    difficulty_level: str = "medium"
    total_attempts: int = 0
    correct_attempts: int = 0
    last_practiced: Optional[str] = None
    problem_history: List[Dict[str, Any]] = field(default_factory=list)
    problem_mastery: Dict[str, float] = field(default_factory=dict)  # problem_type -> mastery_score (0-1)
    seen_problems: Set[str] = field(default_factory=set)  # Set of problem hashes
    weak_areas: Dict[str, float] = field(default_factory=dict)  # topic/subtopic -> error_rate

class LearningTracker:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.students: Dict[str, StudentProgress] = {}
        self.load_all_students()
    
    def _get_student_file(self, student_id: str) -> str:
        return os.path.join(self.data_dir, f"{student_id}.json")
    
    def load_all_students(self):
        """Load all student progress data from disk."""
        if not os.path.exists(self.data_dir):
            return
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(self.data_dir, filename), 'r') as f:
                        data = json.load(f)
                        student = StudentProgress(**data)
                        # Convert list to set for seen_problems
                        student.seen_problems = set(student.seen_problems)
                        self.students[student.student_id] = student
                except Exception as e:
                    print(f"Error loading student data {filename}: {e}")
    
    def get_student(self, student_id: str) -> Optional[StudentProgress]:
        """Get student progress, loading if not already in memory."""
        if student_id not in self.students:
            filepath = self._get_student_file(student_id)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    student = StudentProgress(**data)
                    student.seen_problems = set(student.seen_problems)
                    self.students[student_id] = student
        return self.students.get(student_id)
    
    def create_student(self, name: str, grade: str, difficulty: str = "medium") -> StudentProgress:
        """Create a new student profile."""
        student_id = hashlib.sha256(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        student = StudentProgress(
            student_id=student_id,
            name=name,
            grade=grade,
            difficulty_level=difficulty,
            last_practiced=datetime.now().isoformat()
        )
        self.students[student_id] = student
        self.save_student(student_id)
        return student
    
    def save_student(self, student_id: str):
        """Save student progress to disk."""
        if student_id not in self.students:
            return
            
        student = self.students[student_id]
        filepath = self._get_student_file(student_id)
        
        # Convert set to list for JSON serialization
        student_data = asdict(student)
        student_data['seen_problems'] = list(student.seen_problems)
        
        with open(filepath, 'w') as f:
            json.dump(student_data, f, indent=2)
    
    def record_attempt(
        self,
        student_id: str,
        problem_text: str,
        correct: bool,
        time_taken: float,
        difficulty: str,
        topic: str,
        subtopic: str,
        problem_type: str
    ) -> None:
        """Record a problem attempt and update progress tracking."""
        student = self.get_student(student_id)
        if not student:
            return
        
        # Generate a hash of the problem for deduplication
        problem_hash = hashlib.sha256(problem_text.encode()).hexdigest()
        
        # Record attempt
        attempt = {
            'problem_hash': problem_hash,
            'timestamp': datetime.now().isoformat(),
            'correct': correct,
            'time_taken': time_taken,
            'difficulty': difficulty,
            'topic': topic,
            'subtopic': subtopic,
            'problem_type': problem_type
        }
        
        # Update student progress
        student.problem_history.append(attempt)
        student.total_attempts += 1
        if correct:
            student.correct_attempts += 1
        student.last_practiced = datetime.now().isoformat()
        student.seen_problems.add(problem_hash)
        
        # Update mastery scores (simple moving average)
        current_mastery = student.problem_mastery.get(problem_type, 0.5)  # Start with neutral 0.5
        new_mastery = current_mastery + (0.1 * (1 if correct else -1))
        student.problem_mastery[problem_type] = max(0, min(1, new_mastery))  # Clamp between 0 and 1
        
        # Update weak areas tracking
        topic_key = f"{topic}:{subtopic}"
        if topic_key not in student.weak_areas:
            student.weak_areas[topic_key] = 0.5
        
        # Update weak area score (lower is worse)
        if correct:
            student.weak_areas[topic_key] *= 0.95  # Improve slightly
        else:
            student.weak_areas[topic_key] = min(1, student.weak_areas[topic_key] * 1.1)  # Worsen more
        
        self.save_student(student_id)
    
    def get_recommended_topics(self, student_id: str, count: int = 3) -> List[Tuple[str, str]]:
        """Get recommended topics/subtopics based on weak areas."""
        student = self.get_student(student_id)
        if not student or not student.weak_areas:
            return []
        
        # Sort by worst performing areas first
        sorted_areas = sorted(student.weak_areas.items(), key=lambda x: x[1], reverse=True)
        return [tuple(area[0].split(':', 1)) for area in sorted_areas[:count]]
    
    def get_problem_variations(self, student_id: str) -> List[str]:
        """Get problem types that the student hasn't seen much."""
        student = self.get_student(student_id)
        if not student:
            return []
        
        # Find problem types with lowest mastery
        if not student.problem_mastery:
            return []
            
        sorted_types = sorted(student.problem_mastery.items(), key=lambda x: x[1])
        return [pt[0] for pt in sorted_types[:3]]  # Return 3 least mastered types
    
    def get_practice_summary(self, student_id: str) -> Dict[str, Any]:
        """Get a summary of the student's practice history."""
        student = self.get_student(student_id)
        if not student:
            return {}
        
        # Calculate accuracy by topic
        topic_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
        for attempt in student.problem_history:
            key = f"{attempt['topic']}:{attempt['subtopic']}"
            topic_accuracy[key]['total'] += 1
            if attempt['correct']:
                topic_accuracy[key]['correct'] += 1
        
        # Convert to percentage
        topic_accuracy = {
            topic: (data['correct'] / data['total'] * 100) 
            for topic, data in topic_accuracy.items()
            if data['total'] > 0
        }
        
        return {
            'total_attempts': student.total_attempts,
            'accuracy': (student.correct_attempts / student.total_attempts * 100) if student.total_attempts > 0 else 0,
            'topics_accuracy': topic_accuracy,
            'weak_areas': dict(sorted(student.weak_areas.items(), key=lambda x: x[1])[:3]),
            'last_practiced': student.last_practiced
        }
