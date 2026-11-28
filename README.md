# Tarımsal Su Yönetimi İçin ROS Tabanlı Dağıtık ve Kestirimsel Akıllı Vana Kontrol Sistemi

BIL417 Robot Programlama dersi projesi. ROS Noetic + Gazebo tabanlı, meteorolojik kestirime dayalı
dağıtık hassas sulama sistemi. Merkezi düğüm Open-Meteo yağış ve ET₀ tahminlerinden parsel bazlı su
ihtiyacını hesaplar, pompa kapasitesine uygun sulama sırası planlar; parsellerdeki uç düğümler 1-DOF
motorlu vanaları 30° / 60° / 90° açılara getirerek debiyi ayarlar. Durum RViz'de dijital ikiz olarak
izlenir; iletişim koparsa vanalar otomatik kapanır.

- Yol haritası: [`docs/yol_haritasi.md`](docs/yol_haritasi.md)
- Bu haftanın görevleri: [`docs/hafta1_gorevler.md`](docs/hafta1_gorevler.md)
- Mimari ve topic sözleşmesi: [`docs/mimari.md`](docs/mimari.md)
- Katkı kuralları: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Haftalık raporlar: [`docs/haftalik/`](docs/haftalik/)

## Paketler

| Paket | Sorumlu | Açıklama |
|---|---|---|
| `irrigation_msgs` | Ortak | Özel mesaj tanımları |
| `irrigation_weather` | A | Open-Meteo istemcisi, `weather_node` |
| `irrigation_decision` | A | Sanal su bütçesi, `decision_node` |
| `irrigation_scheduler` | B | Hidrolik çizelgeleme, `scheduler_node` |
| `irrigation_description` | C | Vana URDF/xacro modeli |
| `irrigation_gazebo` | C | Gazebo dünyası, kontrolcü ayarları |
| `valve_edge_node` | C | Uç düğüm vana sürücüsü + fail-safe |
| `irrigation_viz` | D | RViz dijital ikiz |
| `irrigation_bringup` | D | Launch dosyaları, parsel konfigürasyonu |

## 1. İlk Kurulum (sadece ilk seferde)

Ubuntu 20.04 + ROS Noetic gerekir.

```bash
sudo apt install -y python3-pytest ros-noetic-ros-control ros-noetic-ros-controllers \
     ros-noetic-gazebo-ros-control ros-noetic-joint-state-publisher-gui
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone https://github.com/ssevvllkorkmz/ros-akilli-vana-sulama.git akilli_vana
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc && source ~/.bashrc
```

Alternatif: Docker ile aynı ortam → `./docker/run.sh` (GUI için Linux'ta `xhost +local:docker`).

## 2. Çalıştırma ve Test

```bash
python3 -m pytest ~/catkin_ws/src/akilli_vana/src -q        # birim testleri
roslaunch irrigation_description view_valve.launch          # vana modeli, slider ile 0–90°
roslaunch irrigation_weather weather.launch                 # Open-Meteo tahmini -> /weather/forecast
roslaunch irrigation_bringup demo.launch                    # tüm sistem iskeleti + RViz
```

Bir betiğin adı değiştiyse veya silindiyse eski derleme kalıntıları hata verebilir:
`cd ~/catkin_ws && rm -rf build devel && catkin_make`

## 3. Günlük Çalışma Akışı

Hocamız haftalık ilerlemeyi repodan takip ettiği için herkes kendi işini **kendi dalında** yapar ve
**Pull Request** ile `main`'e ekler (ayrıntılar: [`CONTRIBUTING.md`](CONTRIBUTING.md)).

```bash
cd ~/catkin_ws/src/akilli_vana
git checkout main && git pull origin main            # 1. güncel kodu al
git checkout -b feature/a-open-meteo-testleri        # 2. kendi dalını aç
# ... kod yaz, test et ...
git add .
git commit -m "feat(weather): yağış eşiği testleri eklendi"   # 3. kaydet
git push -u origin feature/a-open-meteo-testleri     # 4. gönder, GitHub'da PR aç
```

> **Önemli:** İlk `git push`'ta GitHub şifreniz çalışmaz. **Settings > Developer settings >
> Personal access tokens > Tokens (classic)** yolundan `repo` yetkili bir token üretip şifre yerine
> onu yapıştırın.
