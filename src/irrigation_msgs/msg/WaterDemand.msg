# Bir parselin hesaplanan su ihtiyacı (decision_node -> scheduler_node)
string parcel_id
float32 etc_mm              # bitki su tüketimi Kc*ET0 [mm]
float32 effective_rain_mm   # etkili yağış [mm]
float32 deficit_mm          # sanal su açığı [mm]
float32 raw_mm              # kolay alınabilir su eşiği RAW [mm]
float32 volume_liters       # verilmesi gereken su [L]
float32 priority            # deficit/RAW (büyük = acil)
bool postponed              # yağış beklendiği için ertelendi mi
string reason               # insan okunur açıklama
