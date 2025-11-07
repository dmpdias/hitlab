# HitLab - Boxing Coach AI Agent

An expert AI coaching system that analyzes boxing performance data and provides detailed, actionable feedback to improve technique, strategy, and overall performance.

## Overview

The Boxing Coach AI Agent processes summarized video analysis data (from pose estimation, punch classification, and action recognition systems) to deliver comprehensive coaching feedback covering:

- **Technical Analysis**: Punch mechanics, defensive technique, and footwork evaluation
- **Strategic Assessment**: Ring generalship, tactical awareness, and fight IQ
- **Personalized Corrections**: Step-by-step instructions to fix technical issues
- **Targeted Drill Recommendations**: Specific exercises to address weaknesses
- **Motivational Coaching**: Engaging, educational feedback tailored to athlete's level and goals

## Features

### 🥊 Comprehensive Technical Analysis
- **Punch Analysis**: Power, accuracy, speed, combinations, guard return, telegraphing
- **Defense Analysis**: Head movement, blocking efficiency, chin protection, pattern recognition
- **Footwork Analysis**: Balance, ring control, pivot quality, stance maintenance
- **Strategy Analysis**: Tactical awareness, energy management, rhythm and timing

### 🎯 Intelligent Drill Recommendations
- 50+ curated boxing drills across all skill levels
- Automatically matched to identified weaknesses
- Detailed instructions with sets, reps, and focus points
- Covers: power, accuracy, defense, footwork, speed, stamina, and more

### 💪 Motivational Coaching Style
- Educational and encouraging feedback
- Tailored to skill level (Beginner to Professional)
- Goal-oriented recommendations
- Progress tracking across sessions

### 📊 Flexible Output Formats
- **Detailed Report**: Complete analysis with all sections
- **Summary Report**: Quick overview for rapid feedback
- **JSON Format**: Machine-readable for integrations and APIs

## Installation

```bash
# Clone or download the repository
git clone <repository-url>
cd hitlab

# No external dependencies required for core functionality!
# The agent works with Python 3.7+ standard library

# Optional: Install extras for advanced features
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile, SkillLevel, SessionType

# Initialize the coach
coach = create_boxing_coach()

# Create video analysis data (from your pose estimation/action recognition system)
video_data = VideoAnalysisData(
    session_type=SessionType.TRAINING,
    duration_seconds=180.0,
    punches_thrown=[...],  # List of punch data
    defensive_actions=[...],  # List of defensive movements
    footwork_segments=[...],  # List of footwork data
    pose_data=[...]  # Frame-by-frame pose estimations
)

# Create boxer profile
boxer_profile = BoxerProfile(
    name="Alex",
    skill_level=SkillLevel.INTERMEDIATE,
    goals=["Improve defensive skills", "Increase combination variety"]
)

# Analyze the session
feedback = coach.analyze_session(video_data, boxer_profile)

# Generate report
report = coach.generate_session_report(feedback, format="detailed")
print(report)
```

### Run Example Demo

```bash
python example_usage.py
```

This will run a complete example with sample data and display:
- Detailed coaching report
- Summary version
- JSON format output

## Architecture

### Core Modules

#### 1. `boxing_coach_agent.py` - Main Agent
The orchestrator that coordinates all analysis and feedback generation.

**Key Classes:**
- `BoxingCoachAgent`: Main agent class
- `VideoAnalysisData`: Input data structure for video analysis
- `BoxerProfile`: Athlete profile and context
- `CoachingFeedback`: Structured output with all feedback
- `SkillLevel`, `SessionType`: Enumerations for context

#### 2. `technical_analyzer.py` - Technical Analysis
Analyzes specific technical aspects of boxing performance.

**Analysis Functions:**
- `analyze_punches()`: Punch mechanics, power, accuracy, combinations
- `analyze_defense()`: Defensive technique, head movement, blocking
- `analyze_footwork()`: Balance, ring control, pivots, movement patterns
- `analyze_strategy()`: Tactical awareness, adaptability, energy management

**Key Features:**
- Skill-level aware analysis (different standards for beginners vs professionals)
- Identifies specific technical issues with detailed descriptions
- Provides actionable corrections with key teaching points
- Severity ratings for prioritization

#### 3. `drill_recommender.py` - Drill Recommendation Engine
Recommends targeted drills based on identified weaknesses.

**Features:**
- 50+ drill library covering all boxing fundamentals
- Automatic weakness-to-drill matching
- Skill-level appropriate recommendations
- Detailed instructions with sets, reps, rest periods, and focus points
- Equipment requirements and difficulty ratings

**Drill Categories:**
- Power development
- Accuracy training
- Defensive skills
- Guard maintenance
- Footwork and movement
- Hand speed
- Conditioning/stamina
- Combination work
- Head movement
- Jab mastery
- Anti-telegraphing

#### 4. `feedback_generator.py` - Feedback Generation
Generates motivational, educational coaching feedback in structured format.

**Features:**
- Session summaries with context
- Progress tracking across sessions
- Personalized motivational messages
- Next session focus area generation
- Multiple output formats (detailed, summary, JSON)

## Data Input Format

### Video Analysis Data Structure

The agent expects pre-processed video analysis data:

```python
VideoAnalysisData(
    session_type: SessionType,  # TRAINING, SPARRING, COMPETITION, TECHNICAL_DRILL
    duration_seconds: float,
    
    punches_thrown: [
        {
            'type': 'jab',  # jab, cross, hook, uppercut, overhand
            'timestamp': 0.5,
            'landed': True,
            'power': 7,  # 0-10 scale
            'speed': 8,  # 0-10 scale
            'guard_returned': True,
            'overextended': False,
            'telegraphed': False
        },
        # ... more punches
    ],
    
    defensive_actions: [
        {
            'type': 'slip',  # slip, block, parry, roll, duck, clinch
            'timestamp': 1.5,
            'successful': True,
            'chin_exposed': False,
            'hands_down': False
        },
        # ... more defensive actions
    ],
    
    footwork_segments: [
        {
            'direction': 'forward',  # forward, backward, lateral
            'timestamp': 0.0,
            'flat_footed': False,
            'squared_stance': False,
            'crossed_feet': False,
            'movement_type': 'step',  # step, pivot
            'ring_position': 'center',  # center, edge, corner
            'trapped': False,
            'quality': 7  # for pivots, 0-10 scale
        },
        # ... more footwork segments
    ],
    
    pose_data: [
        {
            'timestamp': 0.0,
            'balance_score': 8  # 0-10 scale from pose analysis
        },
        # ... frame by frame
    ]
)
```

### Boxer Profile Structure

```python
BoxerProfile(
    name: str,
    skill_level: SkillLevel,  # BEGINNER, INTERMEDIATE, ADVANCED, PROFESSIONAL
    goals: List[str],
    previous_feedback: Optional[List[str]],  # For progress tracking
    strengths: Optional[List[str]],
    known_weaknesses: Optional[List[str]],
    training_history: Optional[Dict]
)
```

## Output Format

### Coaching Feedback Structure

```python
CoachingFeedback(
    summary: str,  # Session overview
    strengths: List[str],  # Identified strengths
    weaknesses: List[str],  # Areas for improvement
    technical_corrections: List[Dict],  # Specific fixes
    strategic_insights: List[str],  # Tactical analysis
    recommended_drills: List[Dict],  # Targeted exercises
    motivational_message: str,  # Personalized motivation
    progress_notes: Optional[str],  # Progress tracking
    next_session_focus: List[str]  # Priority areas
)
```

### Technical Correction Format

```python
{
    'category': 'Punching',  # Punching, Defense, Footwork
    'issue': 'Dropping hands after punching',
    'correction': 'Focus on snapping your punches back to guard position immediately...',
    'key_points': [
        'Keep your non-punching hand up protecting your chin',
        'Practice shadow boxing with emphasis on the return motion',
        'Imagine an elastic band pulling your hand back'
    ]
}
```

### Drill Format

```python
{
    'name': 'Heavy Bag Power Shots',
    'description': 'Focus on generating power from legs through core into punches',
    'instructions': [
        'Stand at heavy bag in proper stance',
        'Throw single power shots with full body rotation',
        # ... more steps
    ],
    'sets_reps': '3 rounds × 3 minutes',
    'rest': '30 seconds',
    'difficulty': 'beginner',
    'equipment': ['heavy bag'],
    'focus_points': ['Leg drive', 'Hip rotation', 'Core engagement']
}
```

## Integration Examples

### With Video Processing Pipeline

```python
# Your video processing pipeline
video_file = "boxer_training_session.mp4"

# 1. Pose estimation (MediaPipe, OpenPose, etc.)
pose_data = pose_estimator.process(video_file)

# 2. Action recognition (your classifier)
punches, defenses = action_classifier.classify(video_file, pose_data)

# 3. Footwork analysis
footwork = footwork_analyzer.analyze(pose_data)

# 4. Create VideoAnalysisData
video_data = VideoAnalysisData(
    session_type=SessionType.TRAINING,
    duration_seconds=get_duration(video_file),
    punches_thrown=punches,
    defensive_actions=defenses,
    footwork_segments=footwork,
    pose_data=pose_data
)

# 5. Get coaching feedback
coach = create_boxing_coach()
feedback = coach.analyze_session(video_data, boxer_profile)
```

### REST API Endpoint

```python
from flask import Flask, request, jsonify
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile

app = Flask(__name__)
coach = create_boxing_coach()

@app.route('/api/analyze', methods=['POST'])
def analyze_session():
    data = request.json
    
    # Parse input
    video_data = VideoAnalysisData(**data['video_analysis'])
    boxer_profile = BoxerProfile(**data['boxer_profile'])
    
    # Analyze
    feedback = coach.analyze_session(video_data, boxer_profile)
    
    # Return JSON
    return jsonify({
        'summary': feedback.summary,
        'strengths': feedback.strengths,
        'weaknesses': feedback.weaknesses,
        'corrections': feedback.technical_corrections,
        'drills': feedback.recommended_drills,
        'message': feedback.motivational_message
    })
```

## Customization

### Adding Custom Drills

Edit `drill_recommender.py` and add to the `_build_drill_library()` method:

```python
'custom_category': [
    {
        'name': 'My Custom Drill',
        'description': 'Description here',
        'instructions': ['Step 1', 'Step 2', ...],
        'sets_reps': '3 × 10',
        'rest': '30 seconds',
        'difficulty': 'intermediate',
        'equipment': ['equipment needed'],
        'focus_points': ['Focus 1', 'Focus 2']
    }
]
```

### Adjusting Analysis Thresholds

Modify `technical_analyzer.py` to adjust what constitutes a weakness:

```python
# Example: Change accuracy threshold
if accuracy_rate < 0.5:  # Currently 50%, adjust as needed
    # Add to weaknesses
```

### Customizing Motivational Messages

Edit `feedback_generator.py` to add your own phrases:

```python
self.motivational_phrases = {
    'opening': ['Your custom opening', ...],
    'encouragement': ['Your encouragement', ...],
    'closing': ['Your closing', ...]
}
```

## Use Cases

1. **Personal Training**: Analyze athlete training sessions and provide detailed feedback
2. **Remote Coaching**: Coaches can analyze videos sent by remote athletes
3. **Boxing Gyms**: Automated analysis for multiple members
4. **Competition Prep**: Detailed strategic analysis of sparring sessions
5. **Technique Development**: Track progress on specific technical goals
6. **Self-Coaching**: Athletes can get immediate feedback on their training

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: None required (pure Python), optional packages available
- **Architecture**: Modular design for easy extension and customization
- **Performance**: Lightweight, processes analysis data in milliseconds
- **Data**: Works with pre-processed video analysis data (pose estimation output)

## Limitations & Future Enhancements

### Current Limitations
- Requires pre-processed video analysis data (pose estimation, action recognition)
- Does not process raw video directly
- Analysis thresholds are static (not ML-based)

### Planned Enhancements
- [ ] ML-based pattern recognition for more sophisticated analysis
- [ ] Video file input with integrated pose estimation
- [ ] Historical performance tracking database
- [ ] Visualization generation (charts, heatmaps)
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Real-time analysis during training
- [ ] Opponent-specific strategic recommendations
- [ ] Automated highlight reel generation

## Contributing

Contributions are welcome! Areas for contribution:
- Additional drill library entries
- More sophisticated analysis algorithms
- Integration examples
- Visualization components
- Multi-language support

## License

[Specify your license here]

## Support

For questions, issues, or feature requests, please open an issue on the repository.

## Acknowledgments

Built with expertise in boxing coaching methodology and sports performance analysis.

---

**Note**: This agent processes pre-analyzed video data. Integrate with your preferred pose estimation and action recognition systems (MediaPipe, OpenPose, custom ML models, etc.) to create a complete video-to-feedback pipeline.
