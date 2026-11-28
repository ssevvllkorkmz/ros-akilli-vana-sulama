FROM osrf/ros:noetic-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3-pytest python3-requests python3-yaml python3-catkin-tools \
        ros-noetic-ros-control ros-noetic-ros-controllers \
        ros-noetic-gazebo-ros-control ros-noetic-joint-state-publisher-gui \
        ros-noetic-xacro git \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /ws/src
WORKDIR /ws
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc && \
    echo "[ -f /ws/devel/setup.bash ] && source /ws/devel/setup.bash" >> /root/.bashrc

CMD ["bash"]
