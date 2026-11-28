# Hafta 1 Görevleri (28 Kas – 4 Ara) — GitHub Issue'larına kopyalayın

Milestone: **Hafta 1** · Etiket: `gorev` · Her görev ayrı dal + PR.

İskelet (bu ilk commit) hazır; aşağıdakiler her kişinin bu hafta **kendisinin tamamlayıp PR açacağı** işler.

### Ortak
- [ ] **#1 Mesaj sözleşmesini onayla** — `src/irrigation_msgs/msg/*.msg` ve `docs/mimari.md` topic tablosunu birlikte gözden geçirin, gerekirse düzeltin. 4 onayla birleştirin → mesajlar donar.
- [ ] **#2 Ekip bilgileri** — `docs/yol_haritasi.md` rol tablosuna isimleri yazın.

### Kişi A — Meteorolojik kestirim
- [ ] **#3 Open-Meteo istemcisini kendi makinende doğrula** — `rosrun irrigation_weather weather_node.py` → `rostopic echo /weather/forecast`; ekran görüntüsü PR'a.
- [ ] **#4 Konum seçimi** — `config/weather.yaml` koordinatlarını projenin tarla konumuna göre güncelle, gerekçesini README'ye yaz.
- [ ] **#5 Su bütçesi testlerini önce yaz (TDD)** — `irrigation_decision/test/test_water_balance.py`: effective_rain ve update_deficit için beklenen değerler (uygulama Hafta 2).

### Kişi B — Hidrolik çizelgeleme
- [ ] **#6 Çizelgeleme tasarım dokümanı** — `docs/scheduler_tasarim.md`: problem tanımı, kısıtlar (pompa kapasitesi, sulama penceresi), algoritma (öncelik kuyruğu + açgözlü), sözde kod, 4 parsellik elle çözülmüş örnek.
- [ ] **#7 `planner.py` için test senaryoları** — kapasite aşımı ve öncelik sırası testleri (uygulama Hafta 2).

### Kişi C — Vana robotiği
- [ ] **#8 Vana modelini RViz'de doğrula** — `roslaunch irrigation_description view_valve.launch`; 0°/30°/60°/90° ekran görüntüleri. `check_urdf` çıktısı PR'a.
- [ ] **#9 Gazebo'da tek vana** (erken başlangıç) — `roslaunch irrigation_gazebo field.launch` ile vananın yüklendiğini ve kontrolcünün başladığını doğrula.

### Kişi D — Altyapı, dijital ikiz, fail-safe
- [ ] **#10 Docker + CI** — `./docker/run.sh` ile herkesin ortamı aynı; GitHub Actions ilk koşuda yeşil. `main` için branch protection (PR + 1 onay + CI) aç.
- [ ] **#11 Parsel konfigürasyonu** — `irrigation_bringup/config/parcels.yaml` değerlerini (Kc, TAW, MAD) FAO-56 tablolarından kaynakla doğrula.
- [ ] **#12 İskelet demo** — `roslaunch irrigation_bringup demo.launch` ile RViz'de 4 parsel kutusu görünüyor.

### Cuma teslimi
- [ ] `docs/haftalik/hafta-01.md` doldurulur, `v0.1-hafta1` tag'i atılır.
