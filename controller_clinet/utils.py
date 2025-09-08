#!/usr/bin/env python3
"""
控制器客户端工具模块
提供一些实用的工具函数
"""

import time
from typing import List, Tuple, Optional
from .client import ControllerClient


def wait_for_robot_ready(client: ControllerClient, timeout: float = 30.0) -> bool:
    """
    等待机器人进入就绪状态
    
    Args:
        client (ControllerClient): 控制器客户端实例
        timeout (float): 超时时间（秒）
        
    Returns:
        bool: 是否成功就绪
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            is_ready = client.is_ready()
            if is_ready is True:
                return True
            elif is_ready is False:
                time.sleep(0.1)
                continue
            else:
                # 获取状态失败
                return False
        except Exception:
            return False
    return False


def wait_for_motion_complete(client: ControllerClient, timeout: float = 30.0) -> bool:
    """
    等待机器人运动完成
    
    Args:
        client (ControllerClient): 控制器客户端实例
        timeout (float): 超时时间（秒）
        
    Returns:
        bool: 是否成功完成
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            is_moving = client.is_moving()
            if is_moving is False:
                return True
            elif is_moving is True:
                time.sleep(0.1)
                continue
            else:
                # 获取状态失败
                return False
        except Exception:
            return False
    return False


def move_to_safe_position(client: ControllerClient, 
                         joint_positions: List[float] = None,
                         pose: List[float] = None) -> bool:
    """
    移动到安全位置
    
    Args:
        client (ControllerClient): 控制器客户端实例
        joint_positions (List[float]): 关节位置，如果提供则使用goto_joint
        pose (List[float]): 姿态位置，如果提供则使用goto_pose
        
    Returns:
        bool: 是否成功移动
    """
    if joint_positions is not None:
        return client.goto_joint(joint_positions)
    elif pose is not None:
        return client.goto_pose(pose)
    else:
        # 默认移动到待机位置
        standby_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        return client.goto_joint(standby_position)


def safe_robot_operation(client: ControllerClient, 
                        operation_func, 
                        *args, 
                        **kwargs) -> Optional[bool]:
    """
    安全的机器人操作包装器
    
    Args:
        client (ControllerClient): 控制器客户端实例
        operation_func: 要执行的操作函数
        *args: 函数参数
        **kwargs: 函数关键字参数
        
    Returns:
        Optional[bool]: 操作结果，失败返回None
    """
    try:
        # 检查连接状态
        if not client.is_connected():
            print("错误: 客户端未连接到服务器")
            return None
        
        # 检查机器人是否已连接
        if client.get_state() not in [client.get_state().ROBOT_CONNECTED, client.get_state().ROBOT_ENABLED]:
            print("错误: 机器人未连接或未使能")
            return None
        
        # 执行操作
        result = operation_func(*args, **kwargs)
        return result
        
    except Exception as e:
        print(f"操作执行失败: {e}")
        return None


def create_sample_robot_trajectory() -> List[Tuple[List[float], List[float]]]:
    """
    创建示例机器人轨迹点
    
    Returns:
        List[Tuple[List[float], List[float]]]: 轨迹点列表，每个元素为(关节位置, 笛卡尔位置)
    """
    # 示例轨迹点
    trajectory = [
        ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        ([10.0, 0.0, 0.0, 0.0, 0.0, 0.0], [10.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        ([10.0, 10.0, 0.0, 0.0, 0.0, 0.0], [10.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
        ([0.0, 10.0, 0.0, 0.0, 0.0, 0.0], [0.0, 10.0, 0.0, 0.0, 0.0, 0.0]),
        ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
    ]
    return trajectory


def create_sample_gripper_sequence() -> List[int]:
    """
    创建示例夹爪操作序列
    
    Returns:
        List[int]: 夹爪幅度序列
    """
    # 示例夹爪操作序列
    sequence = [0, 50, 100, 50, 0]
    return sequence
