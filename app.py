import streamlit as st
import g4f

st.set_page_config(page_title="TrackStyler AI", page_icon="🎵", layout="wide")

st.title("🎵 TrackStyler AI")
st.write("Style your lyrics into modern rhythm — 100% Free Version.")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Input Lyrics")
    user_lyrics = st.text_area("Paste your lyrics here:", height=250, placeholder="Enter your text...")
    style_option = st.selectbox("Choose music style:", ["Street-level / Rap", "Q-Pop / Modern Pop", "R&B / Melancholy"])
    process_btn = st.button("✨ Fix Rhythm & Style")

with col2:
    st.subheader("🔥 Ready Music Track")
    if process_btn:
        if user_lyrics.strip() == "":
            st.warning("Please enter your lyrics first!")
        else:
            with st.spinner("AI is processing your Kazakh lyrics..."):
                try:
                    system_instruction = (
                        "You are a professional Kazakh music producer and track-maker. "
                        "Transform the user's provided Kazakh lyrics into a modern, rhythmic song format. "
                        "Strict Rules:\n"
                        "1. Do NOT use old poetic words like 'asqar tau' or 'adal nanmen'. Keep it modern.\n"
                        "2. Use street-level, trending, and contemporary Kazakh language with high-quality rhyming.\n"
                        "3. Equalize the syllable count in lines so it is very easy to sing over a beat.\n"
                        "4. Output ONLY the finalized Kazakh lyrics."
                    )
                    
                    # Тегін провайдерлер арқылы GPT-4o немесе балама модельді шақыру
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.gpt_4o,
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": f"Style: {style_option}\nLyrics:\n{user_lyrics}"}
                        ]
                    )
                    
                    st.success("Done!")
                    st.code(response, language="text")
                except Exception as e:
                    st.error(f"Error: {e}. Please try again.")
    else:
        st.info("Processed lyrics will appear here.")
