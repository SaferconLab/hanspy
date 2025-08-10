# HansRobot Library Python

Python 版本的 HansRobot 控制库，提供对 HansRobot 机器人的完整控制接口。

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
├── test_robot.py      # 测试脚本
└── test_import.py     # 导入测试脚本
```

## 功能特性

- 完整的机器人控制接口
- 状态监控和错误处理机制
- 详细的文档支持
- 易于使用的 Python API

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

```python
from lib.robot_controller import RobotController
from lib.status_monitor import StatusMonitor

# 创建机器人控制器实例
controller = RobotController()

# 初始化机器人
controller.initialize()

# 获取机器人状态
status = controller.get_status()
print(f"机器人状态: {status}")

# 监控机器人状态
monitor = StatusMonitor(controller)
monitor.start_monitoring()
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
