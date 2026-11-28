# Open-Meteo günlük tahmini (weather_node -> decision_node)
Header header
string source               # "open-meteo" veya "cache"
float64 latitude
float64 longitude
string[] dates              # ISO tarih, ör. "2026-11-28" (yerel saat dilimi)
float32[] precipitation_mm  # günlük toplam yağış [mm]
float32[] precipitation_probability_pct  # günlük maks. yağış olasılığı [%]
float32[] et0_mm            # FAO-56 referans evapotranspirasyon [mm/gün]
float32[] temperature_max_c # günlük maks. sıcaklık [°C]
