import streamlit as st
from services.custom_1 import load_mod_config, moderate_chat

st.title("Live Chat Auto-Moderation Filter")
st.caption("Mathematical Engine: Feature Vectors + Sigmoid Classification")

config = load_mod_config()
samples = config["sample_chats"]

choice = st.selectbox("Test Chat Presets:", ["Custom Message"] + list(samples.keys()))
default_msg = samples.get(choice, "")

chat_msg = st.text_input("Incoming Live Chat Message:", value=default_msg)
threshold = st.slider("Auto-Timeout Strictness Threshold (%):", 50, 95, 75)

if st.button("Check Chat Message", type="primary"):
    if not chat_msg.strip():
        st.warning("Please enter a chat message.")
    else:
        result = moderate_chat(chat_msg, threshold / 100)

        st.divider()

        col1, col2, col3 = st.columns(3)
        col1.metric("Violation Probability", f"{result['ban_probability']}%")
        col2.metric("Raw Logit Score (z)", result["z_score"])
        col3.metric("Mod Action", "AUTO-TIMEOUT" if result["is_flagged"] else "ALLOW")

        if result["is_flagged"]:
            st.error(f"Message Blocked: Exceeded {threshold}% auto-moderation threshold.")
        else:
            st.success("Message Approved: Safe to display in live chat.")

        st.subheader("Feature Vector Breakdown (x)")
        st.write("Vector $\\vec{x}$:", result["feature_vector"])
        st.dataframe(result["breakdown"], hide_index=True)