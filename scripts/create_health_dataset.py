import pandas as pd
import os

# Sağlık asistanı chatbot veri seti
health_data = [
    # Greeting Intent
    ("Merhaba sağlık asistanı", "greeting", "Merhaba! Size nasıl yardımcı olabilirim? Sağlık konularında sorularınızı yanıtlayabilirim."),
    ("Selam", "greeting", "Selam! Sağlık asistanınızım. Size nasıl yardımcı olabilirim?"),
    ("İyi günler", "greeting", "İyi günler! Sağlığınızla ilgili nasıl yardımcı olabilirim?"),
    ("Hey sağlık asistanı", "greeting", "Merhaba! Size sağlık konularında yardımcı olmak için buradayım."),
    ("Hoş geldiniz diyebilir misiniz", "greeting", "Hoş geldiniz! Sağlık konularında size nasıl yardımcı olabilirim?"),
    ("Nasılsın", "greeting", "Teşekkürler! Ben bir sağlık asistanıyım ve size yardımcı olmak için buradayım. Sağlığınız nasıl?"),
    ("Kimsin", "greeting", "Ben sağlık konularında size yardımcı olan bir yapay zeka asistanıyım."),
    ("Yardım", "greeting", "Sağlık asistanınızım. Belirtilerinizi, sorularınızı paylaşabilirsiniz."),
    ("Ana menü", "greeting", "Merhaba! Size sağlık konularında nasıl yardımcı olabilirim?"),
    ("Seçenekler", "greeting", "Size şu konularda yardımcı olabilirim: semptomlar, randevu alma, ilaç bilgileri, acil durumlar."),
    
    # Goodbye Intent
    ("Teşekkürler", "goodbye", "Rica ederim! Sağlığınız için buradayım. Geçmiş olsun ve kendinize iyi bakın!"),
    ("Görüşürüz", "goodbye", "Görüşmek üzere! Sağlıklı günler dilerim. İhtiyacınız olduğunda yine buradayım."),
    ("Hoşçakal", "goodbye", "Hoşçakalın! Sağlığınızla ilgili sorularınız olduğunda çekinmeden sorun."),
    ("İyi günler", "goodbye", "İyi günler! Sağlıklı kalın ve kendinize iyi bakın."),
    ("Sağ olun", "goodbye", "Sağ olun! Size yardımcı olabildiysem ne mutlu. Sağlıklı günler dilerim!"),
    ("Görüşürüz sağlık asistanı", "goodbye", "Görüşmek üzere! Sağlıklı kalın ve ihtiyacınız olduğunda tekrar buluşalım."),
    ("Kapanış", "goodbye", "Size yardımcı olabildiysem ne mutlu. Sağlığınızla ilgili her zaman buradayım."),
    ("Bitiriyorum", "goodbye", "Sohbetimizi sonlandırıyoruz. Kendinize iyi bakın ve sağlıklı kalın."),
    ("Çıkış", "goodbye", "Çıkış yapıyoruz. Sağlık konularında çekinmeden danışın. Elveda!"),
    ("Son", "goodbye", "Sohbetimizin sonuna geldik. Sağlıklı kalın!"),
    
    # Symptom Inquiry Intent
    ("Başım ağrıyor", "symptom_inquiry", "Baş ağrısı birçok sebepten kaynaklanabilir. Stres, uykusuzluk, dehidratasyon olabilir. Bol su için ve dinlenin."),
    ("Ateşim var", "symptom_inquiry", "Ateş vücudun enfeksiyonla mücadelesinin bir işaretidir. Bol sıvı alın, dinlenin. 38.5°C üzerindeyse doktora başvurun."),
    ("Boğazım ağrıyor", "symptom_inquiry", "Boğaz ağrısı genellikle viral enfeksiyon belirtisidir. Ilık tuzlu su ile gargara yapın."),
    ("Mide bulantım var", "symptom_inquiry", "Bulantı birçok sebepten olabilir. Az ve sık yemek yiyin, zencefil çayı içebilirsiniz."),
    ("Göğsümde ağrı var", "symptom_inquiry", "Göğüs ağrısı ciddi olabilir. Nefes darlığı, ter basması varsa hemen acile gidin."),
    ("Hastayım", "symptom_inquiry", "Üzgünüm duyduğuma. Şikayetlerinizi detaylandırabilir misiniz?"),
    ("Ağrım var", "symptom_inquiry", "Nerenizde ağrı var? Ağrının karakteri nasıl? Ne zamandan beri devam ediyor?"),
    ("Uykusuzluk", "symptom_inquiry", "Uykusuzluk için uyku hijyeni önemli. Düzenli uyku saatleri, kafein kısıtlaması gerekli."),
    ("Yorgunluk", "symptom_inquiry", "Yorgunluk birçok sebepten kaynaklanabilir. Yetersiz uyku, stres, anemi olabilir."),
    ("Migren ağrısı", "symptom_inquiry", "Migren ağrısında karanlık, sessiz ortamda dinlenin. Soğuk kompres uygulayın."),
    ("Sırt ağrısı", "symptom_inquiry", "Sırt ağrısında doğru duruş önemli. Sıcak-soğuk uygulama faydalı."),
    ("Boyun ağrısı", "symptom_inquiry", "Boyun ağrısı genellikle kas gerginliğinden. Boyun egzersizleri yapın."),
    ("Göz ağrısı", "symptom_inquiry", "Göz ağrısı glokom belirtisi olabilir. Hemen göz doktoruna başvurun."),
    ("Kulak ağrısı", "symptom_inquiry", "Kulak ağrısı genellikle enfeksiyondan. Sıcak kompres uygulayabilirsiniz."),
    ("Diş ağrısı", "symptom_inquiry", "Diş ağrısında soğuk kompres, ağız gargarası faydalı. En kısa sürede diş hekimine gidin."),
    ("Karın ağrısı", "symptom_inquiry", "Karın ağrısının yeri ve şiddeti önemli. Şiddetli ağrıda acile başvurun."),
    ("İshal", "symptom_inquiry", "İshal durumunda bol sıvı alın, probiyotik içeren yiyecekler tüketin."),
    ("Kabızlık", "symptom_inquiry", "Kabızlık için bol lif, su tüketin. Düzenli egzersiz yapın."),
    ("Çarpıntı", "symptom_inquiry", "Çarpıntıda derin nefes alın, soğuk su için. Sürekli çarpıntıda kardiyolog kontrolü gerekli."),
    ("Nefes darlığı", "symptom_inquiry", "Nefes darlığı astım, kalp sorunu belirtisi olabilir. Şiddetliyse 112'yi arayın."),
    
    # Appointment Booking Intent
    ("Doktor randevusu almak istiyorum", "appointment_booking", "Hangi bölümden randevu almak istiyorsunuz? Size en yakın hastane bilgilerini verebilirim."),
    ("Kardiyoloji randevusu", "appointment_booking", "Kardiyoloji randevusu için hastane çağrı merkezini arayabilir veya online randevu sistemlerini kullanabilirsiniz."),
    ("Dahiliye randevusu istiyorum", "appointment_booking", "Dahiliye randevusu için MHRS'den online randevu alabilir veya 182'yi arayabilirsiniz."),
    ("Göz doktoru randevusu", "appointment_booking", "Göz doktoru randevusu için MHRS sistemini kullanabilir veya özel hastanelerden randevu alabilirsiniz."),
    ("Jinekolog randevusu", "appointment_booking", "Jinekolog randevusu için MHRS üzerinden veya özel hastanelerden randevu alabilirsiniz."),
    ("Hastane seçimi", "appointment_booking", "Hastane seçiminde yakınlık, uzmanlık, ekipman kalitesi önemli."),
    ("Sağlık sigortası", "appointment_booking", "Sağlık sigortası ile devlet hastanelerinde ücretsiz tedavi alabilirsiniz."),
    ("Randevu nasıl alınır", "appointment_booking", "MHRS sisteminden online randevu alabilir veya 182 numaralı hattı arayabilirsiniz."),
    ("Özel hastane randevusu", "appointment_booking", "Özel hastaneler için direkt hastane çağrı merkezlerini arayabilirsiniz."),
    ("Acil randevu", "appointment_booking", "Acil durumlar için acil servise başvurun veya 112'yi arayın."),
    
    # Medication Info Intent
    ("Parol ilacı nasıl kullanılır", "medication_info", "Parol (parasetamol) ateş düşürücü ve ağrı kesicidir. Yetişkinler için 8 saatte bir 500mg."),
    ("Aspirin yan etkileri", "medication_info", "Aspirin mide tahrişi yapabilir, kanama riskini artırır. Doktor önerisi olmadan kullanmayın."),
    ("Antibiyotik ne zaman kullanılır", "medication_info", "Antibiyotikler sadece bakteriyel enfeksiyonlarda etkilidir. Doktor reçetesi gerekir."),
    ("Vitamin D eksikliği", "medication_info", "Vitamin D eksikliği kemik sağlığını etkiler. Doktor önerisiyle takviye alınabilir."),
    ("İbuprofen dozu", "medication_info", "İbuprofen yetişkinler için 6-8 saatte bir 200-400mg. Yemekten sonra alın."),
    ("Vitamin takviyesi", "medication_info", "Vitamin takviyesi doktor önerisiyle alınmalı. Aşırı vitamin zararlı olabilir."),
    ("İlaç etkileşimi", "medication_info", "İlaç etkileşimleri tehlikeli olabilir. Doktorunuza tüm kullandığınız ilaçları bildirin."),
    ("Doğal ilaçlar", "medication_info", "Doğal ilaçlar da yan etki yapabilir. Eczacı veya doktor danışmanlığı alın."),
    ("İlaç saklama", "medication_info", "İlaçları kuru, serin yerde, çocukların ulaşamayacağı yerde saklayın."),
    ("İlaç unutma", "medication_info", "İlaç unuttuysanız hatırladığınızda alın. Çift doz almayın."),
    
    # Emergency Intent
    ("Kalp krizi belirtileri", "emergency", "Kalp krizi belirtileri: göğüs ağrısı, nefes darlığı, kol ağrısı. Bu belirtiler varsa hemen 112'yi arayın!"),
    ("Felç belirtileri", "emergency", "Felç belirtileri: yüz asimetrisi, kol zayıflığı, konuşma bozukluğu. Hemen 112'yi arayın!"),
    ("Zehirlenme durumunda", "emergency", "Zehirlenme şüphesinde hemen 114 Zehir Danışma Merkezini arayın."),
    ("Epilepsi nöbeti", "emergency", "Epilepsi nöbetinde kişiyi yere yatırın, etrafındaki tehlikeli eşyaları kaldırın."),
    ("Şiddetli kanama", "emergency", "Şiddetli kanamada basınç uygulayın, yaralanmış yeri kalbin üzerine kaldırın."),
    ("Birinci yardım", "emergency", "Birinci yardımda ABC kuralı: Airway, Breathing, Circulation. Sakin olun, 112'yi arayın."),
    ("Yaralama durumu", "emergency", "Yaralanmalarda kanamayı durdurmak öncelik. Temiz bezle basınç uygulayın."),
    ("Yanık tedavisi", "emergency", "Yanıklarda soğuk su ile soğutun. Buz kullanmayın."),
    ("Kırık şüphesi", "emergency", "Kırık şüphesinde kıpırdatmayın, sabitleyin. Hemen ortopedi doktoruna başvurun."),
    ("Bayılma durumu", "emergency", "Bayılmalarda kişiyi yan yatırın, havası açık yere alın."),
    
    # General Health Intent
    ("Sağlıklı beslenme", "general_health", "Sağlıklı beslenme için çeşitli besinler tüketin. Bol sebze-meyve, tam tahıl, protein."),
    ("Egzersiz önerileri", "general_health", "Haftada en az 150 dakika orta şiddetli egzersiz yapın."),
    ("Su tüketimi", "general_health", "Günde en az 8 bardak su için. Vücut ağırlığınızın 35ml'si kadar su gerekir."),
    ("Uyku düzeni", "general_health", "Günde 7-9 saat uyku önemlidir. Düzenli uyku saatleri, yatak odası serin olmalı."),
    ("Stres yönetimi", "general_health", "Stres yönetimi için nefes egzersizleri, meditasyon, düzenli egzersiz yapın."),
    ("Kilo verme", "general_health", "Sağlıklı kilo verme için kalori açığı oluşturun. Balanced beslenme, düzenli egzersiz."),
    ("Kilo alma", "general_health", "Sağlıklı kilo almak için kaliteli kalori alın. Protein, sağlıklı yağlar önemli."),
    ("Kan basıncı", "general_health", "Normal kan basıncı 120/80 mmHg altındadır. Düşük tuz, egzersiz önemli."),
    ("Aşı takvimi", "general_health", "Aşı takvimi yaşa göre değişir. Çocuklar için rutin aşılar önemli."),
    ("Sağlık kontrolü", "general_health", "Yılda bir genel sağlık kontrolü yaptırın. Kan tahlili, EKG önemli."),
    
    # Doctor Recommendation Intent
    ("Hangi doktora gideyim", "doctor_recommendation", "Şikayetinize göre doktor önerebilirim. Genel sağlık sorunları için dahiliye uygun."),
    ("Baş ağrısı hangi doktor", "doctor_recommendation", "Baş ağrısı için önce dahiliyeye başvurun. Gerekirse nöroloji bölümüne yönlendirilirsiniz."),
    ("Mide sorunları hangi doktor", "doctor_recommendation", "Mide sorunları için gastroenteroloji bölümü uygundur."),
    ("Eklem ağrıları doktor", "doctor_recommendation", "Eklem ağrıları için romatoloji veya ortopedi bölümü uygun."),
    ("Cilt problemleri doktor", "doctor_recommendation", "Cilt problemleri için dermatoloji bölümü uygundur."),
    ("Doktor seçimi", "doctor_recommendation", "Doktor seçiminde uzmanlık alanı, tecrübe, hasta yorumları önemli."),
    ("Uzman doktor", "doctor_recommendation", "Uzman doktor için MHRS sisteminden randevu alabilirsiniz."),
    ("Kadın doktoru", "doctor_recommendation", "Kadın sağlığı için jinekolog, genel durumlar için dahiliye uygun."),
    ("Çocuk doktoru", "doctor_recommendation", "Çocuk sağlığı için çocuk doktoru (pediatrist) en uygunudur."),
    ("Yaşlı doktoru", "doctor_recommendation", "Yaşlı hastalarda geriatri uzmanı veya dahiliye doktoru uygun."),
    
    # Additional diverse examples to reach 1000+
    ("Hamilelik belirtileri", "symptom_inquiry", "Hamilelik belirtileri: adet gecikmesi, bulantı, göğüs hassasiyeti."),
    ("Menopoz belirtileri", "symptom_inquiry", "Menopoz belirtileri: sıcak basması, adet düzensizliği, ruh hali değişikliği."),
    ("Depresyon belirtileri", "symptom_inquiry", "Depresyon belirtileri: sürekli üzüntü, ilgi kaybı, uyku sorunu."),
    ("Anksiyete", "symptom_inquiry", "Anksiyete durumunda derin nefes egzersizleri yapın. Uzman desteği alın."),
    ("Hipertansiyon", "symptom_inquiry", "Yüksek tansiyon sessiz katildir. Düşük tuz, düzenli egzersiz önemli."),
    ("Diyabet", "symptom_inquiry", "Diyabet kontrol edilebilir bir hastalık. Diyet, egzersiz, ilaç uyumu önemli."),
    ("Kolesterol", "symptom_inquiry", "Yüksek kolesterol kalp hastalığı riskini artırır. Sağlıklı beslenme önemli."),
    ("Astım", "symptom_inquiry", "Astım nöbetlerinde sakin olun, inhaler kullanın."),
    ("Alerjik reaksiyon", "symptom_inquiry", "Alerjik reaksiyonda alerjenden uzaklaşın."),
    ("Organ bağışı", "general_health", "Organ bağışı hayat kurtarır. Sağlık Bakanlığı'na başvurabilirsiniz."),
]

# Veri setini genişlet (1000+ satır için)
extended_data = health_data.copy()

# Varyasyonlar ekle
variations = [
    ("Merhaba doktor", "greeting", "Merhaba! Ben bir sağlık asistanıyım. Size nasıl yardımcı olabilirim?"),
    ("Hekimle konuşmak istiyorum", "greeting", "Ben bir sağlık asistanıyım, size yardımcı olabilirim. Sorunuz nedir?"),
    ("Sağlık durumu", "greeting", "Sağlık durumunuzla ilgili nasıl yardımcı olabilirim?"),
    ("Medikal yardım", "greeting", "Medikal konularda size yardımcı olmak için buradayım."),
    ("Hasta durumu", "greeting", "Hasta durumunuzla ilgili size nasıl yardımcı olabilirim?"),
]

# Daha fazla semptom çeşitliliği
symptom_variations = [
    ("Ağrı hissediyorum", "symptom_inquiry", "Ağrının yerini ve şiddetini belirtirseniz daha iyi yardımcı olabilirim."),
    ("Hasta hissediyorum", "symptom_inquiry", "Kendinizi nasıl hasta hissediyorsunuz? Belirtilerinizi açıklayabilir misiniz?"),
    ("Rahatsızım", "symptom_inquiry", "Hangi konuda rahatsızlık yaşıyorsunuz? Detay verebilir misiniz?"),
    ("Kötü hissediyorum", "symptom_inquiry", "Nasıl kötü hissediyorsunuz? Fiziksel belirtileriniz var mı?"),
    ("Ağrım çok şiddetli", "symptom_inquiry", "Şiddetli ağrı ciddi olabilir. Hangi bölgede ağrı yaşıyorsunuz?"),
]

# Randevu çeşitliliği
appointment_variations = [
    ("Hekim randevusu", "appointment_booking", "Hangi uzmanlık dalından hekim randevusu almak istiyorsunuz?"),
    ("Hastane randevusu", "appointment_booking", "Hastane randevusu için MHRS sistemini kullanabilirsiniz."),
    ("Doktor görüşmesi", "appointment_booking", "Doktor görüşmesi için randevu almanız gerekiyor."),
    ("Muayene randevusu", "appointment_booking", "Muayene randevusu için size yardımcı olabilirim."),
    ("Kontrole gitmek istiyorum", "appointment_booking", "Kontrol randevusu için hangi bölümü tercih ediyorsunuz?"),
]

# İlaç bilgisi çeşitliliği  
medication_variations = [
    ("İlaç bilgisi", "medication_info", "Hangi ilaç hakkında bilgi almak istiyorsunuz?"),
    ("Doz bilgisi", "medication_info", "İlaç dozu hasta yaşı ve kilosuna göre değişir. Prospektüse bakın."),
    ("Yan etki", "medication_info", "İlaç yan etkileri için prospektüsü okuyun veya eczacınıza danışın."),
    ("İlaç kullanımı", "medication_info", "İlaç kullanım şeklini doktor veya eczacınız size açıklamalı."),
    ("Reçete", "medication_info", "Reçeteli ilaçlar doktor kontrolünde kullanılmalıdır."),
]

# Acil durum çeşitliliği
emergency_variations = [
    ("Acil durumda ne yapmalı", "emergency", "Acil durumda 112'yi arayın ve sakin kalmaya çalışın."),
    ("İlk yardım", "emergency", "İlk yardımda önce güvenliği sağlayın, sonra yardım edin."),
    ("Kaza geçirdim", "emergency", "Kaza sonrası ciddi yaralanma varsa hemen 112'yi arayın."),
    ("Acil servis", "emergency", "Acil servis için en yakın hastaneye gidin veya ambulans çağırın."),
    ("112 ne zaman aranır", "emergency", "Hayatı tehdit eden durumlarda 112'yi arayın."),
]

# Genel sağlık çeşitliliği
health_variations = [
    ("Sağlıklı nasıl yaşarım", "general_health", "Dengeli beslenme, düzenli egzersiz, yeterli uyku sağlıklı yaşamın temelidir."),
    ("Fitness önerileri", "general_health", "Fitness için düzenli egzersiz programı oluşturun ve beslenmeye dikkat edin."),
    ("Beslenme tavsiyeleri", "general_health", "Çeşitli besin gruplarından dengeli şekilde tüketin."),
    ("Yaşam tarzı", "general_health", "Sağlıklı yaşam tarzı için sigara-alkol bırakın, düzenli egzersiz yapın."),
    ("Önleyici tıp", "general_health", "Önleyici tıp için düzenli check-up yaptırın ve risk faktörlerini kontrol edin."),
]

# Doktor önerisi çeşitliliği
doctor_variations = [
    ("Hangi uzman", "doctor_recommendation", "Şikayetinize uygun uzman doktor önerisi verebilirim."),
    ("Bölüm seçimi", "doctor_recommendation", "Hangi tıp bölümüne başvuracağınızı belirlemenize yardımcı olabilirim."),
    ("Doktor türü", "doctor_recommendation", "Sorununuza uygun doktor türünü önerebilirim."),
    ("Uzmanlık alanı", "doctor_recommendation", "Uzmanlık alanı seçiminde size rehberlik edebilirim."),
    ("Hangi hekim", "doctor_recommendation", "Durumunuza uygun hekim önerisi yapabilirim."),
]

# Vedalaşma çeşitliliği
goodbye_variations = [
    ("Elveda", "goodbye", "Elveda! Sağlıklı kalın ve ihtiyacınız olduğunda buradayım."),
    ("Görüşmek üzere", "goodbye", "Görüşmek üzere! Kendinize iyi bakın."),
    ("Bye", "goodbye", "Bye! Sağlığınız için her zaman buradayım."),
    ("Çıkıyorum", "goodbye", "İyi gün! Sağlıklı kalın."),
    ("Kapatıyorum", "goodbye", "Sağlıklı günler dilerim!"),
]

# Tüm varyasyonları birleştir
extended_data.extend(variations)
extended_data.extend(symptom_variations)
extended_data.extend(appointment_variations)
extended_data.extend(medication_variations)
extended_data.extend(emergency_variations)
extended_data.extend(health_variations)
extended_data.extend(doctor_variations)
extended_data.extend(goodbye_variations)

# Daha da fazla örnek için döngü ile oluştur
base_symptoms = [
    "başım", "karnım", "boğazım", "sırtım", "boynum", "dizim", "ayağım", "elim", 
    "göğsüm", "kalbim", "ciğerim", "böbreğim", "karaciğerim", "midem"
]

for symptom in base_symptoms:
    extended_data.append((f"{symptom} ağrıyor", "symptom_inquiry", f"{symptom.capitalize()} ağrısı için dinlenme ve gerekirse ağrı kesici alabilirsiniz. Sürekli ağrı varsa doktora başvurun."))
    extended_data.append((f"{symptom}da ağrı var", "symptom_inquiry", f"{symptom.capitalize()}daki ağrı çeşitli sebeplerden olabilir. Şiddetli ağrıda doktor kontrolü gerekli."))

# Hastalık isimleri ile örnekler
diseases = [
    "grip", "soğuk algınlığı", "bronşit", "sinüzit", "otitis", "faringit", "laringit", 
    "gastrit", "ülser", "kolit", "nefrit", "sistit", "artrit", "romatizma"
]

for disease in diseases:
    extended_data.append((f"{disease} belirtileri", "symptom_inquiry", f"{disease.capitalize()} belirtileri değişkenlik gösterir. Doktor muayenesi ile kesin tanı konur."))
    extended_data.append((f"{disease}im var", "symptom_inquiry", f"{disease.capitalize()} tedavisi için doktor kontrolü önemlidir. İlaç tedavisi gerekebilir."))

# İlaç çeşitleri
medications = [
    "antibiyotik", "ağrı kesici", "ateş düşürücü", "vitamin", "mineral", "probiyotik",
    "antihistaminik", "dekonjesan", "expectorant", "antasit", "laksatif"
]

for med in medications:
    extended_data.append((f"{med} kullanımı", "medication_info", f"{med.capitalize()} kullanımında doktor veya eczacı önerisi önemlidir."))
    extended_data.append((f"{med} dozu", "medication_info", f"{med.capitalize()} dozu yaş, kilo ve hastalığa göre değişir."))

# Doktor bölümleri
departments = [
    "kardiyoloji", "nöroloji", "ortopedi", "üroloji", "jinekolog", "pediatri",
    "dermatoloji", "psikiyatri", "endokrinoloji", "gastroenteroloji", "göğüs hastalıkları"
]

for dept in departments:
    extended_data.append((f"{dept} randevusu", "appointment_booking", f"{dept.capitalize()} randevusu için MHRS sistemini kullanabilir veya hastane çağrı merkezini arayabilirsiniz."))
    extended_data.append((f"{dept} doktoru", "doctor_recommendation", f"{dept.capitalize()} doktoru {dept} alanındaki sağlık sorunlarında uzmanlaşmıştır."))

print(f"Toplam veri sayısı: {len(extended_data)}")

# DataFrame oluştur
df = pd.DataFrame(extended_data, columns=['text', 'intent', 'response'])

# CSV dosyasına kaydet
df.to_csv('../data/health_assistant_dataset.csv', index=False, encoding='utf-8')
print("Sağlık asistanı veri seti oluşturuldu!")
print(f"Toplam satır sayısı: {len(df)}")
print(f"Intent dağılımı:")
print(df['intent'].value_counts()) 