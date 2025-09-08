#!/usr/bin/env python3
"""
HansRobot 运动测试脚本
使用RobotController的goto接口并配合lebai夹爪
IP: 192.168.31.88, Port: 10003
"""

import time
import sys
import logging
from lib.robot_controller import RobotController
from lib.lebai_controller import GripperController

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 测试参数
ROBOT_IP = "192.168.31.88"
ROBOT_PORT = 10003

# 机械臂待机姿态，直立，运行完所有测试用goto_joint回到这个姿态
STANDBY_JOINTS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

print("=" * 60)
print("HansRobot 运动测试")
print("使用RobotController的goto接口")
print("=" * 60)

def main():
    # 创建机器人控制器实例
    robot = RobotController()
    
    # 创建夹爪控制器实例
    gripper = GripperController()
    
    try:
        # 1. 连接机器人
        print("\n[1] 连接机器人...")
        robot.connect(ROBOT_IP, ROBOT_PORT)
        print("✓ 连接成功")
        
        # 2. 检查并准备机器人
        print("\n[2] 检查机器人状态...")
        
        # 检查当前状态
        current_state = robot.get_current_state()
        state_desc = robot.get_state_description(current_state)
        print(f"当前状态码: {current_state}, 描述: {state_desc}")
        
        # 如果状态不是就绪状态(33)，则进行使能
        if not robot.is_ready():
            print("机器人未就绪，正在使能...")
            
            robot.enable()
            print("✓ 机器人已使能")
        else:
            print("机器人已就绪，无需使能")
        
        # 3. 初始化夹爪
        print("\n[3] 初始化夹爪...")
        try:
            if gripper.open_device():
                print("✓ 夹爪设备已打开")
                gripper.set_baudrate()
                gripper.set_data_characteristics()
                gripper.set_timeouts()
                gripper.flush_buffers()
                print("✓ 夹爪通信参数设置完成")
            else:
                print("⚠ 夹爪设备打开失败")
        except Exception as e:
            print(f"⚠ 夹爪初始化失败: {e}")
        
        # 4. 获取当前位置
        print("\n[4] 获取当前位置...")
        try:
            joint_pos, cartesian_pos = robot.get_current_position()
            print(f"当前关节位置: [{joint_pos[0]:.2f}, {joint_pos[1]:.2f}, {joint_pos[2]:.2f}, "
                  f"{joint_pos[3]:.2f}, {joint_pos[4]:.2f}, {joint_pos[5]:.2f}]")
            print(f"当前笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                  f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
        except Exception as e:
            print(f"⚠ 读取位置信息失败: {e}")
        
        # 5. 设置速度比
        print("\n[5] 设置速度比...")
        try:
            robot.set_override(0.2)
            print("✓ 速度比设置为0.2")
        except Exception as e:
            print(f"⚠ 设置速度比失败: {e}")
        
        # 6. 获取当前关节角度
        print("\n[6] 关节角度信息显示...")
        try:
            current_joints = robot.get_current_joint_positions()
            print(f"当前关节角度: [{current_joints[0]:.2f}, {current_joints[1]:.2f}, {current_joints[2]:.2f}, "
                  f"{current_joints[3]:.2f}, {current_joints[4]:.2f}, {current_joints[5]:.2f}]")
        except Exception as e:
            print(f"⚠ 读取关节角度失败: {e}")
        
        # 7. 使用goto_joint进行关节运动测试
        print("\n[6] 使用goto_joint进行关节运动测试...")
        try:
            # 获取当前关节角度作为基准
            base_joints = robot.get_current_joint_positions()
            print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                  f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
            
            # 设置小范围偏移量（单位：度）
            delta_angle = 10.0  # 10度的小幅运动
            
            # 测试第一个关节的小范围运动
            test_joints_1 = base_joints.copy()
            test_joints_1[0] += delta_angle  # 第一个关节正向运动10度
            
            print(f"使用goto_joint测试关节1正向运动{delta_angle}度...")
            robot.goto_joint(test_joints_1, speed=30.0, acc=30.0, radius=0.0)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 测试第一个关节反向运动
            test_joints_2 = base_joints.copy()
            test_joints_2[0] -= delta_angle  # 第一个关节反向运动10度
            
            print(f"使用goto_joint测试关节1反向运动{delta_angle}度...")
            robot.goto_joint(test_joints_2, speed=30.0, acc=30.0, radius=0.0)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 回到基准位置
            print(f"回到基准位置...")
            robot.goto_joint(base_joints, speed=30.0, acc=30.0, radius=0.0)
            
            print("✓ goto_joint关节运动测试完成")
            
        except Exception as e:
            print(f"⚠ goto_joint关节运动测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 7. 使用goto_delta_joint进行关节增量运动测试
        print("\n[7] 使用goto_delta_joint进行关节增量运动测试...")
        try:
            # 获取当前关节角度作为基准
            base_joints = robot.get_current_joint_positions()
            print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                  f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
            
            # 设置小范围偏移量（单位：度）
            delta_angle = 5.0  # 5度的小幅运动
            
            # 测试第一个关节的正向增量运动
            delta_joints_1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            delta_joints_1[0] = delta_angle  # 第一个关节正向运动5度
            
            print(f"使用goto_delta_joint测试关节1正向增量运动{delta_angle}度...")
            robot.goto_delta_joint(delta_joints_1, speed=30.0, acc=30.0, radius=0.0)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 测试第一个关节的反向增量运动
            delta_joints_2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            delta_joints_2[0] = -delta_angle  # 第一个关节反向运动5度
            
            print(f"使用goto_delta_joint测试关节1反向增量运动{delta_angle}度...")
            robot.goto_delta_joint(delta_joints_2, speed=30.0, acc=30.0, radius=0.0)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 回到基准位置
            print(f"回到基准位置...")
            delta_joints_home = [base_joints[i] - new_joints[i] for i in range(6)]
            robot.goto_delta_joint(delta_joints_home, speed=30.0, acc=30.0, radius=0.0)
            
            print("✓ goto_delta_joint关节增量运动测试完成")
            
        except Exception as e:
            print(f"⚠ goto_delta_joint关节增量运动测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 8. 旋转机械臂末端关节测试
        print("\n[8] 旋转机械臂末端关节测试...")
        try:
            # 先让机械臂运动到一个合适的姿态
            print("让机械臂运动到一个合适姿态...")
            robot.goto_joint([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], speed=30.0, acc=30.0, radius=0.0)
            
            # 获取当前关节角度
            current_joints = robot.get_current_joint_positions()
            print(f"当前关节角度: [{current_joints[0]:.2f}, {current_joints[1]:.2f}, {current_joints[2]:.2f}, "
                  f"{current_joints[3]:.2f}, {current_joints[4]:.2f}, {current_joints[5]:.2f}]")
            
            # 测试末端关节旋转（第6个关节）- 旋转90度
            print("测试末端关节旋转90度...")
            end_effector_joints = current_joints.copy()
            end_effector_joints[5] += 90.0  # 第6个关节旋转90度
            
            robot.goto_joint(end_effector_joints, speed=30.0, acc=30.0, radius=0.0)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"旋转后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 回到原位
            print("回到初始姿态...")
            robot.goto_joint(current_joints, speed=30.0, acc=30.0, radius=0.0)
            
            print("✓ 末端关节旋转测试完成")
            
        except Exception as e:
            print(f"⚠ 末端关节旋转测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 9. 穿插夹爪测试 - 在机械臂运动中间进行夹爪操作
        print("\n[9] 穿插夹爪测试 - 在机械臂运动中间进行夹爪操作...")
        try:
            # 先让机械臂运动到一个合适的位置
            print("让机械臂运动到一个合适的位置...")
            robot.goto_joint([0.0, 30.0, 20.0, 0.0, 0.0, 0.0], speed=30.0, acc=30.0, radius=0.0)
            
            # 测试夹爪位置读取
            print("测试夹爪位置读取...")
            position = gripper.get_gripper_position()
            if position >= 0:
                print(f"✓ 夹爪当前位置: {position}%")
            else:
                print("✗ 获取夹爪位置失败")
            
            # 测试夹爪幅度设置
            print("测试夹爪幅度设置...")
            if gripper.set_gripper_amplitude(0):
                print("✓ 设置夹爪幅度0%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪幅度0%失败")
            
            # 测试夹爪幅度设置
            print("测试夹爪幅度设置...")
            if gripper.set_gripper_amplitude(50):
                print("✓ 设置夹爪幅度50%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪幅度50%失败")
            
            # 测试夹爪幅度设置
            print("测试夹爪幅度设置...")
            if gripper.set_gripper_amplitude(100):
                print("✓ 设置夹爪幅度100%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪幅度100%失败")
            
            # 测试夹爪力度设置
            print("测试夹爪力度设置...")
            if gripper.set_gripper_force(50):
                print("✓ 设置夹爪力度50%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪力度50%失败")
            
            # 测试夹爪力度设置
            print("测试夹爪力度设置...")
            if gripper.set_gripper_force(100):
                print("✓ 设置夹爪力度100%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪力度100%失败")
            
            # 再次读取夹爪位置
            print("再次测试夹爪位置读取...")
            position = gripper.get_gripper_position()
            if position >= 0:
                print(f"✓ 最终夹爪位置: {position}%")
            else:
                print("✗ 最终读取夹爪位置失败")
            
            print("✓ 穿插夹爪测试完成")
            
        except Exception as e:
            print(f"⚠ 穿插夹爪测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 10. 使用goto_pose进行笛卡尔运动测试
        print("\n[10] 使用goto_pose进行笛卡尔运动测试...")
        try:
            #在运行pose测试前，让机械臂运动到一个有弯曲的关节姿态，防止奇异点
            print("正在让机械臂运动到一个有弯曲的关节姿态...")
            robot.goto_joint([30.0, 45.0, 45.0, 0.0, 45.0, 0.0], speed=30.0, acc=30.0, radius=0.0)

            # 获取当前位置作为起点
            current_cartesian = robot.get_current_position()[1]  # 获取笛卡尔位置
            print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                  f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
            
            # 使用更安全的笛卡尔运动测试 - 在当前X,Y平面内移动一小段距离
            target_cartesian = current_cartesian.copy()
            target_cartesian[0] += 30.0  # X轴增加30mm
            target_cartesian[1] += 20.0  # Y轴增加20mm
            
            print(f"使用goto_pose执行笛卡尔运动到X轴+30mm, Y轴+20mm的位置...")
            robot.goto_pose(target_cartesian, speed=30.0, acc=30.0, radius=0.0)
            
            # 检查运动后的笛卡尔位置
            final_cartesian = robot.get_current_position()[1]
            print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                  f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
            
            # 回到起始位置
            print(f"回到起始位置...")
            robot.goto_pose(current_cartesian, speed=30.0, acc=30.0, radius=0.0)
            
            print("✓ goto_pose笛卡尔运动测试完成")
            
        except Exception as e:
            print(f"⚠ goto_pose笛卡尔运动测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 11. 穿插夹爪测试 - 在机械臂运动中间进行夹爪操作
        print("\n[11] 穿插夹爪测试 - 在机械臂运动中间进行夹爪操作...")
        try:
            # 先让机械臂运动到一个合适的位置
            print("让机械臂运动到一个合适的位置...")
            robot.goto_joint([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], speed=30.0, acc=30.0, radius=0.0)
            
            # 测试夹爪位置读取
            print("测试夹爪位置读取...")
            position = gripper.get_gripper_position()
            if position >= 0:
                print(f"✓ 夹爪当前位置: {position}%")
            else:
                print("✗ 获取夹爪位置失败")
            
            # 测试夹爪幅度设置
            print("测试夹爪幅度设置...")
            if gripper.set_gripper_amplitude(0):
                print("✓ 设置夹爪幅度0%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪幅度0%失败")
            
            # 测试夹爪幅度设置
            print("测试夹爪幅度设置...")
            if gripper.set_gripper_amplitude(50):
                print("✓ 设置夹爪幅度50%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪幅度50%失败")
            
            # 测试夹爪幅度设置
            print("测试夹爪幅度设置...")
            if gripper.set_gripper_amplitude(100):
                print("✓ 设置夹爪幅度100%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪幅度100%失败")
            
            # 测试夹爪力度设置
            print("测试夹爪力度设置...")
            if gripper.set_gripper_force(50):
                print("✓ 设置夹爪力度50%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪力度50%失败")
            
            # 测试夹爪力度设置
            print("测试夹爪力度设置...")
            if gripper.set_gripper_force(100):
                print("✓ 设置夹爪力度100%成功")
                time.sleep(1)
            else:
                print("✗ 设置夹爪力度100%失败")
            
            # 再次读取夹爪位置
            print("再次测试夹爪位置读取...")
            position = gripper.get_gripper_position()
            if position >= 0:
                print(f"✓ 最终夹爪位置: {position}%")
            else:
                print("✗ 最终读取夹爪位置失败")
            
            print("✓ 穿插夹爪测试完成")
            
        except Exception as e:
            print(f"⚠ 穿插夹爪测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 12. 使用goto_delta进行笛卡尔增量运动测试
        print("\n[12] 使用goto_delta进行笛卡尔增量运动测试...")
        try:
            # 获取当前位置作为起点
            current_cartesian = robot.get_current_position()[1]  # 获取笛卡尔位置
            print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                  f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
            
            # 定义增量运动
            delta_cartesian = [20.0, 15.0, 0.0, 0.0, 0.0, 0.0]  # X轴增加20mm, Y轴增加15mm
            
            print(f"使用goto_delta执行笛卡尔增量运动X轴+20mm, Y轴+15mm...")
            robot.goto_delta(delta_cartesian, speed=30.0, acc=30.0, radius=0.0)
            
            # 检查运动后的笛卡尔位置
            final_cartesian = robot.get_current_position()[1]
            print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                  f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
            
            # 反向增量运动回到起始位置附近
            delta_cartesian_back = [-20.0, -15.0, 0.0, 0.0, 0.0, 0.0]
            print(f"使用goto_delta执行笛卡尔反向增量运动回到起始位置附近...")
            robot.goto_delta(delta_cartesian_back, speed=30.0, acc=30.0, radius=0.0)
            
            print("✓ goto_delta笛卡尔增量运动测试完成")
            
        except Exception as e:
            print(f"⚠ goto_delta笛卡尔增量运动测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 13. 速度比测试
        print("\n[13] 速度比测试...")
        try:
            # 测试不同的速度比
            speed_ratios = [0.1, 0.3, 0.5, 1.0]
            for ratio in speed_ratios:
                print(f"设置速度比为 {ratio}...")
                robot.set_override(ratio)
                current_ratio = robot.get_override()
                print(f"当前实际速度比: {current_ratio:.2f}")
                
                # 使用goto_joint进行简单的关节运动测试
                base_joints = robot.get_current_joint_positions()
                test_joints = base_joints.copy()
                test_joints[0] += 5.0  # 小幅运动
                
                print(f"使用速度比 {ratio} 执行goto_joint运动...")
                robot.goto_joint(test_joints, speed=50.0, acc=50.0, radius=0.0)
                
                print(f"速度比 {ratio} 测试完成")
            
            print("✓ 速度比测试完成")
            
        except Exception as e:
            print(f"⚠ 速度比测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 14. 测试完成
        print("\n[14] 测试完成")
        try:
            joint_pos, cartesian_pos = robot.get_current_position()
            print(f"最终笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                  f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
        except Exception as e:
            print(f"⚠ 读取最终位置失败: {e}")
        
        print("\n" + "=" * 60)
        print("使用goto接口的运动测试完成!")
        print("测试参数:")
        print("  速度: 30 (默认值)")
        print("  加速度: 30 (默认值)")
        print("  过渡半径: 0 (默认值)")
        print("=" * 60)
        time.sleep(5)

        # 运行完所有测试后，让机械臂回到待机姿态
        print("\n[15] 让机械臂回到待机姿态...")
        robot.goto_joint(STANDBY_JOINTS, speed=30.0, acc=30.0, radius=0.0)
        print("✓ 机械臂已回到待机姿态")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 安全关闭
        print("\n[15] 安全关闭...")
        try:
            # 去使能
            robot.disable()
            
            # 断开连接
            robot.disconnect()
            print("✓ 机器人已安全关闭")
        except Exception as e:
            print(f"✗ 关闭时出错: {e}")
        
        print("\n" + "=" * 60)
        print("测试结束")
        print("=" * 60)

if __name__ == "__main__":
    main()
