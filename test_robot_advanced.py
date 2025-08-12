#!/usr/bin/env python3
"""
HansRobot 运动测试脚本
使用RobotController高级接口
IP: 192.168.31.88, Port: 10003
"""

import time
import sys
import logging
from lib.robot_controller import RobotController

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 测试参数 - 来自Program.cs
ROBOT_IP = "192.168.31.88"
ROBOT_PORT = 10003

print("=" * 60)
print("HansRobot 运动测试")
print("使用RobotController高级接口")
print("=" * 60)

def main():
    # 创建机器人控制器实例
    robot = RobotController()
    
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
        
        # 3. 获取当前位置
        print("\n[3] 获取当前位置...")
        try:
            joint_pos, cartesian_pos = robot.get_current_position()
            print(f"当前关节位置: [{joint_pos[0]:.2f}, {joint_pos[1]:.2f}, {joint_pos[2]:.2f}, "
                  f"{joint_pos[3]:.2f}, {joint_pos[4]:.2f}, {joint_pos[5]:.2f}]")
            print(f"当前笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                  f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
        except Exception as e:
            print(f"⚠ 读取位置信息失败: {e}")
        
        # 4. 设置速度比
        print("\n[4] 设置速度比...")
        try:
            robot.set_override(0.2)
            print("✓ 速度比设置为0.2")
        except Exception as e:
            print(f"⚠ 设置速度比失败: {e}")
        
        # 5. 获取当前关节角度
        print("\n[5] 关节角度信息显示（在 waypoint 前面）...")
        try:
            current_joints = robot.get_current_joint_positions()
            print(f"当前关节角度: [{current_joints[0]:.2f}, {current_joints[1]:.2f}, {current_joints[2]:.2f}, "
                  f"{current_joints[3]:.2f}, {current_joints[4]:.2f}, {current_joints[5]:.2f}]")
        except Exception as e:
            print(f"⚠ 读取关节角度失败: {e}")
        
        # 6. 关节小范围运动测试
        print("\n[6] 关节小范围运动测试...")
        
        # 获取当前关节角度作为基准
        try:
            base_joints = robot.get_current_joint_positions()
            print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                  f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
            
            # 设置小范围偏移量（单位：度）
            delta_angle = 15.0  # 15度的小幅运动
            
            # 测试第一个关节的小范围运动
            test_joints_1 = base_joints.copy()
            test_joints_1[0] += delta_angle  # 第一个关节正向运动15度

            # 定义空间目标位置
            Point = [0, 0, 90, 0, 90, 0]
            # 定义关节目标位置
            RawACSpoints = test_joints_1
            # 定义工具坐标变量
            sTcpName = "TCP"
            # 定义用户坐标变量
            sUcsName = "Base"
            # 定义运动速度
            dVelocity = 50
            # 定义运动加速度
            dAcc = 50
            # 定义过渡半径
            dRadius = 50
            # 定义是否使用关节角度
            nIsUseJoint = 1
            # 定义是否使用检测DI停止
            nIsSeek = 0
            # 定义检测的DI索引
            nIOBit = 0
            # 定义检测的DI状态
            nIOState = 0
            # 定义路点ID
            strCmdID = "0"
            
            print(f"测试关节1正向运动{delta_angle}度...")
            robot.move_j(Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                        nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 测试第一个关节反向运动
            test_joints_2 = base_joints.copy()
            test_joints_2[0] -= delta_angle  # 第一个关节反向运动15度
            RawACSpoints = test_joints_2
            
            print(f"测试关节1反向运动{delta_angle}度...")
            robot.move_j(Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                        nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            
            # 读取运动后位置
            new_joints = robot.get_current_joint_positions()
            print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                  f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 回到基准位置
            print(f"回到基准位置...")
            RawACSpoints = base_joints
            robot.move_j(Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                        nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            
            # 测试其他关节的独立运动
            print("\n[6.1] 测试其他关节的独立运动...")
            for i in range(1, 6):  # 测试关节2到关节6
                test_joints = base_joints.copy()
                test_joints[i] += delta_angle  # 第i个关节正向运动
                
                print(f"测试关节{i+1}正向运动{delta_angle}度...")
                robot.move_j(Point, test_joints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                            nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
                
                # 读取运动后位置
                new_joints = robot.get_current_joint_positions()
                print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                      f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
                
                # 回到基准位置
                print(f"回到基准位置...")
                robot.move_j(Point, base_joints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                            nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            
            print("✓ 关节小范围运动测试完成")
            
        except Exception as e:
            print(f"⚠ 关节运动测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 7. 直线运动测试
        print("\n[7] 直线运动测试...")
        try:
            # 获取当前位置作为起点
            current_cartesian = robot.get_current_position()[1]  # 获取笛卡尔位置
            print(f"起始笛卡尔位置: [X={current_cartesian[0]:.2f}, Y={current_cartesian[1]:.2f}, Z={current_cartesian[2]:.2f}, "
                  f"Rx={current_cartesian[3]:.2f}, Ry={current_cartesian[4]:.2f}, Rz={current_cartesian[5]:.2f}]")
            
            # 使用更安全的直线运动测试 - 在当前X,Y平面内移动一小段距离
            target_cartesian = current_cartesian.copy()
            target_cartesian[0] += 50.0  # X轴增加50mm
            target_cartesian[1] += 30.0  # Y轴增加30mm
            
            # 转换为关节位置（这里简化处理，实际应用中需要正逆解）
            # 使用当前关节位置作为参考关节位置
            current_joints = robot.get_current_joint_positions()
            
            # 定义直线运动参数
            Point = target_cartesian
            RawACSpoints = current_joints  # 使用当前关节位置作为参考
            sTcpName = "TCP"
            sUcsName = "Base"
            dVelocity = 50
            dAcc = 50
            dRadius = 50
            nIsSeek = 0
            nIOBit = 0
            nIOState = 0
            strCmdID = "0"
            
            print(f"执行直线运动到X轴+50mm, Y轴+30mm的位置...")
            robot.move_l(Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                        nIsSeek, nIOBit, nIOState, strCmdID)
            
            # 检查运动后的笛卡尔位置
            final_cartesian = robot.get_current_position()[1]
            print(f"运动后笛卡尔位置: [X={final_cartesian[0]:.2f}, Y={final_cartesian[1]:.2f}, Z={final_cartesian[2]:.2f}, "
                  f"Rx={final_cartesian[3]:.2f}, Ry={final_cartesian[4]:.2f}, Rz={final_cartesian[5]:.2f}]")
            
            print("✓ 直线运动测试完成")
            
        except Exception as e:
            print(f"⚠ 直线运动测试失败: {e}")
            # 如果直线运动失败，我们继续执行后续测试，不影响整体测试流程
            print("跳过直线运动测试，继续执行其他测试...")
            import traceback
            traceback.print_exc()
        
        # 8. 速度比测试
        print("\n[8] 速度比测试...")
        try:
            # 测试不同的速度比
            speed_ratios = [0.1, 0.3, 0.5, 0.7, 1.0]
            for ratio in speed_ratios:
                print(f"设置速度比为 {ratio}...")
                robot.set_override(ratio)
                current_ratio = robot.get_override()
                print(f"当前实际速度比: {current_ratio:.2f}")
                
                # 简单的关节运动测试
                base_joints = robot.get_current_joint_positions()
                test_joints = base_joints.copy()
                test_joints[0] += 5.0  # 小幅运动
                
                Point = [0, 0, 90, 0, 90, 0]
                RawACSpoints = test_joints
                sTcpName = "TCP"
                sUcsName = "Base"
                dVelocity = 50
                dAcc = 50
                dRadius = 50
                nIsUseJoint = 1
                nIsSeek = 0
                nIOBit = 0
                nIOState = 0
                strCmdID = "0"
                
                print(f"使用速度比 {ratio} 执行关节运动...")
                robot.move_j(Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,
                            nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
                
                print(f"速度比 {ratio} 测试完成")
            
            print("✓ 速度比测试完成")
            
        except Exception as e:
            print(f"⚠ 速度比测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 9. 停止功能测试
        print("\n[9] 停止功能测试...")
        try:
            # 获取当前关节位置
            base_joints = robot.get_current_joint_positions()
            print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                  f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
            
            # 准备一个较长的运动路径
            test_joints = base_joints.copy()
            test_joints[0] += 90.0  # 较大角度运动
            
            Point = [0, 0, 90, 0, 90, 0]
            RawACSpoints = test_joints
            sTcpName = "TCP"
            sUcsName = "Base"
            dVelocity = 50
            dAcc = 50
            dRadius = 50
            nIsUseJoint = 1
            nIsSeek = 0
            nIOBit = 0
            nIOState = 0
            strCmdID = "0"
            
            print("启动长距离关节运动（模拟长时间运动）...")
            # 启动运动但不等待完成，然后立即停止
            robot.lib_wrapper.HRIF_MoveJ(
                robot.box_id, robot.robot_id, Point, RawACSpoints,
                sTcpName, sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            
            # 短暂等待让运动开始
            time.sleep(0.5)
            
            # 检查是否正在运动
            if robot.is_moving():
                print("检测到机器人正在运动，执行停止命令...")
                robot.stop()
                print("停止命令已发送")
                
                # 等待运动停止
                robot.wait_for_motion_done(10.0)
                print("✓ 停止功能测试完成")
            else:
                print("警告：运动未开始")
                
        except Exception as e:
            print(f"⚠ 停止功能测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 10. 测试完成
        print("\n[10] 测试完成")
        try:
            joint_pos, cartesian_pos = robot.get_current_position()
            print(f"最终笛卡尔位置: [X={cartesian_pos[0]:.2f}, Y={cartesian_pos[1]:.2f}, Z={cartesian_pos[2]:.2f}, "
                  f"Rx={cartesian_pos[3]:.2f}, Ry={cartesian_pos[4]:.2f}, Rz={cartesian_pos[5]:.2f}]")
        except Exception as e:
            print(f"⚠ 读取最终位置失败: {e}")
        
        print("\n" + "=" * 60)
        print("运动测试完成!")
        print("测试参数:")
        print("  速度: 50 (来自Program.cs)")
        print("  加速度: 50 (来自Program.cs)")
        print("  过渡半径: 50 (来自Program.cs)")
        print("=" * 60)
        time.sleep(5)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 8. 安全关闭
        print("\n[8] 安全关闭...")
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
