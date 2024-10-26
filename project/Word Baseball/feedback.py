def display_feedback(strike, ball):
    """
    스트라이크와 볼 개수를 표시합니다.
    """
    print(f"{strike} Strike(s), {ball} Ball(s)")

def display_result(is_win):
    """
    게임의 최종 결과를 표시합니다.
    """
    if is_win:
        print("축하합니다! 단어를 맞추셨습니다!")
    else:
        print("아쉽네요! 기회를 모두 소진했습니다. 게임에서 패배하였습니다.")