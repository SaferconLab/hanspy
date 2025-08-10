#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
机器人控制器模块
提供易用的机器人控制接口，包装CPS_wrapper.py的原始接口
实现"查询状态-发送指令-阻塞查询状态-根据返回的状态返回成功或异常处理"的模式
"""

import time
from typing import Optional, Tuple, List
from wrapper.CPS_wrapper import CPSClient
from .exceptions import RobotError, RobotStateError, RobotTimeoutError
from .status_monitor import RobotStatusMonitor

class RobotController:
    """机器人控制器类，提供易用的机器人控制接口"""
    
    def __init__(self, box_id: int = 0, robot_id: int = 0):
        """
        初始化机器人控制器
        
        Args:
            box_id (int): 电箱ID，默认为0
            robot_id (int): 机器人ID，默认为0
        """
        self.box_id = box_id
        self.robot_id = robot_id
        self.lib_wrapper = CPSClient()
        self.status_monitor = RobotStatusMonitor(self.lib_wrapper, box_id, robot_id)
        self.default_timeout = 30.0  # 默认超时时间（秒）
        self.default_check_interval = 0.5  # 默认状态检查间隔（秒）
    
    def connect(self, host: str, port: int, timeout: float = 30.0) -> bool:
        """
        连接机器人服务器
        
        Args:
            host (str): 机器人服务器IP地址
            port (int): 机器人服务器端口
            timeout (float): 连接超时时间（秒）
            
        Returns:
            bool: 连接是否成功
            
        Raises:
            RobotError: 连接失败时抛出异常
        """
        # 先检查是否已连接
        if self.is_connected():
            return True
            
        # 发送连接指令
        ret = self.lib_wrapper.HRIF_Connect(self.box_id, host, port)
        if ret != 0:
            raise RobotError(ret, f"连接机器人失败: {self._get_error_message(ret)}")
        
        # 等待连接完成
        if not self._wait_for_connection(timeout):
            raise RobotTimeoutError(-1, "连接超时")
            
        return True
    
    def disconnect(self) -> bool:
        """
        断开连接机器人服务器
        
        Returns:
            bool: 断开连接是否成功
            
        Raises:
            RobotError: 断开连接失败时抛出异常
        """
        ret = self.lib_wrapper.HRIF_DisConnect(self.box_id)
        if ret != 0:
            raise RobotError(ret, f"断开连接失败: {self._get_error_message(ret)}")
        return True
    
    def is_connected(self) -> bool:
        """
        检查机器人是否已连接
        
        Returns:
            bool: 是否已连接
        """
        return self.lib_wrapper.HRIF_IsConnected(self.box_id)
    
    def enable(self, timeout: float = 30.0) -> bool:
        """
        使能机器人
        
        Args:
            timeout (float): 使能超时时间（秒）
            
        Returns:
            bool: 使能是否成功
            
        Raises:
            RobotError: 使能失败时抛出异常
            RobotTimeoutError: 使能超时抛出异常
        """
        # 先检查是否已使能
        if self.status_monitor.is_enabled():
            print("机器人已处于使能状态")
            return True
            
        # 发送使能指令
        ret = self.lib_wrapper.HRIF_GrpEnable(self.box_id, self.robot_id)
        if ret != 0:
            raise RobotError(ret, f"使能机器人失败: {self._get_error_message(ret)}")
        
        # 等待机器人进入就绪状态
        if not self.status_monitor.wait_for_standby(timeout):
            raise RobotTimeoutError(-1, "使能超时，机器人未能进入就绪状态")
            
        return True
    
    def disable(self, timeout: float = 30.0) -> bool:
        """
        去使能机器人
        
        Args:
            timeout (float): 去使能超时时间（秒）
            
        Returns:
            bool: 去使能是否成功
            
        Raises:
            RobotError: 去使能失败时抛出异常
            RobotTimeoutError: 去使能超时抛出异常
        """
        # 先检查是否已去使能
        state = self.status_monitor.get_current_state()
        if state == RobotStatusMonitor.STATE_DISABLE:
            print("机器人已处于去使能状态")
            return True
            
        # 只有在就绪状态(33)下才能发送去使能指令，等待机器人进入去使能状态wait_for_state
        if state != RobotStatusMonitor.STATE_STANDBY:
            if not self.status_monitor.wait_for_state(
                RobotStatusMonitor.STATE_STANDBY, timeout):
                current_state = self.status_monitor.get_current_state()
                description = self.status_monitor.get_state_description(current_state)
                raise RobotStateError(
                    -1, f"去使能失败，当前状态不允许去使能: {current_state} ({description})")
            
        # 发送去使能指令
        ret = self.lib_wrapper.HRIF_GrpDisable(self.box_id, self.robot_id)
        if ret != 0:
            raise RobotError(ret, f"去使能机器人失败，指令发送失败: {self._get_error_message(ret)}")
        else:
            print("去使能指令发送成功，等待机器人进入去使能状态")
        
        # 等待机器人进入去使能状态
        if not self.status_monitor.wait_for_state(
            RobotStatusMonitor.STATE_DISABLE, timeout):
            raise RobotTimeoutError(-1, "去使能超时，机器人未能进入去使能状态")
            
        return True
    
    def electrify(self) -> bool:
        """
        机器人上电
        
        Returns:
            bool: 上电是否成功
            
        Raises:
            RobotError: 上电失败时抛出异常
        """
        ret = self.lib_wrapper.HRIF_Electrify(self.box_id)
        if ret != 0:
            raise RobotError(ret, f"机器人上电失败: {self._get_error_message(ret)}")
        return True
    
    def blackout(self) -> bool:
        """
        机器人断电
        
        Returns:
            bool: 断电是否成功
            
        Raises:
            RobotError: 断电失败时抛出异常
        """
        ret = self.lib_wrapper.HRIF_BlackOut(self.box_id)
        if ret != 0:
            raise RobotError(ret, f"机器人断电失败: {self._get_error_message(ret)}")
        return True
    
    def get_current_state(self) -> int:
        """
        获取机器人当前状态
        
        Returns:
            int: 当前状态码
            
        Raises:
            RobotError: 获取状态失败时抛出异常
        """
        return self.status_monitor.get_current_state()
    
    def get_state_description(self, state: int) -> str:
        """
        获取状态描述
        
        Args:
            state (int): 状态码
            
        Returns:
            str: 状态描述
        """
        return self.status_monitor.get_state_description(state)
    
    def is_ready(self) -> bool:
        """
        检查机器人是否就绪
        
        Returns:
            bool: 是否就绪
        """
        return self.status_monitor.is_ready()
    
    def is_moving(self) -> bool:
        """
        检查机器人是否正在运动
        
        Returns:
            bool: 是否正在运动
        """
        return self.status_monitor.is_moving()
    
    def wait_for_motion_done(self, timeout: float = 30.0) -> bool:
        """
        等待机器人运动完成
        
        Args:
            timeout (float): 等待超时时间（秒）
            
        Returns:
            bool: 是否运动完成
            
        Raises:
            RobotTimeoutError: 等待超时抛出异常
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if not self.is_moving():
                return True
            time.sleep(self.default_check_interval)
        
        raise RobotTimeoutError(-1, "等待运动完成超时")
    
    def move_j(self, points: List[float], raw_acs_points: List[float], 
               tcp: str = "TCP", ucs: str = "Base", 
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               is_joint: int = 1, is_seek: int = 0, bit: int = 0, state: int = 0,
               cmd_id: str = "0", timeout: float = 30.0) -> bool:
        """
        关节运动
        
        Args:
            points: 空间目标位置 [X, Y, Z, Rx, Ry, Rz]
            raw_acs_points: 关节目标位置 [J1, J2, J3, J4, J5, J6]
            tcp: 工具坐标名称
            ucs: 用户坐标名称
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            is_joint: 是否使用关节坐标 (0/1)
            is_seek: 是否检测DI停止 (0/1)
            bit: 检测的DI索引
            state: 检测的DI状态
            cmd_id: 命令ID
            timeout: 运动超时时间（秒）
            
        Returns:
            bool: 运动是否成功
            
        Raises:
            RobotError: 运动失败时抛出异常
            RobotTimeoutError: 运动超时抛出异常
        """
        # 确保机器人已使能
        if not self.status_monitor.is_enabled():
            raise RobotStateError(-1, "机器人未使能，无法执行运动")
        
        # 发送运动指令
        ret = self.lib_wrapper.HRIF_MoveJ(
            self.box_id, self.robot_id, points, raw_acs_points,
            tcp, ucs, speed, acc, radius, is_joint, is_seek, bit, state, cmd_id)
        
        if ret != 0:
            raise RobotError(ret, f"关节运动失败: {self._get_error_message(ret)}")
        
        # 等待运动完成
        self.wait_for_motion_done(timeout)
        return True
    
    def move_l(self, points: List[float], raw_acs_points: List[float],
               tcp: str = "TCP", ucs: str = "Base",
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               is_seek: int = 0, bit: int = 0, state: int = 0,
               cmd_id: str = "0", timeout: float = 30.0) -> bool:
        """
        直线运动
        
        Args:
            points: 空间目标位置 [X, Y, Z, Rx, Ry, Rz]
            raw_acs_points: 关节参考位置 [J1, J2, J3, J4, J5, J6]
            tcp: 工具坐标名称
            ucs: 用户坐标名称
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            is_seek: 是否检测DI停止 (0/1)
            bit: 检测的DI索引
            state: 检测的DI状态
            cmd_id: 命令ID
            timeout: 运动超时时间（秒）
            
        Returns:
            bool: 运动是否成功
            
        Raises:
            RobotError: 运动失败时抛出异常
            RobotTimeoutError: 运动超时抛出异常
        """
        # 确保机器人已使能
        if not self.status_monitor.is_enabled():
            raise RobotStateError(-1, "机器人未使能，无法执行运动")
        
        # 发送运动指令
        ret = self.lib_wrapper.HRIF_MoveL(
            self.box_id, self.robot_id, points, raw_acs_points,
            tcp, ucs, speed, acc, radius, is_seek, bit, state, cmd_id)
        
        if ret != 0:
            raise RobotError(ret, f"直线运动失败: {self._get_error_message(ret)}")
        
        # 等待运动完成
        self.wait_for_motion_done(timeout)
        return True
    
    def get_current_position(self) -> Tuple[List[float], List[float]]:
        """
        获取当前位置信息
        
        Returns:
            Tuple[List[float], List[float]]: (关节坐标, 笛卡尔坐标)
            
        Raises:
            RobotError: 获取位置信息失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_ReadActPos(self.box_id, self.robot_id, result)
        if ret != 0:
            raise RobotError(ret, f"读取位置信息失败: {self._get_error_message(ret)}")
        
        if len(result) >= 12:
            # 关节坐标 [J1, J2, J3, J4, J5, J6]
            joint_coords = [float(x) for x in result[0:6]]
            # 笛卡尔坐标 [X, Y, Z, Rx, Ry, Rz]
            cartesian_coords = [float(x) for x in result[6:12]]
            return joint_coords, cartesian_coords
        else:
            raise RobotError(-1, "读取位置信息格式不正确")
    
    def get_current_joint_positions(self) -> List[float]:
        """
        获取当前关节位置
        
        Returns:
            List[float]: 关节位置 [J1, J2, J3, J4, J5, J6]
            
        Raises:
            RobotError: 获取关节位置失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_ReadActJointPos(self.box_id, self.robot_id, result)
        if ret != 0:
            raise RobotError(ret, f"读取关节位置失败: {self._get_error_message(ret)}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise RobotError(-1, "读取关节位置格式不正确")
    
    def set_override(self, vel: float) -> bool:
        """
        设置速度比
        
        Args:
            vel (float): 速度比 (0.01~1.0)
            
        Returns:
            bool: 设置是否成功
            
        Raises:
            RobotError: 设置失败时抛出异常
        """
        ret = self.lib_wrapper.HRIF_SetOverride(self.box_id, self.robot_id, vel)
        if ret != 0:
            raise RobotError(ret, f"设置速度比失败: {self._get_error_message(ret)}")
        return True
    
    def get_override(self) -> float:
        """
        获取当前速度比
        
        Returns:
            float: 当前速度比
            
        Raises:
            RobotError: 获取失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_ReadOverride(self.box_id, self.robot_id, result)
        if ret != 0:
            raise RobotError(ret, f"读取速度比失败: {self._get_error_message(ret)}")
        
        if result:
            return float(result[0])
        else:
            raise RobotError(-1, "读取速度比格式不正确")
    
    def stop(self) -> bool:
        """
        停止机器人运动
        
        Returns:
            bool: 停止是否成功
            
        Raises:
            RobotError: 停止失败时抛出异常
        """
        ret = self.lib_wrapper.HRIF_GrpStop(self.box_id, self.robot_id)
        if ret != 0:
            raise RobotError(ret, f"停止机器人运动失败: {self._get_error_message(ret)}")
        return True
    
    def reset(self) -> bool:
        """
        复位机器人
        
        Returns:
            bool: 复位是否成功
            
        Raises:
            RobotError: 复位失败时抛出异常
        """
        ret = self.lib_wrapper.HRIF_GrpReset(self.box_id, self.robot_id)
        if ret != 0:
            raise RobotError(ret, f"复位机器人失败: {self._get_error_message(ret)}")
        return True
    
    # 内部辅助方法
    def _wait_for_connection(self, timeout: float) -> bool:
        """等待连接完成"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_connected():
                return True
            time.sleep(self.default_check_interval)
        
        return False
    
    def _get_error_message(self, error_code: int) -> str:
        """获取错误码的详细描述"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_GetErrorCodeStr(self.box_id, error_code, result)
            if ret == 0 and result:
                return result[0]
            else:
                # 如果无法获取详细错误信息，使用预定义的错误信息
                from .exceptions import ErrorCodeHelper
                return ErrorCodeHelper.get_error_message(self.lib_wrapper, error_code, self.box_id)
        except:
            return f"未知错误 (错误码: {error_code})"


# 为了向后兼容，保留原来的文件名拼写错误
RobotConroller = RobotController
