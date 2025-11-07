"""
Example Usage of Boxing Coach AI Agent

This demonstrates how to use the boxing coach agent with sample data.
"""

from boxing_coach_agent import (
    BoxingCoachAgent, VideoAnalysisData, BoxerProfile,
    SkillLevel, SessionType, create_boxing_coach
)


def create_sample_video_data() -> VideoAnalysisData:
    """Create sample video analysis data for demonstration"""
    
    # Sample punch data with various metrics
    punches = [
        {'type': 'jab', 'timestamp': 0.5, 'landed': True, 'power': 5, 'speed': 7, 
         'guard_returned': True, 'overextended': False, 'telegraphed': False},
        {'type': 'cross', 'timestamp': 1.0, 'landed': True, 'power': 8, 'speed': 6,
         'guard_returned': False, 'overextended': True, 'telegraphed': True},
        {'type': 'jab', 'timestamp': 2.0, 'landed': True, 'power': 5, 'speed': 8,
         'guard_returned': True, 'overextended': False, 'telegraphed': False},
        {'type': 'hook', 'timestamp': 2.5, 'landed': False, 'power': 7, 'speed': 5,
         'guard_returned': False, 'overextended': True, 'telegraphed': True},
        {'type': 'cross', 'timestamp': 4.0, 'landed': True, 'power': 8, 'speed': 7,
         'guard_returned': True, 'overextended': False, 'telegraphed': False},
        {'type': 'jab', 'timestamp': 5.0, 'landed': True, 'power': 6, 'speed': 8,
         'guard_returned': True, 'overextended': False, 'telegraphed': False},
        {'type': 'uppercut', 'timestamp': 5.5, 'landed': True, 'power': 9, 'speed': 5,
         'guard_returned': False, 'overextended': False, 'telegraphed': True},
        {'type': 'hook', 'timestamp': 7.0, 'landed': True, 'power': 7, 'speed': 6,
         'guard_returned': True, 'overextended': False, 'telegraphed': False},
    ]
    
    # Sample defensive actions
    defensive_actions = [
        {'type': 'slip', 'timestamp': 1.5, 'successful': True, 'chin_exposed': False, 'hands_down': False},
        {'type': 'block', 'timestamp': 3.0, 'successful': True, 'chin_exposed': False, 'hands_down': False},
        {'type': 'slip', 'timestamp': 3.5, 'successful': False, 'chin_exposed': True, 'hands_down': True},
        {'type': 'block', 'timestamp': 6.0, 'successful': True, 'chin_exposed': False, 'hands_down': False},
        {'type': 'roll', 'timestamp': 6.5, 'successful': True, 'chin_exposed': False, 'hands_down': False},
    ]
    
    # Sample footwork data
    footwork_segments = [
        {'direction': 'forward', 'timestamp': 0.0, 'flat_footed': False, 
         'squared_stance': False, 'crossed_feet': False, 'movement_type': 'step',
         'ring_position': 'center', 'trapped': False},
        {'direction': 'lateral', 'timestamp': 2.0, 'flat_footed': True,
         'squared_stance': False, 'crossed_feet': False, 'movement_type': 'step',
         'ring_position': 'center', 'trapped': False},
        {'direction': 'backward', 'timestamp': 4.0, 'flat_footed': False,
         'squared_stance': True, 'crossed_feet': False, 'movement_type': 'step',
         'ring_position': 'edge', 'trapped': False},
        {'direction': 'forward', 'timestamp': 6.0, 'flat_footed': False,
         'squared_stance': False, 'crossed_feet': False, 'movement_type': 'pivot',
         'ring_position': 'center', 'trapped': False, 'quality': 7},
    ]
    
    # Sample pose data for balance analysis
    pose_data = [
        {'timestamp': 0.0, 'balance_score': 8},
        {'timestamp': 1.0, 'balance_score': 7},
        {'timestamp': 2.0, 'balance_score': 5},
        {'timestamp': 3.0, 'balance_score': 6},
        {'timestamp': 4.0, 'balance_score': 4},
        {'timestamp': 5.0, 'balance_score': 7},
        {'timestamp': 6.0, 'balance_score': 8},
        {'timestamp': 7.0, 'balance_score': 7},
    ]
    
    return VideoAnalysisData(
        session_type=SessionType.TRAINING,
        duration_seconds=180.0,
        punches_thrown=punches,
        defensive_actions=defensive_actions,
        footwork_segments=footwork_segments,
        pose_data=pose_data,
        metadata={'location': 'Main Gym', 'equipment': 'Heavy Bag'}
    )


def create_sample_boxer_profile() -> BoxerProfile:
    """Create sample boxer profile"""
    return BoxerProfile(
        name="Alex",
        skill_level=SkillLevel.INTERMEDIATE,
        goals=[
            "Improve defensive skills",
            "Increase combination variety",
            "Prepare for upcoming sparring session"
        ],
        previous_feedback=[
            "Dropping hands after power punches",
            "Limited head movement"
        ],
        strengths=[
            "Good jab technique",
            "Strong work ethic"
        ],
        known_weaknesses=[
            "Telegraphing power shots",
            "Flat-footed at times"
        ]
    )


def main():
    """Main example demonstrating the boxing coach agent"""
    
    print("=" * 80)
    print("BOXING COACH AI AGENT - EXAMPLE SESSION")
    print("=" * 80)
    print()
    
    # Create the coach
    print("Initializing Boxing Coach AI Agent...")
    coach = create_boxing_coach()
    print("✓ Coach initialized\n")
    
    # Create sample data
    print("Loading session data...")
    video_data = create_sample_video_data()
    boxer_profile = create_sample_boxer_profile()
    print(f"✓ Analyzing {boxer_profile.name}'s {video_data.session_type.value} session")
    print(f"  Duration: {video_data.duration_seconds}s")
    print(f"  Punches thrown: {len(video_data.punches_thrown)}")
    print(f"  Defensive actions: {len(video_data.defensive_actions)}")
    print(f"  Skill level: {boxer_profile.skill_level.value}\n")
    
    # Analyze the session
    print("Analyzing performance...")
    feedback = coach.analyze_session(video_data, boxer_profile)
    print("✓ Analysis complete\n")
    
    # Generate and display the detailed report
    print("\nGenerating detailed coaching report...\n")
    detailed_report = coach.generate_session_report(feedback, format="detailed")
    print(detailed_report)
    
    # Also show summary format
    print("\n\n")
    print("=" * 80)
    print("QUICK SUMMARY VERSION")
    print("=" * 80)
    print()
    summary_report = coach.generate_session_report(feedback, format="summary")
    print(summary_report)
    
    # Show JSON format option
    print("\n\n")
    print("=" * 80)
    print("JSON FORMAT (for API/integration)")
    print("=" * 80)
    print()
    json_report = coach.generate_session_report(feedback, format="json")
    print(json_report[:500] + "...\n[truncated for display]")
    
    print("\n" + "=" * 80)
    print("Example complete! The agent can process real video analysis data")
    print("from pose estimation and action recognition systems.")
    print("=" * 80)


if __name__ == "__main__":
    main()
