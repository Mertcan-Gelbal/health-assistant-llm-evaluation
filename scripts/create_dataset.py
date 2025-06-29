#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sağlık Asistanı Chatbot Veri Seti Oluşturucu
"""

import pandas as pd
import random

def create_health_dataset():
    """Sağlık asistanı chatbot için kapsamlı veri seti oluşturur"""
    
    data = []
    
    # Greeting Intent (50 adet)
    greetings = [
        ("Merhaba", "greeting", "Merhaba! Size nasıl yardımcı olabilirim?"),
        ("Selam", "greeting", "Selam! Sağlık asistanınızım."),
        ("İyi günler", "greeting", "İyi günler! Sağlık konularında yardımcıyım."),
        ("Hey", "greeting", "Hey! Size nasıl yardımcı olabilirim?"),
        ("Nasılsın", "greeting", "İyiyim, teşekkürler! Size nasıl yardımcı olabilirim?"),
    ]
    
    # Her greeting için 10 varyasyon oluştur
    for base_greeting, intent, response in greetings:
        for i in range(10):
            text = base_greeting if i == 0 else f"{base_greeting} sağlık asistanı"
            data.append((text, intent, response))
    
    # Symptom Inquiry Intent (400 adet)
    symptoms_data = [
        ("Başım ağrıyor", "symptom_inquiry", "Baş ağrısı stres, uykusuzluk veya dehidratasyon sebebiyle olabilir."),
        ("Ateşim var", "symptom_inquiry", "Ateş vücudun enfeksiyonla mücadele ettiğini gösterir. Bol sıvı alın."),
        ("Boğazım ağrıyor", "symptom_inquiry", "Boğaz ağrısı için ılık tuzlu su ile gargara yapabilirsiniz."),
        ("Mide bulantım var", "symptom_inquiry", "Bulantı için az ve sık yemek yiyin, zencefil çayı faydalı."),
        ("Göğsümde ağrı", "symptom_inquiry", "Göğüs ağrısı ciddi olabilir, doktora başvurun."),
        ("Sırtım ağrıyor", "symptom_inquiry", "Sırt ağrısı için doğru oturuş ve hafif egzersiz faydalı."),
        ("Diz ağrım var", "symptom_inquiry", "Diz ağrısı için dinlenme ve soğuk kompres uygulayın."),
        ("Uykusuzluk", "symptom_inquiry", "Uyku düzeni için düzenli saatler ve rahat ortam önemli."),
        ("Yorgunluk", "symptom_inquiry", "Sürekli yorgunluk anemi veya tiroid sorunu belirtisi olabilir."),
        ("Çarpıntı", "symptom_inquiry", "Çarpıntı için derin nefes alın, sürekli olursa kardiyolog görün."),
    ]
    
    # Her semptom için 40 varyasyon
    for base_symptom, intent, response in symptoms_data:
        for i in range(40):
            variations = [
                base_symptom,
                f"{base_symptom} var",
                f"{base_symptom} çok şiddetli",
                f"Bu sabah {base_symptom.lower()}",
            ]
            text = random.choice(variations)
            data.append((text, intent, response))
    
    # Appointment Booking Intent (200 adet)
    appointment_data = [
        ("Randevu almak istiyorum", "appointment_booking", "Hangi bölümden randevu almak istiyorsunuz?"),
        ("Doktor randevusu", "appointment_booking", "MHRS sisteminden randevu alabilirsiniz."),
        ("Kardiyoloji randevusu", "appointment_booking", "Kardiyoloji için 182'yi arayabilirsiniz."),
        ("Göz doktoru randevusu", "appointment_booking", "Göz doktoru için online sistem kullanın."),
        ("Acil randevu", "appointment_booking", "Acil durumlar için acil servise başvurun."),
    ]
    
    for base_appointment, intent, response in appointment_data:
        for i in range(40):
            data.append((base_appointment, intent, response))
    
    # Medication Info Intent (200 adet)
    medication_data = [
        ("Parol nasıl kullanılır", "medication_info", "Parol yetişkinler için 8 saatte bir 500mg."),
        ("Aspirin yan etkileri", "medication_info", "Aspirin mide tahriş edebilir, dikkatli kullanın."),
        ("Antibiyotik kullanımı", "medication_info", "Antibiyotik doktor reçetesi ile kullanılır."),
        ("Vitamin D eksikliği", "medication_info", "Vitamin D için güneş ışığı ve takviye önemli."),
        ("İlaç dozu", "medication_info", "İlaç dozu doktor önerisi ile belirlenir."),
    ]
    
    for base_med, intent, response in medication_data:
        for i in range(40):
            data.append((base_med, intent, response))
    
    # Emergency Intent (100 adet)
    emergency_data = [
        ("Kalp krizi", "emergency", "Kalp krizi şüphesinde hemen 112'yi arayın!"),
        ("Nefes alamıyorum", "emergency", "Nefes darlığında hemen acile başvurun!"),
        ("Şiddetli ağrı", "emergency", "Şiddetli ağrı için acil servise gidin."),
        ("Bayıldım", "emergency", "Bayılma durumunda 112'yi arayın."),
        ("Kaza geçirdim", "emergency", "Kaza sonrası hemen sağlık ekibi çağırın."),
    ]
    
    for base_emergency, intent, response in emergency_data:
        for i in range(20):
            data.append((base_emergency, intent, response))
    
    # General Health Intent (150 adet)
    health_data = [
        ("Sağlıklı beslenme", "general_health", "Dengeli beslenme için çeşitli besin grupları tüketin."),
        ("Egzersiz önerileri", "general_health", "Haftada 150 dakika orta tempolu egzersiz yapın."),
        ("Su içme", "general_health", "Günde en az 8 bardak su için."),
        ("Uyku düzeni", "general_health", "7-9 saat düzenli uyku önemli."),
        ("Stres yönetimi", "general_health", "Stres için nefes egzersizleri ve meditasyon faydalı."),
    ]
    
    for base_health, intent, response in health_data:
        for i in range(30):
            data.append((base_health, intent, response))
    
    # Doctor Recommendation Intent (100 adet)
    doctor_data = [
        ("Hangi doktora gideyim", "doctor_recommendation", "Şikayetinize göre doktor önerebilirim."),
        ("Baş ağrısı hangi doktor", "doctor_recommendation", "Baş ağrısı için nöroloji veya dahiliye."),
        ("Kalp problemi doktor", "doctor_recommendation", "Kalp sorunları için kardiyoloji."),
        ("Cilt problemi doktor", "doctor_recommendation", "Cilt için dermatoloji uzmanı."),
        ("Çocuk doktoru", "doctor_recommendation", "Çocuklar için pediatri uzmanı."),
    ]
    
    for base_doctor, intent, response in doctor_data:
        for i in range(20):
            data.append((base_doctor, intent, response))
    
    # Goodbye Intent (50 adet)
    goodbye_data = [
        ("Teşekkürler", "goodbye", "Rica ederim! Sağlıklı kalın."),
        ("Görüşürüz", "goodbye", "Görüşmek üzere! İyi günler."),
        ("Hoşçakal", "goodbye", "Hoşçakalın! Kendinize iyi bakın."),
        ("Sağ ol", "goodbye", "Sağ olun! Sağlıklı günler."),
        ("Bye", "goodbye", "Bye! Her zaman buradayım."),
    ]
    
    for base_goodbye, intent, response in goodbye_data:
        for i in range(10):
            data.append((base_goodbye, intent, response))
    
    return data

if __name__ == "__main__":
    print("Sağlık asistanı veri seti oluşturuluyor...")
    
    # Veri setini oluştur
    dataset = create_health_dataset()
    
    # DataFrame'e çevir
    df = pd.DataFrame(dataset, columns=['text', 'intent', 'response'])
    
    # Karıştır
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Dosyaya kaydet
    df.to_csv('../data/health_assistant_dataset.csv', index=False, encoding='utf-8')
    
    print(f"✅ Veri seti başarıyla oluşturuldu!")
    print(f"📊 Toplam satır sayısı: {len(df)}")
    print(f"📋 Intent dağılımı:")
    print(df['intent'].value_counts())
    print(f"💾 Dosya: data/health_assistant_dataset.csv") 