#!/usr/bin/env bash
# Geliştirme konteynerini kurar ve başlatır. Repo /ws/src/ros-akilli-vana-sulama altına bağlanır.
set -e
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
IMAGE=akilli-vana:noetic

docker build -t "$IMAGE" "$REPO_DIR/docker"

docker run -it --rm \
  --net=host \
  -e DISPLAY="$DISPLAY" \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$REPO_DIR":/ws/src/ros-akilli-vana-sulama \
  --name akilli-vana \
  "$IMAGE" bash
