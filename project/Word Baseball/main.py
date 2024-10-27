from word_generator import generate_word
from game_logic import calculate_feedback
from feedback import display_feedback, display_result

MAX_TRIES = 10  # 최대 시도 횟수

def main():
    word_length = 5  # 영어 단어 길이 (변경 가능)
    answer = generate_word(word_length)
    attempts = 0

    print("=== 영어 단어 맞추기 학습 게임 ===")
    print(f"컴퓨터가 {word_length}글자 영어 단어를 선택했습니다.")
    print("단어를 추측하고, 스트라이크(S)와 볼(B) 피드백을 받으세요!")

    while attempts < MAX_TRIES:
        guess = input(f"추측할 {word_length}글자 단어를 입력하세요 (시도 {attempts + 1}/{MAX_TRIES}): ").lower()

        # 입력 검증
        if len(guess) != word_length or not guess.isalpha():
            print(f"{word_length}글자 영어 단어만 입력 가능합니다. 다시 시도해주세요.")
            continue

        attempts += 1

        # 스트라이크와 볼 계산
        strike, ball = calculate_feedback(guess, answer)
        display_feedback(strike, ball)

        # 승리 조건
        if strike == word_length:
            display_result(True, answer)
            break
    else:
        display_result(False, answer)

if __name__ == "__main__":
    main()