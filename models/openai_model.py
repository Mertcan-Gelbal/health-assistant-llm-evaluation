import openai
import pandas as pd
import os
from typing import Dict, List, Tuple
import logging
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import random

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIModel:
    def __init__(self, api_key: str):
        """
        OpenAI model initialization with demo mode support
        
        Args:
            api_key (str): OpenAI API key
        """
        self.api_key = api_key
        self.client = None
        self.training_data = None
        self.test_data = None
        self.demo_mode = False
        
        # API key kontrolü ve demo mode
        if not api_key:
            self.demo_mode = True
            logger.warning("⚠️ Demo mode aktif - API key bulunamadı")
        else:
            try:
                self.client = openai.OpenAI(api_key=api_key)
                logger.info("✅ OpenAI model başarıyla yüklendi")
            except Exception as e:
                logger.error(f"❌ OpenAI API hatası: {e}")
                self.demo_mode = True
                logger.warning("⚠️ Demo mode'a geçildi")
    
    def load_dataset(self, dataset_path: str) -> pd.DataFrame:
        """
        CSV veri setini yükle
        
        Args:
            dataset_path (str): Veri seti dosya yolu
            
        Returns:
            pd.DataFrame: Yüklenen veri seti
        """
        try:
            df = pd.read_csv(dataset_path)
            logger.info(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise
    
    def prepare_training_data(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Eğitim ve test verilerini ayır
        
        Args:
            df (pd.DataFrame): Veri seti
            test_size (float): Test verisi oranı
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Eğitim ve test verileri
        """
        train_df, test_df = train_test_split(df, test_size=test_size, stratify=df['intent'], random_state=42)
        self.training_data = train_df
        self.test_data = test_df
        
        logger.info(f"Training data: {len(train_df)} rows")
        logger.info(f"Test data: {len(test_df)} rows")
        
        return train_df, test_df
    
    def classify_intent(self, text: str) -> str:
        """
        Intent classification with demo mode support
        """
        if self.demo_mode:
            return self._demo_classify_intent(text)
        
        try:
            prompt = """
Sen bir sağlık asistanı intent sınıflandırıcısısın. Aşağıdaki metni analiz ederek hangi kategoriye ait olduğunu belirle.

Kategoriler:
- greeting: Selamlama mesajları
- goodbye: Vedalaşma mesajları  
- symptom_inquiry: Semptom sorguları ve sağlık şikayetleri
- appointment_booking: Randevu alma istekleri
- medication_info: İlaç bilgileri ve kullanım soruları
- emergency: Acil durumlar
- general_health: Genel sağlık tavsiyeleri
- doctor_recommendation: Doktor önerileri

Metin: "{}"

Sadece kategori adını döndür:
""".format(text)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.1
            )
            
            predicted_intent = response.choices[0].message.content.strip().lower()
            
            # Valid intent kontrolü
            valid_intents = ['greeting', 'goodbye', 'symptom_inquiry', 'appointment_booking', 
                           'medication_info', 'emergency', 'general_health', 'doctor_recommendation']
            
            if predicted_intent in valid_intents:
                return predicted_intent
            else:
                # En yakın intent'i bul
                for intent in valid_intents:
                    if intent in predicted_intent:
                        return intent
                return 'symptom_inquiry'  # Default
                
        except Exception as e:
            logger.error(f"OpenAI Intent classification error: {e}")
            return self._demo_classify_intent(text)
    
    def _demo_classify_intent(self, text: str) -> str:
        """Demo mode için basit intent classification"""
        text_lower = text.lower()
        
        # Basit keyword tabanlı sınıflandırma
        if any(word in text_lower for word in ['merhaba', 'selam', 'hey', 'nasılsın', 'iyi günler']):
            return 'greeting'
        elif any(word in text_lower for word in ['teşekkür', 'sağol', 'görüşürüz', 'hoşçakal', 'bye']):
            return 'goodbye'
        elif any(word in text_lower for word in ['ağrı', 'ateş', 'hasta', 'bulantı', 'başım', 'karnım', 'boğaz']):
            return 'symptom_inquiry'
        elif any(word in text_lower for word in ['randevu', 'doktor', 'muayene', 'hastane']):
            return 'appointment_booking'
        elif any(word in text_lower for word in ['ilaç', 'parol', 'aspirin', 'antibiyotik', 'vitamin']):
            return 'medication_info'
        elif any(word in text_lower for word in ['acil', 'kalp krizi', 'nefes', 'kaza', '112']):
            return 'emergency'
        elif any(word in text_lower for word in ['sağlıklı', 'beslenme', 'egzersiz', 'spor', 'diyet']):
            return 'general_health'
        elif any(word in text_lower for word in ['hangi doktor', 'uzman', 'bölüm', 'doktor öner']):
            return 'doctor_recommendation'
        else:
            return 'symptom_inquiry'  # Default
    
    def generate_response(self, text: str, intent: str = None) -> str:
        """
        Response generation with demo mode support
        """
        if self.demo_mode:
            return self._demo_generate_response(text, intent)
        
        try:
            if not intent:
                intent = self.classify_intent(text)
                
            # Intent'e göre system prompt
            if intent == "greeting":
                system_prompt = "Sen samimi bir sağlık asistanısın. Kullanıcının selamına sıcak karşılık ver. Kısa ve dostane ol."
            elif intent == "goodbye":
                system_prompt = "Sen samimi bir sağlık asistanısın. Kullanıcıya güzel bir veda et. Kısa ve pozitif ol."
            elif intent == "emergency":
                system_prompt = "Sen acil durum sağlık asistanısın. Hemen 112'yi aramasını söyle ve gerekli bilgiyi ver."
            else:
                system_prompt = f"""
Sen yardımsever bir sağlık asistanısın. Kullanıcının sorusuna:
1. Samimi ve anlaşılır dille cevap ver
2. Kısa ve öz ol (max 3-4 cümle)
3. Gerekirse basit öneri ver
4. Ciddi durumlar için doktora yönlendir
5. Türkçe yanıt ver

Soru kategorisi: {intent}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI Response generation error: {e}")
            return self._demo_generate_response(text, intent)
    
    def _demo_generate_response(self, text: str, intent: str = None) -> str:
        """Demo mode için hazır yanıtlar"""
        if not intent:
            intent = self._demo_classify_intent(text)
        
        demo_responses = {
            'greeting': [
                "Merhaba! Size nasıl yardımcı olabilirim? 😊",
                "Selam! Sağlık konularında size yardımcı olmak için buradayım.",
                "İyi günler! Sağlıkla ilgili sorularınızı yanıtlayabilirim."
            ],
            'goodbye': [
                "Hoşçakalın! Sağlıklı kalın ve kendinize iyi bakın. 👋",
                "Görüşmek üzere! İhtiyacınız olduğunda buradayım.",
                "Sağlıklı günler dilerim! 💚"
            ],
            'symptom_inquiry': [
                "Belirtilerinizi anlıyorum. Dinlenmenizi ve bol sıvı almanızı öneririm. Devam ederse doktora başvurun.",
                "Bu semptomlar için öncelikle dinlenme önemli. Şikayetler artarsa sağlık kuruluşuna başvurun.",
                "Yaşadığınız durumu anlıyorum. Genel öneriler: istirahat, hidrasyon. Ciddi durumlarda doktor kontrolü gerekli."
            ],
            'appointment_booking': [
                "Randevu için MHRS sistemini kullanabilir veya hastane çağrı merkezini arayabilirsiniz.",
                "182 numaralı MHRS hattından randevu alabilirsiniz. Hangi bölümden randevu almak istiyorsunuz?",
                "Online randevu sistemleri veya hastane çağrı merkezleri ile iletişime geçebilirsiniz."
            ],
            'medication_info': [
                "İlaç kullanımında doktor veya eczacı önerisi önemlidir. Prospektüsü okuyun ve doz bilgisine uyun.",
                "İlaç bilgileri için eczacınıza danışmanızı öneririm. Doktor önerisi olmadan ilaç kullanmayın.",
                "İlaç dozları kişiye özeldir. Mutlaka sağlık uzmanına danışın."
            ],
            'emergency': [
                "🚨 Bu acil bir durum! Hemen 112'yi arayın ve acil servise gidin!",
                "ACİL DURUM! Vakit kaybetmeden 112'yi arayın. Sakin kalmaya çalışın.",
                "Bu ciddi bir durum. Hemen ambulans çağırın: 112"
            ],
            'general_health': [
                "Sağlıklı yaşam için düzenli egzersiz, dengeli beslenme ve yeterli uyku önemli.",
                "Genel sağlık için: bol su için, dengeli beslenin, düzenli egzersiz yapın, stresi yönetin.",
                "Sağlıklı yaşam tarzı benimseyin: kaliteli uyku, sağlıklı beslenme, aktif yaşam."
            ],
            'doctor_recommendation': [
                "Şikayetinize göre hangi doktora gideceğinizi önerebilirim. Durumunuzu detaylandırabilir misiniz?",
                "Genel sorunlar için dahiliye, uzman durumlar için ilgili bölüm doktorları uygun.",
                "Belirtilerinize göre doktor önerisi verebilirim. Hangi konuda yardım istiyorsunuz?"
            ]
        }
        
        responses = demo_responses.get(intent, demo_responses['symptom_inquiry'])
        return random.choice(responses) + f" [Demo Mode - Intent: {intent}]"
    
    def evaluate_model(self) -> Dict:
        """Model performansını değerlendir (Demo mode destekli)"""
        if self.test_data is None:
            raise ValueError("Test data not available. Run prepare_training_data first.")
        
        predictions = []
        true_labels = []
        response_times = []
        
        logger.info(f"Evaluating OpenAI model performance... (Demo: {self.demo_mode})")
        
        for idx, row in self.test_data.iterrows():
            start_time = time.time()
            
            try:
                predicted_intent = self.classify_intent(row['text'])
                predictions.append(predicted_intent)
                true_labels.append(row['intent'])
                
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                if idx % 10 == 0:
                    logger.info(f"Processed {idx+1}/{len(self.test_data)} samples")
                    
            except Exception as e:
                logger.error(f"Error processing sample {idx}: {e}")
                predictions.append('symptom_inquiry')
                true_labels.append(row['intent'])
                response_times.append(0.5)
        
        # Metrikleri hesapla
        precision = precision_score(true_labels, predictions, average='weighted', zero_division='warn')
        recall = recall_score(true_labels, predictions, average='weighted', zero_division='warn')
        f1 = f1_score(true_labels, predictions, average='weighted', zero_division='warn')
        
        # Intent bazında accuracy
        intent_accuracy = {}
        unique_intents = list(set(true_labels))
        
        for intent in unique_intents:
            intent_indices = [i for i, x in enumerate(true_labels) if x == intent]
            intent_predictions = [predictions[i] for i in intent_indices]
            intent_true = [true_labels[i] for i in intent_indices]
            
            correct = sum([1 for i, j in zip(intent_predictions, intent_true) if i == j])
            total = len(intent_true)
            intent_accuracy[intent] = correct / total if total > 0 else 0
        
        results = {
            'model_name': f'GPT-3.5-Turbo{"(Demo)" if self.demo_mode else ""}',
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'avg_response_time': np.mean(response_times),
            'intent_accuracy': intent_accuracy,
            'total_samples': len(true_labels),
            'predictions': predictions,
            'true_labels': true_labels,
            'demo_mode': self.demo_mode
        }
        
        logger.info(f"OpenAI Model Evaluation Results:")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall: {recall:.4f}")
        logger.info(f"F1 Score: {f1:.4f}")
        logger.info(f"Avg Response Time: {np.mean(response_times):.2f}s")
        logger.info(f"Demo Mode: {self.demo_mode}")
        
        return results
    
    def chat_demo(self):
        """
        Basit chat demo'su
        """
        print("🏥 Sağlık Asistanı OpenAI Chatbot Demo")
        print("Çıkmak için 'quit' yazın\n")
        
        while True:
            user_input = input("👤 Siz: ")
            
            if user_input.lower() in ['quit', 'exit', 'çıkış']:
                print("👋 Hoşçakalın! Sağlıklı günler dilerim!")
                break
            
            try:
                intent = self.classify_intent(user_input)
                response = self.generate_response(user_input, intent)
                print(f"🤖 Sağlık Asistanı ({intent}): {response}\n")
                
            except Exception as e:
                print(f"❌ Hata: {e}\n")

if __name__ == "__main__":
    # Test için
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        model = OpenAIModel(api_key)
        model.chat_demo()
    else:
        print("OPENAI_API_KEY environment variable not found!") 