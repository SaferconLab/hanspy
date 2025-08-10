#!/usr/bin/env python3
"""
HansRobot 运动测试脚本
使用CPS_wrapper.py直接调用API
IP: 192.168.31.88, Port: 10003
"""

import time
import sys
from wrapper.CPS_wrapper import CPSClient

# 测试参数 - 来自Program.cs
ROBOT_IP = "192.168.31.88"
ROBOT_PORT = 10003

print("=" * 60)
print("HansRobot 运动测试")
print("使用CPS_wrapper.py直接调用API")
print("=" * 60)

# 创建CPS客户端
cps = CPSClient()

def wait_for_robot_ready(box_id=0, rbt_id=0, timeout=30):
    """等待机器人就绪"""
    print("等待机器人状态就绪...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = []
        ret = cps.HRIF_ReadCurFSMFromCPS(box_id, rbt_id, result)
        current_state = result[0] if result else None
        print(f"当前状态码: {result[0] if result else '无结果'} (错误码: {ret})")
        if int(ret) == 0 and len(result) > 0 and int(result[0]) == 33:  # 33表示机器人就绪
            print("✓ 机器人已就绪")
            return True
        time.sleep(0.1)
    print("✗ 等待机器人就绪超时")
    return False

try:
    # 1. 连接机器人
    print("\n[1] 连接机器人...")
    ret = cps.HRIF_Connect(0, ROBOT_IP, ROBOT_PORT)
    if ret != 0:
        raise Exception(f"连接失败，错误码: {ret}")
    print("✓ 连接成功")
    
    # # 2. 连接控制器
    # print("\n[2] 连接控制器...")
    # ret = cps.HRIF_Connect2Controller(0)
    # if ret != 0:
    #     raise Exception(f"连接控制器失败，错误码: {ret}")
    # print("✓ 控制器连接成功")
    
    # 3. 检查并准备机器人
    print("\n[3] 检查机器人状态...")
    result = []
    ret = cps.HRIF_ReadCurFSMFromCPS(0, 0, result)
    if ret != 0:
        raise Exception(f"读取状态失败，错误码: {ret}")
    
    if len(result) > 0:
        print(type(result[0]))
        current_state = int(result[0])
        print(f"当前状态码: {current_state}")
        
        # 如果状态不是33（就绪），则进行使能
        if current_state != 33:
            print("机器人未就绪，正在使能...")
            
            ret = cps.HRIF_GrpEnable(0, 0)
            if ret != 0:
                raise Exception(f"使能失败，错误码: {ret}")
            
            # 等待机器人就绪
            if not wait_for_robot_ready():
                raise Exception("机器人未能就绪")
    
    # 4. 获取当前位置
    print("\n[4] 获取当前位置...")
    result = []
    ret = cps.HRIF_ReadActPos(0, 0, result)
    if ret != 0:
        raise Exception(f"读取位置失败，错误码: {ret}")
    
    if len(result) >= 6:
        current_pos =[float(x) for x in result[:6]]
        print(f"当前笛卡尔位置: [X={current_pos[0]:.2f}, Y={current_pos[1]:.2f}, Z={current_pos[2]:.2f}, "
              f"Rx={current_pos[3]:.2f}, Ry={current_pos[4]:.2f}, Rz={current_pos[5]:.2f}]")
    
    # 5. 设置速度比
    print("\n[5] 设置速度比...")
    ret = cps.HRIF_SetOverride(0, 0, 0.2)
    if ret != 0:
        print(f"⚠ 设置速度比失败，错误码: {ret}，继续执行...")
    else:
        print("✓ 速度比设置为0.2")
    
    # 6. 获取当前关节角度
    print("\n[6] 关节角度信息显示（在 waypoint 前面）...")
    result = []
    ret = cps.HRIF_ReadActJointPos(0, 0, result)
    if ret != 0:
        print(f"⚠ 读取关节角度失败，错误码: {ret}")
    else:
        if len(result) >= 6:
            current_joints =[float(x) for x in result[:6]]
            print(f"当前关节角度: [{current_joints[0]:.2f}, {current_joints[1]:.2f}, {current_joints[2]:.2f}, "
                  f"{current_joints[3]:.2f}, {current_joints[4]:.2f}, {current_joints[5]:.2f}]")
    
    # 7. 关节小范围运动测试
    print("\n[7] 关节小范围运动测试...")
    
    # 获取当前关节角度作为基准
    result = []
    ret = cps.HRIF_ReadActJointPos(0, 0, result)
    if ret != 0:
        print(f"⚠ 读取关节角度失败，错误码: {ret}")
    else:
        if len(result) >= 6:
            base_joints = [float(x) for x in result[:6]]
            print(f"基准关节角度: [{base_joints[0]:.2f}, {base_joints[1]:.2f}, {base_joints[2]:.2f}, "
                  f"{base_joints[3]:.2f}, {base_joints[4]:.2f}, {base_joints[5]:.2f}]")
            
            # 设置小范围偏移量（单位：度）
            delta_angle = 5.0  # 5度的小幅运动
            
            # 测试第一个关节的小范围运动
            test_joints_1 = base_joints.copy()
            test_joints_1[0] += delta_angle  # 第一个关节正向运动5度
            
            # 定义空间目标位置
            Point = [ 0, 0, 90, 0, 90, 0]
            # 定义关节目标位置
            RawACSpoints = [ 0, 0, 90, 0, 90, 0]
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
            nIsUseJoint= 1
            # 定义是否使用检测 DI 停止
            nIsSeek = 0
            # 定义检测的 DI 索引
            nIOBit = 0
            # 定义检测的 DI 状态
            nIOState = 0
            # 定义路点 ID
            strCmdID = "0"
            # 执行路点运动
            print(f"测试关节1...")
            ret = cps._client.HRIF_MoveJ(0,0, Point, RawACSpoints, sTcpName , sUcsName, dVelocity, dAcc,
            dRadius,nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            if ret != 0:
                print(f"⚠ 关节运动失败，错误码: {ret}")
            else:
                # 等待运动完成
                time.sleep(5)
                
                # 读取运动后位置
                result = []
                cps.HRIF_ReadActJointPos(0, 0, result)
                if len(result) >= 6:
                    new_joints = [float(x) for x in result[:6]]
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 测试第一个关节反向运动
            test_joints_2 = base_joints.copy()
            test_joints_2[0] -= delta_angle  # 第一个关节反向运动5度
            
                    # 定义空间目标位置
            Point = [ 0, 0, 0, 0, 0, 0]
            # 定义关节目标位置
            RawACSpoints = [ 0, 0, 0, 0, 0, 0]
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
            nIsUseJoint= 1
            # 定义是否使用检测 DI 停止
            nIsSeek = 0
            # 定义检测的 DI 索引
            nIOBit = 0
            # 定义检测的 DI 状态
            nIOState = 0
            # 定义路点 ID
            strCmdID = "0"
            # 执行路点运动
            print(f"测试关节2反向运动...")
            ret = cps._client.HRIF_MoveJ(0,0, Point, RawACSpoints, sTcpName , sUcsName, dVelocity, dAcc,
            dRadius,nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)

            if ret != 0:
                print(f"⚠ 关节运动失败，错误码: {ret}")
            else:
                # 等待运动完成
                time.sleep(5)
                
                # 读取运动后位置
                result = []
                cps.HRIF_ReadActJointPos(0, 0, result)
                if len(result) >= 6:
                    new_joints = [float(x) for x in result[:6]]
                    print(f"运动后关节角度: [{new_joints[0]:.2f}, {new_joints[1]:.2f}, {new_joints[2]:.2f}, "
                          f"{new_joints[3]:.2f}, {new_joints[4]:.2f}, {new_joints[5]:.2f}]")
            
            # 回到基准位置
            print(f"回到基准位置...")
            ret = cps.HRIF_MoveJ(0,0, Point, RawACSpoints, sTcpName , sUcsName, dVelocity, dAcc,
            dRadius,nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
            if ret != 0:
                print(f"⚠ 回基准位置失败，错误码: {ret}")
            else:
                time.sleep(5)
                print("✓ 关节小范围运动测试完成")
    
    # 8. 测试完成
    print("\n[8] 测试完成")
    result = []
    ret = cps.HRIF_ReadActPos(0, 0, result)
    if ret == 0 and len(result) >= 6:
        final_pos = [float(x) for x in result[:6]]
        print(f"最终笛卡尔位置: [X={final_pos[0]:.2f}, Y={final_pos[1]:.2f}, Z={final_pos[2]:.2f}, "
              f"Rx={final_pos[3]:.2f}, Ry={final_pos[4]:.2f}, Rz={final_pos[5]:.2f}]")
    
    print("\n" + "=" * 60)
    print("运动测试完成!")
    print("测试参数:")
    print("  速度: 50 (来自Program.cs)")
    print("  加速度: 1000 (来自Program.cs)")
    print("  过渡半径: 0 (来自Program.cs)")
    print("注意: 原始参数可能导致运动超出安全范围，已改为小幅度测试")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # 9. 安全关闭
    print("\n[9] 安全关闭...")
    
    # 去使能
    cps.HRIF_GrpDisable(0, 0)
    # wait for disable
    while True:
        result = []
        ret = cps.HRIF_ReadCurFSMFromCPS(0, 0, result)
        if int(ret) != 0 or len(result) == 0:
            print(f"读取状态失败，错误码: {ret}")
            break
        if len(result) > 0 and int(result[0]) == 24:
            print("✓ 去使能成功")
            print(f"当前状态码: {result[0]}")
            break
        else:
            print(f"当前状态码: {result[0] if result else '无结果'} (错误码: {ret})")
            cps.HRIF_GrpDisable(0, 0)
        time.sleep(1)
    
    # 断电
    # cps.HRIF_BlackOut(0)
    # time.sleep(1)
    
    # 断开连接
    cps.HRIF_DisConnect(0)
    print("✓ 机器人已安全关闭")

    print("\n" + "=" * 60)
    print("测试结束")
    print("=" * 60)
