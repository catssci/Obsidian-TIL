
def calculate_feedback(guess, answer):
    """
    플레이어의 추측과 정답을 비교하여 스트라이크와 볼을 계산합니다.
    """
    strike = sum(1 for i in range(len(answer)) if guess[i] == answer[i])
    ball = sum(1 for char in guess if char in answer) - strike
    return strike, ball