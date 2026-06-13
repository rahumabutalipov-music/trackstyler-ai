import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TrackStyler AI", page_icon="🎵", layout="wide")

st.title("🎵 TrackStyler AI")
st.write("Style your lyrics into modern rhythm — Stable Free Version.")
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
                    # Gemini баптаулары
                    api_key = os.environ.get("GEMINI_API_KEY")
                    if not api_key:
                        st.error("Missing GEMINI_API_KEY in Secrets!")
                    else:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        system_instruction = (
                            "You are a professional Kazakh music producer and track-maker. "
                            f"Transform the user's provided Kazakh lyrics into a modern, rhythmic {style_option} song format. "
                            "Strict Rules:\n"
                            "1. Do NOT use old, overly traditional poetic words (like 'asqar tau' or 'adal nanmen'). Keep it raw and modern.\n"
                            "2. Use street-level, trending, and contemporary Kazakh language with high-quality rhyming.\n"
                            "3. Equalize the syllable count in lines so it fits perfectly over a beat.\n"
                            "4. Output ONLY the finalized Kazakh lyrics without extra text."
                        )
                        
                        response = model.generate_content(f"{system_instruction}\n\nUser Lyrics:\n{user_lyrics}")
                        
                        st.success("Done!")
                        st.code(response.text, language="text")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Processed lyrics will appear here.")
