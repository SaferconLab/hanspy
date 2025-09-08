#!/usr/bin/env python3
"""
控制器服务器测试客户端
用于测试控制器服务器的功能
参考 test_robot_goto.py 的测试流程
"""

import socket
import json
import time
import threading
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 测试参数
ROBOT_IP = "192.168.31.88"
ROBOT_PORT = 10003
SERVER_HOST = "localhost"
SERVER_PORT = 8888

# 机械臂待机姿态，直立，运行完所有测试用goto_joint回到这个姿态
STANDBY_JOINTS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def send_command(client, command_type, data=None, message_id=None):
    """发送命令并接收响应"""
    if message_id is None:
        message_id = f"msg_{int(time.time())}"
    
    command = {
        "type": command_type,
        "message_id": message_id,
        "data": data or {}
    }
    
    try:
        client.send(json.dumps(command).encode('utf-8'))
        response = client.recv(4096)
        return json.loads(response.decode('utf-8'))
    except Exception as e:
        print(f"发送命令失败: {e}")
        return None

def test_gripper(client):
    """测试夹爪功能"""
    print("\n[15] 开始测试夹爪功能...")
    
    # 连接夹爪
    print("\n[15.1] 连接夹爪...")
    response = send_command(client, "connect_gripper", {}, "connect_gripper_1")
    if response and response.get("status") == "success":
        print("✓ 夹爪连接成功")
    else:
        print("✗ 夹爪连接失败")
        if response:
            print(f"  错误详情: {response}")
        return False
    
    # 测试夹爪幅度设置
    print("\n[15.2] 测试夹爪幅度设置...")
    try:
        # 设置夹爪幅度为0%
        print("设置夹爪幅度为0%...")
        response = send_command(client, "set_gripper_amplitude", {"amplitude": 0}, "set_amp_0")
        if response and response.get("status") == "success":
            print("✓ 夹爪幅度设置为0%成功")
        else:
            print("✗ 夹爪幅度设置为0%失败")
        
        # 等待一段时间
        time.sleep(1)
        
        # 获取当前夹爪位置
        print("获取当前夹爪位置...")
        response = send_command(client, "get_gripper_position", {}, "get_pos_0")
        if response and response.get("status") == "success":
            position = response.get("data", {}).get("position", -1)
            print(f"✓ 当前夹爪位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
        
        # 设置夹爪幅度为50%
        print("设置夹爪幅度为50%...")
        response = send_command(client, "set_gripper_amplitude", {"amplitude": 50}, "set_amp_50")
        if response and response.get("status") == "success":
            print("✓ 夹爪幅度设置为50%成功")
        else:
            print("✗ 夹爪幅度设置为50%失败")
        
        # 等待一段时间
        time.sleep(1)
        
        # 获取当前夹爪位置
        print("获取当前夹爪位置...")
        response = send_command(client, "get_gripper_position", {}, "get_pos_50")
        if response and response.get("status") == "success":
            position = response.get("data", {}).get("position", -1)
            print(f"✓ 当前夹爪位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
        
        # 设置夹爪幅度为100%
        print("设置夹爪幅度为100%...")
        response = send_command(client, "set_gripper_amplitude", {"amplitude": 100}, "set_amp_100")
        if response and response.get("status") == "success":
            print("✓ 夹爪幅度设置为100%成功")
        else:
            print("✗ 夹爪幅度设置为100%失败")
        
        # 等待一段时间
        time.sleep(1)
        
        # 获取当前夹爪位置
        print("获取当前夹爪位置...")
        response = send_command(client, "get_gripper_position", {}, "get_pos_100")
        if response and response.get("status") == "success":
            position = response.get("data", {}).get("position", -1)
            print(f"✓ 当前夹爪位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
    except Exception as e:
        print(f"⚠ 夹爪幅度测试失败: {e}")
    
    # 测试夹爪力度设置
    print("\n[15.3] 测试夹爪力度设置...")
    try:
        # 设置夹爪力度为50%
        print("设置夹爪力度为50%...")
        response = send_command(client, "set_gripper_force", {"force": 50}, "set_force_50")
        if response and response.get("status") == "success":
            print("✓ 夹爪力度设置为50%成功")
        else:
            print("✗ 夹爪力度设置为50%失败")
        
        # 等待一段时间
        time.sleep(1)
        
        # 设置夹爪力度为100%
        print("设置夹爪力度为100%...")
        response = send_command(client, "set_gripper_force", {"force": 100}, "set_force_100")
        if response and response.get("status") == "success":
            print("✓ 夹爪力度设置为100%成功")
        else:
            print("✗ 夹爪力度设置为100%失败")
            
    except Exception as e:
        print(f"⚠ 夹爪力度测试失败: {e}")
    
    # 测试获取夹爪力矩
    print("\n[15.4] 测试获取夹爪力矩...")
    try:
        print("获取当前夹爪力矩...")
        response = send_command(client, "get_gripper_torque", {}, "get_torque")
        if response and response.get("status") == "success":
            torque = response.get("data", {}).get("torque", -1)
            print(f"✓ 当前夹爪力矩: {torque}%")
        else:
            print("✗ 获取夹爪力矩失败")
    except Exception as e:
        print(f"⚠ 获取夹爪力矩失败: {e}")
    
    # 测试夹爪找行程
    print("\n[15.5] 测试夹爪找行程...")
    try:
        print("发送夹爪找行程指令...")
        response = send_command(client, "find_gripper_travel", {}, "find_travel")
        if response and response.get("status") == "success":
            print("✓ 夹爪找行程指令已发送")
        else:
            print("✗ 夹爪找行程指令发送失败")
    except Exception as e:
        print(f"⚠ 夹爪找行程失败: {e}")
    
    # 断开夹爪连接
    print("\n[15.6] 断开夹爪连接...")
    response = send_command(client, "disconnect_gripper", {}, "disconnect_gripper_1")
    if response and response.get("status") == "success":
        print("✓ 夹爪连接已断开")
    else:
        print("✗ 夹爪断开连接失败")
    
    print("✓ 夹爪功能测试完成")
    return True

def test_connection():
    """测试连接"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))
        
        # 接收欢迎消息
        data = client.recv(4096)
        print("收到欢迎消息:", data.decode('utf-8'))
        
        # 连接机器人
        print("\n[1] 连接机器人...")
        response = send_command(client, "connect_robot", {}, "connect_1")
        if response and response.get("status") == "success":
            print("✓ 机器人连接成功")
        else:
            print("✗ 机器人连接失败")
            # 尝试获取更详细的错误信息
            if response:
                print(f"  错误详情: {response}")
            client.close()
            return False
        
        # 使能机器人
        print("\n[2] 使能机器人...")
        response = send_command(client, "enable_robot", {}, "enable_1")
        if response and response.get("status") == "success":
            print("✓ 机器人已使能")
        else:
            print("✗ 机器人使能失败")
            client.close()
            return False
        
        # 获取当前位置
        print("\n[3] 获取当前位置...")
        response = send_command(client, "get_position", {}, "pos_1")
        if response and response.get("status") == "success":
            joint_pos = response.get("data", {}).get("joint_positions", [])
            cartesian_pos = response.get("data", {}).get("cartesian_positions", [])
            print(f"当前关节位置: [{joint_pos[0]:.2f}, {joint_pos[1]:.2f}, {joint_pos[2]:.2f}, "
                  f"{joint_pos[3]:.2f}, {joint_pos[4]:.2f}, {joint_pos[5]:.2f}]")
            print(f"当前笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                  f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
        else:
            print("⚠ 读取位置信息失败")
        
        # 设置速度比
        print("\n[4] 设置速度比...")
        response = send_command(client, "set_override", {"velocity": 0.2}, "override_1")
        if response and response.get("status") == "success":
            print("✓ 速度比设置为0.2")
        else:
            print("⚠ 设置速度比失败")
        
        # 获取当前关节角度
        print("\n[5] 关节角度信息显示...")
        response = send_command(client, "get_position", {}, "pos_2")
        if response and response.get("status") == "success":
            joint_pos = response.get("data", {}).get("joint_positions", [])
            print(f"当前关节角度: [{joint_pos[0]:.2f}, {joint_pos[1]:.2f}, {joint_pos[2]:.2f}, "
                  f"{joint_pos[3]:.2f}, {joint_pos[4]:.2f}, {joint_pos[5]:.2f}]")
        else:
            print("⚠ 读取关节角度失败")
        
        # 使用goto_joint进行关节运动测试
        print("\n[6] 使用goto_joint进行关节运动测试...")
        try:
            # 获取当前关节角度作为基准
            response = send_command(client, "get_position", {}, "pos_3")
            if response and response.get("status") == "success":
                base_joints = response.get("data", {}).get("joint_positions", [])
                print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                      f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
                
                # 设置小范围偏移量（单位：度）
                delta_angle = 10.0  # 10度的小幅运动
                
                # 测试第一个关节的小范围运动
                test_joints_1 = base_joints.copy()
                test_joints_1[0] += delta_angle  # 第一个关节正向运动10度
                
                print(f"使用goto_joint测试关节1正向运动{delta_angle}度...")
                response = send_command(client, "goto_joint", {
                    "joint_positions": test_joints_1,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_joint_1")
                
                if response and response.get("status") == "success":
                    print("✓ 关节1正向运动完成")
                else:
                    print("✗ 关节1正向运动失败")
                
                # 读取运动后位置
                response = send_command(client, "get_position", {}, "pos_4")
                if response and response.get("status") == "success":
                    new_joints = response.get("data", {}).get("joint_positions", [])
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 测试第一个关节反向运动
                test_joints_2 = base_joints.copy()
                test_joints_2[0] -= delta_angle  # 第一个关节反向运动10度
                
                print(f"使用goto_joint测试关节1反向运动{delta_angle}度...")
                response = send_command(client, "goto_joint", {
                    "joint_positions": test_joints_2,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_joint_2")
                
                if response and response.get("status") == "success":
                    print("✓ 关节1反向运动完成")
                else:
                    print("✗ 关节1反向运动失败")
                
                # 读取运动后位置
                response = send_command(client, "get_position", {}, "pos_5")
                if response and response.get("status") == "success":
                    new_joints = response.get("data", {}).get("joint_positions", [])
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 回到基准位置
                print(f"回到基准位置...")
                response = send_command(client, "goto_joint", {
                    "joint_positions": base_joints,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_joint_home")
                
                if response and response.get("status") == "success":
                    print("✓ 回到基准位置完成")
                else:
                    print("✗ 回到基准位置失败")
                
                print("✓ goto_joint关节运动测试完成")
            else:
                print("⚠ 获取基准位置失败")
        except Exception as e:
            print(f"⚠ goto_joint关节运动测试失败: {e}")
        
        # 使用goto_delta_joint进行关节增量运动测试
        print("\n[7] 使用goto_delta_joint进行关节增量运动测试...")
        try:
            # 获取当前关节角度作为基准
            response = send_command(client, "get_position", {}, "pos_6")
            if response and response.get("status") == "success":
                base_joints = response.get("data", {}).get("joint_positions", [])
                print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                      f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
                
                # 设置小范围偏移量（单位：度）
                delta_angle = 5.0  # 5度的小幅运动
                
                # 测试第一个关节的正向增量运动
                delta_joints_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                delta_joints_1[0] = delta_angle  # 第一个关节正向运动5度
                
                print(f"使用goto_delta_joint测试关节1正向增量运动{delta_angle}度...")
                response = send_command(client, "goto_delta_joint", {
                    "delta_joints": delta_joints_1,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_delta_joint_1")
                
                if response and response.get("status") == "success":
                    print("✓ 关节1正向增量运动完成")
                else:
                    print("✗ 关节1正向增量运动失败")
                
                # 读取运动后位置
                response = send_command(client, "get_position", {}, "pos_7")
                if response and response.get("status") == "success":
                    new_joints = response.get("data", {}).get("joint_positions", [])
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 测试第一个关节的反向增量运动
                delta_joints_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                delta_joints_2[0] = -delta_angle  # 第一个关节反向运动5度
                
                print(f"使用goto_delta_joint测试关节1反向增量运动{delta_angle}度...")
                response = send_command(client, "goto_delta_joint", {
                    "delta_joints": delta_joints_2,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_delta_joint_2")
                
                if response and response.get("status") == "success":
                    print("✓ 关节1反向增量运动完成")
                else:
                    print("✗ 关节1反向增量运动失败")
                
                # 读取运动后位置
                response = send_command(client, "get_position", {}, "pos_8")
                if response and response.get("status") == "success":
                    new_joints = response.get("data", {}).get("joint_positions", [])
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 回到基准位置
                print(f"回到基准位置...")
                # 计算回退增量
                delta_joints_home = [base_joints[i] - new_joints[i] for i in range(6)]
                response = send_command(client, "goto_delta_joint", {
                    "delta_joints": delta_joints_home,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_delta_joint_home")
                
                if response and response.get("status") == "success":
                    print("✓ 回到基准位置完成")
                else:
                    print("✗ 回到基准位置失败")
                
                print("✓ goto_delta_joint关节增量运动测试完成")
            else:
                print("⚠ 获取基准位置失败")
        except Exception as e:
            print(f"⚠ goto_delta_joint关节增量运动测试失败: {e}")
        
        # 使用goto_pose进行笛卡尔运动测试
        print("\n[8] 使用goto_pose进行笛卡尔运动测试...")
        try:
            # 在运行pose测试前，让机械臂运动到一个有弯曲的关节姿态，防止奇异点
            print("正在让机械臂运动到一个有弯曲的关节姿态...")
            response = send_command(client, "goto_joint", {
                "joint_positions": [30.0, 45.0, 45.0, 0.0, 45.0, 0.0],
                "speed": 30.0,
                "acc": 30.0,
                "radius": 0.0
            }, "goto_joint_bend")
            
            if response and response.get("status") == "success":
                print("✓ 机械臂已运动到弯曲姿态")
            else:
                print("✗ 机械臂运动到弯曲姿态失败")
            
            # 获取当前位置作为起点
            response = send_command(client, "get_position", {}, "pos_9")
            if response and response.get("status") == "success":
                current_cartesian = response.get("data", {}).get("cartesian_positions", [])
                print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                      f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
                
                # 使用更安全的笛卡尔运动测试 - 在当前X,Y平面内移动一小段距离
                target_cartesian = current_cartesian.copy()
                target_cartesian[0] += 30.0  # X轴增加30mm
                target_cartesian[1] += 20.0  # Y轴增加20mm
                
                print(f"使用goto_pose执行笛卡尔运动到X轴+30mm, Y轴+20mm的位置...")
                response = send_command(client, "goto_pose", {
                    "pose": target_cartesian,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_pose_1")
                
                if response and response.get("status") == "success":
                    print("✓ 笛卡尔运动完成")
                else:
                    print("✗ 笛卡尔运动失败")
                
                # 检查运动后的笛卡尔位置
                response = send_command(client, "get_position", {}, "pos_10")
                if response and response.get("status") == "success":
                    final_cartesian = response.get("data", {}).get("cartesian_positions", [])
                    print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                          f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
                
                # 回到起始位置
                print(f"回到起始位置...")
                response = send_command(client, "goto_pose", {
                    "pose": current_cartesian,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_pose_home")
                
                if response and response.get("status") == "success":
                    print("✓ 回到起始位置完成")
                else:
                    print("✗ 回到起始位置失败")
                
                print("✓ goto_pose笛卡尔运动测试完成")
            else:
                print("⚠ 获取起始位置失败")
        except Exception as e:
            print(f"⚠ goto_pose笛卡尔运动测试失败: {e}")
        
        # 使用goto_delta进行笛卡尔增量运动测试
        print("\n[9] 使用goto_delta进行笛卡尔增量运动测试...")
        try:
            # 获取当前位置作为起点
            response = send_command(client, "get_position", {}, "pos_11")
            if response and response.get("status") == "success":
                current_cartesian = response.get("data", {}).get("cartesian_positions", [])
                print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                      f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
                
                # 定义增量运动
                delta_cartesian = [20.0, 15.0, 0.0, 0.0, 0.0, 0.0]  # X轴增加20mm, Y轴增加15mm
                
                print(f"使用goto_delta执行笛卡尔增量运动X轴+20mm, Y轴+15mm...")
                response = send_command(client, "goto_delta", {
                    "delta_pose": delta_cartesian,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_delta_1")
                
                if response and response.get("status") == "success":
                    print("✓ 笛卡尔增量运动完成")
                else:
                    print("✗ 笛卡尔增量运动失败")
                
                # 检查运动后的笛卡尔位置
                response = send_command(client, "get_position", {}, "pos_12")
                if response and response.get("status") == "success":
                    final_cartesian = response.get("data", {}).get("cartesian_positions", [])
                    print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                          f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
                
                # 反向增量运动回到起始位置附近
                delta_cartesian_back = [-20.0, -15.0, 0.0, 0.0, 0.0, 0.0]
                print(f"使用goto_delta执行笛卡尔反向增量运动回到起始位置附近...")
                response = send_command(client, "goto_delta", {
                    "delta_pose": delta_cartesian_back,
                    "speed": 30.0,
                    "acc": 30.0,
                    "radius": 0.0
                }, "goto_delta_back")
                
                if response and response.get("status") == "success":
                    print("✓ 反向增量运动完成")
                else:
                    print("✗ 反向增量运动失败")
                
                print("✓ goto_delta笛卡尔增量运动测试完成")
            else:
                print("⚠ 获取起始位置失败")
        except Exception as e:
            print(f"⚠ goto_delta笛卡尔增量运动测试失败: {e}")
        
        # 速度比测试
        print("\n[10] 速度比测试...")
        try:
            # 测试不同的速度比
            speed_ratios = [0.1, 0.3, 0.5, 1.0]
            for ratio in speed_ratios:
                print(f"设置速度比为 {ratio}...")
                response = send_command(client, "set_override", {"velocity": ratio}, f"override_{ratio}")
                if response and response.get("status") == "success":
                    print(f"✓ 速度比设置为 {ratio}")
                else:
                    print(f"✗ 设置速度比 {ratio} 失败")
                
                # 使用goto_joint进行简单的关节运动测试
                response = send_command(client, "get_position", {}, f"pos_speed_{ratio}")
                if response and response.get("status") == "success":
                    base_joints = response.get("data", {}).get("joint_positions", [])
                    test_joints = base_joints.copy()
                    test_joints[0] += 5.0  # 小幅运动
                    
                    print(f"使用速度比 {ratio} 执行goto_joint运动...")
                    response = send_command(client, "goto_joint", {
                        "joint_positions": test_joints,
                        "speed": 50.0,
                        "acc": 50.0,
                        "radius": 0.0
                    }, f"goto_joint_speed_{ratio}")
                    
                    if response and response.get("status") == "success":
                        print(f"✓ 速度比 {ratio} 测试完成")
                    else:
                        print(f"✗ 速度比 {ratio} 测试失败")
                else:
                    print(f"⚠ 获取基准位置失败，速度比 {ratio} 测试跳过")
            
            print("✓ 速度比测试完成")
        except Exception as e:
            print(f"⚠ 速度比测试失败: {e}")
        
        # 测试完成
        print("\n[11] 测试完成")
        try:
            response = send_command(client, "get_position", {}, "final_pos")
            if response and response.get("status") == "success":
                cartesian_pos = response.get("data", {}).get("cartesian_positions", [])
                print(f"最终笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                      f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
            else:
                print("⚠ 读取最终位置失败")
        except Exception as e:
            print(f"⚠ 读取最终位置失败: {e}")
        
        print("\n" + "=" * 60)
        print("使用控制器服务器的运动测试完成!")
        print("测试参数:")
        print("  速度: 30 (默认值)")
        print("  加速度: 30 (默认值)")
        print("  过渡半径: 0 (默认值)")
        print("=" * 60)
        time.sleep(5)

        # 运行完所有测试后，让机械臂回到待机姿态
        print("\n[12] 让机械臂回到待机姿态...")
        response = send_command(client, "goto_joint", {
            "joint_positions": STANDBY_JOINTS,
            "speed": 30.0,
            "acc": 30.0,
            "radius": 0.0
        }, "goto_standby")
        
        if response and response.get("status") == "success":
            print("✓ 机械臂已回到待机姿态")
        else:
            print("✗ 机械臂回到待机姿态失败")
        
        # 去使能机器人
        print("\n[13] 去使能机器人...")
        response = send_command(client, "disable_robot", {}, "disable_1")
        if response and response.get("status") == "success":
            print("✓ 机器人已去使能")
        else:
            print("✗ 机器人去使能失败")
        
        # 断开机器人连接
        print("\n[14] 断开机器人连接...")
        response = send_command(client, "disconnect_robot", {}, "disconnect_1")
        if response and response.get("status") == "success":
            print("✓ 机器人连接已断开")
        else:
            print("✗ 机器人连接断开失败")
        
        # 测试夹爪功能
        print("\n[15] 测试夹爪功能...")
        test_gripper(client)
        
        client.close()
        print("✓ 测试完成")
        return True
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("开始测试控制器服务器...")
    
    # 等待服务器启动
    time.sleep(1)
    
    # 测试连接
    if test_connection():
        print("\n测试通过!")
    else:
        print("\n测试失败!")


if __name__ == "__main__":
    main()
