import json
import math


def load_mod_config():
    with open("data/mod_config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def extract_chat_vector(message, config):

    lower_msg = message.lower()

    banned_hits = sum(1 for word in config["banned_words"] if word in lower_msg)

    has_promo = 1.0 if any(p in lower_msg for p in config["promo_patterns"]) else 0.0

    punct_spam = float(message.count("!") + message.count("?"))

    letters = [c for c in message if c.isalpha()]
    upper_letters = [c for c in letters if c.isupper()]
    caps_ratio = len(upper_letters) / len(letters) if letters else 0.0

    return [
        float(banned_hits),
        has_promo,
        punct_spam,
        round(caps_ratio, 4),
    ]


def dot_product(vec_a, vec_b):

    total = 0.0
    for i in range(len(vec_a)):
        total += vec_a[i] * vec_b[i]
    return total


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


def moderate_chat(message, threshold=0.75):
    config = load_mod_config()
    x_vec = extract_chat_vector(message, config)

    z_score = dot_product(config["weights"], x_vec) + config["bias"]

    ban_prob = sigmoid(z_score)

    labels = ["Banned Keywords", "Promo / Link (0/1)", "Punctuation (!/?)", "ALL-CAPS Ratio"]
    breakdown = []
    for i in range(len(labels)):
        breakdown.append({
            "Rule Feature": labels[i],
            "Extracted Value (x)": x_vec[i],
            "Penalty Weight (w)": config["weights"][i],
            "Score Added (w * x)": round(x_vec[i] * config["weights"][i], 3),
        })

    return {
        "feature_vector": x_vec,
        "z_score": round(z_score, 4),
        "ban_probability": round(ban_prob * 100, 2),
        "is_flagged": ban_prob >= threshold,
        "breakdown": breakdown,
    }