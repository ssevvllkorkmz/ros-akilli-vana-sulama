# Uç düğüm -> merkez/RViz vana durumu
uint8 MODE_NORMAL = 0
uint8 MODE_FAILSAFE = 1

Header header
string parcel_id
float32 target_angle_deg
float32 current_angle_deg
float32 flow_lpm            # anlık debi [L/dk]
float32 delivered_liters    # bu sulamada verilen toplam su [L]
uint8 mode
