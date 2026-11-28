# Akıllı Vana Modeli

Sorumlu: Kişi C · Paketler: `irrigation_description`, `irrigation_gazebo`, `valve_edge_node`

## 1. Mekanik model
Motorlu **kelebek vana**: boru içindeki disk, dikey eksen etrafında döner.
Tek serbestlik dereceli (1-DOF) bir robot kolu gibi modellenmiştir.

| Link | Açıklama |
|---|---|
| `<prefix>valve_body` | Sabit gövde: boru (Ø100 mm, 400 mm), vana gövdesi, motor kutusu |
| `<prefix>valve_disc` | Hareketli disk + motorun üstündeki kırmızı açı göstergesi |

| Eklem | Tip | Eksen | Limit | Effort | Hız |
|---|---|---|---|---|---|
| `<prefix>valve_joint` | revolute | z | 0 – π/2 rad (0–90°) | 20 N·m | 0.8 rad/s |

- **0° = kapalı**, **90° = tam açık**
- 0°'den 90°'ye dönüş ≈ 2 s (0.8 rad/s hız limiti); gerçek vana motorlarına yakın
- `prefix` parametresi sayesinde 4 parsel aynı RViz/TF ağacında çakışmadan gösterilir
  (`parcel_1_valve_joint`, `parcel_2_valve_joint`, ...)

## 2. Kontrol
- `transmission_interface/SimpleTransmission` + `EffortJointInterface`
- Gazebo'da `gazebo_ros_control` eklentisi, her parsel kendi namespace'inde (`/parcel_N`)
- Kontrolcü: `effort_controllers/JointPositionController`, PID `p=40, i=0.5, d=2`
  (Hafta 2'de Gazebo'da adım yanıtı ile ayarlanacak: aşım < %5, oturma < 3 s hedefi)

Komut zinciri:
```
/parcel_N/valve/command (ValveCommand, derece)
   └─ valve_edge_node: açıyı doğrula, dereceyi radyana çevir
        └─ /parcel_N/valve_position_controller/command (Float64, rad) ─► Gazebo eklemi
```

## 3. İzinli açılar
Sistem yalnızca **0°, 30°, 60°, 90°** kabul eder (`valve_logic.validate_angle`).
Karar: izinli olmayan açı **reddedilir** (ValueError), en yakına yuvarlanmaz. Neden: yanlış
komut sessizce düzeltilirse scheduler'ın planladığı debi ile gerçekleşen debi farklı olur ve
hata gözden kaçar. Reddedilen komut loglanır, vana önceki konumunda kalır.

## 4. Debi modeli (Hafta 3)
İlk sürüm doğrusal: `Q = Q_max × açı / 90` (Kişi B'nin `flow_for_angle` ile aynı).

Gerçek kelebek vanalarda karakteristik doğrusal değildir: küçük açılarda debi azdır, 60°'den
sonra hızla artar. Hafta 3'te istenirse eşit yüzdeli yaklaşık bir model denenebilir; değişiklik
tek fonksiyonda olduğu için scheduler ile birlikte güncellenir.

## 5. Doğrulama
```bash
bash src/irrigation_description/scripts/check_valve.sh       # xacro -> URDF -> check_urdf
roslaunch irrigation_description view_valve.launch           # slider ile 0/30/60/90°
roslaunch irrigation_gazebo field.launch                     # Gazebo'da tek vana
rostopic pub -1 /parcel_1/valve_position_controller/command std_msgs/Float64 "data: 1.047"  # 60°
```
