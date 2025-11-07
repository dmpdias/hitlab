"""
Drill Recommender Module

Recommends specific drills and exercises to address identified weaknesses
and improve boxing performance.
"""

from typing import List, Dict, Any
from boxing_coach_agent import SkillLevel, SessionType


class DrillRecommender:
    """Recommends targeted drills based on identified weaknesses"""
    
    def __init__(self):
        self.drill_library = self._build_drill_library()
    
    def recommend_drills(
        self,
        weaknesses: List[str],
        skill_level: SkillLevel,
        session_type: SessionType,
        specific_issues: List[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Recommend drills based on weaknesses and context
        
        Args:
            weaknesses: List of identified weaknesses
            skill_level: Boxer's skill level
            session_type: Type of session being analyzed
            specific_issues: Detailed technical issues
            
        Returns:
            List of recommended drills with descriptions and instructions
        """
        recommended_drills = []
        
        # Map weaknesses to drill categories
        weakness_keywords = {
            'power': ['power', 'strength'],
            'accuracy': ['accuracy', 'precision', 'missing'],
            'defense': ['defensive', 'defensive gaps', 'absorbing', 'chin exposure'],
            'guard': ['guard', 'hands', 'dropping'],
            'footwork': ['footwork', 'balance', 'flat-footed', 'squared', 'movement'],
            'speed': ['speed', 'slow'],
            'stamina': ['energy', 'stamina', 'conditioning', 'fading'],
            'combinations': ['combination', 'variety', 'limited'],
            'head_movement': ['head movement', 'evasion', 'slip', 'roll'],
            'jab': ['jab', 'jabbing'],
            'telegraph': ['telegraph', 'predictable']
        }
        
        # Identify relevant drill categories
        relevant_categories = set()
        for weakness in weaknesses:
            weakness_lower = weakness.lower()
            for category, keywords in weakness_keywords.items():
                if any(keyword in weakness_lower for keyword in keywords):
                    relevant_categories.add(category)
        
        # Also check specific issues
        if specific_issues:
            for issue in specific_issues:
                issue_text = issue.get('issue', '').lower() + ' ' + issue.get('category', '').lower()
                for category, keywords in weakness_keywords.items():
                    if any(keyword in issue_text for keyword in keywords):
                        relevant_categories.add(category)
        
        # Get drills for each relevant category
        for category in relevant_categories:
            category_drills = self.drill_library.get(category, [])
            
            # Filter drills by skill level
            suitable_drills = [
                drill for drill in category_drills
                if self._is_suitable_for_level(drill, skill_level)
            ]
            
            # Add top drills from this category
            recommended_drills.extend(suitable_drills[:2])  # Top 2 per category
        
        # Ensure we have at least some drills
        if not recommended_drills:
            recommended_drills = self._get_general_fundamentals(skill_level)
        
        # Limit total drills to avoid overwhelming
        max_drills = {
            SkillLevel.BEGINNER: 4,
            SkillLevel.INTERMEDIATE: 6,
            SkillLevel.ADVANCED: 8,
            SkillLevel.PROFESSIONAL: 10
        }.get(skill_level, 6)
        
        return recommended_drills[:max_drills]
    
    def _build_drill_library(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build comprehensive drill library"""
        return {
            'power': [
                {
                    'name': 'Heavy Bag Power Shots',
                    'description': 'Focus on generating power from legs through core into punches',
                    'instructions': [
                        'Stand at heavy bag in proper stance',
                        'Throw single power shots with full body rotation',
                        'Focus on driving from back leg, rotating hips, turning shoulders',
                        'Snap punches into bag, don\'t push',
                        '3 rounds × 3 minutes, 30 seconds rest between rounds'
                    ],
                    'sets_reps': '3 rounds × 3 minutes',
                    'rest': '30 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['heavy bag'],
                    'focus_points': ['Leg drive', 'Hip rotation', 'Core engagement']
                },
                {
                    'name': 'Medicine Ball Rotational Throws',
                    'description': 'Build explosive rotational power for hooks and crosses',
                    'instructions': [
                        'Stand sideways to wall holding medicine ball (6-10 lbs)',
                        'Rotate and explosively throw ball at wall',
                        'Catch rebound and immediately repeat',
                        'Perform on both sides',
                        '3 sets × 15 reps per side'
                    ],
                    'sets_reps': '3 sets × 15 reps per side',
                    'rest': '60 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['medicine ball', 'wall'],
                    'focus_points': ['Explosive rotation', 'Core power', 'Balance']
                }
            ],
            'accuracy': [
                {
                    'name': 'Target Pad Precision Work',
                    'description': 'Improve punch accuracy with moving targets',
                    'instructions': [
                        'Partner holds focus mitts at various positions',
                        'Throw single punches hitting center of mitt',
                        'Start slow, emphasize accuracy over speed',
                        'Gradually increase speed while maintaining accuracy',
                        'Mix up punch types and angles',
                        '3 rounds × 2 minutes'
                    ],
                    'sets_reps': '3 rounds × 2 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['focus mitts', 'partner'],
                    'focus_points': ['Eye on target', 'Straight punches', 'Follow-through']
                },
                {
                    'name': 'Double-End Bag Training',
                    'description': 'Develop timing, accuracy, and hand-eye coordination',
                    'instructions': [
                        'Start with light taps to establish rhythm',
                        'Progress to crisp jabs maintaining rhythm',
                        'Add crosses and hooks once comfortable',
                        'Work on 3-4 punch combinations',
                        '4 rounds × 2 minutes'
                    ],
                    'sets_reps': '4 rounds × 2 minutes',
                    'rest': '30 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['double-end bag'],
                    'focus_points': ['Timing', 'Accuracy', 'Rhythm']
                }
            ],
            'defense': [
                {
                    'name': 'Slip Line Drill',
                    'description': 'Practice slipping punches with proper head movement',
                    'instructions': [
                        'Hang rope or cord at head height',
                        'Move along the line, slipping under it side to side',
                        'Keep hands up, bend at waist and knees',
                        'Move head just enough to avoid the line',
                        'Progress to adding counters after each slip',
                        '3 rounds × 2 minutes'
                    ],
                    'sets_reps': '3 rounds × 2 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['rope/cord'],
                    'focus_points': ['Minimal movement', 'Hands stay up', 'Balance']
                },
                {
                    'name': 'Partner Slip and Counter',
                    'description': 'Reactive defense with counter-punching',
                    'instructions': [
                        'Partner throws light jabs at 50% speed',
                        'Slip the jab and counter with cross or hook',
                        'Partner varies timing and height',
                        'Defender focuses on minimal head movement',
                        'Switch roles every round',
                        '3 rounds × 2 minutes per person'
                    ],
                    'sets_reps': '3 rounds × 2 minutes',
                    'rest': '60 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['partner', 'gloves'],
                    'focus_points': ['Reaction time', 'Counter timing', 'Defense-to-offense']
                }
            ],
            'guard': [
                {
                    'name': 'Shadow Boxing Guard Focus',
                    'description': 'Maintain proper guard through all movements',
                    'instructions': [
                        'Shadow box with emphasis on guard position',
                        'After every punch, snap hand back to guard',
                        'Keep non-punching hand glued to face',
                        'Practice in front of mirror',
                        'Call out "guard" after each punch as reminder',
                        '3 rounds × 3 minutes'
                    ],
                    'sets_reps': '3 rounds × 3 minutes',
                    'rest': '30 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['mirror (optional)'],
                    'focus_points': ['Fast return', 'Static hand', 'Awareness']
                },
                {
                    'name': 'Rubber Band Resistance Training',
                    'description': 'Build muscle memory for guard return',
                    'instructions': [
                        'Attach light resistance bands to hands',
                        'Bands should pull hands back toward guard position',
                        'Practice all punch types against resistance',
                        'Focus on fighting band to extend, then riding it back',
                        '4 sets × 1 minute per punch type'
                    ],
                    'sets_reps': '4 sets × 1 minute',
                    'rest': '30 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['resistance bands'],
                    'focus_points': ['Muscle memory', 'Return speed', 'Control']
                }
            ],
            'footwork': [
                {
                    'name': 'Ladder Footwork Drills',
                    'description': 'Improve foot speed, coordination, and balance',
                    'instructions': [
                        'Set up agility ladder on ground',
                        'Perform various patterns: in-out, lateral, forward-back',
                        'Stay on balls of feet',
                        'Maintain boxing stance throughout',
                        'Keep hands up in guard position',
                        '5 patterns × 3 runs each'
                    ],
                    'sets_reps': '5 patterns × 3 runs',
                    'rest': '30 seconds between patterns',
                    'difficulty': 'beginner',
                    'equipment': ['agility ladder'],
                    'focus_points': ['Ball of foot', 'Quick steps', 'Balance']
                },
                {
                    'name': 'Ring Control Drill',
                    'description': 'Practice cutting off the ring and controlling space',
                    'instructions': [
                        'Partner moves around ring avoiding corners',
                        'You work on cutting angles and controlling center',
                        'Use lateral movement, not chasing',
                        'Maintain proper stance while moving',
                        'Switch roles each round',
                        '3 rounds × 2 minutes per person'
                    ],
                    'sets_reps': '3 rounds × 2 minutes',
                    'rest': '60 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['ring/marked area', 'partner'],
                    'focus_points': ['Angle cutting', 'Center control', 'Positioning']
                },
                {
                    'name': 'Pivot and Angle Drill',
                    'description': 'Master pivoting to create angles',
                    'instructions': [
                        'Start facing heavy bag in stance',
                        'Throw 2-3 punch combination',
                        'Pivot 45-90 degrees to side',
                        'Reset and repeat from new angle',
                        'Alternate pivot directions',
                        '4 rounds × 3 minutes'
                    ],
                    'sets_reps': '4 rounds × 3 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['heavy bag'],
                    'focus_points': ['Pivot on ball', 'Balance', 'Smooth transition']
                }
            ],
            'speed': [
                {
                    'name': 'Speed Bag Training',
                    'description': 'Develop hand speed, rhythm, and shoulder endurance',
                    'instructions': [
                        'Start with basic three-hit rhythm',
                        'Maintain consistent tempo',
                        'Keep hands at shoulder height',
                        'Progress to faster rhythms and combinations',
                        '5 rounds × 2 minutes'
                    ],
                    'sets_reps': '5 rounds × 2 minutes',
                    'rest': '30 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['speed bag'],
                    'focus_points': ['Rhythm', 'Relaxation', 'Endurance']
                },
                {
                    'name': 'Burst Combinations',
                    'description': 'Explosive speed in short bursts',
                    'instructions': [
                        'On heavy bag, throw max speed combinations for 10 seconds',
                        'Focus on speed, not power',
                        'Rest 20 seconds between bursts',
                        'Maintain proper form despite speed',
                        '10 bursts × 10 seconds'
                    ],
                    'sets_reps': '10 bursts × 10 seconds',
                    'rest': '20 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['heavy bag'],
                    'focus_points': ['Maximum speed', 'Form maintenance', 'Explosion']
                }
            ],
            'stamina': [
                {
                    'name': 'High-Intensity Interval Shadowboxing',
                    'description': 'Build boxing-specific endurance',
                    'instructions': [
                        '30 seconds max effort shadow boxing',
                        '30 seconds active rest (light movement)',
                        'Maintain proper technique when fatigued',
                        'Focus on breathing rhythm',
                        '8-12 rounds'
                    ],
                    'sets_reps': '8-12 rounds',
                    'rest': '30 seconds active',
                    'difficulty': 'intermediate',
                    'equipment': ['none'],
                    'focus_points': ['Intensity maintenance', 'Breathing', 'Form under fatigue']
                },
                {
                    'name': 'Continuous Combinations',
                    'description': 'Build work capacity and mental toughness',
                    'instructions': [
                        'Set timer for 3-minute rounds',
                        'Throw non-stop combinations on heavy bag',
                        'No breaks during round',
                        'Focus on steady pace, not sprinting',
                        '5-6 rounds × 3 minutes'
                    ],
                    'sets_reps': '5-6 rounds × 3 minutes',
                    'rest': '60 seconds',
                    'difficulty': 'advanced',
                    'equipment': ['heavy bag', 'timer'],
                    'focus_points': ['Pace management', 'Breathing', 'Consistency']
                }
            ],
            'combinations': [
                {
                    'name': 'Numbered Combination Practice',
                    'description': 'Master fundamental punch combinations',
                    'instructions': [
                        'Assign numbers to punches (1=jab, 2=cross, 3=lead hook, 4=rear hook, 5=lead uppercut, 6=rear uppercut)',
                        'Practice combinations: 1-2, 1-2-3, 1-2-3-2, 3-2-3, etc.',
                        'Start slow, build to fight speed',
                        'Focus on smooth transitions',
                        '4 rounds × 3 minutes'
                    ],
                    'sets_reps': '4 rounds × 3 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['heavy bag or mitts'],
                    'focus_points': ['Smooth flow', 'Balance', 'Power transfer']
                },
                {
                    'name': 'Freestyle Combination Flow',
                    'description': 'Develop creative combination skills',
                    'instructions': [
                        'On heavy bag, flow between random combinations',
                        'Mix punches to head and body',
                        'Vary punch count from 2-6 per combo',
                        'Include footwork and pivots between combos',
                        'No predetermined pattern',
                        '5 rounds × 3 minutes'
                    ],
                    'sets_reps': '5 rounds × 3 minutes',
                    'rest': '60 seconds',
                    'difficulty': 'advanced',
                    'equipment': ['heavy bag'],
                    'focus_points': ['Creativity', 'Flow', 'Adaptability']
                }
            ],
            'head_movement': [
                {
                    'name': 'Slip and Roll Shadowboxing',
                    'description': 'Practice defensive head movement fundamentals',
                    'instructions': [
                        'Shadow box imagining opponent throwing punches',
                        'Slip jabs and crosses (move head off center)',
                        'Roll under hooks (duck and rotate)',
                        'Add counters after defensive movement',
                        '4 rounds × 2 minutes'
                    ],
                    'sets_reps': '4 rounds × 2 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['mirror (optional)'],
                    'focus_points': ['Minimal movement', 'Balance', 'Counters']
                },
                {
                    'name': 'Tennis Ball Reflex Training',
                    'description': 'Improve reaction time and head movement',
                    'instructions': [
                        'Partner throws tennis ball at your head (not hard)',
                        'Slip, duck, or roll to avoid ball',
                        'Add counter punch after each evasion',
                        'Vary speeds and angles',
                        '3 rounds × 2 minutes'
                    ],
                    'sets_reps': '3 rounds × 2 minutes',
                    'rest': '60 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['tennis balls', 'partner'],
                    'focus_points': ['Reaction', 'Decision making', 'Multiple planes']
                }
            ],
            'jab': [
                {
                    'name': 'Jab-Only Rounds',
                    'description': 'Master the jab in all its variations',
                    'instructions': [
                        'Throw only jabs for entire round',
                        'Vary types: stiff jab, flick jab, power jab, double jab, triple jab',
                        'Mix speeds and targets (head/body)',
                        'Focus on perfect technique each time',
                        '5 rounds × 2 minutes on heavy bag'
                    ],
                    'sets_reps': '5 rounds × 2 minutes',
                    'rest': '30 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['heavy bag'],
                    'focus_points': ['Variety', 'Snap', 'Guard return']
                },
                {
                    'name': 'Jab Control and Setup Drill',
                    'description': 'Use jab to control distance and set up power shots',
                    'instructions': [
                        'On mitts or bag, establish rhythm with jabs',
                        'Use jab to create openings',
                        'Set up power shots with 2-3 jabs first',
                        'Practice jab-and-move patterns',
                        '4 rounds × 3 minutes'
                    ],
                    'sets_reps': '4 rounds × 3 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'intermediate',
                    'equipment': ['heavy bag or mitts'],
                    'focus_points': ['Distance control', 'Setup', 'Timing']
                }
            ],
            'telegraph': [
                {
                    'name': 'Mirror Self-Analysis',
                    'description': 'Identify and eliminate telegraphing movements',
                    'instructions': [
                        'Shadow box in front of mirror',
                        'Watch for pre-punch movements: shoulder dips, hand drops, weight shifts',
                        'Throw punches from static guard position',
                        'Keep upper body still until punch commitment',
                        '4 rounds × 2 minutes'
                    ],
                    'sets_reps': '4 rounds × 2 minutes',
                    'rest': '45 seconds',
                    'difficulty': 'beginner',
                    'equipment': ['mirror'],
                    'focus_points': ['Still upper body', 'No wind-up', 'Relaxation']
                },
                {
                    'name': 'Feint and Strike Drill',
                    'description': 'Use feints instead of telegraphing',
                    'instructions': [
                        'Practice feinting movements (subtle fakes)',
                        'Follow feints with actual strikes',
                        'Keep opponent guessing which is real',
                        'Vary feint-to-strike timing',
                        '3 rounds × 3 minutes on bag or with partner'
                    ],
                    'sets_reps': '3 rounds × 3 minutes',
                    'rest': '60 seconds',
                    'difficulty': 'advanced',
                    'equipment': ['heavy bag or partner'],
                    'focus_points': ['Deception', 'Timing variation', 'Commitment']
                }
            ]
        }
    
    def _is_suitable_for_level(self, drill: Dict[str, Any], skill_level: SkillLevel) -> bool:
        """Check if drill is suitable for boxer's skill level"""
        drill_difficulty = drill.get('difficulty', 'intermediate')
        
        level_hierarchy = {
            SkillLevel.BEGINNER: ['beginner'],
            SkillLevel.INTERMEDIATE: ['beginner', 'intermediate'],
            SkillLevel.ADVANCED: ['beginner', 'intermediate', 'advanced'],
            SkillLevel.PROFESSIONAL: ['beginner', 'intermediate', 'advanced', 'professional']
        }
        
        suitable_difficulties = level_hierarchy.get(skill_level, ['intermediate'])
        return drill_difficulty in suitable_difficulties
    
    def _get_general_fundamentals(self, skill_level: SkillLevel) -> List[Dict[str, Any]]:
        """Get general fundamental drills"""
        return [
            {
                'name': 'Basic Stance and Movement',
                'description': 'Master fundamental boxing stance and footwork',
                'instructions': [
                    'Practice proper boxing stance',
                    'Work on forward/backward movement',
                    'Add lateral movement',
                    'Combine with basic punches',
                    '3 rounds × 3 minutes'
                ],
                'sets_reps': '3 rounds × 3 minutes',
                'rest': '45 seconds',
                'difficulty': 'beginner',
                'equipment': ['none'],
                'focus_points': ['Balance', 'Posture', 'Weight distribution']
            },
            {
                'name': 'Fundamental Technique Shadow Boxing',
                'description': 'Perfect basic techniques through shadow boxing',
                'instructions': [
                    'Focus on jab, cross, hook, uppercut technique',
                    'Slow, deliberate movements',
                    'Check form in mirror if available',
                    'Progress to combinations',
                    '4 rounds × 3 minutes'
                ],
                'sets_reps': '4 rounds × 3 minutes',
                'rest': '60 seconds',
                'difficulty': 'beginner',
                'equipment': ['mirror (optional)'],
                'focus_points': ['Perfect form', 'Balance', 'Breathing']
            }
        ]
