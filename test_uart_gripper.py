#!/usr/bin/env python3
"""
测试串口夹爪控制器
"""

import sys
import time
from lib.lebai_controller_uart import GripperController

def test_gripper():
    """测试夹爪控制器"""
    print("=" * 50)
    print("夹爪控制器测试 - 串口版本")
    print("=" * 50)
    
    # 列出可用串口
    print("\n可用串口设备:")
    available_ports = GripperController.list_available_ports()
    for i, (device, desc, hwid) in enumerate(available_ports):
        print(f"{i}: {device} - {desc} ({hwid})")
    
    # 创建夹爪控制器
    gripper = GripperController()
    
    try:
        # 打开设备
        print("\n正在打开串口设备...")
        if not gripper.open_device():
            print("无法打开设备，请检查连接和权限")
            return False
            
        # 设置通信参数
        print("设置通信参数...")
        gripper.set_baudrate()
        gripper.set_data_characteristics()
        gripper.set_timeouts()
        
        # 清空缓冲区
        gripper.flush_buffers()
        
        # 测试获取夹爪位置
        print("\n1. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试设置夹爪幅度
        print("\n2. 测试设置夹爪幅度为0%...")
        if gripper.set_gripper_amplitude(0):
            print("✓ 设置夹爪幅度0%成功")
        else:
            print("✗ 设置夹爪幅度0%失败")
            
        time.sleep(3)
        
        # 测试获取夹爪位置
        print("\n3. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试设置夹爪幅度
        print("\n4. 测试设置夹爪幅度为50%...")
        if gripper.set_gripper_amplitude(50):
            print("✓ 设置夹爪幅度50%成功")
        else:
            print("✗ 设置夹爪幅度50%失败")
            
        time.sleep(3)

        # 测试获取夹爪位置
        print("\n5. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试设置夹爪幅度
        print("\n6. 测试设置夹爪幅度为100%...")
        if gripper.set_gripper_amplitude(100):
            print("✓ 设置夹爪幅度100%成功")
        else:
            print("✗ 设置夹爪幅度100%失败")
            
        time.sleep(2)

        # 测试获取夹爪位置
        print("\n7. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试获取夹爪力矩
        print("\n8. 测试获取夹爪力矩...")
        torque = gripper.get_gripper_torque()
        if torque >= 0:
            print(f"✓ 夹爪当前力矩: {torque}%")
        else:
            print("✗ 获取夹爪力矩失败")
            
        time.sleep(1)

        # 测试设置夹爪力度
        print("\n9. 测试设置夹爪力度为50%...")
        if gripper.set_gripper_force(50):
            print("✓ 设置夹爪力度50%成功")
        else:
            print("✗ 设置夹爪力度50%失败")
            
        time.sleep(1)
        
        # 测试获取夹爪力矩
        print("\n10. 测试获取夹爪力矩...")
        torque = gripper.get_gripper_torque()
        if torque >= 0:
            print(f"✓ 夹爪当前力矩: {torque}%")
        else:
            print("✗ 获取夹爪力矩失败")
            
        time.sleep(1)
        
        # 测试找行程
        print("\n11. 测试找行程...")
        if gripper.find_travel():
            print("✓ 找行程指令发送成功")
        else:
            print("✗ 找行程指令发送失败")
            
        time.sleep(1)
        
        # 测试检查指令完成状态
        print("\n12. 测试检查指令完成状态...")
        completed = gripper.is_command_completed()
        if completed is not None:
            print(f"✓ 指令状态: {'完成' if completed else '执行中'}")
        else:
            print("✗ 检查指令状态失败")
        
        print("\n测试完成！")
        return True
        
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 关闭设备
        gripper.close_device()
        print("\n设备已关闭")

if __name__ == "__main__":
    success = test_gripper()
    sys.exit(0 if success else 1)