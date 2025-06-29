# 🏥 Sağlık Asistanı Chatbot

Modern AI teknolojileri kullanarak geliştirilen akıllı sağlık asistanı chatbot'u. Google Gemini ve OpenAI GPT modellerini karşılaştırır.

## ✨ Özellikler

- 🤖 **Çift Model Desteği**: Gemini vs OpenAI GPT karşılaştırması
- 🎯 **Intent Sınıflandırma**: 8 farklı sağlık kategorisi
- 📊 **Performans Metrikleri**: Precision, Recall, F1-Score
- 🎨 **Modern Arayüz**: Streamlit tabanlı interaktif web uygulaması
- 📈 **Veri Analizi**: 1,250+ örnekli kapsamlı dataset
- 🔄 **Demo Mode**: API key olmadan test edilebilir

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
# Depoyu klonla
git clone <repository-url>
cd Chatbot

# Gerekli paketleri yükle
pip install -r requirements.txt
```

### 2. API Key Yapılandırması

Workspace ana dizininde `.env` dosyası oluşturun:

```bash
# .env dosyası oluşturun
GOOGLE_API_KEY=your_google_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=True
PORT=8501
```

**API Key Alma Rehberi:**
- **Google Gemini (Ücretsiz)**: https://makersuite.google.com/app/apikey
  1. Google hesabıyla giriş yapın
  2. "Create API Key" tıklayın
  3. Oluşturulan key'i kopyalayın

- **OpenAI (Ücretli)**: https://platform.openai.com/api-keys  
  1. OpenAI hesabı oluşturun
  2. "Create new secret key" tıklayın
  3. sk-... ile başlayan key'i kopyalayın

### 3. Uygulamayı Çalıştır
```bash
streamlit run run_app.py
```

Uygulama **http://localhost:8501** adresinde açılacak.

## 📊 Dataset Bilgileri

- **Toplam Örnek**: 1,250
- **Intent Kategorileri**: 8
- **Konular**: Selamlama, Semptom Sorguları, Randevu, İlaç Bilgileri, Acil Durumlar, Genel Sağlık, Doktor Önerileri, Vedalaşma

## 🎯 Intent Kategorileri

1. **👋 Greeting**: Selamlama mesajları
2. **🩺 Symptom Inquiry**: Semptom sorguları
3. **📅 Appointment Booking**: Randevu alma
4. **💊 Medication Info**: İlaç bilgileri
5. **🚨 Emergency**: Acil durumlar
6. **💪 General Health**: Genel sağlık tavsiyeleri
7. **👨‍⚕️ Doctor Recommendation**: Doktor önerileri
8. **👋 Goodbye**: Vedalaşma mesajları

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **AI Models**: Google Gemini-1.5-Flash, OpenAI GPT-3.5-Turbo
- **Web Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **ML Metrics**: Scikit-learn

### Proje Yapısı
```
Chatbot/
├── models/                 # AI model sınıfları
│   ├── gemini_model.py
│   ├── openai_model.py
│   └── __init__.py
├── data/                   # Dataset
│   └── health_assistant_dataset.csv
├── scripts/                # Yardımcı scriptler
│   ├── create_dataset.py
│   └── model_comparison.py
├── run_app.py             # Ana Streamlit uygulaması
├── requirements.txt       # Python bağımlılıkları
└── README.md
```

## 📈 Model Performansı

Her iki model de:
- Intent sınıflandırma doğruluğu
- Yanıt kalitesi
- Yanıt hızı
- Türkçe dil desteği

metrikleri ile karşılaştırılır.

## 🔄 Demo Mode

API key'ler olmadan da test edilebilir:
- Hazır yanıtlar kullanılır
- Keyword tabanlı intent sınıflandırma
- Gerçekçi sağlık asistanı deneyimi

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request açın

---

**Not**: Bu uygulama sadece bilgilendirme amaçlıdır. Ciddi sağlık sorunları için mutlaka bir sağlık uzmanına başvurun. 