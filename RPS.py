# Enhanced Rock Paper Scissors player with multiple strategies to beat different bots

def player(prev_play, opponent_history=[]):
    # Add the previous play to history
    if prev_play != "":
        opponent_history.append(prev_play)
    
    # Default guess
    guess = "R"
    
    # If we don't have enough history, use a mixed strategy
    if len(opponent_history) < 3:
        import random
        guess = random.choice(["R", "P", "S"])
        return guess
    
    # Strategy 1: Pattern matching for sequences
    def find_pattern_strategy():
        # Look for patterns of length 2, 3, and 4
        for pattern_length in [4, 3, 2]:
            if len(opponent_history) >= pattern_length:
                recent_pattern = opponent_history[-pattern_length:]
                
                # Count occurrences of this pattern in history
                pattern_count = 0
                next_moves_after_pattern = []
                
                for i in range(len(opponent_history) - pattern_length):
                    if opponent_history[i:i+pattern_length] == recent_pattern:
                        if i + pattern_length < len(opponent_history):
                            next_moves_after_pattern.append(opponent_history[i + pattern_length])
                            pattern_count += 1
                
                if pattern_count > 0:
                    # Predict the most common next move after this pattern
                    from collections import Counter
                    counter = Counter(next_moves_after_pattern)
                    predicted_move = counter.most_common(1)[0][0]
                    return counter_move(predicted_move)
        
        return None
    
    # Strategy 2: Frequency analysis
    def frequency_strategy():
        from collections import Counter
        recent_moves = opponent_history[-20:] if len(opponent_history) >= 20 else opponent_history
        counter = Counter(recent_moves)
        most_common = counter.most_common(1)[0][0]
        return counter_move(most_common)
    
    # Strategy 3: Anti-frequency (assuming opponent tries to balance)
    def anti_frequency_strategy():
        from collections import Counter
        counter = Counter(opponent_history)
        # Predict they'll play the least common move to balance
        least_common = counter.most_common()[-1][0]
        return counter_move(least_common)
    
    # Strategy 4: Markov chain (transition probabilities)
    def markov_strategy():
        if len(opponent_history) < 2:
            return None
            
        # Build transition matrix
        transitions = {}
        for i in range(len(opponent_history) - 1):
            current = opponent_history[i]
            next_move = opponent_history[i + 1]
            if current not in transitions:
                transitions[current] = []
            transitions[current].append(next_move)
        
        last_move = opponent_history[-1]
        if last_move in transitions:
            from collections import Counter
            counter = Counter(transitions[last_move])
            predicted = counter.most_common(1)[0][0]
            return counter_move(predicted)
        
        return None
    
    # Strategy 5: Beat the last move (simple reactive)
    def beat_last_strategy():
        return counter_move(opponent_history[-1])
    
    # Strategy 6: Rotational strategy detection
    def rotation_strategy():
        if len(opponent_history) < 6:
            return None
            
        # Check for rotation patterns like R->P->S->R->P->S
        rotations = ["RPS", "RSP", "PRS", "PSR", "SRP", "SPR"]
        recent = "".join(opponent_history[-6:])
        
        for rotation in rotations:
            # Check if recent moves follow this rotation
            matches = 0
            for i in range(len(recent)):
                if recent[i] == rotation[i % 3]:
                    matches += 1
            
            if matches >= 4:  # If most moves match the rotation
                next_in_rotation = rotation[len(recent) % 3]
                return counter_move(next_in_rotation)
        
        return None
    
    # Helper function to counter a move
    def counter_move(move):
        if move == "R":
            return "P"
        elif move == "P":
            return "S"
        elif move == "S":
            return "R"
        return "R"
    
    # Try strategies in order of preference
    strategies = [
        find_pattern_strategy,
        rotation_strategy,
        markov_strategy,
        frequency_strategy,
        anti_frequency_strategy,
        beat_last_strategy
    ]
    
    for strategy in strategies:
        result = strategy()
        if result is not None:
            return result
    
    # Fallback
    return guess
