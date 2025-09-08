#!/usr/bin/env python3
"""
机器人控制器封装模块
基于现有的lib/robot_controller.py封装，提供统一的接口
"""

import logging
import time
import sys
import os
from typing import List, Tuple, Union

# 添加项目根目录到Python路径，以便能够正确导入lib模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.robot_controller import RobotController
from lib.exceptions import RobotError, RobotStateError, RobotTimeoutError


class RobotControllerWrapper:
    """机器人控制器封装类"""
    
    def __init__(self, config: dict):
        """
        初始化机器人控制器
        
        Args:
            config (dict): 配置信息
        """
        self.config = config
        self.robot = RobotController(
            box_id=config.get('box_id', 0),
            robot_id=config.get('robot_id', 0)
        )
        self.logger = logging.getLogger(__name__)
        self.connected = False
    
    def connect(self) -> bool:
        """
        连接到机器人
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.logger.info(f"正在连接机器人 {self.config['ip']}:{self.config['port']}")
            self.robot.connect(
                self.config['ip'], 
                self.config['port'],
                timeout=self.config.get('timeout', 30.0)
            )
            self.connected = True
            self.logger.info("机器人连接成功")
            return True
        except Exception as e:
            self.logger.error(f"机器人连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> bool:
        """
        断开机器人连接
        
        Returns:
            bool: 断开是否成功
        """
        try:
            if self.connected:
                self.robot.disconnect()
                self.connected = False
                self.logger.info("机器人连接已断开")
            return True
        except Exception as e:
            self.logger.error(f"机器人断开连接失败: {e}")
            return False
    
    def is_connected(self) -> bool:
        """
        检查机器人是否已连接
        
        Returns:
            bool: 是否已连接
        """
        return self.connected and self.robot.is_connected()
    
    def enable(self) -> bool:
        """
        使能机器人
        
        Returns:
            bool: 使能是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法使能")
                return False
            self.robot.enable(timeout=self.config.get('timeout', 30.0))
            self.logger.info("机器人已使能")
            return True
        except Exception as e:
            self.logger.error(f"机器人使能失败: {e}")
            return False
    
    def disable(self) -> bool:
        """
        去使能机器人
        
        Returns:
            bool: 去使能是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法去使能")
                return False
            self.robot.disable(timeout=self.config.get('timeout', 30.0))
            self.logger.info("机器人已去使能")
            return True
        except Exception as e:
            self.logger.error(f"机器人去使能失败: {e}")
            return False
    
    def move_j(self, points: List[float], raw_acs_points: List[float],
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               timeout: float = 30.0) -> bool:
        """
        关节运动
        
        Args:
            points: 空间目标位置 [X, Y, Z, Rx, Ry, Rz]
            raw_acs_points: 关节目标位置 [J1, J2, J3, J4, J5, J6]
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            timeout: 运动超时时间（秒）
            
        Returns:
            bool: 运动是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法执行运动")
                return False
            self.robot.move_j(
                points, raw_acs_points, "TCP", "Base",
                speed, acc, radius, 1, 0, 0, 0, "0", timeout
            )
            self.logger.info("关节运动完成")
            return True
        except Exception as e:
            self.logger.error(f"关节运动失败: {e}")
            return False
    
    def move_l(self, points: List[float], raw_acs_points: List[float],
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               timeout: float = 30.0) -> bool:
        """
        直线运动
        
        Args:
            points: 空间目标位置 [X, Y, Z, Rx, Ry, Rz]
            raw_acs_points: 关节参考位置 [J1, J2, J3, J4, J5, J6]
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            timeout: 运动超时时间（秒）
            
        Returns:
            bool: 运动是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法执行运动")
                return False
            self.robot.move_l(
                points, raw_acs_points, "TCP", "Base",
                speed, acc, radius, 0, 0, 0, "0", timeout
            )
            self.logger.info("直线运动完成")
            return True
        except Exception as e:
            self.logger.error(f"直线运动失败: {e}")
            return False
    
    def get_current_position(self) -> Tuple[List[float], List[float]]:
        """
        获取当前位置信息
        
        Returns:
            Tuple[List[float], List[float]]: (关节坐标, 笛卡尔坐标)
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法获取位置信息")
                return [], []
            return self.robot.get_current_position()
        except Exception as e:
            self.logger.error(f"获取位置信息失败: {e}")
            return [], []
    
    def get_current_joint_positions(self) -> List[float]:
        """
        获取当前关节位置
        
        Returns:
            List[float]: 关节位置 [J1, J2, J3, J4, J5, J6]
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法获取关节位置")
                return []
            return self.robot.get_current_joint_positions()
        except Exception as e:
            self.logger.error(f"获取关节位置失败: {e}")
            return []
    
    def set_override(self, vel: float) -> bool:
        """
        设置速度比
        
        Args:
            vel (float): 速度比 (0.01~1.0)
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法设置速度比")
                return False
            self.robot.set_override(vel)
            self.logger.info(f"速度比设置为 {vel}")
            return True
        except Exception as e:
            self.logger.error(f"设置速度比失败: {e}")
            return False
    
    def stop(self) -> bool:
        """
        停止机器人运动
        
        Returns:
            bool: 停止是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法停止运动")
                return False
            self.robot.stop()
            self.logger.info("机器人运动已停止")
            return True
        except Exception as e:
            self.logger.error(f"停止机器人运动失败: {e}")
            return False
    
    def reset(self) -> bool:
        """
        复位机器人
        
        Returns:
            bool: 复位是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法复位")
                return False
            self.robot.reset()
            self.logger.info("机器人已复位")
            return True
        except Exception as e:
            self.logger.error(f"机器人复位失败: {e}")
            return False
    
    def goto_pose(self, pose: List[float], speed: float = 50.0, 
                  acc: float = 50.0, radius: float = 50.0) -> bool:
        """
        运动到指定末端6d姿态
        
        Args:
            pose: 末端6d姿态 [X, Y, Z, Rx, Ry, Rz]
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            
        Returns:
            bool: 运动是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法执行运动")
                return False
            self.robot.goto_pose(pose, speed=speed, acc=acc, radius=radius)
            self.logger.info("运动到指定姿态完成")
            return True
        except Exception as e:
            self.logger.error(f"运动到指定姿态失败: {e}")
            return False
    
    def goto_joint(self, joint_positions: List[float], 
                   speed: float = 50.0, acc: float = 50.0, radius: float = 50.0) -> bool:
        """
        运动到指定关节位置
        
        Args:
            joint_positions: 关节位置 [J1, J2, J3, J4, J5, J6]
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            
        Returns:
            bool: 运动是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法执行运动")
                return False
            self.robot.goto_joint(joint_positions, speed=speed, acc=acc, radius=radius)
            self.logger.info("运动到指定关节位置完成")
            return True
        except Exception as e:
            self.logger.error(f"运动到指定关节位置失败: {e}")
            return False
    
    def electrify(self) -> bool:
        """
        机器人上电
        
        Returns:
            bool: 上电是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法上电")
                return False
            self.robot.electrify()
            self.logger.info("机器人已成功上电")
            return True
        except Exception as e:
            self.logger.error(f"机器人上电失败: {e}")
            return False
    
    def blackout(self) -> bool:
        """
        机器人断电
        
        Returns:
            bool: 断电是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法断电")
                return False
            self.robot.blackout()
            self.logger.info("机器人已成功断电")
            return True
        except Exception as e:
            self.logger.error(f"机器人断电失败: {e}")
            return False
    
    def get_current_state(self) -> int:
        """
        获取机器人当前状态
        
        Returns:
            int: 当前状态码
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法获取状态")
                return -1
            return self.robot.get_current_state()
        except Exception as e:
            self.logger.error(f"获取机器人状态失败: {e}")
            return -1
    
    def get_state_description(self, state: int) -> str:
        """
        获取状态描述
        
        Args:
            state (int): 状态码
            
        Returns:
            str: 状态描述
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法获取状态描述")
                return ""
            return self.robot.get_state_description(state)
        except Exception as e:
            self.logger.error(f"获取状态描述失败: {e}")
            return ""
    
    def is_ready(self) -> bool:
        """
        检查机器人是否就绪
        
        Returns:
            bool: 是否就绪
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法检查就绪状态")
                return False
            return self.robot.is_ready()
        except Exception as e:
            self.logger.error(f"检查就绪状态失败: {e}")
            return False
    
    def is_moving(self) -> bool:
        """
        检查机器人是否正在运动
        
        Returns:
            bool: 是否正在运动
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法检查运动状态")
                return False
            return self.robot.is_moving()
        except Exception as e:
            self.logger.error(f"检查运动状态失败: {e}")
            return False
    
    def wait_for_motion_done(self, timeout: float = 30.0) -> bool:
        """
        等待机器人运动完成
        
        Args:
            timeout (float): 等待超时时间（秒）
            
        Returns:
            bool: 是否运动完成
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法等待运动完成")
                return False
            return self.robot.wait_for_motion_done(timeout)
        except Exception as e:
            self.logger.error(f"等待运动完成失败: {e}")
            return False
    
    def get_override(self) -> float:
        """
        获取当前速度比
        
        Returns:
            float: 当前速度比
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法获取速度比")
                return -1.0
            return self.robot.get_override()
        except Exception as e:
            self.logger.error(f"获取速度比失败: {e}")
            return -1.0
    
    def goto_delta(self, delta_pose: List[float], tcp: List[float] = None, ucs: List[float] = None,
                   speed: float = 50.0, acc: float = 50.0, radius: float = 50.0) -> bool:
        """
        运动到指定末端6d姿态的增量位置
        
        Args:
            delta_pose: 末端6d姿态增量 [dX, dY, dZ, dRx, dRy, dRz]
            tcp: 工具坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            ucs: 用户坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            speed: 速度，默认为50.0
            acc: 加速度，默认为50.0
            radius: 过渡半径，默认为50.0
            
        Returns:
            bool: 运动是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法执行运动")
                return False
            self.robot.goto_delta(delta_pose, tcp, ucs, speed, acc, radius)
            self.logger.info("增量运动到指定姿态完成")
            return True
        except Exception as e:
            self.logger.error(f"增量运动到指定姿态失败: {e}")
            return False
    
    def goto_delta_joint(self, delta_joints: List[float],
                         speed: float = 50.0, acc: float = 50.0, radius: float = 50.0) -> bool:
        """
        运动到指定关节位置的增量位置
        
        Args:
            delta_joints: 关节位置增量 [dJ1, dJ2, dJ3, dJ4, dJ5, dJ6]
            speed: 速度，默认为50.0
            acc: 加速度，默认为50.0
            radius: 过渡半径，默认为50.0
            
        Returns:
            bool: 运动是否成功
        """
        try:
            if not self.connected:
                self.logger.error("机器人未连接，无法执行运动")
                return False
            self.robot.goto_delta_joint(delta_joints, speed, acc, radius)
            self.logger.info("增量运动到指定关节位置完成")
            return True
        except Exception as e:
            self.logger.error(f"增量运动到指定关节位置失败: {e}")
            return False
