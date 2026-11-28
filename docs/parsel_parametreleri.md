# Parsel Parametreleri ve Kaynakları

Sorumlu: Kişi D · Dosya: `src/irrigation_bringup/config/parcels.yaml`

Kaynak: Allen, R.G., Pereira, L.S., Raes, D., Smith, M. (1998). *Crop evapotranspiration —
Guidelines for computing crop water requirements.* FAO Irrigation and Drainage Paper 56, Roma.
https://www.fao.org/3/x0490e/x0490e00.htm

## 1. Bitki katsayısı Kc (FAO-56 Tablo 12, orta dönem)

| Parsel | Bitki | Kc ini | **Kc mid** | Kc end |
|---|---|---|---|---|
| parcel_1 | Domates | 0.6 | **1.15** | 0.70–0.90 |
| parcel_2 | Mısır (dane) | 0.3 | **1.20** | 0.35–0.60 |
| parcel_3 | Biber (dolmalık) | 0.6 | **1.05** | 0.90 |
| parcel_4 | Şeker pancarı | 0.35 | **1.20** | 0.70 |

İlk etapta en yüksek su tüketimini temsil ettiği için **Kc mid** kullanılıyor. Kc'nin gelişme
dönemine göre değişmesi (Kc eğrisi) ileriki etaplara bırakıldı.

> Not: Simülasyon tarihi Kasım–Aralık; bu bitkiler o dönemde tarlada değildir. Hava verisi
> gerçek, bitki dönemi varsayımsaldır. Raporda bu varsayım belirtilmeli.

## 2. Kök derinliği Zr ve tüketim oranı p (FAO-56 Tablo 22)

| Bitki | Zr aralığı [m] | Kullanılan Zr | p (= `mad`) |
|---|---|---|---|
| Domates | 0.7–1.5 | 0.7 | 0.40 |
| Mısır | 1.0–1.7 | 1.0 | 0.55 |
| Biber | 0.5–1.0 | 0.5 | 0.30 |
| Şeker pancarı | 0.7–1.2 | 0.7 | 0.55 |

Zr için aralığın **alt sınırı** seçildi: su bütçesi daha temkinli olur (daha erken sulama).

## 3. Toplam ve kolay alınabilir su (TAW, RAW)

FAO-56 Denklem 82–83:
- `TAW = 1000 × (θFC − θWP) × Zr` [mm]
- `RAW = p × TAW` [mm]

Kabul: **tın toprak**, `θFC − θWP = 0.14 m³/m³`.

| Parsel | TAW [mm] | RAW [mm] | Anlamı |
|---|---|---|---|
| parcel_1 domates | 1000×0.14×0.7 = **98** | 39.2 | ~39 mm açıkta sulama |
| parcel_2 mısır | 1000×0.14×1.0 = **140** | 77.0 | en seyrek sulanan |
| parcel_3 biber | 1000×0.14×0.5 = **70** | 21.0 | en sık sulanan (hassas) |
| parcel_4 ş. pancarı | 1000×0.14×0.7 = **98** | 53.9 | |

## 4. Hidrolik parametreler (proje varsayımı)

| Parametre | Değer | Gerekçe |
|---|---|---|
| Pompa kapasitesi | 120 L/dk | Toplam vana debisinin (255 L/dk) yarısından az → çizelgeleme zorunlu |
| Vana tam açık debileri | 45–80 L/dk | Parsel alanıyla orantılı |
| Sulama penceresi | 05:00–09:00 | Buharlaşma ve rüzgâr kaybı en düşük |
| Etkili yağış | P ≥ 5 mm ise 0.8×P | Küçük yağışlar yaprakta/yüzeyde buharlaşır kabulü |
