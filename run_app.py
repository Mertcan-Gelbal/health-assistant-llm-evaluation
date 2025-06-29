#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sağlık Asistanı Streamlit Uygulaması Launcher
Ana dizinden çalıştırarak import sorunlarını çözer
"""

import streamlit as st
import sys
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import time
import plotly.express as px
import plotly.graph_objects as go
import warnings

# Uyarıları gizle
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

# SSL uyarılarını gizle
import urllib3
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

# .env dosyasını yükle
load_dotenv()

# Models import
from models.gemini_model import GeminiModel
from models.openai_model import OpenAIModel

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="🏥 Sağlık Asistanı Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .demo-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        min-height: 400px;
    }
    .example-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .example-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Session state'i başlat"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'gemini_model' not in st.session_state:
        st.session_state.gemini_model = None
    if 'openai_model' not in st.session_state:
        st.session_state.openai_model = None
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'gemini'

@st.cache_resource
def load_models():
    """Modelleri yükle (cache ile)"""
    with st.spinner("🤖 Modeller yükleniyor..."):
        # API keys
        google_api_key = os.getenv("GOOGLE_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Modelleri initialize et
        gemini_model = GeminiModel(google_api_key or "")
        openai_model = OpenAIModel(openai_api_key or "")
        
        return gemini_model, openai_model



def display_chat():
    """Chat geçmişini göster"""
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 Siz</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                intent_emoji = {
                    'greeting': '👋',
                    'goodbye': '👋',
                    'symptom_inquiry': '🩺',
                    'appointment_booking': '📅',
                    'medication_info': '💊',
                    'emergency': '🚨',
                    'general_health': '💪',
                    'doctor_recommendation': '👨‍⚕️'
                }.get(message.get('intent', ''), '🤖')
                
                model_name = message.get('model', 'unknown')
                model_class = f"{model_name.lower()}-message"
                
                st.markdown(f"""
                <div class="chat-message {model_class}">
                    <strong>{intent_emoji} {model_name} ({message.get('intent', 'unknown')})</strong><br>
                    {message["content"]}
                    <br><small>Yanıt süresi: {message.get('response_time', 0):.2f}s</small>
                </div>
                """, unsafe_allow_html=True)

def chat_page(gemini_model, openai_model):
    """Chat sayfası"""
    st.header("💬 Sağlık Asistanı Chat")
    
    # Model seçimi
    col1, col2 = st.columns([3, 1])
    
    with col2:
        model_choice = st.selectbox(
            "🤖 Model Seçin:",
            ["Google Gemini", "OpenAI GPT"],
            key="model_selector"
        )
    
    # Seçilen modeli belirle
    if model_choice == "Google Gemini":
        current_model = gemini_model
        model_name = "Google Gemini"
    else:
        current_model = openai_model
        model_name = "OpenAI GPT"
    
    # Demo mode uyarısı
    display_demo_warning(model_name, current_model.demo_mode)
    
    # Örnek sorular
    st.markdown("### 💡 Örnek Sorular")
    example_questions = [
        "👋 Merhaba, nasılsın?",
        "🤒 Başım çok ağrıyor",
        "🏥 Ateşim var, ne yapmalıyım?",
        "💊 Parol nasıl kullanılır?",
        "📋 Kardiyoloji randevusu",
        "🚨 Göğsümde şiddetli ağrı",
        "🥗 Sağlıklı beslenme tavsiyeleri",
        "👨‍⚕️ Hangi doktora gideyim?"
    ]
    
    # Örnek soruları 4'erli satırlar halinde göster
    for i in range(0, len(example_questions), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(example_questions):
                if col.button(example_questions[i + j], key=f"example_{i+j}"):
                    st.session_state.user_input = example_questions[i + j].split(" ", 1)[1]  # Emoji'yi kaldır
    
    # Chat interface
    st.markdown("### 💬 Sohbet")
    
    # Chat history initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # User input
    user_input = st.text_input(
        "💬 Sağlık sorunuzu yazın:",
        value=st.session_state.get("user_input", ""),
        placeholder="Örn: Başım ağrıyor, ne yapmalıyım?",
        key="chat_input"
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        send_pressed = st.button("📤 Gönder", type="primary")
    with col2:
        if st.button("🗑️ Temizle"):
            st.session_state.chat_history = []
            st.session_state.user_input = ""
            st.rerun()
    
    # Process message
    if send_pressed and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user", 
            "content": user_input.strip(),
            "timestamp": time.time()
        })
        
        # Generate response
        with st.spinner(f"🤖 {model_name} düşünüyor..."):
            try:
                start_time = time.time()
                
                # Intent classification
                intent = current_model.classify_intent(user_input.strip())
                
                # Generate response
                response = current_model.generate_response(user_input.strip(), intent)
                
                response_time = time.time() - start_time
                
                # Add bot response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "intent": intent,
                    "response_time": response_time,
                    "model": model_name,
                    "timestamp": time.time()
                })
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "Üzgünüm, şu anda bir sorun yaşıyorum. Lütfen tekrar deneyin.",
                    "timestamp": time.time()
                })
        
        # Clear input
        st.session_state.user_input = ""
        st.rerun()
    
    # Display chat history
    st.markdown("### 💬 Sohbet Geçmişi")
    
    if st.session_state.chat_history:
        for i, message in enumerate(reversed(st.session_state.chat_history[-10:])):  # Son 10 mesaj
            if message["role"] == "user":
                st.markdown(f"""
                <div style="text-align: right; margin: 1rem 0;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                color: white; padding: 1rem; border-radius: 15px 15px 5px 15px; 
                                display: inline-block; max-width: 70%; text-align: left;">
                        <strong>👤 Sen:</strong><br>
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                intent_info = f" (Intent: {message.get('intent', 'N/A')}) " if 'intent' in message else ""
                response_time = f" ({message.get('response_time', 0):.2f}s)" if 'response_time' in message else ""
                model_info = f" [{message.get('model', 'Unknown')}]" if 'model' in message else ""
                
                st.markdown(f"""
                <div style="text-align: left; margin: 1rem 0;">
                    <div style="background: #e8f4fd; color: #333; padding: 1rem; 
                                border-radius: 15px 15px 15px 5px; display: inline-block; 
                                max-width: 70%; border-left: 4px solid #667eea;">
                        <strong>🤖 Asistan{model_info}:</strong><br>
                        {message['content']}
                        <div style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
                            {intent_info}{response_time}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👋 Merhaba! Size nasıl yardımcı olabilirim? Yukarıdaki örnek sorulardan birini seçebilir veya kendi sorunuzu yazabilirsiniz.")

def dataset_info_page():
    """Veri seti bilgi sayfası"""
    st.header("📊 Veri Seti Bilgileri")
    
    try:
        # Veri setini yükle
        df = pd.read_csv('data/health_assistant_dataset.csv')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📝 Toplam Örnek", len(df))
            st.metric("🏷️ Intent Sayısı", df['intent'].nunique())
        
        with col2:
            st.metric("📋 Ortalama Metin Uzunluğu", f"{df['text'].str.len().mean():.1f}")
            st.metric("💬 Ortalama Yanıt Uzunluğu", f"{df['response'].str.len().mean():.1f}")
        
        # Intent dağılımı
        st.subheader("📊 Intent Dağılımı")
        intent_counts = df['intent'].value_counts()
        st.bar_chart(intent_counts)
        
        # Örnek veriler
        st.subheader("📋 Örnek Veriler")
        st.dataframe(df.head(10), use_container_width=True)
        
        # İstatistikler
        st.subheader("📈 Detaylı İstatistikler")
        for intent in df['intent'].unique():
            intent_data = df[df['intent'] == intent]
            st.write(f"**{intent}:** {len(intent_data)} örnek")
        
    except Exception as e:
        st.error(f"Veri seti yükleme hatası: {e}")

def display_demo_warning(model_name, is_demo):
    """Demo mode uyarısı göster"""
    if is_demo:
        st.markdown(f"""
        <div class="demo-warning">
            <h4>⚠️ DEMO MODE - {model_name}</h4>
            <p>API key bulunamadı veya geçersiz. Uygulama demo mode'da çalışıyor.</p>
            <p><strong>Demo Mode:</strong> Hazır yanıtlar kullanılıyor, gerçek AI model aktif değil.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Ana fonksiyon"""
    initialize_session_state()
    
    # Sidebar navigasyon
    st.sidebar.title("🏥 Sağlık Asistanı")
    
    page = st.sidebar.selectbox(
        "Sayfa Seçin:",
        ["💬 Chat", "📊 Veri Seti"]
    )
    
    # Modelleri yükle
    gemini_model, openai_model = load_models()
    
    if page == "💬 Chat":
        chat_page(gemini_model, openai_model)
    elif page == "📊 Veri Seti":
        dataset_info_page()
    
    # Sidebar bilgileri
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    ### 🤖 Model Durumu
    
    **Google Gemini:**
    - Durum: {'✅ Aktif' if not gemini_model.demo_mode else '⚠️ Demo Mode'}
    - Model: Gemini-1.5-Flash
    
    **OpenAI GPT:**
    - Durum: {'✅ Aktif' if not openai_model.demo_mode else '⚠️ Demo Mode'}
    - Model: GPT-3.5-Turbo
    
    ### 📊 Veri Seti
    - **Konu:** Sağlık Asistanı
    - **Toplam:** 1,250+ örnek
    - **Intent:** 8 kategori
    """)

if __name__ == "__main__":
    main() 