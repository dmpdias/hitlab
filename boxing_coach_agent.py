"""
Boxing Coach AI Agent - Main Module

This agent analyzes boxing video data and provides expert coaching feedback
on technique, strategy, and performance improvements.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum
import json


class SkillLevel(Enum):
    """Boxer skill levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"


class SessionType(Enum):
    """Type of boxing session"""
    TRAINING = "training"
    SPARRING = "sparring"
    COMPETITION = "competition"
    TECHNICAL_DRILL = "technical_drill"


@dataclass
class VideoAnalysisData:
    """Parsed video analysis data from pose estimation and action recognition"""
    session_type: SessionType
    duration_seconds: float
    punches_thrown: List[Dict[str, Any]]  # Each punch with type, speed, accuracy, form
    defensive_actions: List[Dict[str, Any]]  # Slips, blocks, parries, rolls
    footwork_segments: List[Dict[str, Any]]  # Movement patterns, stance transitions
    pose_data: List[Dict[str, Any]]  # Frame-by-frame pose estimations
    heart_rate_data: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class BoxerProfile:
    """Athlete profile and context"""
    name: str
    skill_level: SkillLevel
    goals: List[str]
    previous_feedback: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    known_weaknesses: Optional[List[str]] = None
    training_history: Optional[Dict[str, Any]] = None


@dataclass
class CoachingFeedback:
    """Structured coaching feedback output"""
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    technical_corrections: List[Dict[str, str]]
    strategic_insights: List[str]
    recommended_drills: List[Dict[str, Any]]
    motivational_message: str
    progress_notes: Optional[str] = None
    next_session_focus: List[str] = None


class BoxingCoachAgent:
    """
    Expert Boxing Coach AI Agent
    
    Analyzes video data and provides comprehensive coaching feedback covering:
    - Technical analysis (punches, defense, footwork)
    - Strategic assessment
    - Drill recommendations
    - Motivational coaching
    """
    
    def __init__(self):
        from technical_analyzer import TechnicalAnalyzer
        from drill_recommender import DrillRecommender
        from feedback_generator import FeedbackGenerator
        
        self.technical_analyzer = TechnicalAnalyzer()
        self.drill_recommender = DrillRecommender()
        self.feedback_generator = FeedbackGenerator()
    
    def analyze_session(
        self, 
        video_data: VideoAnalysisData, 
        boxer_profile: BoxerProfile
    ) -> CoachingFeedback:
        """
        Main method to analyze a boxing session and generate coaching feedback
        
        Args:
            video_data: Parsed video analysis data
            boxer_profile: Athlete profile and context
            
        Returns:
            CoachingFeedback: Comprehensive coaching feedback
        """
        # Perform technical analysis
        punch_analysis = self.technical_analyzer.analyze_punches(
            video_data.punches_thrown, boxer_profile.skill_level
        )
        defense_analysis = self.technical_analyzer.analyze_defense(
            video_data.defensive_actions, boxer_profile.skill_level
        )
        footwork_analysis = self.technical_analyzer.analyze_footwork(
            video_data.footwork_segments, video_data.pose_data, boxer_profile.skill_level
        )
        
        # Analyze strategy and tactics
        strategy_analysis = self.technical_analyzer.analyze_strategy(
            video_data, boxer_profile.skill_level
        )
        
        # Compile strengths and weaknesses
        strengths = self._extract_strengths(
            punch_analysis, defense_analysis, footwork_analysis, strategy_analysis
        )
        weaknesses = self._extract_weaknesses(
            punch_analysis, defense_analysis, footwork_analysis, strategy_analysis
        )
        
        # Generate technical corrections
        corrections = self._generate_corrections(
            punch_analysis, defense_analysis, footwork_analysis
        )
        
        # Recommend drills based on weaknesses
        drills = self.drill_recommender.recommend_drills(
            weaknesses=weaknesses,
            skill_level=boxer_profile.skill_level,
            session_type=video_data.session_type,
            specific_issues=corrections
        )
        
        # Generate motivational and educational feedback
        feedback = self.feedback_generator.generate_feedback(
            boxer_name=boxer_profile.name,
            strengths=strengths,
            weaknesses=weaknesses,
            corrections=corrections,
            drills=drills,
            strategy_insights=strategy_analysis.get('insights', []),
            skill_level=boxer_profile.skill_level,
            goals=boxer_profile.goals,
            previous_context=boxer_profile.previous_feedback
        )
        
        return feedback
    
    def _extract_strengths(self, punch_analysis, defense_analysis, 
                          footwork_analysis, strategy_analysis) -> List[str]:
        """Extract key strengths from technical analyses"""
        strengths = []
        
        # Punch strengths
        if punch_analysis.get('power_rating', 0) >= 7:
            strengths.append("Strong punching power and technique")
        if punch_analysis.get('accuracy_rate', 0) >= 0.7:
            strengths.append("High punch accuracy and precision")
        if punch_analysis.get('combination_quality', 0) >= 7:
            strengths.append("Effective combination punching")
        if punch_analysis.get('hand_speed_rating', 0) >= 7:
            strengths.append("Excellent hand speed")
        
        # Defense strengths
        if defense_analysis.get('effectiveness_rating', 0) >= 7:
            strengths.append("Solid defensive fundamentals")
        if defense_analysis.get('head_movement_quality', 0) >= 7:
            strengths.append("Good head movement and evasion")
        if defense_analysis.get('blocking_efficiency', 0) >= 0.75:
            strengths.append("Effective blocking technique")
        
        # Footwork strengths
        if footwork_analysis.get('balance_rating', 0) >= 7:
            strengths.append("Excellent balance and stability")
        if footwork_analysis.get('ring_control', 0) >= 7:
            strengths.append("Strong ring generalship and positioning")
        if footwork_analysis.get('pivot_quality', 0) >= 7:
            strengths.append("Skilled pivoting and angles")
        
        # Strategy strengths
        if strategy_analysis.get('tactical_awareness', 0) >= 7:
            strengths.append("High tactical awareness and ring IQ")
        if strategy_analysis.get('adaptability', 0) >= 7:
            strengths.append("Good adaptability and adjustment")
        
        return strengths if strengths else ["Showing dedication and effort in training"]
    
    def _extract_weaknesses(self, punch_analysis, defense_analysis, 
                           footwork_analysis, strategy_analysis) -> List[str]:
        """Extract key weaknesses that need addressing"""
        weaknesses = []
        
        # Punch weaknesses
        if punch_analysis.get('power_rating', 10) < 5:
            weaknesses.append("Limited punching power - needs strength and technique work")
        if punch_analysis.get('accuracy_rate', 1) < 0.5:
            weaknesses.append("Low punch accuracy - missing target frequently")
        if punch_analysis.get('guard_return_rate', 1) < 0.7:
            weaknesses.append("Slow guard return after punching - defensive vulnerability")
        if punch_analysis.get('overextension_count', 0) > 5:
            weaknesses.append("Overextending on punches - losing balance")
        if punch_analysis.get('telegraph_count', 0) > 3:
            weaknesses.append("Telegraphing punches - opponent can read intentions")
        
        # Defense weaknesses
        if defense_analysis.get('effectiveness_rating', 10) < 5:
            weaknesses.append("Defensive gaps - absorbing too many clean shots")
        if defense_analysis.get('chin_exposure_count', 0) > 5:
            weaknesses.append("Excessive chin exposure - vulnerable to counters")
        if defense_analysis.get('predictable_patterns', False):
            weaknesses.append("Predictable defensive patterns - easy to time")
        
        # Footwork weaknesses
        if footwork_analysis.get('balance_rating', 10) < 5:
            weaknesses.append("Balance issues - getting knocked off-center")
        if footwork_analysis.get('flat_footed_percentage', 0) > 0.4:
            weaknesses.append("Too flat-footed - limited mobility")
        if footwork_analysis.get('squared_up_count', 0) > 3:
            weaknesses.append("Squaring up stance - vulnerable position")
        
        # Strategy weaknesses
        if strategy_analysis.get('tactical_awareness', 10) < 5:
            weaknesses.append("Low tactical awareness - missing opportunities")
        if strategy_analysis.get('energy_management', 10) < 5:
            weaknesses.append("Poor energy management - fading in later rounds")
        
        return weaknesses if weaknesses else ["Minor technical refinements needed"]
    
    def _generate_corrections(self, punch_analysis, defense_analysis, 
                             footwork_analysis) -> List[Dict[str, str]]:
        """Generate specific technical corrections with instructions"""
        corrections = []
        
        # Punch corrections
        for issue in punch_analysis.get('issues', []):
            corrections.append({
                'category': 'Punching',
                'issue': issue['description'],
                'correction': issue['correction'],
                'key_points': issue.get('key_points', [])
            })
        
        # Defense corrections
        for issue in defense_analysis.get('issues', []):
            corrections.append({
                'category': 'Defense',
                'issue': issue['description'],
                'correction': issue['correction'],
                'key_points': issue.get('key_points', [])
            })
        
        # Footwork corrections
        for issue in footwork_analysis.get('issues', []):
            corrections.append({
                'category': 'Footwork',
                'issue': issue['description'],
                'correction': issue['correction'],
                'key_points': issue.get('key_points', [])
            })
        
        return corrections
    
    def generate_session_report(
        self, 
        feedback: CoachingFeedback, 
        format: str = "detailed"
    ) -> str:
        """
        Generate a formatted coaching report
        
        Args:
            feedback: CoachingFeedback object
            format: "detailed", "summary", or "json"
            
        Returns:
            Formatted report string
        """
        if format == "json":
            return json.dumps(feedback.__dict__, indent=2, default=str)
        
        elif format == "summary":
            return self.feedback_generator.format_summary_report(feedback)
        
        else:  # detailed
            return self.feedback_generator.format_detailed_report(feedback)


def create_boxing_coach() -> BoxingCoachAgent:
    """Factory function to create a boxing coach agent"""
    return BoxingCoachAgent()


if __name__ == "__main__":
    # Example usage
    coach = create_boxing_coach()
    print("Boxing Coach AI Agent initialized and ready for analysis.")
