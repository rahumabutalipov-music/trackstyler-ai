import os
import streamlit as st
import google.generativeai as genai
import requests
import time

st.set_page_config(page_title="TrackStyler AI", page_icon="🎵", layout="wide")

st.title("🎵 TrackStyler AI & BeatMaker Pro")
st.write("Көркем ұйқасты мәтін дайындау және авторлық құқығы таза заманауи қазақша әуендер шығару жүйесі.")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Мәтін және Стиль баптаулары")
    user_lyrics = st.text_area("Өлең жолдарын немесе идеяңызды жазыңыз:", height=200, placeholder="Осы жерге мәтінді енгізіңіз...")
    
    # Жаңа сұралған стильдер тізімі
    style_option = st.selectbox("Музыкалық стильді таңдаңыз:", [
        "Домбыра / Этно-Acoustic (Терең мағыналы)", 
        "Той стилі / Toi Synth (Хит, билейтін)", 
        "Клубный / EDM Pop (Заманауи, динамикалық)",
        "Q-Pop / Modern Pop", 
        "Street-level / Rap"
    ])
    
    st.write("---")
    st.subheader("🎹 Әуенді теңшеу (Beat Settings)")
    
    # Әр стильге сай MusicGen үшін автоматты сипаттама дайындау
    if "Домбыра" in style_option:
        default_prompt = "Authentic Kazakh dombra instrumental acoustic track, deep emotional strings, beautiful folk rhythm, studio quality"
    elif "Той" in style_option:
        default_prompt = "Kazakh Toi style synthesizer beat, energetic 140 bpm, local wedding hit vibe, upbeat commercial pop keys"
    elif "Клубный" in style_option:
        default_prompt = "Modern club EDM pop beat, punchy bassline, driving electronic synth, festival dance floor tempo"
    elif "Q-Pop" in style_option:
        default_prompt = "Modern Q-Pop beat, futuristic synths, K-pop style vocal chops rhythm, commercial audio"
    else:
        default_prompt = "Contemporary street-level hip hop beat, 90 bpm, underground melodic rap instrumental"
        
    prompt_input = st.text_input("Әуен сипаттамасы (Автоматты түрде реттелген):", value=default_prompt)
    
    process_btn = st.button("✨ Әнді және Мәтінді дайындау")

with col2:
    st.subheader("🔥 AI Дайын Туынды")
    
    if process_btn:
        if user_lyrics.strip() == "":
            st.warning("Алдымен өлең мәтінін жазыңыз!")
        else:
            # 1. Көркем мәтін өңдеу бөлімі (Gemini)
            with st.spinner("AI мәтінді көркемдеп, ұйқасын реттеп жатыр..."):
                try:
                    gemini_key = os.environ.get("GEMINI_API_KEY")
                    if not gemini_key:
                        st.error("Баптаулардан (Secrets) GEMINI_API_KEY табылмады!")
                    else:
                        genai.configure(api_key=gemini_key)
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        # Мәтінді әсерлі, әдеби сөздермен, көркем және мінсіз ұйқаспен шығару нұсқаулығы
                        system_instruction = (
                            "Сіз — кәсіби қазақстандық хитмейкер әрі ақынсыз. "
                            f"Пайдаланушы берген мәтінді {style_option} стиліне сай өңдеңіз. "
                            "ҚАТАҢ ТАЛАПТАР:\n"
                            "1. Өлеңнің ұйқасына (рифма) өте қатты мән беріңіз, буын сандарын теңестіріңіз, ән айтуға ыңғайлы ырғаққа келтіріңіз.\n"
                            "2. Мәтінді қарапайым қалдырмай, әсерлі, терең мағыналы әдеби сөздермен, көркем метафоралармен және әдемі терминдермен байытыңыз.\n"
                            "3. Сезімді, астарлы мағынаны, тыңдарманның жүрегін қозғайтын көркемдікті жеткізіңіз.\n"
                            "4. Жауап ретінде ТЕК ҚАНА дайын өлең мәтінін шығарыңыз, артық сөз жазбаңыз."
                        )
                        
                        response = model.generate_content(f"{system_instruction}\n\nБастапқы идея мәтіні:\n{user_lyrics}")
                        st.success("Мәтін көркемделіп, дайын болды!")
                        st.code(response.text, language="text")
                except Exception as e:
                    st.error(f"Мәтін қатесі: {e}")
            
            # 2. Нағыз қазақша музыка шығару бөлімі (MusicGen)
            with st.spinner("🎵 Сіз таңдаған стильде ерекше авторлық минус жасалуда (10-30 сек)..."):
                try:
                    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
                    headers = {"Authorization": "Bearer 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"}
                    
                    payload = {"inputs": prompt_input}
                    
                    for attempt in range(3):
                        res = requests.post(API_URL, headers=headers, json=payload)
                        if res.status_code == 200:
                            st.success("🎵 Сіздің 100% ТЕГІН және таза минусыңыз дайын!")
                            st.audio(res.content, format="audio/wav")
                            break
                        elif res.status_code == 503:
                            time.sleep(10)
                        else:
                            st.error(f"Музыка қатесі (Статус код): {res.status_code}")
                            break
                except Exception as e:
                    st.error(f"Музыка қатесі: {e}")
    else:
        st.info("Дайын өлең мәтіні мен музыкалық плеер осы жерде пайда болады.")
