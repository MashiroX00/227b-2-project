import json
import random


def load_sentences(filepath="data/raw_data.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["sentences"]


def build_transitions(sentences):
    transitions = {}
    for sentence in sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 1):
            curr_w = words[i]
            next_w = words[i + 1]

            if curr_w not in transitions:
                transitions[curr_w] = []
            transitions[curr_w].append(next_w)

    return transitions


def get_latest(user_input):

    tokens = user_input.strip().lower().split()
    return tokens[-1] if tokens else ""


def predict_next(transitions, word):

    last_word = get_latest(word)
    candidates = transitions.get(last_word, [])
    return random.choice(candidates) if candidates else None


def get_probabilities(transitions, word):

    last_word = get_latest(word)
    candidates = transitions.get(last_word, [])
    if not candidates:
        return []

    total = len(candidates)
    unique_words = sorted(set(candidates))

    return [
        {
            "Next Word": w,
            "Count": candidates.count(w),
            "Probability (%)": round((candidates.count(w) / total) * 100, 2),
        }
        for w in unique_words
    ]


def generate_sentence(transitions, start_word, steps=6):

    words = start_word.strip().split()
    if not words:
        return ""

    current = get_latest(start_word)
    result = list(words)

    for _ in range(steps):
        next_w = predict_next(transitions, current)
        if not next_w:
            break
        result.append(next_w)
        current = next_w

    return " ".join(result)