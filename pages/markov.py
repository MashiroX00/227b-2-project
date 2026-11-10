import streamlit as st
import pandas as pd
from services.markov_services import (
    load_sentences,
    build_transitions,
    predict_next,
    get_probabilities,
    generate_sentence
)

st.title("Markov Chain Predictor")
st.write("Predict the next word or generate a sequence based on `raw_data.json`.")

# 1. Fetch data & model via service
sentences = load_sentences("data/raw_data.json")
transitions = build_transitions(sentences)
available_words = sorted(transitions.keys())

# Show raw data preview
with st.expander("View raw_data.json content"):
    st.write(sentences)

# 2. Input Selection
input_mode = st.radio("Choose input method:", ["Select from corpus", "Type your own word"])

if input_mode == "Select from corpus":
    word = st.selectbox("Select starting word:", available_words)
else:
    word = st.text_input("Enter starting word:").strip().lower()

st.divider()

col1, col2 = st.columns(2)

# Action 1: Next Word Prediction & Probabilities
with col1:
    st.subheader("1. Next Word Prediction")
    if st.button("Predict Next Word"):
        if not word:
            st.warning("Please choose or type a word.")
        else:
            next_word = predict_next(transitions, word)
            probs = get_probabilities(transitions, word)

            if next_word:
                st.success(f"Predicted next word: **{next_word}**")
                st.write("**Transition Probabilities:**")
                st.dataframe(pd.DataFrame(probs), use_container_width=True)
            else:
                st.error(f"No transitions found for '{word}'. Ensure the last word is in raw_data.json.")

# Action 2: Generate Sentence / Sequence
with col2:
    st.subheader("2. Sequence Generator")
    steps = st.slider("Prediction Steps (Max words):", min_value=1, max_value=15, value=6)

    if st.button("Generate Sequence"):
        if not word:
            st.warning("Please choose or type a word.")
        else:
            output = generate_sentence(transitions, word, steps=steps)
            # If output is identical to input, no transitions could be made
            if output == word and not predict_next(transitions, word):
                st.error(f"Cannot generate sequence: '{word}' is not in raw_data.json.")
            else:
                st.success("Generated Sequence:")
                st.code(output, language="text")