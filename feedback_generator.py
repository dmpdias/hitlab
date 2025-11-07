"""
Feedback Generator Module

Generates motivational and educational coaching feedback in a structured format.
"""

from typing import List, Dict, Any
from boxing_coach_agent import CoachingFeedback, SkillLevel


class FeedbackGenerator:
    """Generates motivational, educational coaching feedback"""
    
    def __init__(self):
        self.motivational_phrases = {
            'opening': [
                "Great work in today's session!",
                "I can see the dedication in your training!",
                "You're showing real improvement!",
                "Strong effort today!",
                "Your commitment is evident!"
            ],
            'encouragement': [
                "Keep up this energy!",
                "You're on the right track!",
                "This is exactly the kind of work that leads to breakthroughs!",
                "Your progress is noticeable!",
                "Stay focused on these improvements!"
            ],
            'closing': [
                "Keep pushing forward!",
                "You've got what it takes!",
                "Stay hungry and keep training smart!",
                "The hard work will pay off!",
                "Trust the process and stay dedicated!"
            ]
        }
    
    def generate_feedback(
        self,
        boxer_name: str,
        strengths: List[str],
        weaknesses: List[str],
        corrections: List[Dict[str, str]],
        drills: List[Dict[str, Any]],
        strategy_insights: List[Dict[str, str]],
        skill_level: SkillLevel,
        goals: List[str],
        previous_context: List[str] = None
    ) -> CoachingFeedback:
        """
        Generate comprehensive coaching feedback
        
        Args:
            boxer_name: Athlete's name
            strengths: List of identified strengths
            weaknesses: List of identified weaknesses
            corrections: Technical corrections needed
            drills: Recommended drills
            strategy_insights: Strategic analysis insights
            skill_level: Boxer's skill level
            goals: Boxer's training goals
            previous_context: Previous feedback for continuity
            
        Returns:
            CoachingFeedback object with complete feedback
        """
        # Generate summary
        summary = self._generate_summary(
            boxer_name, strengths, weaknesses, skill_level
        )
        
        # Generate strategic insights section
        strategic_insights_list = [
            f"{insight.get('type', 'tactical').upper()}: {insight.get('insight', '')} - {insight.get('recommendation', '')}"
            for insight in strategy_insights
        ]
        
        # Generate motivational message
        motivational_message = self._generate_motivational_message(
            boxer_name, strengths, weaknesses, goals, skill_level
        )
        
        # Generate progress notes if previous context exists
        progress_notes = self._generate_progress_notes(
            previous_context, weaknesses
        ) if previous_context else None
        
        # Generate next session focus areas
        next_session_focus = self._generate_next_session_focus(
            weaknesses, corrections, goals
        )
        
        return CoachingFeedback(
            summary=summary,
            strengths=strengths,
            weaknesses=weaknesses,
            technical_corrections=corrections,
            strategic_insights=strategic_insights_list,
            recommended_drills=drills,
            motivational_message=motivational_message,
            progress_notes=progress_notes,
            next_session_focus=next_session_focus
        )
    
    def _generate_summary(
        self,
        boxer_name: str,
        strengths: List[str],
        weaknesses: List[str],
        skill_level: SkillLevel
    ) -> str:
        """Generate session summary"""
        import random
        
        opening = random.choice(self.motivational_phrases['opening'])
        
        strength_summary = f"Your {strengths[0].lower()} stands out" if strengths else "You're showing commitment"
        
        if len(weaknesses) > 0:
            focus_area = "we need to address some technical areas"
        else:
            focus_area = "let's continue refining your skills"
        
        level_context = {
            SkillLevel.BEGINNER: "As you build your foundation, ",
            SkillLevel.INTERMEDIATE: "As you develop your skills, ",
            SkillLevel.ADVANCED: "At your level, ",
            SkillLevel.PROFESSIONAL: "At the professional level, "
        }.get(skill_level, "")
        
        summary = (
            f"{opening} {boxer_name}, {strength_summary}. "
            f"{level_context}{focus_area} to take your boxing to the next level. "
            f"Let's break down what we saw and create a clear path forward."
        )
        
        return summary
    
    def _generate_motivational_message(
        self,
        boxer_name: str,
        strengths: List[str],
        weaknesses: List[str],
        goals: List[str],
        skill_level: SkillLevel
    ) -> str:
        """Generate personalized motivational message"""
        import random
        
        encouragement = random.choice(self.motivational_phrases['encouragement'])
        closing = random.choice(self.motivational_phrases['closing'])
        
        # Reference their goals if available
        goal_reference = ""
        if goals:
            goal_reference = f"Your goal of {goals[0].lower()} is within reach. "
        
        # Tailor message to their development stage
        stage_message = {
            SkillLevel.BEGINNER: "Every champion started where you are. Focus on the fundamentals and build solid habits.",
            SkillLevel.INTERMEDIATE: "You're past the basics and building real skills. This is where dedication separates good from great.",
            SkillLevel.ADVANCED: "Your technical foundation is strong. Now it's about refinement and strategic mastery.",
            SkillLevel.PROFESSIONAL: "At this level, tiny improvements make huge differences. Stay detail-oriented and trust your training."
        }.get(skill_level, "Keep working hard and staying focused.")
        
        # Build the message
        if weaknesses:
            main_message = (
                f"{boxer_name}, {encouragement} The areas we identified aren't weaknesses - "
                f"they're your next opportunities for growth. {goal_reference}"
                f"{stage_message} {closing}"
            )
        else:
            main_message = (
                f"{boxer_name}, {encouragement} You're executing well across the board. "
                f"{goal_reference}Continue this level of focus and dedication. "
                f"{stage_message} {closing}"
            )
        
        return main_message
    
    def _generate_progress_notes(
        self,
        previous_context: List[str],
        current_weaknesses: List[str]
    ) -> str:
        """Generate notes on progress from previous sessions"""
        if not previous_context:
            return None
        
        # Compare previous weaknesses with current
        # This is simplified - in production would do more sophisticated comparison
        improvements = []
        ongoing_issues = []
        
        for prev_issue in previous_context[:3]:  # Check last 3 issues
            if not any(prev_issue.lower() in weak.lower() for weak in current_weaknesses):
                improvements.append(prev_issue)
            else:
                ongoing_issues.append(prev_issue)
        
        notes = []
        
        if improvements:
            notes.append(
                f"IMPROVEMENTS FROM LAST SESSION: "
                f"Great progress on {', '.join(improvements[:2])}! This shows your training is working."
            )
        
        if ongoing_issues:
            notes.append(
                f"CONTINUED FOCUS NEEDED: "
                f"We're still working on {', '.join(ongoing_issues[:2])}. "
                f"Stay patient - these areas need more time and reps."
            )
        
        if not notes:
            notes.append(
                "PROGRESS CHECK: Keep maintaining your current training consistency. "
                "Building on solid fundamentals."
            )
        
        return " | ".join(notes)
    
    def _generate_next_session_focus(
        self,
        weaknesses: List[str],
        corrections: List[Dict[str, str]],
        goals: List[str]
    ) -> List[str]:
        """Generate focus areas for next session"""
        focus_areas = []
        
        # Top 3-4 priority items
        priority_weaknesses = weaknesses[:3]
        
        for weakness in priority_weaknesses:
            # Find related correction for more specific guidance
            related_correction = next(
                (c for c in corrections if weakness.lower() in c.get('issue', '').lower()),
                None
            )
            
            if related_correction:
                focus_areas.append(
                    f"{related_correction.get('category', 'Technical')}: {weakness}"
                )
            else:
                focus_areas.append(weakness)
        
        # Add goal-related focus if relevant
        if goals and len(focus_areas) < 4:
            focus_areas.append(f"Goal work: {goals[0]}")
        
        # Always include conditioning
        if len(focus_areas) < 4:
            focus_areas.append("Conditioning: Maintain endurance and work capacity")
        
        return focus_areas
    
    def format_detailed_report(self, feedback: CoachingFeedback) -> str:
        """Format feedback as detailed text report"""
        lines = []
        lines.append("=" * 80)
        lines.append("BOXING COACHING SESSION ANALYSIS")
        lines.append("=" * 80)
        lines.append("")
        
        # Summary
        lines.append("SESSION SUMMARY")
        lines.append("-" * 80)
        lines.append(feedback.summary)
        lines.append("")
        
        # Progress notes if available
        if feedback.progress_notes:
            lines.append("PROGRESS UPDATE")
            lines.append("-" * 80)
            lines.append(feedback.progress_notes)
            lines.append("")
        
        # Strengths
        lines.append("STRENGTHS DEMONSTRATED")
        lines.append("-" * 80)
        for i, strength in enumerate(feedback.strengths, 1):
            lines.append(f"{i}. {strength}")
        lines.append("")
        
        # Weaknesses
        lines.append("AREAS FOR IMPROVEMENT")
        lines.append("-" * 80)
        for i, weakness in enumerate(feedback.weaknesses, 1):
            lines.append(f"{i}. {weakness}")
        lines.append("")
        
        # Technical corrections
        if feedback.technical_corrections:
            lines.append("TECHNICAL CORRECTIONS")
            lines.append("-" * 80)
            for i, correction in enumerate(feedback.technical_corrections, 1):
                lines.append(f"\n{i}. {correction.get('category', 'Technical').upper()}")
                lines.append(f"   Issue: {correction.get('issue', '')}")
                lines.append(f"   Correction: {correction.get('correction', '')}")
                
                if correction.get('key_points'):
                    lines.append("   Key Points:")
                    for point in correction.get('key_points', []):
                        lines.append(f"      • {point}")
            lines.append("")
        
        # Strategic insights
        if feedback.strategic_insights:
            lines.append("STRATEGIC ANALYSIS")
            lines.append("-" * 80)
            for i, insight in enumerate(feedback.strategic_insights, 1):
                lines.append(f"{i}. {insight}")
            lines.append("")
        
        # Recommended drills
        lines.append("RECOMMENDED TRAINING DRILLS")
        lines.append("-" * 80)
        for i, drill in enumerate(feedback.recommended_drills, 1):
            lines.append(f"\n{i}. {drill.get('name', 'Drill').upper()}")
            lines.append(f"   {drill.get('description', '')}")
            lines.append(f"   Volume: {drill.get('sets_reps', 'As prescribed')}")
            lines.append(f"   Rest: {drill.get('rest', 'As needed')}")
            
            if drill.get('instructions'):
                lines.append("   Instructions:")
                for instruction in drill.get('instructions', []):
                    lines.append(f"      • {instruction}")
            
            if drill.get('focus_points'):
                lines.append("   Focus Points:")
                for point in drill.get('focus_points', []):
                    lines.append(f"      • {point}")
        lines.append("")
        
        # Next session focus
        if feedback.next_session_focus:
            lines.append("NEXT SESSION FOCUS AREAS")
            lines.append("-" * 80)
            for i, focus in enumerate(feedback.next_session_focus, 1):
                lines.append(f"{i}. {focus}")
            lines.append("")
        
        # Motivational message
        lines.append("COACH'S MESSAGE")
        lines.append("-" * 80)
        lines.append(feedback.motivational_message)
        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def format_summary_report(self, feedback: CoachingFeedback) -> str:
        """Format feedback as brief summary report"""
        lines = []
        lines.append("BOXING SESSION SUMMARY")
        lines.append("=" * 60)
        lines.append("")
        lines.append(feedback.summary)
        lines.append("")
        
        lines.append(f"Strengths ({len(feedback.strengths)}): {', '.join(feedback.strengths[:3])}")
        lines.append(f"Focus Areas ({len(feedback.weaknesses)}): {', '.join(feedback.weaknesses[:3])}")
        lines.append(f"Drills Recommended: {len(feedback.recommended_drills)}")
        lines.append("")
        
        lines.append("TOP PRIORITY:")
        if feedback.technical_corrections:
            lines.append(f"• {feedback.technical_corrections[0].get('issue', '')}")
            lines.append(f"  → {feedback.technical_corrections[0].get('correction', '')}")
        lines.append("")
        
        lines.append(feedback.motivational_message)
        lines.append("=" * 60)
        
        return "\n".join(lines)
