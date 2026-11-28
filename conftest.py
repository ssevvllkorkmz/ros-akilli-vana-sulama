"""pytest'in ROS kurulu olmadan paket modüllerini bulabilmesi için src/<paket>/src yollarını ekler."""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
for path in glob.glob(os.path.join(ROOT, "src", "*", "src")):
    if path not in sys.path:
        sys.path.insert(0, path)
