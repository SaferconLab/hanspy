# HansRobot Library Python

Python 版本的 HansRobot 控制库，提供对 HansRobot 机器人的完整控制接口。
支持使用原始CPS接口或高级RobotController封装接口。

## 项目概述

HansRobot Library Python 是一套完整的机器人控制系统库，旨在为HansRobot系列机器人提供易于使用的Python接口。该库采用分层架构设计，包含底层CPS接口封装、高级机器人控制器封装、TCP通信控制器架构以及深度相机集成等功能模块。

## 项目结构

```
HansRobot_Library_Python/
├── README.md          # 项目说明文档
├── docs/              # 项目文档
│   ├── chapter_1_overview.md         # 概述
│   ├── chapter_2_environment_setup.md # 环境设置
│   ├── chapter_3_available_interfaces_part1.md # 可用接口(第一部分)
│   ├── chapter_3_available_interfaces_part2.md # 可用接口(第二部分)
│   ├── chapter_3_available_interfaces_part3.md # 可用接口(第三部分)
│   ├── chapter_3_available_interfaces_part4.md # 可用接口(第四部分)
│   ├── chapter_3_available_interfaces_part5.md # 可用接口(第五部分)
│   ├── chapter_3_available_interfaces_part6.md # 可用接口(第六部分)
│   └── HansRobot错误说明及状态机文档.md # 错误说明和状态机文档
├── lib/               # 核心库文件
│   ├── __init__.py
│   ├── exceptions.py   # 自定义异常类
│   ├── robot_controller.py  # 机器人控制器
│   └── status_monitor.py    # 状态监控器
├── wrapper/           # 包装器文件
│   ├── __init__.py
│   └── CPS_wrapper.py   # CPS包装器
├── controller_clinet/ # 控制器客户端
│   ├── __init__.py
│   ├── client.py       # 客户端实现
│   ├── protocol.py     # 协议定义
│   └── requirements.txt # 客户端依赖
├── controller_server/ # 控制器服务器
│   ├── __init__.py
│   ├── main.py         # 服务器主程序
│   ├── config.json     # 服务器配置文件
│   ├── server/         # 服务器模块
│   │   ├── __init__.py
│   │   └── tcp_server.py # TCP服务器实现
│   └── controller/     # 控制器模块
│       ├── __init__.py
│       └── session_manager.py # 会话管理器
├── realsense_demo/    # Intel RealSense 深度相机演示
│   ├── readme.md       # 演示说明
│   └── ...             # 多个深度相机示例
├── test_robot.py      # 测试脚本
└── test_import.py     # 导入测试脚本
```

## 功能特性

### 1. 核心控制功能

- **完整的机器人控制接口**：提供对HansRobot机器人的完整控制能力
- **状态监控和错误处理机制**：实时监控机器人状态，提供完善的错误处理
- **详细的文档支持**：包含完整的使用文档和技术说明
- **易于使用的 Python API**：简洁直观的API设计，降低学习成本

### 2. 高级封装特性

- **自动状态检查和等待机制**：自动检查机器人状态，确保操作安全性
- **连接、使能、去使能的封装处理**：简化机器人控制流程
- **运动指令的阻塞式执行**：自动等待运动完成，避免并发问题
- **统一的异常处理机制**：提供标准化的错误处理方式
- **便捷的位置获取和设置接口**：简化位置信息的读取和设置

### 3. 控制器架构支持

- **TCP通信协议**：基于TCP的可靠通信机制
- **机器人和夹爪设备分离控制**：支持多设备协同控制
- **会话管理**：维护客户端连接状态和会话信息
- **安全的连接管理**：提供连接状态检查和自动重连机制

### 4. 深度相机集成支持

- **Intel RealSense SDK 集成**：支持多种深度相机型号
- **多种深度相机示例**：包含基础深度流、图像渲染、深度对齐等示例
- **点云可视化功能**：支持点云数据的实时可视化
- **多相机物体尺寸测量**：支持多相机协同测量功能
- **以太网远程传输**：支持深度数据的网络传输

## 安装说明

```bash
# 克隆仓库
git clone <repository-url>

# 进入项目目录
cd HansRobot_Library_Python

# 安装依赖（如果有的话）
pip install -r requirements.txt
```

## 使用示例

### 基本使用

```python
from lib.robot_controller import RobotController

# 创建机器人控制器实例
robot = RobotController(box_id=0, robot_id=0)

# 连接机器人
robot.connect("192.168.31.88", 10003)

# 使能机器人
robot.enable()

# 执行关节运动
robot.move_j(
    points=[0, 0, 0, 0, 0, 0],
    raw_acs_points=[0, 0, 90, 0, 90, 0],
    speed=30.0,
    acc=30.0
)

# 去使能并断开连接
robot.disable()
robot.disconnect()
```

### 使用原始CPS接口

```python
from wrapper.CPS_wrapper import CPSClient

# 创建CPS客户端实例
cps = CPSClient()

# 连接机器人
ret = cps.HRIF_Connect(0, "192.168.31.88", 10003)

# 使能机器人
ret = cps.HRIF_GrpEnable(0, 0)

# 执行关节运动
ret = cps.HRIF_MoveJ(0, 0, [0, 0, 0, 0, 0, 0], [0, 0, 90, 0, 90, 0], 
                     "TCP", "Base", 30.0, 30.0, 10.0, 1, 0, 0, 0, "0")

# 去使能并断开连接
cps.HRIF_GrpDisable(0, 0)
cps.HRIF_DisConnect(0)
```

### 使用控制器客户端

```python
from controller_clinet.client import ControllerClient

# 创建控制器客户端实例
client = ControllerClient(host="192.168.31.88", port=8888)

# 连接服务器
if client.connect():
    # 连接机器人
    if client.connect_robot():
        # 使能机器人
        if client.enable_robot():
            # 执行关节运动
            client.move_j(
                points=[0, 0, 0, 0, 0, 0],
                raw_acs_points=[0, 0, 90, 0, 90, 0],
                speed=30.0,
                acc=30.0
            )
            
            # 去使能并断开连接
            client.disable_robot()
            client.disconnect_robot()
        client.disconnect()
```

### 深度相机使用示例

```python
import cv2
import numpy as np
from realsense_demo.opencv_viewer_example import RealSenseViewer

# 创建深度相机查看器
viewer = RealSenseViewer()

# 启动相机
viewer.start()

# 实时显示深度和彩色图像
while True:
    # 获取深度和彩色帧
    depth_frame, color_frame = viewer.get_frames()
    
    # 显示图像
    viewer.display(color_frame, depth_frame)
    
    # 按ESC键退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 停止相机
viewer.stop()
```

## 控制器架构详解

### 1. 控制器服务器 (controller_server)

控制器服务器运行在控制机A上，负责接收来自上位机B的指令并控制机械臂和夹爪设备。

#### 主要功能：
- **TCP服务器监听**：监听来自客户端的连接请求
- **命令解析**：解析客户端发送的各种控制命令
- **设备控制**：控制机器人和夹爪设备的连接、使能、运动等操作
- **状态管理**：维护设备连接状态和会话信息
- **日志记录**：记录服务器运行状态和错误信息

#### 配置文件 (config.json)：
```json
{
    "server": {
        "host": "0.0.0.0",
        "port": 8888,
        "max_connections": 10
    },
    "robot": {
        "ip": "192.168.31.88",
        "port": 10003,
        "box_id": 0,
        "robot_id": 0
    },
    "gripper": {
        "device_index": 0
    },
    "logging": {
        "level": "INFO",
        "file": "controller_server.log"
    }
}
```

### 2. 控制器客户端 (controller_clinet)

控制器客户端通过TCP协议与服务器通信，提供统一的机器人控制接口。

#### 主要功能：
- **TCP连接管理**：建立和维护与服务器的TCP连接
- **命令发送**：将控制命令发送到服务器
- **响应处理**：处理服务器返回的响应消息
- **状态跟踪**：跟踪客户端连接状态和设备连接状态
- **异常处理**：处理网络异常和设备异常

#### 支持的命令类型：
- **机器人连接相关**：连接/断开机器人
- **机器人使能相关**：使能/去使能机器人
- **运动控制**：关节运动、直线运动、姿态运动等
- **位置获取**：获取当前位置信息
- **速度控制**：设置速度比、获取当前速度比
- **安全控制**：停止、复位、上电、断电等
- **夹爪控制**：连接/断开夹爪，设置夹爪参数等

### 3. 会话管理器 (session_manager)

会话管理器负责管理客户端连接状态和会话信息。

#### 主要功能：
- **会话创建**：为每个新连接创建会话
- **状态跟踪**：跟踪机器人和夹爪的连接状态
- **会话清理**：自动清理过期会话
- **并发控制**：确保多客户端访问的安全性

## 深度相机集成

### 1. 支持的深度相机型号
- Intel RealSense D400系列
- Intel RealSense L515系列
- 其他兼容的深度相机设备

### 2. 主要功能
- **深度图像采集**：实时采集深度图像数据
- **彩色图像采集**：采集彩色图像数据
- **图像对齐**：将深度图像与彩色图像对齐
- **点云生成**：从深度数据生成3D点云
- **物体测量**：基于深度数据进行物体尺寸测量
- **实时可视化**：提供点云和图像的实时显示

### 3. 示例功能
- 基础深度流显示
- OpenCV 图像渲染
- 深度图像对齐
- 高级模式控制
- 多相机物体尺寸测量
- 以太网远程传输

## API参考

### RobotController 类

```python
class RobotController:
    def __init__(self, box_id: int = 0, robot_id: int = 0)
    def connect(self, host: str, port: int, timeout: float = 30.0) -> bool
    def disconnect(self) -> bool
    def is_connected(self) -> bool
    def enable(self, timeout: float = 30.0) -> bool
    def disable(self, timeout: float = 30.0) -> bool
    def electrify(self) -> bool
    def blackout(self) -> bool
    def get_current_state(self) -> int
    def get_state_description(self, state: int) -> str
    def is_ready(self) -> bool
    def is_moving(self) -> bool
    def wait_for_motion_done(self, timeout: float = 30.0) -> bool
    def move_j(self, points: Union[List[float], np.ndarray], raw_acs_points: Union[List[float], np.ndarray], 
               tcp: str = "TCP", ucs: str = "Base", 
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               is_joint: int = 1, is_seek: int = 0, bit: int = 0, state: int = 0,
               cmd_id: str = "0", timeout: float = 30.0) -> bool
    def move_l(self, points: Union[List[float], np.ndarray], raw_acs_points: Union[List[float], np.ndarray],
               tcp: str = "TCP", ucs: str = "Base",
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               is_seek: int = 0, bit: int = 0, state: int = 0,
               cmd_id: str = "0", timeout: float = 30.0) -> bool
    def get_current_position(self) -> Tuple[List[float], List[float]]
    def get_current_joint_positions(self) -> List[float]
    def set_override(self, vel: float) -> bool
    def get_override(self) -> float
    def stop(self) -> bool
    def reset(self) -> bool
    def goto_pose(self, pose: List[float], tcp: List[float] = None, ucs: List[float] = None, 
                  speed: float = 50.0, acc: float = 50.0, radius: float = 50.0)
    def goto_joint(self, joint_positions: List[float], 
                   speed: float = 50.0, acc: float = 50.0, radius: float = 50.0)
    def goto_delta(self, delta_pose: List[float], tcp: List[float] = None, ucs: List[float] = None,
                   speed: float = 50.0, acc: float = 50.0, radius: float = 50.0)
    def goto_delta_joint(self, delta_joints: List[float],
                         speed: float = 50.0, acc: float = 50.0, radius: float = 50.0)
```

### ControllerClient 类

```python
class ControllerClient:
    def __init__(self, host: str = "localhost", port: int = 8888, 
                 timeout: float = 30.0, reconnect_attempts: int = 3)
    def connect(self) -> bool
    def disconnect(self) -> bool
    def connect_robot(self) -> bool
    def disconnect_robot(self) -> bool
    def enable_robot(self) -> bool
    def disable_robot(self) -> bool
    def move_j(self, points: List[float], raw_acs_points: List[float],
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               timeout: float = 30.0) -> bool
    def move_l(self, points: List[float], raw_acs_points: List[float],
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               timeout: float = 30.0) -> bool
    def get_position(self) -> Optional[tuple]
    def set_override(self, velocity: float) -> bool
    def stop(self) -> bool
    def reset(self) -> bool
    def goto_pose(self, pose: List[float], speed: float = 50.0, 
                  acc: float = 50.0, radius: float = 50.0) -> bool
    def goto_joint(self, joint_positions: List[float], 
                   speed: float = 50.0, acc: float = 50.0, radius: float = 50.0) -> bool
    def electrify(self) -> bool
    def blackout(self) -> bool
    def get_current_state(self) -> Optional[int]
    def get_state_description(self, state: int) -> Optional[str]
    def is_ready(self) -> Optional[bool]
    def is_moving(self) -> Optional[bool]
    def wait_for_motion_done(self, timeout: float = 30.0) -> Optional[bool]
    def get_override(self) -> Optional[float]
    def goto_delta(self, delta_pose: List[float], tcp: List[float] = None, ucs: List[float] = None,
                   speed: float = 50.0, acc: float = 50.0, radius: float = 50.0) -> bool
    def goto_delta_joint(self, delta_joints: List[float],
                         speed: float = 50.0, acc: float = 50.0, radius: float = 50.0) -> bool
    def connect_gripper(self) -> bool
    def disconnect_gripper(self) -> bool
    def set_gripper_amplitude(self, amplitude: int) -> bool
    def set_gripper_force(self, force: int) -> bool
    def get_gripper_position(self) -> Optional[int]
    def get_gripper_torque(self) -> Optional[int]
    def find_gripper_travel(self) -> bool
    def is_gripper_command_completed(self) -> Optional[bool]
    def is_connected(self) -> bool
    def get_state(self) -> ClientState
```

## 文档

请参阅 docs/ 目录下的文档文件获取详细信息：
- 概述: chapter_1_overview.md
- 环境设置: chapter_2_environment_setup.md
- 可用接口: chapter_3_available_interfaces_part1.md 到 part6.md
- 错误说明: HansRobot错误说明及状态机文档.md

## 贡献

欢迎提交 issue 和 pull request 来改进这个项目。

## 许可证

[在此处添加许可证信息]
