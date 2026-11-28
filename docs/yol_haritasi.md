# Yol Haritası — İlk Etap (4 Hafta)

**Proje:** Tarımsal Su Yönetimi İçin ROS Tabanlı Dağıtık ve Kestirimsel Akıllı Vana Kontrol Sistemi
**Kapsam kararı (28 Kasım 2026):** Toprak nemi sensörü/simülasyonu kapsamdan çıkarıldı.
Sulama kararı **yalnızca meteorolojik kestirime** (Open-Meteo yağış + referans evapotranspirasyon ET₀)
ve parsellerin bitki katsayısına (Kc) dayanır. Parsel su durumu ölçülmez, hava verisinden
**sanal su bütçesi** (FAO-56 "checkbook" yöntemi) ile hesaplanır.

**İlk etap sonu hedefi (MVP):** `roslaunch irrigation_bringup demo.launch` tek komutuyla:
Open-Meteo tahmini → parsel bazlı su ihtiyacı → pompa kapasitesine uygun sulama sırası →
uç düğümlerdeki vanaların 30° / 60° / 90° açılara gelmesi → RViz'de canlı dijital ikiz →
iletişim kopunca vanaların otomatik kapanması.

---

## Takvim

| Hafta | Tarih | Tema | Tag |
|---|---|---|---|
| 1 | 28 Kas – 4 Ara | Altyapı, mesaj sözleşmesi, iskelet | `v0.1-hafta1` |
| 2 | 5 – 11 Ara | Bileşenler tek başına çalışıyor | `v0.2-hafta2` |
| 3 | 12 – 18 Ara | Uçtan uca entegrasyon | `v0.3-hafta3` |
| 4 | 19 – 25 Ara | Fail-safe, sağlamlaştırma, MVP | `v0.4-mvp` |

## Roller

| Kişi | Rol | Paketler | Reviewer |
|---|---|---|---|
| A | Meteorolojik kestirim & karar | `irrigation_weather`, `irrigation_decision` | B |
| B | Hidrolik çizelgeleme | `irrigation_scheduler` | A |
| C | Uç düğüm & vana robotiği | `irrigation_description`, `irrigation_gazebo`, `valve_edge_node` | D |
| D | Dijital ikiz, fail-safe, entegrasyon & CI | `irrigation_viz`, `irrigation_bringup`, `.github/`, `docker/` | C |

> Ekip isimlerini buraya yazın: A = …, B = …, C = …, D = …

---

## Karar modeli (nemsiz)

Her parsel *p* ve gün *t* için:

- Bitki su tüketimi: `ETc = Kc × ET₀`
- Etkili yağış: `Pe = 0.8 × P` (P ≥ 5 mm ise), aksi halde 0 *(parametre)*
- Sanal açık (deficit): `D_t = clip(D_{t-1} + ETc − Pe − I_{t-1}, 0, TAW)`
- Sulama tetikleyici: `D_t ≥ RAW` (`RAW = MAD × TAW`)
- Erteleme: önümüzdeki 48 saatte beklenen etkili yağış açığın ≥ %70'ini karşılıyorsa sulama ertelenir
- Hacim: `V [L] = D [mm] × alan [m²]` (1 mm × 1 m² = 1 L)
- Öncelik: `D / RAW` oranı (büyük olan önce)

Scheduler, aynı anda açık vanaların toplam debisi **pompa kapasitesini** aşmayacak şekilde
öncelik sırasına göre slot yerleştirir; açı (30/60/90°) hacim ve zaman penceresine göre seçilir.

---

## Hafta 1 — Altyapı ve Arayüz Sözleşmesi
**En kritik çıktı:** `irrigation_msgs` donar; sonrasında herkes bağımsız çalışır.

- **Ortak:** Mesajlar ve topic listesi üzerinde anlaşma (`docs/mimari.md`), PR ile onay
- **A:** Open-Meteo istemcisi (çevrimdışı önbellekli) + birim testleri; `weather_node` taslağı
- **B:** Çizelgeleme algoritma taslağı (`docs/scheduler_tasarim.md`), `scheduler_node` iskeleti
- **C:** Vana URDF/xacro (1-DOF revolute 0–90°), RViz'de joint slider ile test
- **D:** Docker ortamı, CI (catkin_make + pytest), PR/Issue şablonları, `parcels.yaml`

✅ Teslim: CI yeşil, mesajlar tanımlı, vana modeli RViz'de dönüyor, hava verisi çekiliyor, hafta raporu.

## Hafta 2 — Bileşenler Tek Başına Çalışıyor
- **A:** `weather_node` periyodik `WeatherForecast` yayını; `decision_node` su bütçesi + `WaterDemand` (sahte forecast ile test)
- **B:** `scheduler_node` sahte `WaterDemand` → `IrrigationPlan`; kapasite kısıtı birim testleri
- **C:** Gazebo'da vana + `JointPositionController`; `valve_edge_node` `ValveCommand` → kontrolcü
- **D:** RViz marker düğümü (parsel kutuları, vana açısı, debi metni); `demo.launch` ilk sürüm

✅ Teslim: her düğüm tek başına çalışıyor, her kişiden ekran görüntüsü/GIF.

## Hafta 3 — Uçtan Uca Entegrasyon
- **A:** Gerçek Open-Meteo verisiyle karar; yağış ertelemesi senaryosu
- **B:** Plan zamanlayıcısı: slot zamanı gelince ilgili namespace'e `ValveCommand`
- **C:** Açı → debi modeli, `ValveState` (anlık debi + verilen toplam litre); 4 uç düğüm `/parcel_N/` namespace'lerinde
- **D:** Dijital ikizde plan / gerçekleşen karşılaştırması; tüm sistem tek launch

✅ Teslim: tam döngü çalışıyor, demo videosu.

## Hafta 4 — Fail-Safe ve MVP
- **D (lider) + C:** Heartbeat; uç düğüm `timeout` süresince heartbeat alamazsa vanayı 0°'ye kapatır, `mode=FAILSAFE`
- **A:** API hatası/çevrimdışı durumda son geçerli tahminle güvenli çalışma
- **B:** Senaryo testleri (kuru hafta, yağışlı gün, kapasite aşımı)
- **C:** Bir uç düğümü ayrı Docker konteynerinde (`ROS_MASTER_URI` ile) çalıştırma — dağıtıklık kanıtı
- **Ortak:** README kurulum/çalıştırma, `v0.4-mvp` tag, ilk etap raporu

✅ Teslim: MVP demosu, fail-safe test videosu, ilk etap raporu.

---

## Haftalık teslim kontrol listesi (hoca için)
- [ ] O haftanın Milestone'undaki Issue'lar kapandı (PR linkli)
- [ ] CI yeşil
- [ ] `docs/haftalik/hafta-0N.md` eklendi (kim ne yaptı + görsel)
- [ ] Hafta tag'i atıldı
