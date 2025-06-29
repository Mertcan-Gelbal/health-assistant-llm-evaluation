#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini vs OpenAI Model Karşılaştırma Sistemi
"""

import sys
import os
import pandas as pd
# import matplotlib.pyplot as plt  # Not used currently
# import seaborn as sns              # Not used currently
from pathlib import Path
import time
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Kök dizini path'e ekle
sys.path.append(str(Path(__file__).parent.parent))

# Modelleri import et
from models.gemini_model import GeminiModel
from models.openai_model import OpenAIModel

# .env dosyasını yükle
load_dotenv()

class ModelComparison:
    def __init__(self):
        """Model karşılaştırma sınıfı"""
        self.google_api_key = os.getenv('GOOGLE_API_KEY', 'your_google_api_key_here')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        self.gemini_model = None
        self.openai_model = None
        self.dataset = None
        
    def load_models(self):
        """Modelleri yükle ve başlat"""
        print("🚀 Modeller yükleniyor...")
        
        try:
            # Gemini modelini başlat
            self.gemini_model = GeminiModel(self.google_api_key)
            print("✅ Gemini model yüklendi")
            
            # OpenAI modelini başlat
            if self.openai_api_key:
                self.openai_model = OpenAIModel(self.openai_api_key)
                print("✅ OpenAI model yüklendi")
            else:
                print("❌ OpenAI API key bulunamadı!")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
            return False
    
    def load_dataset(self, dataset_path: str = "../data/health_assistant_dataset.csv"):
        """Veri setini yükle"""
        try:
            self.dataset = pd.read_csv(dataset_path)
            print(f"📊 Veri seti yüklendi: {len(self.dataset)} satır")
            print(f"📋 Intent dağılımı:")
            print(self.dataset['intent'].value_counts())
            return True
        except Exception as e:
            print(f"❌ Veri seti yükleme hatası: {e}")
            return False
    
    def evaluate_models(self, sample_size: int = 100):
        """İki modeli karşılaştır"""
        print(f"\n🔍 Model değerlendirmesi başlıyor... (Örnek sayısı: {sample_size})")
        
        if self.dataset is None:
            print("❌ Veri seti yüklenmemiş!")
            return None
        
        # Küçük bir örnek al (API maliyeti için)
        sample_data = self.dataset.sample(n=min(sample_size, len(self.dataset)), random_state=42)
        
        # Gemini modeli değerlendirmesi
        print("\n🤖 Gemini Model değerlendiriliyor...")
        gemini_results = self.evaluate_single_model(self.gemini_model, sample_data, "Gemini")
        
        # OpenAI modeli değerlendirmesi
        print("\n🧠 OpenAI Model değerlendiriliyor...")
        openai_results = self.evaluate_single_model(self.openai_model, sample_data, "OpenAI")
        
        # Karşılaştırma raporu
        comparison_results = {
            'gemini': gemini_results,
            'openai': openai_results,
            'sample_size': sample_size
        }
        
        return comparison_results
    
    def evaluate_single_model(self, model, sample_data, model_name):
        """Tek bir modeli değerlendir"""
        predictions = []
        true_labels = []
        response_times = []
        
        total_samples = len(sample_data)
        
        for idx, row in sample_data.iterrows():
            try:
                start_time = time.time()
                
                # Intent tahmini yap
                predicted_intent = model.classify_intent(row['text'])
                predictions.append(predicted_intent)
                true_labels.append(row['intent'])
                
                # Yanıt süresi
                response_time = time.time() - start_time
                response_times.append(response_time)
                
                # Progress göster
                if len(predictions) % 10 == 0:
                    print(f"  {model_name}: {len(predictions)}/{total_samples} tamamlandı")
                
            except Exception as e:
                print(f"  ❌ Hata ({model_name}): {e}")
                predictions.append('symptom_inquiry')  # Default
                true_labels.append(row['intent'])
                response_times.append(1.0)
        
        # Metrikleri hesapla
        from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
        
        precision = precision_score(true_labels, predictions, average='weighted', zero_division='warn')
        recall = recall_score(true_labels, predictions, average='weighted', zero_division='warn')
        f1 = f1_score(true_labels, predictions, average='weighted', zero_division='warn')
        accuracy = accuracy_score(true_labels, predictions)
        
        # Intent bazında accuracy
        intent_accuracy = {}
        unique_intents = list(set(true_labels))
        
        for intent in unique_intents:
            intent_indices = [i for i, x in enumerate(true_labels) if x == intent]
            intent_predictions = [predictions[i] for i in intent_indices]
            intent_true = [true_labels[i] for i in intent_indices]
            
            if len(intent_true) > 0:
                correct = sum([1 for i, j in zip(intent_predictions, intent_true) if i == j])
                intent_accuracy[intent] = correct / len(intent_true)
        
        results = {
            'model_name': model_name,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'accuracy': accuracy,
            'avg_response_time': sum(response_times) / len(response_times),
            'intent_accuracy': intent_accuracy,
            'predictions': predictions,
            'true_labels': true_labels,
            'total_samples': len(true_labels)
        }
        
        print(f"  ✅ {model_name} değerlendirmesi tamamlandı!")
        return results
    
    def create_comparison_report(self, results):
        """Karşılaştırma raporu oluştur"""
        print("\n" + "="*60)
        print("📊 MODEL KARŞILAŞTIRMA RAPORU")
        print("="*60)
        
        gemini_results = results['gemini']
        openai_results = results['openai']
        
        # Genel performans tablosu
        print("\n🏆 GENEL PERFORMANS METRİKLERİ:")
        print("-" * 60)
        print(f"{'Metrik':<20} {'Gemini':<15} {'OpenAI':<15} {'Kazanan':<10}")
        print("-" * 60)
        
        # Metrikler
        metrics = ['precision', 'recall', 'f1_score', 'accuracy']
        winners = []
        
        for metric in metrics:
            gemini_val = gemini_results[metric]
            openai_val = openai_results[metric]
            
            if gemini_val > openai_val:
                winner = "Gemini ⭐"
                winners.append("Gemini")
            elif openai_val > gemini_val:
                winner = "OpenAI ⭐"
                winners.append("OpenAI")
            else:
                winner = "Berabere"
                winners.append("Tie")
            
            print(f"{metric.capitalize():<20} {gemini_val:.4f}{'':8} {openai_val:.4f}{'':8} {winner}")
        
        # Yanıt süreleri
        print(f"{'Response Time':<20} {gemini_results['avg_response_time']:.2f}s{'':7} {openai_results['avg_response_time']:.2f}s{'':7} {'OpenAI' if openai_results['avg_response_time'] < gemini_results['avg_response_time'] else 'Gemini'} ⚡")
        
        print("-" * 60)
        
        # Genel kazanan
        gemini_wins = winners.count("Gemini")
        openai_wins = winners.count("OpenAI")
        
        if gemini_wins > openai_wins:
            overall_winner = "🏆 GENEL KAZANAN: GEMINI MODEL"
        elif openai_wins > gemini_wins:
            overall_winner = "🏆 GENEL KAZANAN: OPENAI MODEL"
        else:
            overall_winner = "🤝 GENEL DURUM: BERABERE"
        
        print(f"\n{overall_winner}")
        
        # Intent bazında detay
        print(f"\n📋 INTENT BAZINDA DOĞRULUK ORANI:")
        print("-" * 60)
        print(f"{'Intent':<20} {'Gemini':<15} {'OpenAI':<15}")
        print("-" * 60)
        
        all_intents = set(list(gemini_results['intent_accuracy'].keys()) + 
                         list(openai_results['intent_accuracy'].keys()))
        
        for intent in sorted(all_intents):
            gemini_acc = gemini_results['intent_accuracy'].get(intent, 0)
            openai_acc = openai_results['intent_accuracy'].get(intent, 0)
            print(f"{intent:<20} {gemini_acc:.4f}{'':8} {openai_acc:.4f}")
        
        print("-" * 60)
        print(f"📊 Toplam Test Örnekleri: {results['sample_size']}")
        print("="*60)
        
        return results
    
    def save_results_to_csv(self, results, filename="../results/model_comparison.csv"):
        """Sonuçları CSV'ye kaydet"""
        try:
            os.makedirs("../results", exist_ok=True)
            
            # DataFrame oluştur
            comparison_data = []
            
            for model_name in ['gemini', 'openai']:
                model_results = results[model_name]
                
                row = {
                    'Model': model_results['model_name'],
                    'Precision': model_results['precision'],
                    'Recall': model_results['recall'],
                    'F1_Score': model_results['f1_score'],
                    'Accuracy': model_results['accuracy'],
                    'Avg_Response_Time': model_results['avg_response_time'],
                    'Total_Samples': model_results['total_samples']
                }
                
                comparison_data.append(row)
            
            df = pd.DataFrame(comparison_data)
            df.to_csv(filename, index=False)
            print(f"✅ Sonuçlar kaydedildi: {filename}")
            
        except Exception as e:
            print(f"❌ Sonuç kaydetme hatası: {e}")
    
    def run_full_comparison(self, sample_size: int = 50):
        """Tam karşılaştırma çalıştır"""
        print("🚀 Sağlık Asistanı Chatbot Model Karşılaştırması")
        print("="*60)
        
        # Modelleri yükle
        if not self.load_models():
            return None
        
        # Veri setini yükle
        if not self.load_dataset():
            return None
        
        # Modelleri değerlendir
        results = self.evaluate_models(sample_size)
        
        if results:
            # Rapor oluştur
            self.create_comparison_report(results)
            
            # CSV'ye kaydet
            self.save_results_to_csv(results)
            
            return results
        
        return None

def main():
    """Ana fonksiyon"""
    comparison = ModelComparison()
    
    # Karşılaştırmayı çalıştır (API maliyeti için küçük sample)
    results = comparison.run_full_comparison(sample_size=30)
    
    if results:
        print("\n🎉 Model karşılaştırması başarıyla tamamlandı!")
    else:
        print("\n❌ Model karşılaştırması başarısız!")

if __name__ == "__main__":
    main() 