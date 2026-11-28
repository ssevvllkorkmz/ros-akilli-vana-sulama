# Hidrolik Çizelgeleme Tasarımı

Sorumlu: Kişi B · Paket: `irrigation_scheduler` · Durum: Hafta 1 tasarım, Hafta 2 uygulama

## 1. Problem
Tüm vanalar aynı anda açılırsa toplam debi pompanın verebileceğinden fazla olur, ana hatta
basınç düşer ve parsellere planlanan su ulaşmaz. Scheduler, `decision_node`'dan gelen parsel
ihtiyaçlarını **pompa kapasitesini hiçbir anda aşmayacak** biçimde zamana yayar.

## 2. Girdiler / Çıktılar

**Girdi** (`/irrigation/demand`, her parsel için):
`parcel_id`, `volume_liters` (V), `priority` (D/RAW), `postponed`

**Konfigürasyon** (`parcels.yaml`):
pompa kapasitesi `Q_pump` [L/dk], parsel başına `max_flow_lpm` (`Q_max`, vana 90°'de),
sulama penceresi `[t_start, t_end]` (ör. 05:00–09:00)

**Çıktı** (`/irrigation/plan`): slot listesi
`(parcel_id, angle_deg, start, duration, flow_lpm, planned_volume_liters)`

## 3. Kısıtlar
1. **Kapasite:** her t anında `Σ flow_i(t) ≤ Q_pump`
2. **Pencere:** her slot `[t_start, t_end]` içinde başlar ve biter
3. **Açı:** `angle ∈ {30°, 60°, 90°}`
4. **Hacim:** `flow × duration = V` (parsel başına tek slot)
5. Ertelenmiş (`postponed`) veya `V = 0` parsel planlanmaz

## 4. Debi modeli
İlk sürümde doğrusal kabul (Kişi C ile ortak):

| Açı | Debi |
|---|---|
| 30° | Q_max × 1/3 |
| 60° | Q_max × 2/3 |
| 90° | Q_max |

Gerçek kelebek vanalarda açı–debi ilişkisi doğrusal değildir; bu `flow_for_angle()` tek
fonksiyonda tutulduğu için Hafta 3'te C'nin modeliyle değiştirilebilir.

## 5. Algoritma: Öncelik sıralı açgözlü yerleştirme
Toplam sulama süresini kısaltmak için her parsel mümkün olan **en büyük açıyla**, mümkün olan
**en erken zamanda** başlatılır. Kritik parseller önce yerleştirildiği için en erken onlar sulanır.

```
make_plan(demands, parcels, Q_pump, t_start, t_end):
    istekler = [d ∈ demands | ¬d.postponed ∧ d.V > 0]
    istekler'i priority'ye göre büyükten küçüğe sırala
    slots = []
    for d in istekler:
        aday_zamanlar = {t_start} ∪ {s.bitiş | s ∈ slots}     # debinin boşaldığı anlar
        for t in sorted(aday_zamanlar):
            for açı in (90, 60, 30):
                q   = flow_for_angle(Q_max[d], açı)
                dur = d.V / q
                if t + dur ≤ t_end  ve  [t, t+dur) boyunca kullanılan_debi + q ≤ Q_pump:
                    slots.append(Slot(d, açı, t, dur, q, d.V)); sonraki d'ye geç
        sığmadıysa: uyarı logla (Hafta 3: kısmi sulama / ertesi güne aktarma)
    return slots
```

`[t, t+dur)` aralığındaki en yüksek kullanım, aralıkla çakışan slotların debileri toplanarak
bulunur. Kullanım yalnızca bir slot başlarken artabileceği için t ve aralık içinde başlayan
slotların başlangıç anlarını kontrol etmek yeterlidir.

**Karmaşıklık:** n parsel için O(n³), n ≤ 20 için önemsiz.

**Neden açgözlü?** Problem, kapasite kısıtlı bir çizelgeleme problemidir (genel hali NP-zor).
Parsel sayısı az olduğu ve öncelik sırası açıkça istendiği için açgözlü yaklaşım yeterli ve
açıklanabilir. Hafta 4'te istenirse küçük n için tam arama ile karşılaştırılabilir.

## 6. Elle çözülmüş örnek (parcels.yaml, Q_pump = 120 L/dk, pencere 05:00–09:00)

| Parsel | Q_max | V [L] | priority |
|---|---|---|---|
| parcel_3 | 45 | 2 700 | 1.60 |
| parcel_1 | 60 | 3 600 | 1.20 |
| parcel_2 | 80 | 4 800 | 1.05 |
| parcel_4 | 70 | 0 (ertelendi) | 0.90 |

1. **parcel_3**: 05:00'te 90° → 45 L/dk, 60 dk → 05:00–06:00 (kullanım 45)
2. **parcel_1**: 05:00'te 90° → 60 L/dk; 45+60 = 105 ≤ 120 ✓ → 60 dk → 05:00–06:00
3. **parcel_2**: 05:00'te 90° (80) → 185 ✗, 60° (53.3) → 158 ✗, 30° (26.7) → 131.7 ✗.
   06:00'da (diğerleri bitti) 90° → 80 L/dk, 60 dk → 06:00–07:00 ✓
4. **parcel_4**: ertelendi, planlanmaz.

Sonuç: tüm su 07:00'de verilmiş olur. Kapasite hiçbir anda 120 L/dk'yı aşmaz.

## 7. Test senaryoları (`test/test_planner.py`)
- Kapasite hiçbir anda aşılmıyor
- Ertelenen parsel planda yok
- Yüksek öncelikli parsel daha geç başlamıyor
- Planlanan hacim = istenen hacim
- Tüm slotlar pencere içinde ve açılar izinli kümede
- Yukarıdaki elle çözülmüş örnek birebir üretiliyor

## 8. Açık sorular (ekip toplantısında)
- Pencereye sığmayan parsel: kısmi sulama mı, ertesi güne aktarma mı?
- Plan gün içinde yeni tahminle güncellenirse çalışan slotlar ne olacak?
