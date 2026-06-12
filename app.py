import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="TrackStyler AI", page_icon="🎵", layout="wide")

st.title("🎵 TrackStyler AI")
st.write("Мәтініңізді заманауи ырғаққа салыңыз.")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Шикі мәтін")
    user_lyrics = st.text_area("Өлең жолдарын осы жерге жазыңыз:", height=250, placeholder="Сағындым сені, артқа қарамастан жүгірдім...")
    style_option = st.selectbox("Қандай стильге өңдейміз?", ["Көше стилі (Street-level / Rap)", "Q-Pop / Заманауи Pop", "R&B / Меланхолия"])
    process_btn = st.button("✨ Ритм мен Стильді Түзеу")

with col2:
    st.subheader("🔥 Дайын Музыкалық Текст")
    if process_btn:
        if user_lyrics.strip() == "":
            st.warning("Алдымен сол жаққа мәтін жазыңыз!")
        else:
            with st.spinner("AI мәтінді өңдеп жатыр..."):
                try:
                    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                    system_instruction = (
                        "Сен — заманауи қазақша музыка бойынша кәсіби трек-мейкерсің. "
                        "Пайдаланушы берген мәтінді музыкалық ырғаққа келтіріп, өңдеп бер. "
                        "Ережелер:\n"
                        "1. Тым поэтикалық сөздерді ('асқар тау', 'адал нанмен') мүлдем қолданба.\n"
                        "2. Мәтінді қарапайым, трендтегі, көше тілімен, бірақ сапалы рифмамен жаз.\n"
                        "3. Жолдардың буын санын теңестір, әуенге оңай түсетіндей болсын.\n"
                        "4. Тек дайын өңделген мәтінді қайтар."
                    )
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": f"Стиль: {style_option}\nМәтін:\n{user_lyrics}"}
                        ],
                        temperature=0.7
                    )
                    st.success("Дайын!")
                    st.code(response.choices[0].message.content, language="text")
                except Exception as e:
                    st.error(f"Қате орын алды: {e}")
    else:
        st.info("Өңделген мәтін осы жерде пайда болады.")
