"""
Technical Analyzer Module

Analyzes specific technical aspects of boxing performance:
- Punch mechanics and effectiveness
- Defensive technique and positioning
- Footwork and movement patterns
- Overall ring strategy
"""

from typing import List, Dict, Any
from boxing_coach_agent import SkillLevel


class TechnicalAnalyzer:
    """Analyzes technical aspects of boxing performance"""
    
    def __init__(self):
        self.punch_types = ['jab', 'cross', 'hook', 'uppercut', 'overhand']
        self.defensive_types = ['slip', 'block', 'parry', 'roll', 'duck', 'clinch']
    
    def analyze_punches(
        self, 
        punches: List[Dict[str, Any]], 
        skill_level: SkillLevel
    ) -> Dict[str, Any]:
        """
        Analyze punch technique, power, accuracy, and combinations
        
        Args:
            punches: List of punch data with type, speed, power, accuracy
            skill_level: Boxer's skill level for context
            
        Returns:
            Dictionary with punch analysis results
        """
        if not punches:
            return {
                'power_rating': 0,
                'accuracy_rate': 0,
                'combination_quality': 0,
                'hand_speed_rating': 0,
                'issues': [],
                'total_punches': 0
            }
        
        total_punches = len(punches)
        issues = []
        
        # Analyze punch accuracy
        accurate_punches = sum(1 for p in punches if p.get('landed', False))
        accuracy_rate = accurate_punches / total_punches if total_punches > 0 else 0
        
        # Analyze power (0-10 scale)
        avg_power = sum(p.get('power', 5) for p in punches) / total_punches
        power_rating = min(10, avg_power)
        
        # Analyze hand speed (0-10 scale)
        avg_speed = sum(p.get('speed', 5) for p in punches) / total_punches
        hand_speed_rating = min(10, avg_speed)
        
        # Check for common technical issues
        guard_returns = sum(1 for p in punches if p.get('guard_returned', True))
        guard_return_rate = guard_returns / total_punches
        
        if guard_return_rate < 0.7:
            issues.append({
                'description': 'Dropping hands after punching',
                'correction': 'Focus on snapping your punches back to guard position immediately after extending. Your hands should return as fast as they go out.',
                'key_points': [
                    'Keep your non-punching hand up protecting your chin',
                    'Practice shadow boxing with emphasis on the return motion',
                    'Imagine an elastic band pulling your hand back'
                ],
                'severity': 'high'
            })
        
        # Check for overextension
        overextension_count = sum(1 for p in punches if p.get('overextended', False))
        if overextension_count > 5:
            issues.append({
                'description': f'Overextending on {overextension_count} punches',
                'correction': 'Stop your punches 2-3 inches before full arm extension. This maintains balance, protects your joints, and allows faster recovery.',
                'key_points': [
                    'Keep a slight bend in your elbow at full extension',
                    'Punch through the target, not at it',
                    'Maintain your center of gravity'
                ],
                'severity': 'medium'
            })
        
        # Check for telegraphing
        telegraph_count = sum(1 for p in punches if p.get('telegraphed', False))
        if telegraph_count > 3:
            issues.append({
                'description': f'Telegraphing punches {telegraph_count} times',
                'correction': 'Eliminate preliminary movements before punching. No shoulder dips, no hand drops, no weight shifts that signal your intentions.',
                'key_points': [
                    'Start punches from your guard position',
                    'Keep your eyes on the target, not where you\'re punching',
                    'Stay relaxed until the moment of commitment'
                ],
                'severity': 'high'
            })
        
        # Analyze punch variety
        punch_types_used = set(p.get('type', 'unknown') for p in punches)
        if len(punch_types_used) < 3 and skill_level != SkillLevel.BEGINNER:
            issues.append({
                'description': 'Limited punch variety',
                'correction': 'Expand your offensive arsenal. Work on incorporating all punch types - jabs, crosses, hooks, and uppercuts - to keep opponents guessing.',
                'key_points': [
                    'Master each punch individually first',
                    'Combine different punches in fluid combinations',
                    'Attack from different angles and levels'
                ],
                'severity': 'medium'
            })
        
        # Analyze combinations
        combinations = self._analyze_combinations(punches)
        combination_quality = self._rate_combinations(combinations, skill_level)
        
        # Check jab usage (should be 30-40% of total punches)
        jab_count = sum(1 for p in punches if p.get('type') == 'jab')
        jab_percentage = jab_count / total_punches if total_punches > 0 else 0
        
        if jab_percentage < 0.25 and skill_level != SkillLevel.BEGINNER:
            issues.append({
                'description': 'Insufficient jab usage',
                'correction': 'Your jab is your most important weapon. Increase jab frequency to set up power punches, control distance, and disrupt opponent\'s rhythm.',
                'key_points': [
                    'Double and triple up your jab',
                    'Use different jab types: flicking, stiff, power',
                    'Jab to the body as well as the head'
                ],
                'severity': 'medium'
            })
        
        return {
            'power_rating': power_rating,
            'accuracy_rate': accuracy_rate,
            'combination_quality': combination_quality,
            'hand_speed_rating': hand_speed_rating,
            'guard_return_rate': guard_return_rate,
            'overextension_count': overextension_count,
            'telegraph_count': telegraph_count,
            'jab_percentage': jab_percentage,
            'total_punches': total_punches,
            'issues': issues,
            'punch_distribution': self._get_punch_distribution(punches)
        }
    
    def analyze_defense(
        self, 
        defensive_actions: List[Dict[str, Any]], 
        skill_level: SkillLevel
    ) -> Dict[str, Any]:
        """
        Analyze defensive technique and effectiveness
        
        Args:
            defensive_actions: List of defensive movements
            skill_level: Boxer's skill level
            
        Returns:
            Dictionary with defensive analysis
        """
        if not defensive_actions:
            return {
                'effectiveness_rating': 0,
                'head_movement_quality': 0,
                'blocking_efficiency': 0,
                'issues': [],
                'total_defensive_actions': 0
            }
        
        total_actions = len(defensive_actions)
        issues = []
        
        # Analyze defensive effectiveness
        successful_defenses = sum(1 for d in defensive_actions if d.get('successful', False))
        effectiveness_rate = successful_defenses / total_actions if total_actions > 0 else 0
        effectiveness_rating = effectiveness_rate * 10
        
        # Analyze head movement quality
        head_movements = [d for d in defensive_actions if d.get('type') in ['slip', 'duck', 'roll']]
        head_movement_quality = self._rate_head_movement(head_movements, skill_level)
        
        # Analyze blocking
        blocks = [d for d in defensive_actions if d.get('type') in ['block', 'parry']]
        blocking_efficiency = (
            sum(1 for b in blocks if b.get('successful', False)) / len(blocks)
            if blocks else 0.5
        )
        
        # Check for chin exposure
        chin_exposure_count = sum(1 for d in defensive_actions if d.get('chin_exposed', False))
        if chin_exposure_count > 5:
            issues.append({
                'description': f'Chin exposed {chin_exposure_count} times',
                'correction': 'Keep your chin tucked behind your lead shoulder at all times. Your chin should never be in the center or elevated.',
                'key_points': [
                    'Tuck chin down, look through your eyebrows',
                    'Lead shoulder should protect your chin',
                    'Raise your shoulders slightly to create a barrier'
                ],
                'severity': 'high'
            })
        
        # Check for predictable defensive patterns
        if self._has_predictable_patterns(defensive_actions):
            issues.append({
                'description': 'Predictable defensive patterns',
                'correction': 'Vary your defensive responses. Mix slips, rolls, blocks, and steps. Don\'t slip the same direction twice in a row.',
                'key_points': [
                    'Alternate directions when slipping',
                    'Combine defensive moves (slip + roll, block + counter)',
                    'Occasionally do the unexpected'
                ],
                'severity': 'high'
            })
        
        # Check for static defense
        movement_defense_count = len(head_movements)
        blocking_defense_count = len(blocks)
        
        if blocking_defense_count > movement_defense_count * 2:
            issues.append({
                'description': 'Over-reliance on blocking vs. head movement',
                'correction': 'Make them miss rather than blocking everything. Active defense through head movement is more effective and less tiring.',
                'key_points': [
                    'Slip straight punches (jabs, crosses)',
                    'Roll under hooks',
                    'Duck under wide swings'
                ],
                'severity': 'medium'
            })
        
        # Check for hands-down behavior
        hands_down_count = sum(1 for d in defensive_actions if d.get('hands_down', False))
        if hands_down_count > 0:
            issues.append({
                'description': 'Lowering hands during defense',
                'correction': 'Keep your hands up at all times, even when moving your head. Hands and head movement work together, not separately.',
                'key_points': [
                    'Hands stay at chin/temple level',
                    'Move your head, not your hands down',
                    'Stay ready to counter'
                ],
                'severity': 'high'
            })
        
        return {
            'effectiveness_rating': effectiveness_rating,
            'head_movement_quality': head_movement_quality,
            'blocking_efficiency': blocking_efficiency,
            'chin_exposure_count': chin_exposure_count,
            'predictable_patterns': self._has_predictable_patterns(defensive_actions),
            'total_defensive_actions': total_actions,
            'issues': issues,
            'defense_distribution': self._get_defense_distribution(defensive_actions)
        }
    
    def analyze_footwork(
        self,
        footwork_segments: List[Dict[str, Any]],
        pose_data: List[Dict[str, Any]],
        skill_level: SkillLevel
    ) -> Dict[str, Any]:
        """
        Analyze footwork, movement patterns, and ring positioning
        
        Args:
            footwork_segments: Movement pattern data
            pose_data: Pose estimation data for balance analysis
            skill_level: Boxer's skill level
            
        Returns:
            Dictionary with footwork analysis
        """
        if not footwork_segments:
            return {
                'balance_rating': 5,
                'ring_control': 5,
                'pivot_quality': 5,
                'issues': [],
                'movement_quality': 5
            }
        
        issues = []
        
        # Analyze balance from pose data
        balance_rating = self._analyze_balance(pose_data)
        
        # Analyze ring positioning
        ring_control = self._analyze_ring_control(footwork_segments, skill_level)
        
        # Analyze pivots and angles
        pivot_quality = self._analyze_pivots(footwork_segments)
        
        # Check for flat-footed movement
        flat_footed_segments = sum(1 for s in footwork_segments if s.get('flat_footed', False))
        flat_footed_percentage = flat_footed_segments / len(footwork_segments)
        
        if flat_footed_percentage > 0.4:
            issues.append({
                'description': 'Fighting flat-footed too often',
                'correction': 'Stay on the balls of your feet. This allows quick movement in any direction and generates power from the ground up.',
                'key_points': [
                    'Weight forward on balls of feet',
                    'Heels lightly touching but not bearing weight',
                    'Keep knees slightly bent for spring'
                ],
                'severity': 'high'
            })
        
        # Check for squared stance
        squared_up_count = sum(1 for s in footwork_segments if s.get('squared_stance', False))
        if squared_up_count > 3:
            issues.append({
                'description': f'Squaring up your stance {squared_up_count} times',
                'correction': 'Maintain a staggered stance at all times. Never square up - it exposes your centerline and limits your mobility.',
                'key_points': [
                    'Lead foot points at opponent',
                    'Rear foot at 45-degree angle',
                    'Shoulder-width apart for balance'
                ],
                'severity': 'high'
            })
        
        # Check for crossing feet
        crossed_feet_count = sum(1 for s in footwork_segments if s.get('crossed_feet', False))
        if crossed_feet_count > 0:
            issues.append({
                'description': 'Crossing feet during movement',
                'correction': 'Never cross your feet. Use proper step-drag or pivot techniques to maintain balance and defensive readiness.',
                'key_points': [
                    'Step with lead foot first when moving forward',
                    'Step with rear foot first when moving back',
                    'Pivot to change angles without crossing'
                ],
                'severity': 'high'
            })
        
        # Check for excessive retreating
        backward_steps = sum(1 for s in footwork_segments if s.get('direction') == 'backward')
        backward_percentage = backward_steps / len(footwork_segments) if footwork_segments else 0
        
        if backward_percentage > 0.5 and skill_level != SkillLevel.BEGINNER:
            issues.append({
                'description': 'Retreating too often',
                'correction': 'Work on lateral movement and pivoting instead of backing straight up. Control the ring by using angles.',
                'key_points': [
                    'Side-step instead of backing up',
                    'Pivot out after combinations',
                    'Cut off the ring when advancing'
                ],
                'severity': 'medium'
            })
        
        # Check for pivot usage
        pivot_count = sum(1 for s in footwork_segments if s.get('movement_type') == 'pivot')
        if pivot_count < len(footwork_segments) * 0.1 and skill_level != SkillLevel.BEGINNER:
            issues.append({
                'description': 'Insufficient use of pivots',
                'correction': 'Use pivots to create angles and avoid getting cornered. Pivot after combinations to reset position.',
                'key_points': [
                    'Pivot on ball of lead foot',
                    'Turn 45-90 degrees to create angles',
                    'Keep balance during pivot'
                ],
                'severity': 'medium'
            })
        
        movement_quality = (balance_rating + ring_control + pivot_quality) / 3
        
        return {
            'balance_rating': balance_rating,
            'ring_control': ring_control,
            'pivot_quality': pivot_quality,
            'flat_footed_percentage': flat_footed_percentage,
            'squared_up_count': squared_up_count,
            'crossed_feet_count': crossed_feet_count,
            'movement_quality': movement_quality,
            'issues': issues
        }
    
    def analyze_strategy(
        self,
        video_data: Any,
        skill_level: SkillLevel
    ) -> Dict[str, Any]:
        """
        Analyze overall ring strategy and tactical decisions
        
        Args:
            video_data: Complete video analysis data
            skill_level: Boxer's skill level
            
        Returns:
            Dictionary with strategic analysis
        """
        insights = []
        
        # Analyze offensive/defensive balance
        punch_count = len(video_data.punches_thrown)
        defense_count = len(video_data.defensive_actions)
        
        if punch_count > defense_count * 3:
            insights.append({
                'type': 'tactical',
                'insight': 'Overly aggressive approach - leaving yourself open to counters',
                'recommendation': 'Balance offense with defense. Every combination should end with defensive movement or guard reset.'
            })
        elif defense_count > punch_count * 2:
            insights.append({
                'type': 'tactical',
                'insight': 'Too defensive/passive - missing offensive opportunities',
                'recommendation': 'Be more assertive. Defense should create opportunities for counters and combinations.'
            })
        
        # Analyze rhythm and timing
        if self._has_predictable_rhythm(video_data.punches_thrown):
            insights.append({
                'type': 'timing',
                'insight': 'Predictable rhythm making you easy to time',
                'recommendation': 'Vary your timing - use feints, change speeds, and break your patterns.'
            })
        
        # Analyze energy management
        if video_data.duration_seconds > 180:  # If session longer than 3 minutes
            energy_distribution = self._analyze_energy_distribution(video_data)
            if energy_distribution.get('early_fade', False):
                insights.append({
                    'type': 'conditioning',
                    'insight': 'Activity level drops significantly in later rounds',
                    'recommendation': 'Work on cardiovascular conditioning and pacing. Don\'t empty the tank early.'
                })
        
        # Calculate tactical ratings
        tactical_awareness = self._rate_tactical_awareness(video_data, skill_level)
        adaptability = self._rate_adaptability(video_data)
        energy_management = self._rate_energy_management(video_data)
        
        return {
            'insights': insights,
            'tactical_awareness': tactical_awareness,
            'adaptability': adaptability,
            'energy_management': energy_management
        }
    
    # Helper methods
    
    def _analyze_combinations(self, punches: List[Dict]) -> List[List[Dict]]:
        """Group punches into combinations"""
        combinations = []
        current_combo = []
        
        for i, punch in enumerate(punches):
            if i == 0 or punches[i-1].get('timestamp', 0) + 2 > punch.get('timestamp', 0):
                current_combo.append(punch)
            else:
                if len(current_combo) > 1:
                    combinations.append(current_combo)
                current_combo = [punch]
        
        if len(current_combo) > 1:
            combinations.append(current_combo)
        
        return combinations
    
    def _rate_combinations(self, combinations: List[List[Dict]], skill_level: SkillLevel) -> float:
        """Rate quality of punch combinations"""
        if not combinations:
            return 3.0
        
        avg_combo_length = sum(len(c) for c in combinations) / len(combinations)
        
        # Expected combination complexity by skill level
        expected_length = {
            SkillLevel.BEGINNER: 2,
            SkillLevel.INTERMEDIATE: 3,
            SkillLevel.ADVANCED: 4,
            SkillLevel.PROFESSIONAL: 5
        }.get(skill_level, 3)
        
        rating = min(10, (avg_combo_length / expected_length) * 7)
        return rating
    
    def _get_punch_distribution(self, punches: List[Dict]) -> Dict[str, int]:
        """Get distribution of punch types"""
        distribution = {}
        for punch in punches:
            punch_type = punch.get('type', 'unknown')
            distribution[punch_type] = distribution.get(punch_type, 0) + 1
        return distribution
    
    def _get_defense_distribution(self, defensive_actions: List[Dict]) -> Dict[str, int]:
        """Get distribution of defensive actions"""
        distribution = {}
        for action in defensive_actions:
            action_type = action.get('type', 'unknown')
            distribution[action_type] = distribution.get(action_type, 0) + 1
        return distribution
    
    def _rate_head_movement(self, head_movements: List[Dict], skill_level: SkillLevel) -> float:
        """Rate quality of head movement"""
        if not head_movements:
            return 3.0
        
        successful = sum(1 for hm in head_movements if hm.get('successful', False))
        success_rate = successful / len(head_movements)
        
        base_rating = success_rate * 10
        
        # Adjust for skill level expectations
        if skill_level == SkillLevel.BEGINNER:
            base_rating = min(10, base_rating * 1.2)  # More forgiving
        
        return base_rating
    
    def _has_predictable_patterns(self, defensive_actions: List[Dict]) -> bool:
        """Check if defensive patterns are predictable"""
        if len(defensive_actions) < 4:
            return False
        
        # Check for repeating patterns
        last_three = [d.get('type') for d in defensive_actions[-3:]]
        prev_three = [d.get('type') for d in defensive_actions[-6:-3]]
        
        return last_three == prev_three
    
    def _analyze_balance(self, pose_data: List[Dict]) -> float:
        """Analyze balance from pose estimation data"""
        if not pose_data:
            return 5.0
        
        balance_scores = [p.get('balance_score', 5) for p in pose_data]
        return sum(balance_scores) / len(balance_scores)
    
    def _analyze_ring_control(self, footwork_segments: List[Dict], skill_level: SkillLevel) -> float:
        """Analyze ring control and positioning"""
        if not footwork_segments:
            return 5.0
        
        # Check for center control
        center_control = sum(1 for s in footwork_segments if s.get('ring_position') == 'center')
        center_percentage = center_control / len(footwork_segments)
        
        # Check for corner/rope avoidance
        trapped_count = sum(1 for s in footwork_segments if s.get('trapped', False))
        
        base_score = (center_percentage * 5) + (1 - trapped_count / len(footwork_segments)) * 5
        
        return min(10, base_score)
    
    def _analyze_pivots(self, footwork_segments: List[Dict]) -> float:
        """Analyze pivot quality and usage"""
        pivots = [s for s in footwork_segments if s.get('movement_type') == 'pivot']
        
        if not pivots:
            return 3.0
        
        quality_scores = [p.get('quality', 5) for p in pivots]
        return sum(quality_scores) / len(quality_scores)
    
    def _has_predictable_rhythm(self, punches: List[Dict]) -> bool:
        """Check if punching rhythm is predictable"""
        if len(punches) < 6:
            return False
        
        # Analyze time intervals between punches
        intervals = []
        for i in range(1, len(punches)):
            interval = punches[i].get('timestamp', 0) - punches[i-1].get('timestamp', 0)
            intervals.append(round(interval, 1))
        
        # Check if intervals are too consistent
        if len(set(intervals)) < len(intervals) / 3:
            return True
        
        return False
    
    def _analyze_energy_distribution(self, video_data: Any) -> Dict[str, Any]:
        """Analyze energy distribution across session"""
        duration = video_data.duration_seconds
        
        if duration < 180:
            return {'early_fade': False}
        
        # Split into thirds
        third = duration / 3
        
        early_punches = sum(1 for p in video_data.punches_thrown 
                           if p.get('timestamp', 0) < third)
        late_punches = sum(1 for p in video_data.punches_thrown 
                          if p.get('timestamp', 0) > third * 2)
        
        if late_punches < early_punches * 0.6:
            return {'early_fade': True, 'fade_percentage': (1 - late_punches/early_punches) * 100}
        
        return {'early_fade': False}
    
    def _rate_tactical_awareness(self, video_data: Any, skill_level: SkillLevel) -> float:
        """Rate tactical awareness and ring IQ"""
        # Simplified rating based on variety and effectiveness
        punch_variety = len(set(p.get('type') for p in video_data.punches_thrown))
        defense_variety = len(set(d.get('type') for d in video_data.defensive_actions))
        
        variety_score = (punch_variety + defense_variety) / 2
        
        return min(10, variety_score * 1.5)
    
    def _rate_adaptability(self, video_data: Any) -> float:
        """Rate ability to adapt during session"""
        # Placeholder - would need more context about opponent/situation
        return 6.0
    
    def _rate_energy_management(self, video_data: Any) -> float:
        """Rate energy management and pacing"""
        energy_data = self._analyze_energy_distribution(video_data)
        
        if energy_data.get('early_fade'):
            return 4.0
        
        return 7.0
