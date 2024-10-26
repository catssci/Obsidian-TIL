import random

# 샘플 단어 목록
WORDS = ["dog", "cat", "banana", "apple", "mango", "tiger", "rabbit"]

def generate_word(word_length=3):
    """
    랜덤한 단어를 생성합니다.
    """
    # 지정된 길이의 단어만 필터링
    filtered_words = [word for word in WORDS if len(word) == word_length]
    return random.choice(filtered_words)