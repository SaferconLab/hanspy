#!/usr/bin/env python3
"""
控制器客户端基本使用示例
演示如何使用控制器客户端控制机械臂和夹爪
"""

import time
from controller_clinet.client import ControllerClient
from controller_clinet.utils import wait_for_robot_ready, wait_for_motion_complete


def basic_robot_control_example():
    """基本机器人控制示例"""
    print("=== 基本机器人控制示例 ===")
    
    # 创建客户端实例
    client = ControllerClient(host="localhost", port=8888, timeout=30.0)
    
    try:
        # 连接到服务器
        print("正在连接到控制器服务器...")
        if not client.connect():
            print("连接失败！")
            return
        
        print("连接成功！")
        
        # 连接机器人
        print("正在连接机器人...")
        if not client.connect_robot():
            print("机器人连接失败！")
            return
        
        print("机器人连接成功！")
        
        # 使能机器人
        print("正在使能机器人...")
        if not client.enable_robot():
            print("机器人使能失败！")
            return
        
        print("机器人已使能！")
        
        # 获取当前位置
        print("获取当前位置...")
        position = client.get_position()
        if position:
            joint_pos, cartesian_pos = position
            print(f"当前关节位置: {joint_pos}")
            print(f"当前笛卡尔位置: {cartesian_pos}")
        else:
            print("获取位置失败")
        
        # 设置速度比
        print("设置速度比为0.5...")
        if client.set_override(0.5):
            print("速度比设置成功")
        else:
            print("速度比设置失败")
        
        # 运动到指定关节位置
        print("运动到关节位置 [10, 10, 10, 10, 10, 10]...")
        if client.goto_joint([10, 10, 10, 10, 10, 10]):
            print("关节运动完成")
        else:
            print("关节运动失败")
        
        # 等待运动完成
        print("等待运动完成...")
        if wait_for_motion_complete(client, timeout=10.0):
            print("运动完成")
        else:
            print("等待运动完成超时")
        
        # 获取新位置
        print("获取新位置...")
        position = client.get_position()
        if position:
            joint_pos, cartesian_pos = position
            print(f"新关节位置: {joint_pos}")
            print(f"新笛卡尔位置: {cartesian_pos}")
        
        # 停止机器人
        print("停止机器人...")
        if client.stop():
            print("机器人已停止")
        else:
            print("停止失败")
        
        # 去使能机器人
        print("去使能机器人...")
        if client.disable_robot():
            print("机器人已去使能")
        else:
            print("去使能失败")
        
        # 断开机器人连接
        print("断开机器人连接...")
        if client.disconnect_robot():
            print("机器人连接已断开")
        else:
            print("断开连接失败")
        
        # 断开服务器连接
        print("断开服务器连接...")
        if client.disconnect():
            print("服务器连接已断开")
        else:
            print("断开连接失败")
            
    except Exception as e:
        print(f"示例执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 确保断开连接
        try:
            client.disconnect()
        except:
            pass


def basic_gripper_control_example():
    """基本夹爪控制示例"""
    print("\n=== 基本夹爪控制示例 ===")
    
    # 创建客户端实例
    client = ControllerClient(host="localhost", port=8888, timeout=30.0)
    
    try:
        # 连接到服务器
        print("正在连接到控制器服务器...")
        if not client.connect():
            print("连接失败！")
            return
        
        print("连接成功！")
        
        # 连接夹爪
        print("正在连接夹爪...")
        if not client.connect_gripper():
            print("夹爪连接失败！")
            return
        
        print("夹爪连接成功！")
        
        # 设置夹爪幅度
        print("设置夹爪幅度为50%...")
        if client.set_gripper_amplitude(50):
            print("夹爪幅度设置成功")
        else:
            print("夹爪幅度设置失败")
        
        # 获取夹爪位置
        print("获取夹爪位置...")
        position = client.get_gripper_position()
        if position is not None:
            print(f"夹爪当前位置: {position}%")
        else:
            print("获取夹爪位置失败")
        
        # 设置夹爪力度
        print("设置夹爪力度为70%...")
        if client.set_gripper_force(70):
            print("夹爪力度设置成功")
        else:
            print("夹爪力度设置失败")
        
        # 获取夹爪力矩
        print("获取夹爪力矩...")
        torque = client.get_gripper_torque()
        if torque is not None:
            print(f"夹爪当前力矩: {torque}%")
        else:
            print("获取夹爪力矩失败")
        
        # 执行夹爪找行程
        print("执行夹爪找行程...")
        if client.find_gripper_travel():
            print("夹爪找行程指令已发送")
        else:
            print("夹爪找行程失败")
        
        # 检查夹爪指令状态
        print("检查夹爪指令状态...")
        completed = client.is_gripper_command_completed()
        if completed is not None:
            print(f"夹爪指令状态: {'完成' if completed else '执行中'}")
        else:
            print("检查夹爪指令状态失败")
        
        # 断开夹爪连接
        print("断开夹爪连接...")
        if client.disconnect_gripper():
            print("夹爪连接已断开")
        else:
            print("断开连接失败")
        
        # 断开服务器连接
        print("断开服务器连接...")
        if client.disconnect():
            print("服务器连接已断开")
        else:
            print("断开连接失败")
            
    except Exception as e:
        print(f"示例执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 确保断开连接
        try:
            client.disconnect()
        except:
            pass


def combined_robot_gripper_example():
    """机器人和夹爪联合控制示例"""
    print("\n=== 机器人和夹爪联合控制示例 ===")
    
    # 创建客户端实例
    client = ControllerClient(host="localhost", port=8888, timeout=30.0)
    
    try:
        # 连接到服务器
        print("正在连接到控制器服务器...")
        if not client.connect():
            print("连接失败！")
            return
        
        print("连接成功！")
        
        # 连接机器人
        print("正在连接机器人...")
        if not client.connect_robot():
            print("机器人连接失败！")
            return
        
        print("机器人连接成功！")
        
        # 使能机器人
        print("正在使能机器人...")
        if not client.enable_robot():
            print("机器人使能失败！")
            return
        
        print("机器人已使能！")
        
        # 连接夹爪
        print("正在连接夹爪...")
        if not client.connect_gripper():
            print("夹爪连接失败！")
            return
        
        print("夹爪连接成功！")
        
        # 设置夹爪幅度
        print("设置夹爪幅度为30%...")
        if not client.set_gripper_amplitude(30):
            print("夹爪幅度设置失败！")
            return
        
        print("夹爪幅度设置成功！")
        
        # 运动到指定位置
        print("运动到关节位置 [5, 5, 5, 5, 5, 5]...")
        if not client.goto_joint([5, 5, 5, 5, 5, 5]):
            print("关节运动失败！")
            return
        
        print("关节运动完成！")
        
        # 等待运动完成
        print("等待运动完成...")
        if not wait_for_motion_complete(client, timeout=10.0):
            print("等待运动完成超时")
        
        # 改变夹爪幅度
        print("改变夹爪幅度为80%...")
        if not client.set_gripper_amplitude(80):
            print("夹爪幅度设置失败！")
            return
        
        print("夹爪幅度设置成功！")
        
        # 再次运动
        print("运动到关节位置 [10, 10, 10, 10, 10, 10]...")
        if not client.goto_joint([10, 10, 10, 10, 10, 10]):
            print("关节运动失败！")
            return
        
        print("关节运动完成！")
        
        # 等待运动完成
        print("等待运动完成...")
        if not wait_for_motion_complete(client, timeout=10.0):
            print("等待运动完成超时")
        
        # 最终改变夹爪幅度
        print("改变夹爪幅度为0%...")
        if not client.set_gripper_amplitude(0):
            print("夹爪幅度设置失败！")
            return
        
        print("夹爪幅度设置成功！")
        
        # 去使能机器人
        print("去使能机器人...")
        if not client.disable_robot():
            print("机器人去使能失败！")
            return
        
        print("机器人已去使能！")
        
        # 断开机器人连接
        print("断开机器人连接...")
        if not client.disconnect_robot():
            print("机器人连接断开失败！")
            return
        
        print("机器人连接已断开！")
        
        # 断开夹爪连接
        print("断开夹爪连接...")
        if not client.disconnect_gripper():
            print("夹爪连接断开失败！")
            return
        
        print("夹爪连接已断开！")
        
        # 断开服务器连接
        print("断开服务器连接...")
        if not client.disconnect():
            print("服务器连接断开失败！")
            return
        
        print("服务器连接已断开！")
        print("联合控制示例完成！")
            
    except Exception as e:
        print(f"示例执行出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 确保断开连接
        try:
            client.disconnect()
        except:
            pass


if __name__ == "__main__":
    # 运行基本示例
    basic_robot_control_example()
    basic_gripper_control_example()
    combined_robot_gripper_example()
    
    print("\n所有示例执行完毕！")
