# Boxing Coach AI Agent - API Integration Guide

Complete guide for integrating the Boxing Coach AI Agent into your applications, video processing pipelines, and coaching platforms.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core API Reference](#core-api-reference)
3. [Data Formats](#data-formats)
4. [Integration Patterns](#integration-patterns)
5. [REST API Examples](#rest-api-examples)
6. [Video Processing Pipeline](#video-processing-pipeline)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

## Quick Start

### Basic Analysis Flow

```python
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile, SkillLevel, SessionType

# 1. Initialize coach (do once, reuse)
coach = create_boxing_coach()

# 2. Prepare data
video_data = VideoAnalysisData(
    session_type=SessionType.TRAINING,
    duration_seconds=180.0,
    punches_thrown=[...],
    defensive_actions=[...],
    footwork_segments=[...],
    pose_data=[...]
)

boxer_profile = BoxerProfile(
    name="Athlete Name",
    skill_level=SkillLevel.INTERMEDIATE,
    goals=["Goal 1", "Goal 2"]
)

# 3. Analyze
feedback = coach.analyze_session(video_data, boxer_profile)

# 4. Get formatted output
report = coach.generate_session_report(feedback, format="detailed")
```

## Core API Reference

### BoxingCoachAgent

Main agent class for analyzing boxing performance.

#### Methods

##### `analyze_session(video_data, boxer_profile) -> CoachingFeedback`

Analyzes a boxing session and generates comprehensive coaching feedback.

**Parameters:**
- `video_data` (VideoAnalysisData): Pre-processed video analysis data
- `boxer_profile` (BoxerProfile): Athlete profile and context

**Returns:**
- `CoachingFeedback`: Complete coaching feedback object

**Example:**
```python
feedback = coach.analyze_session(video_data, boxer_profile)
print(f"Found {len(feedback.strengths)} strengths")
print(f"Identified {len(feedback.weaknesses)} areas to improve")
print(f"Recommended {len(feedback.recommended_drills)} drills")
```

##### `generate_session_report(feedback, format) -> str`

Generates a formatted report from coaching feedback.

**Parameters:**
- `feedback` (CoachingFeedback): Feedback object from analyze_session
- `format` (str): Output format - "detailed", "summary", or "json"

**Returns:**
- `str`: Formatted report

**Example:**
```python
# Detailed report for athlete
detailed = coach.generate_session_report(feedback, format="detailed")

# Quick summary for dashboard
summary = coach.generate_session_report(feedback, format="summary")

# JSON for API response
json_data = coach.generate_session_report(feedback, format="json")
```

### Factory Function

##### `create_boxing_coach() -> BoxingCoachAgent`

Factory function to create a configured boxing coach instance.

**Returns:**
- `BoxingCoachAgent`: Initialized coach ready for analysis

**Example:**
```python
coach = create_boxing_coach()
```

## Data Formats

### VideoAnalysisData

Complete video analysis data structure.

```python
from boxing_coach_agent import VideoAnalysisData, SessionType

video_data = VideoAnalysisData(
    session_type=SessionType.TRAINING,  # Required
    duration_seconds=180.0,              # Required
    punches_thrown=[...],                # Required
    defensive_actions=[...],             # Required
    footwork_segments=[...],             # Required
    pose_data=[...],                     # Required
    heart_rate_data=[120, 130, ...],    # Optional
    metadata={'key': 'value'}           # Optional
)
```

#### Punch Data Format

```python
punch = {
    'type': 'jab',           # Required: 'jab', 'cross', 'hook', 'uppercut', 'overhand'
    'timestamp': 1.5,        # Required: seconds from start
    'landed': True,          # Required: bool
    'power': 7,              # Required: 0-10 scale
    'speed': 8,              # Required: 0-10 scale
    'guard_returned': True,  # Required: bool
    'overextended': False,   # Required: bool
    'telegraphed': False     # Required: bool
}
```

#### Defensive Action Format

```python
defense = {
    'type': 'slip',          # Required: 'slip', 'block', 'parry', 'roll', 'duck', 'clinch'
    'timestamp': 2.0,        # Required: seconds from start
    'successful': True,      # Required: bool
    'chin_exposed': False,   # Required: bool
    'hands_down': False      # Required: bool
}
```

#### Footwork Segment Format

```python
footwork = {
    'direction': 'forward',     # Required: 'forward', 'backward', 'lateral'
    'timestamp': 0.5,           # Required: seconds from start
    'flat_footed': False,       # Required: bool
    'squared_stance': False,    # Required: bool
    'crossed_feet': False,      # Required: bool
    'movement_type': 'step',    # Required: 'step', 'pivot'
    'ring_position': 'center',  # Required: 'center', 'edge', 'corner'
    'trapped': False,           # Required: bool
    'quality': 7                # Optional: 0-10 scale (for pivots)
}
```

#### Pose Data Format

```python
pose = {
    'timestamp': 0.1,      # Required: seconds from start
    'balance_score': 8     # Required: 0-10 scale from pose estimation
}
```

### BoxerProfile

Athlete profile and context.

```python
from boxing_coach_agent import BoxerProfile, SkillLevel

profile = BoxerProfile(
    name="Alex Martinez",                    # Required
    skill_level=SkillLevel.INTERMEDIATE,     # Required
    goals=[                                  # Required
        "Improve defensive skills",
        "Increase combination variety"
    ],
    previous_feedback=[                      # Optional (for progress tracking)
        "Work on guard return",
        "Improve footwork balance"
    ],
    strengths=[                              # Optional
        "Strong jab",
        "Good work ethic"
    ],
    known_weaknesses=[                       # Optional
        "Telegraphing power shots"
    ],
    training_history={                       # Optional
        'sessions_completed': 45,
        'last_session': '2025-11-01'
    }
)
```

#### SkillLevel Enum

```python
from boxing_coach_agent import SkillLevel

SkillLevel.BEGINNER       # New to boxing
SkillLevel.INTERMEDIATE   # 1-3 years experience
SkillLevel.ADVANCED       # 3+ years, competitive
SkillLevel.PROFESSIONAL   # Pro or elite amateur
```

#### SessionType Enum

```python
from boxing_coach_agent import SessionType

SessionType.TRAINING         # General training
SessionType.SPARRING        # Sparring session
SessionType.COMPETITION     # Actual fight
SessionType.TECHNICAL_DRILL # Focused technical work
```

### CoachingFeedback

Output structure with complete feedback.

```python
# Returned from analyze_session()
feedback = CoachingFeedback(
    summary="Session overview...",                    # str
    strengths=["Strength 1", "Strength 2"],          # List[str]
    weaknesses=["Weakness 1", "Weakness 2"],         # List[str]
    technical_corrections=[...],                      # List[Dict]
    strategic_insights=["Insight 1", "Insight 2"],   # List[str]
    recommended_drills=[...],                        # List[Dict]
    motivational_message="Keep pushing...",          # str
    progress_notes="Improved from last...",          # Optional[str]
    next_session_focus=["Focus 1", "Focus 2"]       # List[str]
)

# Access feedback components
print(feedback.summary)
for strength in feedback.strengths:
    print(f"✓ {strength}")

for drill in feedback.recommended_drills:
    print(f"Drill: {drill['name']}")
    print(f"  {drill['description']}")
```

## Integration Patterns

### Pattern 1: Batch Video Processing

Process multiple videos and generate reports.

```python
from pathlib import Path
from boxing_coach_agent import create_boxing_coach
from your_video_processor import process_video  # Your video processing module

def batch_process_sessions(video_folder, output_folder):
    coach = create_boxing_coach()
    
    for video_file in Path(video_folder).glob("*.mp4"):
        # 1. Process video to get analysis data
        video_data, boxer_profile = process_video(video_file)
        
        # 2. Get coaching feedback
        feedback = coach.analyze_session(video_data, boxer_profile)
        
        # 3. Save report
        report = coach.generate_session_report(feedback, format="detailed")
        output_file = Path(output_folder) / f"{video_file.stem}_report.txt"
        output_file.write_text(report)
        
        # 4. Save JSON for dashboard
        json_data = coach.generate_session_report(feedback, format="json")
        json_file = Path(output_folder) / f"{video_file.stem}_data.json"
        json_file.write_text(json_data)
        
        print(f"✓ Processed {video_file.name}")
```

### Pattern 2: Real-time Analysis

Analyze live training sessions.

```python
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, SessionType
from your_tracker import LivePerformanceTracker  # Your real-time tracking

def analyze_live_session(boxer_profile, session_duration=180):
    coach = create_boxing_coach()
    tracker = LivePerformanceTracker()
    
    # Track session
    print("Recording session...")
    tracker.start()
    time.sleep(session_duration)
    tracker.stop()
    
    # Get collected data
    video_data = VideoAnalysisData(
        session_type=SessionType.TRAINING,
        duration_seconds=tracker.get_duration(),
        punches_thrown=tracker.get_punches(),
        defensive_actions=tracker.get_defenses(),
        footwork_segments=tracker.get_footwork(),
        pose_data=tracker.get_pose_data()
    )
    
    # Analyze
    feedback = coach.analyze_session(video_data, boxer_profile)
    
    # Display immediate feedback
    summary = coach.generate_session_report(feedback, format="summary")
    print(summary)
    
    return feedback
```

### Pattern 3: Progressive Training System

Track progress across multiple sessions.

```python
from boxing_coach_agent import create_boxing_coach
import json
from datetime import datetime

class ProgressiveTrainingSystem:
    def __init__(self, athlete_id):
        self.athlete_id = athlete_id
        self.coach = create_boxing_coach()
        self.history_file = f"athlete_{athlete_id}_history.json"
        self.load_history()
    
    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = {'sessions': [], 'profile': None}
    
    def analyze_session(self, video_data, boxer_profile):
        # Update profile with previous feedback for context
        if self.history['sessions']:
            last_session = self.history['sessions'][-1]
            boxer_profile.previous_feedback = last_session.get('weaknesses', [])
        
        # Analyze
        feedback = coach.analyze_session(video_data, boxer_profile)
        
        # Save to history
        session_record = {
            'date': datetime.now().isoformat(),
            'strengths': feedback.strengths,
            'weaknesses': feedback.weaknesses,
            'drills_assigned': [d['name'] for d in feedback.recommended_drills],
            'summary': feedback.summary
        }
        self.history['sessions'].append(session_record)
        self.save_history()
        
        return feedback
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_progress_report(self):
        """Generate progress report across all sessions"""
        if len(self.history['sessions']) < 2:
            return "Not enough sessions for progress analysis"
        
        first = self.history['sessions'][0]
        latest = self.history['sessions'][-1]
        
        # Compare weaknesses
        improved = set(first['weaknesses']) - set(latest['weaknesses'])
        ongoing = set(first['weaknesses']) & set(latest['weaknesses'])
        
        report = f"Progress Report ({len(self.history['sessions'])} sessions)\n"
        report += f"\nImproved Areas:\n"
        for item in improved:
            report += f"  ✓ {item}\n"
        
        report += f"\nStill Working On:\n"
        for item in ongoing:
            report += f"  → {item}\n"
        
        return report
```

## REST API Examples

### Flask API

```python
from flask import Flask, request, jsonify
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile, SkillLevel, SessionType

app = Flask(__name__)
coach = create_boxing_coach()

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_session():
    """
    Analyze a boxing session
    
    Request body:
    {
        "video_analysis": {...},  # VideoAnalysisData fields
        "boxer_profile": {...}    # BoxerProfile fields
    }
    
    Returns: CoachingFeedback as JSON
    """
    try:
        data = request.json
        
        # Parse session type
        session_type = SessionType[data['video_analysis']['session_type'].upper()]
        
        # Create video data
        video_data = VideoAnalysisData(
            session_type=session_type,
            duration_seconds=data['video_analysis']['duration_seconds'],
            punches_thrown=data['video_analysis']['punches_thrown'],
            defensive_actions=data['video_analysis']['defensive_actions'],
            footwork_segments=data['video_analysis']['footwork_segments'],
            pose_data=data['video_analysis']['pose_data'],
            metadata=data['video_analysis'].get('metadata')
        )
        
        # Create boxer profile
        skill_level = SkillLevel[data['boxer_profile']['skill_level'].upper()]
        boxer_profile = BoxerProfile(
            name=data['boxer_profile']['name'],
            skill_level=skill_level,
            goals=data['boxer_profile']['goals'],
            previous_feedback=data['boxer_profile'].get('previous_feedback'),
            strengths=data['boxer_profile'].get('strengths'),
            known_weaknesses=data['boxer_profile'].get('known_weaknesses')
        )
        
        # Analyze
        feedback = coach.analyze_session(video_data, boxer_profile)
        
        # Return JSON response
        return jsonify({
            'success': True,
            'feedback': {
                'summary': feedback.summary,
                'strengths': feedback.strengths,
                'weaknesses': feedback.weaknesses,
                'corrections': feedback.technical_corrections,
                'strategic_insights': feedback.strategic_insights,
                'drills': feedback.recommended_drills,
                'motivational_message': feedback.motivational_message,
                'progress_notes': feedback.progress_notes,
                'next_session_focus': feedback.next_session_focus
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/v1/report/<format>', methods=['POST'])
def get_formatted_report(format):
    """
    Get formatted report from feedback
    
    Formats: detailed, summary, json
    """
    try:
        # Assuming feedback is posted
        # In production, you'd retrieve from database
        data = request.json
        feedback = CoachingFeedback(**data['feedback'])
        
        report = coach.generate_session_report(feedback, format=format)
        
        if format == 'json':
            return jsonify(json.loads(report))
        else:
            return report, 200, {'Content-Type': 'text/plain'}
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile, SkillLevel, SessionType

app = FastAPI(title="Boxing Coach AI API")
coach = create_boxing_coach()

# Pydantic models for request validation
class PunchData(BaseModel):
    type: str
    timestamp: float
    landed: bool
    power: int
    speed: int
    guard_returned: bool
    overextended: bool
    telegraphed: bool

class DefenseData(BaseModel):
    type: str
    timestamp: float
    successful: bool
    chin_exposed: bool
    hands_down: bool

class FootworkData(BaseModel):
    direction: str
    timestamp: float
    flat_footed: bool
    squared_stance: bool
    crossed_feet: bool
    movement_type: str
    ring_position: str
    trapped: bool
    quality: Optional[int] = None

class PoseData(BaseModel):
    timestamp: float
    balance_score: int

class VideoAnalysis(BaseModel):
    session_type: str
    duration_seconds: float
    punches_thrown: List[PunchData]
    defensive_actions: List[DefenseData]
    footwork_segments: List[FootworkData]
    pose_data: List[PoseData]
    metadata: Optional[Dict[str, Any]] = None

class BoxerProfileRequest(BaseModel):
    name: str
    skill_level: str
    goals: List[str]
    previous_feedback: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    known_weaknesses: Optional[List[str]] = None

class AnalysisRequest(BaseModel):
    video_analysis: VideoAnalysis
    boxer_profile: BoxerProfileRequest

@app.post("/api/v1/analyze")
async def analyze_session(request: AnalysisRequest):
    """Analyze a boxing session and return coaching feedback"""
    try:
        # Convert Pydantic models to agent data structures
        video_data = VideoAnalysisData(
            session_type=SessionType[request.video_analysis.session_type.upper()],
            duration_seconds=request.video_analysis.duration_seconds,
            punches_thrown=[p.dict() for p in request.video_analysis.punches_thrown],
            defensive_actions=[d.dict() for d in request.video_analysis.defensive_actions],
            footwork_segments=[f.dict() for f in request.video_analysis.footwork_segments],
            pose_data=[p.dict() for p in request.video_analysis.pose_data],
            metadata=request.video_analysis.metadata
        )
        
        boxer_profile = BoxerProfile(
            name=request.boxer_profile.name,
            skill_level=SkillLevel[request.boxer_profile.skill_level.upper()],
            goals=request.boxer_profile.goals,
            previous_feedback=request.boxer_profile.previous_feedback,
            strengths=request.boxer_profile.strengths,
            known_weaknesses=request.boxer_profile.known_weaknesses
        )
        
        # Analyze
        feedback = coach.analyze_session(video_data, boxer_profile)
        
        return {
            "success": True,
            "feedback": {
                "summary": feedback.summary,
                "strengths": feedback.strengths,
                "weaknesses": feedback.weaknesses,
                "corrections": feedback.technical_corrections,
                "strategic_insights": feedback.strategic_insights,
                "drills": feedback.recommended_drills,
                "motivational_message": feedback.motivational_message,
                "progress_notes": feedback.progress_notes,
                "next_session_focus": feedback.next_session_focus
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "boxing-coach-ai"}
```

## Video Processing Pipeline

### Complete Integration Example

```python
"""
Complete pipeline from raw video to coaching feedback
"""
import cv2
import mediapipe as mp
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile, SkillLevel, SessionType

class BoxingVideoProcessor:
    def __init__(self):
        self.coach = create_boxing_coach()
        self.pose_estimator = mp.solutions.pose.Pose()
        # Initialize your action classifier here
        self.action_classifier = YourActionClassifier()
    
    def process_video(self, video_path, boxer_profile):
        """
        Complete pipeline: video → analysis → feedback
        """
        # 1. Extract frames and process
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        punches = []
        defenses = []
        footwork = []
        poses = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_count / fps
            
            # 2. Pose estimation
            results = self.pose_estimator.process(frame)
            if results.pose_landmarks:
                balance = self._calculate_balance(results.pose_landmarks)
                poses.append({'timestamp': timestamp, 'balance_score': balance})
                
                # 3. Action recognition
                action = self.action_classifier.predict(frame, results.pose_landmarks)
                
                if action['type'] == 'punch':
                    punches.append(self._create_punch_data(action, timestamp))
                elif action['type'] == 'defense':
                    defenses.append(self._create_defense_data(action, timestamp))
                
                # 4. Footwork analysis
                footwork_data = self._analyze_footwork(results.pose_landmarks, timestamp)
                if footwork_data:
                    footwork.append(footwork_data)
            
            frame_count += 1
        
        cap.release()
        
        # 5. Create video analysis data
        duration = frame_count / fps
        video_data = VideoAnalysisData(
            session_type=SessionType.TRAINING,
            duration_seconds=duration,
            punches_thrown=punches,
            defensive_actions=defenses,
            footwork_segments=footwork,
            pose_data=poses
        )
        
        # 6. Get coaching feedback
        feedback = self.coach.analyze_session(video_data, boxer_profile)
        
        return feedback
    
    def _calculate_balance(self, landmarks):
        # Your balance calculation logic
        return 7  # 0-10 scale
    
    def _create_punch_data(self, action, timestamp):
        return {
            'type': action['punch_type'],
            'timestamp': timestamp,
            'landed': action.get('landed', False),
            'power': action.get('power', 5),
            'speed': action.get('speed', 5),
            'guard_returned': action.get('guard_returned', True),
            'overextended': action.get('overextended', False),
            'telegraphed': action.get('telegraphed', False)
        }
    
    def _create_defense_data(self, action, timestamp):
        return {
            'type': action['defense_type'],
            'timestamp': timestamp,
            'successful': action.get('successful', True),
            'chin_exposed': action.get('chin_exposed', False),
            'hands_down': action.get('hands_down', False)
        }
    
    def _analyze_footwork(self, landmarks, timestamp):
        # Your footwork analysis logic
        return {
            'direction': 'forward',
            'timestamp': timestamp,
            'flat_footed': False,
            'squared_stance': False,
            'crossed_feet': False,
            'movement_type': 'step',
            'ring_position': 'center',
            'trapped': False
        }

# Usage
processor = BoxingVideoProcessor()
boxer_profile = BoxerProfile(name="Alex", skill_level=SkillLevel.INTERMEDIATE, goals=["Improve technique"])
feedback = processor.process_video("training_session.mp4", boxer_profile)
print(processor.coach.generate_session_report(feedback, format="detailed"))
```

## Error Handling

### Handling Invalid Data

```python
from boxing_coach_agent import create_boxing_coach, VideoAnalysisData, BoxerProfile

def safe_analyze(video_data_dict, profile_dict):
    """Safely analyze with error handling"""
    try:
        coach = create_boxing_coach()
        
        # Validate and create data structures
        video_data = VideoAnalysisData(**video_data_dict)
        boxer_profile = BoxerProfile(**profile_dict)
        
        # Analyze
        feedback = coach.analyze_session(video_data, boxer_profile)
        
        return {'success': True, 'feedback': feedback}
        
    except TypeError as e:
        return {'success': False, 'error': f'Invalid data format: {str(e)}'}
    except ValueError as e:
        return {'success': False, 'error': f'Invalid value: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}
```

### Validation Helpers

```python
def validate_punch_data(punch):
    """Validate punch data before processing"""
    required_fields = ['type', 'timestamp', 'landed', 'power', 'speed', 
                      'guard_returned', 'overextended', 'telegraphed']
    
    for field in required_fields:
        if field not in punch:
            raise ValueError(f"Missing required field: {field}")
    
    if punch['type'] not in ['jab', 'cross', 'hook', 'uppercut', 'overhand']:
        raise ValueError(f"Invalid punch type: {punch['type']}")
    
    if not 0 <= punch['power'] <= 10:
        raise ValueError(f"Power must be 0-10: {punch['power']}")
    
    return True
```

## Best Practices

### 1. Reuse Coach Instance

```python
# Good: Create once, reuse
coach = create_boxing_coach()
for session in sessions:
    feedback = coach.analyze_session(session.video_data, session.profile)

# Bad: Creating new instance each time
for session in sessions:
    coach = create_boxing_coach()  # Unnecessary overhead
    feedback = coach.analyze_session(session.video_data, session.profile)
```

### 2. Provide Complete Context

```python
# Good: Full context for better analysis
boxer_profile = BoxerProfile(
    name="Alex",
    skill_level=SkillLevel.INTERMEDIATE,
    goals=["Improve defense", "Build stamina"],
    previous_feedback=["Work on guard return"],  # Helps track progress
    strengths=["Strong jab"],
    known_weaknesses=["Flat-footed"]
)

# Okay: Minimal but functional
boxer_profile = BoxerProfile(
    name="Alex",
    skill_level=SkillLevel.INTERMEDIATE,
    goals=["General improvement"]
)
```

### 3. Handle Empty Data Gracefully

```python
# Agent handles empty data, but validate upstream
if not video_data.punches_thrown:
    print("Warning: No punches detected in session")
    # Decide if you want to proceed or not

feedback = coach.analyze_session(video_data, boxer_profile)
# Agent will still provide feedback, noting lack of data
```

### 4. Store Feedback for Progress Tracking

```python
import json
from datetime import datetime

def save_session_feedback(athlete_id, feedback):
    """Save feedback for historical tracking"""
    record = {
        'timestamp': datetime.now().isoformat(),
        'athlete_id': athlete_id,
        'summary': feedback.summary,
        'strengths': feedback.strengths,
        'weaknesses': feedback.weaknesses,
        'drills_assigned': [d['name'] for d in feedback.recommended_drills]
    }
    
    with open(f'athlete_{athlete_id}_history.jsonl', 'a') as f:
        f.write(json.dumps(record) + '\n')
```

### 5. Format Selection

```python
# For athletes: Use detailed or summary
athlete_report = coach.generate_session_report(feedback, format="detailed")

# For coaches dashboard: Use summary
dashboard_report = coach.generate_session_report(feedback, format="summary")

# For APIs and storage: Use JSON
api_response = coach.generate_session_report(feedback, format="json")
```

---

## Support & Feedback

For integration support, bug reports, or feature requests, please open an issue on the repository.

## Version History

- v1.0.0: Initial release with core coaching functionality
