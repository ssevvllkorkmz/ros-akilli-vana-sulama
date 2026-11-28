# Sistem Mimarisi

```
                ┌──────────────────────── ROS Master (merkez) ────────────────────────┐
 Open-Meteo ──► │ weather_node ──/weather/forecast──► decision_node ──/irrigation/demand──►│
   (HTTPS)      │                                                     scheduler_node       │
                │                       /irrigation/plan ◄──────────────┘   │              │
                │  heartbeat (merkez) ──/irrigation/heartbeat──┐            │              │
                └──────────────────────────────────────────────┼────────────┼──────────────┘
                                                               ▼            ▼ /parcel_N/valve/command
                   ┌──────── Uç düğüm (Edge Node) parcel_N ─────────────────────────┐
                   │ valve_edge_node ──► /parcel_N/valve_position_controller/command │──► Gazebo vana (1-DOF)
                   │        │  fail-safe: heartbeat yoksa 0°                          │
                   │        └──► /parcel_N/valve/state                                │
                   └──────────────────────────────────────────────────────────────────┘
                                         │
                              valve_viz_node ──► /irrigation/markers ──► RViz (dijital ikiz)
```

## Topic sözleşmesi

| Topic | Tip | Yayıncı | Dinleyici | Sıklık |
|---|---|---|---|---|
| `/weather/forecast` | `irrigation_msgs/WeatherForecast` | weather_node | decision_node | 1 saatte 1 (latched) |
| `/irrigation/demand` | `irrigation_msgs/WaterDemandArray` | decision_node | scheduler_node, viz | tahmin geldikçe |
| `/irrigation/plan` | `irrigation_msgs/IrrigationPlan` | scheduler_node | viz | plan değiştikçe (latched) |
| `/parcel_N/valve/command` | `irrigation_msgs/ValveCommand` | scheduler_node | valve_edge_node | olay bazlı |
| `/parcel_N/valve/state` | `irrigation_msgs/ValveState` | valve_edge_node | viz, scheduler | 5 Hz |
| `/irrigation/heartbeat` | `irrigation_msgs/Heartbeat` | scheduler_node | tüm uç düğümler | 2 Hz |
| `/irrigation/markers` | `visualization_msgs/MarkerArray` | valve_viz_node | RViz | 2 Hz |

## Parametreler
- Parsel tanımları: `src/irrigation_bringup/config/parcels.yaml`
- Konum ve API: `src/irrigation_weather/config/weather.yaml`

## Değişiklik kuralı
`irrigation_msgs` 1. hafta sonunda donar. Değişiklik yalnızca 4 kişinin onayladığı bir PR ile yapılır.
