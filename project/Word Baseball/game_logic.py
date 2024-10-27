from collections import Counter

def calculate_feedback(guess, answer):
    """
    추측한 단어와 정답 단어를 비교하여 중복 글자를 고려한 스트라이크와 볼을 계산합니다.
    """
    strike, ball = 0, 0
    answer_count = Counter(answer)
    guess_count = Counter(guess)

    # 스트라이크 계산
    for i in range(len(answer)):
        if guess[i] == answer[i]:
            strike += 1
            answer_count[guess[i]] -= 1
            guess_count[guess[i]] -= 1

    # 볼 계산 (위치가 다르지만 글자가 포함된 경우)
    for char in guess_count:
        if char in answer_count:
            ball += min(guess_count[char], answer_count[char])

    return strike, ball