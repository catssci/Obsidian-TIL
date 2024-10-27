def display_feedback(strike, ball):
    """
    스트라이크와 볼 개수를 표시합니다.
    """
    print(f"{strike} Strike(s), {ball} Ball(s)")

def display_result(is_win, answer):
    """
    게임의 최종 결과와 정답을 표시합니다.
    """
    if is_win:
        print("축하합니다! 정답을 맞추셨습니다!")
    else:
        print("아쉽네요! 기회를 모두 소진했습니다.")
        print(f"정답은 '{answer}'였습니다. 다음에 다시 도전하세요!")