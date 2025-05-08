from unicodedata import normalize
import re, string
from collections import Counter

def normalize_text(text: str) -> str:
    s = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
            normalize( "NFD", text), 0, re.I
        )
    s = s.translate(str.maketrans('', '', string.punctuation))
    return s.lower().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')

def open_file(filename) -> str:
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found"

def count_words(text: str) -> dict[str, int]:
    word_count = {}
    for word in text.split():
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def get_conditional_probability(text: str, word_count: dict[str, int]) -> dict[str, dict[str, float]]:
    words = text.split()
    word_pairs = [(words[i], words[i+1]) for i in range(len(words)-1)]
    pair_counts = Counter(word_pairs)

    combinations_probability: dict[str, dict[str, float]] = {}

    for (w1, w2), count in pair_counts.items():
        prob = count / word_count[w1]
        combinations_probability.setdefault(w1, {})[w2] = prob

    return combinations_probability

def suggest_word(text: str, char: str) -> str | None:

    word_count = count_words(text)

    possible_words = [word for word, count in word_count.items() if word.startswith(char)]

    probabilities: dict[str, float] = {} # P(Ai)

    total_words = sum(word_count.values())

    total_words_with_char = 0
    for word in text.split():
        if word.startswith(char):
            total_words_with_char += 1

    probability_of_word_with_char = total_words_with_char / total_words # P(B)

    for word in possible_words:
        probabilities[word] = word_count[word] / total_words

    # P(char|word) = 1

    bayes_probabilities: dict[str, float] = {} # P(A|B)
    for word in possible_words:
        bayes_probabilities[word] = probabilities[word] / probability_of_word_with_char

    print(bayes_probabilities)

    return None



# Eventos
# A = la palabra es este
# A2 = la palabra es en
# An = la palabra es e*
# B = la letra es e
# P(A|B) = P(B|A) * P(A) / P(B)
# P(este | e) = P(e | este) * P(este) / P(e)
# P(A) = (apariciones de la palabra) / total de palabras
# P(B) = (apariciones de la letra) / total de letras
# P(e | este) = 1 * P(este) / P(e)

if __name__ == "__main__":
    phrase = open_file("frase.txt")
    print(f'frase original:\n{phrase}')
    phrase = normalize_text(phrase)
    print(f'frase normalizada:\n{phrase}\n')
    words_count = count_words(phrase)
    print(f'Conteo de palabras:\n{words_count}\n')
    print("Introduzca una letra:")
    char = input()
    suggest_word(phrase, char)
