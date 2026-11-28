# irrigation_weather

Open-Meteo'dan günlük hava tahminini çekip `/weather/forecast` topic'ine yayınlar.
Sorumlu: Kişi A.

## Çalıştırma
```bash
roslaunch irrigation_weather weather.launch
rostopic echo /weather/forecast     # başka bir terminalde
```

## Kullanılan değişkenler

| Open-Meteo alanı | Mesaj alanı | Birim | Neden gerekli |
|---|---|---|---|
| `precipitation_sum` | `precipitation_mm` | mm/gün | Etkili yağış ve sulama ertelemesi |
| `precipitation_probability_max` | `precipitation_probability_pct` | % | Tahmin güvenilirliği (Hafta 3'te kullanılabilir) |
| `et0_fao_evapotranspiration` | `et0_mm` | mm/gün | Bitki su tüketimi: ETc = Kc × ET₀ |
| `temperature_2m_max` | `temperature_max_c` | °C | Görselleştirme ve raporlama |

ET₀, Open-Meteo tarafından FAO-56 Penman-Monteith yöntemiyle hesaplanır; bu yüzden ayrıca
sıcaklık/rüzgâr/nemden ET₀ hesaplamamız gerekmez.

## Konum seçimi
Varsayılan konum **Konya Ovası (37.87° K, 32.49° D)**:
- Türkiye'nin en büyük tarım ovalarından biri ve yarı kurak iklimi nedeniyle sulamaya en çok
  ihtiyaç duyan bölgelerden; su tasarrufu senaryosunu göstermek için uygun.
- Yağışlı ve kurak günler arasındaki fark belirgin olduğundan "yağış bekleniyor → ertele"
  davranışı test edilebilir.

Konumu değiştirmek için `config/weather.yaml` içindeki `latitude` / `longitude` değerlerini düzenleyin.

## Çevrimdışı çalışma
Her başarılı istekten sonra yanıt `cache/last_forecast.json` dosyasına kaydedilir. İnternet yoksa
veya API hata verirse düğüm son kaydedilen tahmini `source: cache` olarak yayınlar.

## Testler
```bash
python3 -m pytest src/irrigation_weather -q
```
