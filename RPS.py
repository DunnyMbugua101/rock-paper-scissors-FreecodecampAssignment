def player(prev_play, opponent_history=[]):
    # Initialize opponent history if empty
    if not opponent_history:
        opponent_history.clear()
    opponent_history.append(prev_play)

    # Counter moves dictionary
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    
    # Default guess if no pattern is detected
    guess = "R"

    # Early game: not enough data to identify opponent
    if len(opponent_history) < 5:
        return guess

    # Detect Quincy: check for repeating sequence ["R", "R", "P", "P", "S"]
    quincy_sequence = ["R", "R", "P", "P", "S"]
    is_quincy = True
    for i in range(min(len(opponent_history), 5)):
        if opponent_history[i] != quincy_sequence[i % 5]:
            is_quincy = False
            break
    if is_quincy:
        # Predict Quincy's next move and counter it
        next_move = quincy_sequence[len(opponent_history) % 5]
        return counter_moves[next_move]

    # Detect Kris: Kris counters the player's last move
    # Check if opponent’s moves follow the counter pattern
    my_last_move = opponent_history[-2] if len(opponent_history) >= 2 else "R"
    kris_expected = counter_moves[my_last_move]
    is_kris = len(opponent_history) > 1 and opponent_history[-1] == kris_expected
    if is_kris:
        # Kris will counter our last move, so we counter Kris’s move
        return counter_moves[kris_expected]

    # Detect Mrugesh: plays counter to most frequent move in last 10
    if len(opponent_history) >= 10:
        last_ten = opponent_history[-11:-1]  # Player’s moves (opponent’s history)
        most_frequent = max(set(last_ten), key=last_ten.count, default="S")
        mrugesh_play = counter_moves[most_frequent]
        # Play the counter to Mrugesh’s play
        return counter_moves[mrugesh_play]

    # Detect Abbey: predicts based on last two moves
    if len(opponent_history) >= 3:
        last_two = "".join(opponent_history[-3:-1])  # Player’s last two moves
        # Assume Abbey predicts the second move of the pair
        predicted_move = last_two[-1]
        abbey_play = counter_moves[predicted_move]
        # Play the counter to Abbey’s play
        return counter_moves[abbey_play]

    # Fallback: random choice if no clear pattern
    import random
    return random.choice(["R", "P", "S"])
