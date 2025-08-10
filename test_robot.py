#!/usr/bin/env python3
"""
HansRobot 运动测试脚本
使用RobotController类调用API
IP: 192.168.31.88, Port: 10003
"""

import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.robot_controller import RobotController
from lib.exceptions import RobotError, RobotTimeoutError

# 测试参数
ROBOT_IP = "192.168.31.88"
ROBOT_PORT = 10003

print("=" * 60)
print("HansRobot 运动测试")
print("使用RobotController类调用API")
print("=" * 60)

# 创建机器人控制器实例
robot = RobotController(box_id=0, robot_id=0)

try:
    # 1. 连接机器人
    print("\n[1] 连接机器人...")
    if robot.connect(ROBOT_IP, ROBOT_PORT, timeout=10.0):
        print("✓ 连接成功")
    else:
        print("✗ 连接失败")
        raise Exception("连接失败")
    
    # 2. 检查连接状态
    print("\n[2] 检查连接状态...")
    if robot.is_connected():
        print("✓ 机器人已连接")
    else:
        print("✗ 机器人未连接")
        raise Exception("机器人未连接")
    
    # 3. 获取当前状态
    print("\n[3] 获取当前状态...")
    try:
        current_state = robot.get_current_state()
        state_desc = robot.get_state_description(current_state)
        print(f"当前状态: {current_state} ({state_desc})")
    except RobotError as e:
        print(f"⚠ 获取状态失败: {e}")
    
    # 4. 使能机器人
    print("\n[4] 使能机器人...")
    try:
        if robot.enable(timeout=30.0):
            print("✓ 机器人使能成功")
        else:
            print("✗ 机器人使能失败")
            raise Exception("使能失败")
    except RobotError as e:
        print(f"⚠ 使能失败: {e}")
        raise
    except RobotTimeoutError as e:
        print(f"⚠ 使能超时: {e}")
        raise
    
    # 5. 检查是否就绪
    print("\n[5] 检查机器人是否就绪...")
    if robot.is_ready():
        print("✓ 机器人已就绪")
    else:
        print("✗ 机器人未就绪")
    
    # 6. 获取当前位置
    print("\n[6] 获取当前位置...")
    try:
        joint_pos, cartesian_pos = robot.get_current_position()
        print(f"关节位置: [{', '.join(f'{x:.2f}' for x in joint_pos)}]")
        print(f"笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
              f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
    except RobotError as e:
        print(f"⚠ 获取位置失败: {e}")
    
    # 7. 设置速度比
    print("\n[7] 设置速度比...")
    try:
        if robot.set_override(0.2):
            print("✓ 速度比设置为0.2")
    except RobotError as e:
        print(f"⚠ 设置速度比失败: {e}")
    
    # 8. 获取当前关节角度
    print("\n[8] 获取当前关节角度...")
    try:
        joints = robot.get_current_joint_positions()
        print(f"当前关节角度: [{', '.join(f'{x:.2f}' for x in joints)}]")
    except RobotError as e:
        print(f"⚠ 获取关节角度失败: {e}")
    
    # 9. 关节小范围运动测试
    print("\n[9] 关节小范围运动测试...")
    try:
        # 获取当前关节位置作为基准
        base_joints = robot.get_current_joint_positions()
        print(f"基准关节角度: [{', '.join(f'{x:.2f}' for x in base_joints)}]")
        
        # 设置小范围偏移量
        test_joints = base_joints.copy()
        test_joints[0] += 2.0  # 第一个关节正向运动2度
        
        # 执行关节运动
        print("执行关节运动...")
        if robot.move_j(
            points=[0, 0, 0, 0, 0, 0],  # 空间目标位置（不使用）
            raw_acs_points=test_joints,  # 关节目标位置
            tcp="TCP",
            ucs="Base",
            speed=30.0,
            acc=30.0,
            radius=10.0,
            is_joint=1,
            timeout=10.0
        ):
            print("✓ 关节运动完成")
        
        # 回到基准位置
        print("回到基准位置...")
        if robot.move_j(
            points=[0, 0, 0, 0, 0, 0],  # 空间目标位置（不使用）
            raw_acs_points=base_joints,  # 关节目标位置
            tcp="TCP",
            ucs="Base",
            speed=30.0,
            acc=30.0,
            radius=10.0,
            is_joint=1,
            timeout=10.0
        ):
            print("✓ 回到基准位置完成")
            
    except RobotError as e:
        print(f"⚠ 关节运动失败: {e}")
    except RobotTimeoutError as e:
        print(f"⚠ 关节运动超时: {e}")
    
    # 10. 测试完成
    print("\n[10] 测试完成")
    try:
        joint_pos, cartesian_pos = robot.get_current_position()
        print(f"最终笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
              f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
    except RobotError as e:
        print(f"⚠ 获取最终位置失败: {e}")
    
    print("\n" + "=" * 60)
    print("运动测试完成!")
    print("测试参数:")
    print("  速度: 30")
    print("  加速度: 30")
    print("  过渡半径: 10")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # 11. 安全关闭
    print("\n[11] 安全关闭...")
    
    try:
        # 去使能
        if robot.disable(timeout=10.0):
            print("✓ 机器人去使能成功")
        
        # 断开连接
        if robot.disconnect():
            print("✓ 断开连接成功")
    except RobotError as e:
        print(f"⚠ 关闭过程中发生错误: {e}")
    except RobotTimeoutError as e:
        print(f"⚠ 关闭超时: {e}")
    
    print("\n" + "=" * 60)
    print("测试结束")
    print("=" * 60)
