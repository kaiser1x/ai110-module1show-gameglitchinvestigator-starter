from logic_utils import check_guess, reset_game_state

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New Game reset bug ---
# Old bug: new_game only reset attempts + secret. status/score/history kept
# stale, so a won/lost game stayed blocked by st.stop() and never restarted.
# secret was also hardcoded randint(1, 100), ignoring difficulty range.

def test_reset_clears_all_per_game_state():
    state = reset_game_state(1, 100)
    assert state["status"] == "playing"  # was stuck "won"/"lost" -> game frozen
    assert state["score"] == 0           # stale score carried over
    assert state["history"] == []        # stale guesses carried over
    assert state["attempts"] == 0

def test_reset_secret_respects_difficulty_range():
    # Hard range is 1..50; secret must stay inside given range, not 1..100.
    for _ in range(200):
        secret = reset_game_state(1, 50)["secret"]
        assert 1 <= secret <= 50
