# 도커를 활용한 자율주행 로봇 시뮬레이션 자료

## Docker 설치 ( [Link](https://docs.docker.com/engine/install/ubuntu/) )

#### - apt repository 설정 -
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

#### - 도커 다운로드 -
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 프로젝트 Git Clone
```
cd ~
git clone https://github.com/Jabee7531/nav2_simulation_with_docker.git
```

## Docker 사용법

#### Dockerfile 빌드
```
cd ~/nav2_simulation_with_docker
sudo docker build --progress=plain -t nav2:humble ./
```

#### Docker 이미지 실행
```
sudo docker run -it -d --network=host --privileged --env="DISPLAY=$DISPLAY" --volume="${XAUTHORITY}:/root/.Xauthority" --volume="/home/$USER/nav2_simulation_with_docker:/nav2_simulation_with_docker" --name tb3 nav2:humble
```

#### Docker 프로세스 확인
```
sudo docker ps -a
```

#### Docker 프로세스 터미널 접근
```
sudo docker exec -it tb3 bash
```

#### Docker 작업 후 이미지 업데이트
```
docker commit tb3 updated_nav2
```

#### Docker 이미지 실행
```
sudo docker run -it -d --name updated_tb3 updated_nav2
```

#### Docker 프로세스 종료
```
# 종료
docker stop tb3
```
or
```
# 강제 종료
docker kill updated_tb3
```

#### Docker 프로세스 삭제
```
docker rm tb3
docker rm updated_tb3
```

## Ros2 실습
#### Docker 이미지 실행
```
sudo docker run -it -d --network=host --privileged --env="DISPLAY=$DISPLAY" --volume="${XAUTHORITY}:/root/.Xauthority" --volume="/home/$USER/nav2_simulation_with_docker:/nav2_simulation_with_docker" --name tb3 nav2:humble
```

#### Docker 프로세스 터미널 접근
```
sudo docker exec -it tb3 bash
```

#### 터틀봇 시뮬레이션 실행
```
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```
#### 키보드 조작
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

#### URDF 수정 (옵션)
```
cd /opt/ros/humble/share/nav2_bringup/urdf
# 원본 파일 백업
cp turtlebot3_waffle.urdf turtlebot3_waffle_backup.urdf
# URDF 수정
gedit turtlebot3_waffle.urdf
# 수정
```

#### SDF 수정 (옵션)
```
cd /opt/ros/humble/share/nav2_bringup/worlds
# 원본 파일 백업
cp waffle.model waffle_backup.model
# SDF 수정
gedit waffle.model
# 수정
```

#### Cartographer 실행
```
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

#### Cartographer 지도 저장
```
ros2 run nav2_map_server map_saver_cli --free 0.196 -t /map -f /nav2_simulation_with_docker/my_map
```

#### Cartographer 지도 불러오기
```
ros2 service call /map_server/load_map nav2_msgs/srv/LoadMap "{map_url : /nav2_simulation_with_docker/my_map.yaml}"
```


#### Ros2 examples 패키지 빌드
```
cd /nav2_simulation_with_docker

colcon build --symlink-install
```

#### Ros2 cmd_vel_example 실행
```
source /nav2_simulation_with_docker/install/local_setup.bash
ros2 run examples cmd_vel_example
```
```
# Cmd Vel Scale 조회 & 수정
ros2 param get /cmd_vel_example linear_scale
ros2 param get /cmd_vel_example angular_scale
ros2 param set /cmd_vel_example linear_scale 0.8
ros2 param set /cmd_vel_example angular_scale 1.5
```

#### Ros2 scan_example 실행
```
source /nav2_simulation_with_docker/install/local_setup.bash
ros2 run examples scan_example
```
```
# Obstacle Detect Range 조회 & 수정
ros2 param get /scan_example obstacle_detect_range
ros2 param set /scan_example obstacle_detect_range 0.7
```

#### Ros2 image_example 실행
```
source /nav2_simulation_with_docker/install/local_setup.bash
ros2 run examples image_example
```

#### Ros2 새로운 패키지 만들기
```
cd /nav2_simulation_with_docker/src
ros2 pkg create --build-type ament_python new_packages

cd /nav2_simulation_with_docker/src/new_packages/new_packages && gedit new_example.py
# 작성
```


#### entry_points 설정
```
gedit /nav2_simulation_with_docker/src/new_packages/setup.py

# 아래 쪽 entry_points 수정
entry_points={
        'console_scripts': [
                'new_example_node = new_packages.new_example:main',
        ],
},
```

#### Ros2 examples 패키지 빌드
```
cd /nav2_simulation_with_docker

colcon build --symlink-install --packages-select new_packages
```

#### Ros2 new_packages 패키지 실행
```
source /nav2_simulation_with_docker/install/local_setup.bash
ros2 run examples new_example_node
```
