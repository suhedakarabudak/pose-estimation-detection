# pose-estimation-detection



Squat, fitness dünyasında en temel ve etkili egzersizlerden biri olarak bilinir. Ancak, doğru yapılmadığında sakatlanma riskini artırabilir. Bu nedenle, doğru formda squat yapmanın önemi büyüktür.Squat hareketinin analizini gerçekleştiren ve doğru formda yapılıp yapılmadığını tespit eden bir sistem geliştirme sürecini adım adım açıklayacağım. Bu projede Medipipe kütüphanesi, Streamlit ve FastAPI kullanarak bir squat analizi uygulaması geliştirdim.

![](https://github.com/user-attachments/assets/f86f8b64-8bad-49db-8279-c5d9edfd343b)


Proje Akışı
-- 
1. Video Yükleme: Kullanıcı, Streamlit arayüzünden squat videosunu yükler. 

2. Koordinatların Çıkarılması: Medipipe Pose Estimation modeli, videodaki her karedeki vücut eklemlerinin x, y, z koordinatlarını çıkarır.

3. Makine Öğrenimi Analizi: Bu koordinatlar, FastAPI üzerinden çalışan makine öğrenimi modeline gönderilir.

4. Sonuçların Görüntülenmesi: Model, squat hareketinin doğru olup olmadığını analiz eder ve sonucu Streamlit arayüzüne geri gönderir.

5. Sonuçların İndirilmesi: Kullanıcı, analiz sonuçlarını isterse bir dosya olarak indirebilir.

Sonuç
-- 

Bu projede, squat analizini otomatikleştiren bir sistem geliştirdim. Medipipe kütüphanesi ile vücut eklemlerinin koordinatlarını çıkardım.Buradan elde ettiğim ham verileri kullanarak  makine öğrenmesi modeli ile doğru ve yanlış squatları belirledim ve bu sistemi FastAPI ile bir servise entegre ettim. Sonuç olarak, kullanıcıların squat formunu analiz edebileceği, interaktif ve kullanışlı bir proje ortaya koydum.

Bu tür projeler, fitness ve sağlık alanında daha güvenli ve etkili egzersizler yapılmasına olanak sağlar. Makine öğrenimi ve pose estimation tekniklerinin birleşimi, daha da gelişmiş analizler ve uygulamalar için büyük bir öneme sahiptir.



[Bu videoyu izleyin](https://drive.google.com/file/d/1OsIYYOlfW9zmPDxc9Xr-8n0XUQh2QEC_/view?usp=drive_link)


