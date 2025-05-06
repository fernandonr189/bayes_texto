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

def suggest_word(probabilities: dict[str, dict[str, float]], previous_word: str, initial_char: str) -> str | None:
    if previous_word not in probabilities:
        return None

    candidates = {
        word: prob
        for word, prob in probabilities[previous_word].items()
        if word.startswith(initial_char)
    }

    if not candidates:
        return None

    return max(candidates, key=lambda k: candidates[k])

if __name__ == "__main__":
    phrase = open_file("frase.txt")
    print(f'frase original:\n{phrase}')
    phrase = normalize_text(phrase)
    print(f'frase normalizada:\n{phrase}\n')
    words_count = count_words(phrase)
    print(f'Conteo de palabras:\n{words_count}\n')
    combinations_probability = get_conditional_probability(phrase, words_count)
    print(f'Probabilidades condicionales:\n{combinations_probability}\n')
    target_word = 'en'
    palabras_despues_de_en = combinations_probability.get(target_word, {})
    print(f'Probabilidades condicionales despues de "{target_word}":\n{palabras_despues_de_en}\n')
    palabra_sugerida = suggest_word(combinations_probability, target_word, 'b')
    print(f'Palabra sugerida despues de "{target_word}" con letra inicial "b": {palabra_sugerida}\n')
