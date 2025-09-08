#!/usr/bin/env python3
"""
夹爪控制器封装模块
基于现有的lib/lebai_controller.py封装，提供统一的接口
"""

import logging
import time
from typing import Optional
from lib.lebai_controller import GripperController


class GripperControllerWrapper:
    """夹爪控制器封装类"""
    
    def __init__(self, config: dict):
        """
        初始化夹爪控制器
        
        Args:
            config (dict): 配置信息
        """
        self.config = config
        self.gripper = GripperController(device_index=config.get('device_index', 0))
        self.logger = logging.getLogger(__name__)
        self.connected = False
    
    def connect(self) -> bool:
        """
        连接到夹爪
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.logger.info(f"正在连接夹爪设备索引 {self.config['device_index']}")
            if self.gripper.open_device():
                self.gripper.set_baudrate()
                self.gripper.set_data_characteristics()
                self.gripper.set_timeouts()
                self.gripper.flush_buffers()
                self.connected = True
                self.logger.info("夹爪连接成功")
                return True
            else:
                self.logger.error("夹爪设备打开失败")
                self.connected = False
                return False
        except Exception as e:
            self.logger.error(f"夹爪连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> bool:
        """
        断开夹爪连接
        
        Returns:
            bool: 断开是否成功
        """
        try:
            if self.connected:
                self.gripper.close_device()
                self.connected = False
                self.logger.info("夹爪连接已断开")
            return True
        except Exception as e:
            self.logger.error(f"夹爪断开连接失败: {e}")
            return False
    
    def is_connected(self) -> bool:
        """
        检查夹爪是否已连接
        
        Returns:
            bool: 是否已连接
        """
        # 注意：这里简单判断，实际可能需要更复杂的连接状态检测
        return self.connected
    
    def set_amplitude(self, amplitude: int) -> bool:
        """
        设置夹爪幅度(开合程度)
        
        Args:
            amplitude (int): 幅度值，范围0-100
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not self.connected:
                self.logger.error("夹爪未连接，无法设置幅度")
                return False
            if 0 <= amplitude <= 100:
                result = self.gripper.set_gripper_amplitude(amplitude)
                if result:
                    self.logger.info(f"夹爪幅度设置为 {amplitude}%")
                else:
                    self.logger.error(f"夹爪幅度设置失败: {amplitude}%")
                return result
            else:
                self.logger.error(f"幅度值超出范围: {amplitude} (应为0-100)")
                return False
        except Exception as e:
            self.logger.error(f"设置夹爪幅度失败: {e}")
            return False
    
    def set_force(self, force: int) -> bool:
        """
        设置夹爪力度
        
        Args:
            force (int): 力度值，范围0-100
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not self.connected:
                self.logger.error("夹爪未连接，无法设置力度")
                return False
            if 0 <= force <= 100:
                result = self.gripper.set_gripper_force(force)
                if result:
                    self.logger.info(f"夹爪力度设置为 {force}%")
                else:
                    self.logger.error(f"夹爪力度设置失败: {force}%")
                return result
            else:
                self.logger.error(f"力度值超出范围: {force} (应为0-100)")
                return False
        except Exception as e:
            self.logger.error(f"设置夹爪力度失败: {e}")
            return False
    
    def get_position(self) -> Optional[int]:
        """
        获取夹爪当前位置
        
        Returns:
            int: 当前位置值，范围0-100，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("夹爪未连接，无法获取位置")
                return None
            position = self.gripper.get_gripper_position()
            if position >= 0:
                self.logger.info(f"夹爪当前位置: {position}%")
                return position
            else:
                self.logger.error("获取夹爪位置失败")
                return None
        except Exception as e:
            self.logger.error(f"获取夹爪位置失败: {e}")
            return None
    
    def get_torque(self) -> Optional[int]:
        """
        获取夹爪当前力矩
        
        Returns:
            int: 当前力矩值，范围0-100，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("夹爪未连接，无法获取力矩")
                return None
            torque = self.gripper.get_gripper_torque()
            if torque >= 0:
                self.logger.info(f"夹爪当前力矩: {torque}%")
                return torque
            else:
                self.logger.error("获取夹爪力矩失败")
                return None
        except Exception as e:
            self.logger.error(f"获取夹爪力矩失败: {e}")
            return None
    
    def find_travel(self) -> bool:
        """
        执行找行程指令
        
        Returns:
            bool: 执行是否成功
        """
        try:
            if not self.connected:
                self.logger.error("夹爪未连接，无法执行找行程")
                return False
            result = self.gripper.find_travel()
            if result:
                self.logger.info("夹爪找行程指令已发送")
            else:
                self.logger.error("夹爪找行程指令发送失败")
            return result
        except Exception as e:
            self.logger.error(f"夹爪找行程失败: {e}")
            return False
    
    def is_command_completed(self) -> Optional[bool]:
        """
        检查指令是否执行完成
        
        Returns:
            bool: 完成返回True，执行中返回False，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("夹爪未连接，无法检查指令状态")
                return None
            result = self.gripper.is_command_completed()
            if result is not None:
                self.logger.info(f"夹爪指令状态: {'完成' if result else '执行中'}")
            else:
                self.logger.error("检查夹爪指令状态失败")
            return result
        except Exception as e:
            self.logger.error(f"检查夹爪指令状态失败: {e}")
            return None
