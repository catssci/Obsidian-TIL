import random

# 영어 단어 목록 (교육용으로 적절한 단어)
WORDS = ["apple", "banana", "grape", "peach", "melon", "cherry", "plum"]

def generate_word(word_length=5):
    """
    랜덤한 영어 단어를 생성합니다.
    """
    filtered_words = [word for word in WORDS if len(word) == word_length]
    return random.choice(filtered_words)