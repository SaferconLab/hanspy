#!/usr/bin/env python3
"""
测试控制器客户端 - 机械臂和夹爪交叉测试
"""

import sys
import os
import time
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controller_clinet.client import ControllerClient
from controller_clinet.utils import wait_for_robot_ready, wait_for_motion_complete

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 测试参数
SERVER_HOST = "192.168.31.190"
SERVER_PORT = 8888

# 机械臂待机姿态，直立
STANDBY_JOINTS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def test_simple_gripper(client, gripper_test_name):
    """简化版夹爪测试 - 只进行基本的开合和位置获取测试"""
    print(f"\n[{gripper_test_name}] 简化夹爪测试...")
    
    # 设置夹爪幅度为50%
    print("设置夹爪幅度为50%...")
    if client.set_gripper_amplitude(50):
        print("✓ 夹爪幅度设置为50%成功")
    else:
        print("✗ 夹爪幅度设置为50%失败")
        return False
    
    # 等待一段时间
    time.sleep(1)
    
    # 获取当前夹爪位置
    print("获取当前夹爪位置...")
    position = client.get_gripper_position()
    if position is not None:
        print(f"✓ 当前夹爪位置: {position}%")
    else:
        print("✗ 获取夹爪位置失败")
        return False
    
    # 设置夹爪幅度为100%
    print("设置夹爪幅度为100%...")
    if client.set_gripper_amplitude(100):
        print("✓ 夹爪幅度设置为100%成功")
    else:
        print("✗ 夹爪幅度设置为100%失败")
        return False
    
    # 等待一段时间
    time.sleep(1)
    
    # 获取当前夹爪位置
    print("获取当前夹爪位置...")
    position = client.get_gripper_position()
    if position is not None:
        print(f"✓ 当前夹爪位置: {position}%")
    else:
        print("✗ 获取夹爪位置失败")
        return False
    
    # 设置夹爪幅度为0%
    print("设置夹爪幅度为0%...")
    if client.set_gripper_amplitude(0):
        print("✓ 夹爪幅度设置为0%成功")
    else:
        print("✗ 夹爪幅度设置为0%失败")
        return False
    
    # 等待一段时间
    time.sleep(1)
    
    # 获取当前夹爪位置
    print("获取当前夹爪位置...")
    position = client.get_gripper_position()
    if position is not None:
        print(f"✓ 当前夹爪位置: {position}%")
    else:
        print("✗ 获取夹爪位置失败")
        return False
    
    print("✓ 简化夹爪测试完成")
    return True

def test_cross_movement(client):
    """执行机械臂和夹爪的交叉测试"""
    print("\n开始机械臂和夹爪交叉测试...")
    
    try:
        # 1. 连接机器人
        print("\n[1] 连接机器人...")
        if not client.connect_robot():
            print("✗ 机器人连接失败")
            return False
        print("✓ 机器人连接成功")
        
        # 2. 连接夹爪
        print("\n[1.5] 连接夹爪...")
        if not client.connect_gripper():
            print("✗ 夹爪连接失败")
            return False
        print("✓ 夹爪连接成功")
        
        # 3. 使能机器人
        print("\n[2] 使能机器人...")
        if not client.enable_robot():
            print("✗ 机器人使能失败")
            return False
        print("✓ 机器人已使能")
        
        # 4. 获取当前位置
        print("\n[3] 获取当前位置...")
        position_data = client.get_position()
        if position_data is not None:
            joint_pos, cartesian_pos = position_data
            print(f"当前关节位置: [{joint_pos[0]:.2f}, {joint_pos[1]:.2f}, {joint_pos[2]:.2f}, "
                  f"{joint_pos[3]:.2f}, {joint_pos[4]:.2f}, {joint_pos[5]:.2f}]")
            print(f"当前笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                  f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
        else:
            print("⚠ 读取位置信息失败")
        
        # 5. 设置速度比
        print("\n[4] 设置速度比...")
        if client.set_override(0.2):
            print("✓ 速度比设置为0.2")
        else:
            print("⚠ 设置速度比失败")
        
        # 6. 获取当前关节角度
        print("\n[5] 关节角度信息显示...")
        position_data = client.get_position()
        if position_data is not None:
            joint_pos, cartesian_pos = position_data
            print(f"当前关节角度: [{joint_pos[0]:.2f}, {joint_pos[1]:.2f}, {joint_pos[2]:.2f}, "
                  f"{joint_pos[3]:.2f}, {joint_pos[4]:.2f}, {joint_pos[5]:.2f}]")
        else:
            print("⚠ 读取关节角度失败")

        #设置基准关节角度
        base_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # 7. 使用goto_joint进行关节运动测试 - 机械臂动作
        print("\n[6] 使用goto_joint进行关节运动测试...")
        try:
            # 获取当前关节角度作为基准
            position_data = client.get_position()
            if position_data is not None:
                print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                      f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
                #打印当前位置
                print(f"当前关节角度: [{position_data[0][0]:.2f}, {position_data[0][1]:.2f}, {position_data[0][2]:.2f}, "
                      f"{position_data[0][3]:.2f}, {position_data[0][4]:.2f}, {position_data[0][5]:.2f}]")
                
                # 设置小范围偏移量（单位：度）
                delta_angle = 10.0  # 10度的小幅运动
                
                # 测试第一个关节的小范围运动 - 机械臂动作
                test_joints_1 = base_joints.copy()
                test_joints_1[0] += delta_angle  # 第一个关节正向运动10度
                
                print(f"使用goto_joint测试关节1正向运动{delta_angle}度...")
                if client.goto_joint(test_joints_1, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 关节1正向运动完成")
                else:
                    print("✗ 关节1正向运动失败")
                    return False
                
                # 读取运动后位置
                position_data = client.get_position()
                if position_data is not None:
                    new_joints = position_data[0]
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 夹爪测试 - 交叉测试
                print("\n[6.5] 交叉测试 - 夹爪测试 (正向运动后)...")
                if not test_simple_gripper(client, "gripper_6.5"):
                    print("✗ 夹爪测试失败")
                    return False
                
                # 测试第一个关节反向运动
                test_joints_2 = base_joints.copy()
                test_joints_2[0] -= delta_angle  # 第一个关节反向运动10度
                
                print(f"使用goto_joint测试关节1反向运动{delta_angle}度...")
                if client.goto_joint(test_joints_2, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 关节1反向运动完成")
                else:
                    print("✗ 关节1反向运动失败")
                    return False
                
                # 读取运动后位置
                position_data = client.get_position()
                if position_data is not None:
                    new_joints = position_data[0]
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 夹爪测试 - 交叉测试
                print("\n[6.7] 交叉测试 - 夹爪测试 (反向运动后)...")
                if not test_simple_gripper(client, "gripper_6.7"):
                    print("✗ 夹爪测试失败")
                    return False
                
                # 回到基准位置
                print(f"回到基准位置...")
                if client.goto_joint(base_joints, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 回到基准位置完成")
                else:
                    print("✗ 回到基准位置失败")
                    return False
                
                print("✓ goto_joint关节运动测试完成")
            else:
                print("⚠ 获取基准位置失败")
                return False
        except Exception as e:
            print(f"⚠ goto_joint关节运动测试失败: {e}")
            return False
        
        # 8. 使用goto_delta_joint进行关节增量运动测试
        print("\n[7] 使用goto_delta_joint进行关节增量运动测试...")
        try:
            # 获取当前关节角度作为基准
            position_data = client.get_position()
            if position_data is not None:
                base_joints = position_data[0]
                print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                      f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
                
                # 设置小范围偏移量（单位：度）
                delta_angle = 15.0  # 5度的小幅运动
                
                # 测试第一个关节的正向增量运动 - 机械臂动作
                delta_joints_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                delta_joints_1[0] = delta_angle  # 第一个关节正向运动
                delta_joints_1[1] = -delta_angle   # 第二个关节反向运动，增加测试复杂度
                delta_joints_1[2] = delta_angle 
                
                print(f"使用goto_delta_joint测试关节1正向增量运动{delta_angle}度...")
                if client.goto_delta_joint(delta_joints_1, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 关节1正向增量运动完成")
                else:
                    print("✗ 关节1正向增量运动失败")
                    return False
                
                # 读取运动后位置
                position_data = client.get_position()
                if position_data is not None:
                    new_joints = position_data[0]
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 夹爪测试 - 交叉测试
                print("\n[7.5] 交叉测试 - 夹爪测试 (正向增量运动后)...")
                if not test_simple_gripper(client, "gripper_7.5"):
                    print("✗ 夹爪测试失败")
                    return False
                
                # 测试第一个关节的反向增量运动
                delta_joints_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                delta_joints_2[0] = -delta_angle  # 第一个关节反向运动5度
                
                print(f"使用goto_delta_joint测试关节1反向增量运动{delta_angle}度...")
                if client.goto_delta_joint(delta_joints_2, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 关节1反向增量运动完成")
                else:
                    print("✗ 关节1反向增量运动失败")
                    return False
                
                # 读取运动后位置
                position_data = client.get_position()
                if position_data is not None:
                    new_joints = position_data[0]
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 夹爪测试 - 交叉测试
                print("\n[7.7] 交叉测试 - 夹爪测试 (反向增量运动后)...")
                if not test_simple_gripper(client, "gripper_7.7"):
                    print("✗ 夹爪测试失败")
                    return False
                
                # 回到基准位置
                print(f"回到基准位置...")
                # 计算回退增量
                delta_joints_home = [base_joints[i] - new_joints[i] for i in range(6)]
                if client.goto_delta_joint(delta_joints_home, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 回到基准位置完成")
                else:
                    print("✗ 回到基准位置失败")
                    return False
                
                print("✓ goto_delta_joint关节增量运动测试完成")
            else:
                print("⚠ 获取基准位置失败")
                return False
        except Exception as e:
            print(f"⚠ goto_delta_joint关节增量运动测试失败: {e}")
            return False
        
        # 9. 使用goto_pose进行笛卡尔运动测试
        print("\n[8] 使用goto_pose进行笛卡尔运动测试...")
        try:
            # 在运行pose测试前，让机械臂运动到一个有弯曲的关节姿态，防止奇异点
            print("正在让机械臂运动到一个有弯曲的关节姿态...")
            if client.goto_joint([30.0, 45.0, 45.0, 0.0, 45.0, 0.0], speed=30.0, acc=30.0, radius=0.0):
                print("✓ 机械臂已运动到弯曲姿态")
            else:
                print("✗ 机械臂运动到弯曲姿态失败")
                return False
            
            # 获取当前位置作为起点
            position_data = client.get_position()
            if position_data is not None:
                current_cartesian = position_data[1]
                print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                      f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
                
                # 使用更安全的笛卡尔运动测试 - 在当前X,Y平面内移动一小段距离 - 机械臂动作
                target_cartesian = current_cartesian.copy()
                target_cartesian[0] += 30.0  # X轴增加30mm
                target_cartesian[1] += 20.0  # Y轴增加20mm
                
                print(f"使用goto_pose执行笛卡尔运动到X轴+30mm, Y轴+20mm的位置...")
                if client.goto_pose(target_cartesian, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 笛卡尔运动完成")
                else:
                    print("✗ 笛卡尔运动失败")
                    return False
                
                # 检查运动后的笛卡尔位置
                position_data = client.get_position()
                if position_data is not None:
                    final_cartesian = position_data[1]
                    print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                          f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
                
                # 夹爪测试 - 交叉测试
                print("\n[8.5] 交叉测试 - 夹爪测试 (笛卡尔运动后)...")
                if not test_simple_gripper(client, "gripper_8.5"):
                    print("✗ 夹爪测试失败")
                    return False
                
                # 回到起始位置
                print(f"回到起始位置...")
                if client.goto_pose(current_cartesian, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 回到起始位置完成")
                else:
                    print("✗ 回到起始位置失败")
                    return False
                
                print("✓ goto_pose笛卡尔运动测试完成")
            else:
                print("⚠ 获取起始位置失败")
                return False
        except Exception as e:
            print(f"⚠ goto_pose笛卡尔运动测试失败: {e}")
            return False
        
        # 10. 使用goto_delta进行笛卡尔增量运动测试
        print("\n[9] 使用goto_delta进行笛卡尔增量运动测试...")
        try:
            # 获取当前位置作为起点
            position_data = client.get_position()
            if position_data is not None:
                current_cartesian = position_data[1]
                print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                      f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
                
                # 定义增量运动 - 机械臂动作
                delta_cartesian = [20.0, 15.0, 0.0, 0.0, 0.0, 0.0]  # X轴增加20mm, Y轴增加15mm
                
                print(f"使用goto_delta执行笛卡尔增量运动X轴+20mm, Y轴+15mm...")
                if client.goto_delta(delta_cartesian, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 笛卡尔增量运动完成")
                else:
                    print("✗ 笛卡尔增量运动失败")
                    return False
                
                # 检查运动后的笛卡尔位置
                position_data = client.get_position()
                if position_data is not None:
                    final_cartesian = position_data[1]
                    print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                          f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
                
                # 夹爪测试 - 交叉测试
                print("\n[9.5] 交叉测试 - 夹爪测试 (笛卡尔增量运动后)...")
                if not test_simple_gripper(client, "gripper_9.5"):
                    print("✗ 夹爪测试失败")
                    return False
                
                # 反向增量运动回到起始位置附近
                delta_cartesian_back = [-20.0, -15.0, 0.0, 0.0, 0.0, 0.0]
                print(f"使用goto_delta执行笛卡尔反向增量运动回到起始位置附近...")
                if client.goto_delta(delta_cartesian_back, speed=30.0, acc=30.0, radius=0.0):
                    print("✓ 反向增量运动完成")
                else:
                    print("✗ 反向增量运动失败")
                    return False
                
                print("✓ goto_delta笛卡尔增量运动测试完成")
            else:
                print("⚠ 获取起始位置失败")
                return False
        except Exception as e:
            print(f"⚠ goto_delta笛卡尔增量运动测试失败: {e}")
            return False
        
        # 11. 速度比测试
        print("\n[10] 速度比测试...")
        try:
            # 测试不同的速度比
            speed_ratios = [0.1, 0.3, 0.5, 1.0]
            for ratio in speed_ratios:
                print(f"设置速度比为 {ratio}...")
                if client.set_override(ratio):
                    print(f"✓ 速度比设置为 {ratio}")
                else:
                    print(f"✗ 设置速度比 {ratio} 失败")
                    return False
                
                # 使用goto_joint进行简单的关节运动测试
                position_data = client.get_position()
                if position_data is not None:
                    base_joints = position_data[0]
                    test_joints = base_joints.copy()
                    test_joints[0] += 5.0  # 小幅运动
                    
                    print(f"使用速度比 {ratio} 执行goto_joint运动...")
                    if client.goto_joint(test_joints, speed=50.0, acc=50.0, radius=0.0):
                        print(f"✓ 速度比 {ratio} 测试完成")
                    else:
                        print(f"✗ 速度比 {ratio} 测试失败")
                        return False
                else:
                    print(f"⚠ 获取基准位置失败，速度比 {ratio} 测试跳过")
            
            print("✓ 速度比测试完成")
        except Exception as e:
            print(f"⚠ 速度比测试失败: {e}")
            return False
        
        # 测试完成
        print("\n[11] 测试完成")
        try:
            position_data = client.get_position()
            if position_data is not None:
                cartesian_pos = position_data[1]
                print(f"最终笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                      f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
            else:
                print("⚠ 读取最终位置失败")
        except Exception as e:
            print(f"⚠ 读取最终位置失败: {e}")
        
        print("\n" + "=" * 60)
        print("使用控制器客户端的运动测试完成!")
        print("测试参数:")
        print("  速度: 30 (默认值)")
        print("  加速度: 30 (默认值)")
        print("  过渡半径: 0 (默认值)")
        print("=" * 60)
        time.sleep(5)

        # 运行完所有测试后，让机械臂回到待机姿态
        print("\n[12] 让机械臂回到待机姿态...")
        if client.goto_joint(STANDBY_JOINTS, speed=30.0, acc=30.0, radius=0.0):
            print("✓ 机械臂已回到待机姿态")
        else:
            print("✗ 机械臂回到待机姿态失败")
            return False
        
        # 去使能机器人
        print("\n[13] 去使能机器人...")
        if client.disable_robot():
            print("✓ 机器人已去使能")
        else:
            print("✗ 机器人去使能失败")
            return False
        
        # 断开机器人连接
        print("\n[14] 断开机器人连接...")
        if client.disconnect_robot():
            print("✓ 机器人连接已断开")
        else:
            print("✗ 机器人连接断开失败")
            return False
        
        # 断开夹爪连接
        print("\n[15] 断开夹爪连接...")
        if client.disconnect_gripper():
            print("✓ 夹爪连接已断开")
        else:
            print("✗ 夹爪连接断开失败")
            return False
        
        print("✓ 测试完成")
        return True
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始测试控制器客户端...")
    
    # 创建客户端实例
    client = ControllerClient(SERVER_HOST, SERVER_PORT)
    
    try:
        # 连接到服务器
        print("正在连接到控制器服务器...")
        if not client.connect():
            print("✗ 连接服务器失败")
            return
        
        print("✓ 成功连接到控制器服务器")
        
        # 等待服务器启动
        time.sleep(1)
        
        # 执行交叉测试
        if test_cross_movement(client):
            print("\n测试通过!")
        else:
            print("\n测试失败!")
            
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 确保断开连接
        try:
            if client.is_connected():
                client.disconnect()
                print("✓ 已断开与服务器的连接")
        except Exception as e:
            print(f"断开连接时出错: {e}")

if __name__ == "__main__":
    main()
