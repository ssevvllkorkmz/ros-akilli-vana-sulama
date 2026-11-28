#!/usr/bin/env bash
# Vana modelini xacro'dan URDF'e çevirir ve check_urdf ile doğrular.
# Kullanım: bash src/irrigation_description/scripts/check_valve.sh [prefix]
set -e
PREFIX="${1:-parcel_1_}"
PKG_DIR="$(rospack find irrigation_description)"
OUT="/tmp/smart_valve.urdf"

xacro "$PKG_DIR/urdf/single_valve.urdf.xacro" prefix:="$PREFIX" namespace:="/parcel_1" > "$OUT"
echo "URDF üretildi: $OUT"
check_urdf "$OUT"

echo
echo "Eklem limitleri:"
grep -A1 "<limit" "$OUT" | head -2
