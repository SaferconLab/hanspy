#!/usr/bin/env python3
"""
控制器客户端主模块
用于通过TCP连接控制机械臂和夹爪设备
"""

import socket
import json
import time
import threading
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from .protocol import (
    CommandType, MessageStatus, BaseMessage, CommandMessage, 
    ResponseMessage, parse_message, create_success_response,
    create_error_response, create_pending_response
)


class ClientState(Enum):
    """客户端状态枚举"""
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ROBOT_CONNECTED = "robot_connected"
    GRIPPER_CONNECTED = "gripper_connected"
    ROBOT_ENABLED = "robot_enabled"


class ControllerClient:
    """控制器客户端类"""
    
    def __init__(self, host: str = "localhost", port: int = 8888, 
                 timeout: float = 30.0, reconnect_attempts: int = 3):
        """
        初始化控制器客户端
        
        Args:
            host (str): 服务器主机地址
            port (int): 服务器端口号
            timeout (float): 连接和操作超时时间（秒）
            reconnect_attempts (int): 自动重连尝试次数
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.reconnect_attempts = reconnect_attempts
        
        # 客户端状态
        self.state = ClientState.DISCONNECTED
        self.client_socket = None
        self.message_id_counter = 0
        
        # 连接相关
        self._lock = threading.Lock()
        
        # 日志记录器
        import logging
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """
        连接到控制器服务器
        
        Returns:
            bool: 连接是否成功
        """
        try:
            with self._lock:
                if self.state != ClientState.DISCONNECTED:
                    self.logger.warning("客户端已连接或正在连接")
                    return True
                
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(self.timeout)
                self.client_socket.connect((self.host, self.port))
                
                # 接收欢迎消息
                welcome_data = self.client_socket.recv(4096)
                welcome_msg = parse_message(welcome_data.decode('utf-8'))
                
                if welcome_msg.msg_type == "response" and hasattr(welcome_msg, 'status') and welcome_msg.status == MessageStatus.SUCCESS:
                    self.state = ClientState.CONNECTED
                    self.logger.info(f"成功连接到控制器服务器 {self.host}:{self.port}")
                    return True
                else:
                    self.logger.error("连接服务器失败，未收到有效的欢迎消息")
                    self.client_socket.close()
                    self.client_socket = None
                    return False
                    
        except Exception as e:
            self.logger.error(f"连接到服务器失败: {e}")
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
            return False
    
    def disconnect(self) -> bool:
        """
        断开与控制器服务器的连接
        
        Returns:
            bool: 断开是否成功
        """
        try:
            with self._lock:
                if self.state == ClientState.DISCONNECTED:
                    return True
                
                if self.client_socket:
                    self.client_socket.close()
                    self.client_socket = None
                
                self.state = ClientState.DISCONNECTED
                self.logger.info("已断开与控制器服务器的连接")
                return True
                
        except Exception as e:
            self.logger.error(f"断开连接时发生错误: {e}")
            return False
    
    def _send_command(self, command_type: CommandType, data: Optional[Dict] = None) -> Optional[ResponseMessage]:
        """
        发送命令到服务器并接收响应
        
        Args:
            command_type (CommandType): 命令类型
            data (Dict): 命令数据
            
        Returns:
            ResponseMessage: 服务器响应
        """
        try:
            with self._lock:
                if self.state == ClientState.DISCONNECTED:
                    self.logger.error("客户端未连接到服务器")
                    return None
                
                # 生成唯一的消息ID
                self.message_id_counter += 1
                message_id = f"msg_{self.message_id_counter}_{int(time.time())}"
                
                # 构造命令消息
                command = CommandMessage(
                    command_type=command_type,
                    data=data or {},
                    message_id=message_id
                )
                
                # 发送消息
                self.client_socket.send(command.to_json().encode('utf-8'))
                
                # 接收响应
                response_data = self.client_socket.recv(4096)
                response = parse_message(response_data.decode('utf-8'))
                
                return response
                
        except Exception as e:
            self.logger.error(f"发送命令失败: {e}")
            return None
    
    def _handle_response(self, response: ResponseMessage) -> bool:
        """
        处理服务器响应
        
        Args:
            response (ResponseMessage): 服务器响应
            
        Returns:
            bool: 处理是否成功
        """
        if response.status == MessageStatus.SUCCESS:
            self.logger.info(f"命令执行成功: {response.message}")
            return True
        elif response.status == MessageStatus.ERROR:
            self.logger.error(f"命令执行失败: {response.message}")
            return False
        else:
            self.logger.warning(f"命令状态: {response.message}")
            return True
    
    # ==================== 机器人连接相关 ====================
    
    def connect_robot(self) -> bool:
        """
        连接到机器人设备
        
        Returns:
            bool: 连接是否成功
        """
        response = self._send_command(CommandType.CONNECT_ROBOT)
        if response and self._handle_response(response):
            self.state = ClientState.ROBOT_CONNECTED
            return True
        return False
    
    def disconnect_robot(self) -> bool:
        """
        断开与机器人的连接
        
        Returns:
            bool: 断开是否成功
        """
        response = self._send_command(CommandType.DISCONNECT_ROBOT)
        if response and self._handle_response(response):
            if self.state == ClientState.ROBOT_CONNECTED:
                self.state = ClientState.CONNECTED
            elif self.state == ClientState.ROBOT_ENABLED:
                self.state = ClientState.CONNECTED
            return True
        return False
    
    def enable_robot(self) -> bool:
        """
        使能机器人，允许其运动
        
        Returns:
            bool: 使能是否成功
        """
        response = self._send_command(CommandType.ENABLE_ROBOT)
        if response and self._handle_response(response):
            self.state = ClientState.ROBOT_ENABLED
            return True
        return False
    
    def disable_robot(self) -> bool:
        """
        去使能机器人，禁止其运动
        
        Returns:
            bool: 去使能是否成功
        """
        response = self._send_command(CommandType.DISABLE_ROBOT)
        if response and self._handle_response(response):
            if self.state == ClientState.ROBOT_ENABLED:
                self.state = ClientState.ROBOT_CONNECTED
            return True
        return False
    
    # ==================== 机器人运动相关 ====================
    
    def move_j(self, points: List[float], raw_acs_points: List[float],
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               timeout: float = 30.0) -> bool:
        """
        执行关节空间运动
        
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
        data = {
            "points": points,
            "raw_acs_points": raw_acs_points,
            "speed": speed,
            "acc": acc,
            "radius": radius,
            "timeout": timeout
        }
        response = self._send_command(CommandType.MOVE_J, data)
        return response and self._handle_response(response)
    
    def move_l(self, points: List[float], raw_acs_points: List[float],
               speed: float = 50.0, acc: float = 50.0, radius: float = 50.0,
               timeout: float = 30.0) -> bool:
        """
        执行直线空间运动
        
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
        data = {
            "points": points,
            "raw_acs_points": raw_acs_points,
            "speed": speed,
            "acc": acc,
            "radius": radius,
            "timeout": timeout
        }
        response = self._send_command(CommandType.MOVE_L, data)
        return response and self._handle_response(response)
    
    def get_position(self) -> Optional[tuple]:
        """
        获取机器人当前位置信息
        
        Returns:
            tuple: (关节坐标, 笛卡尔坐标)，失败返回None
        """
        response = self._send_command(CommandType.GET_POSITION)
        if response and response.status == MessageStatus.SUCCESS:
            data = response.data
            joint_positions = data.get("joint_positions", [])
            cartesian_positions = data.get("cartesian_positions", [])
            return (joint_positions, cartesian_positions)
        return None
    
    def set_override(self, velocity: float) -> bool:
        """
        设置机器人运动速度比
        
        Args:
            velocity (float): 速度比 (0.01~1.0)
            
        Returns:
            bool: 设置是否成功
        """
        data = {"velocity": velocity}
        response = self._send_command(CommandType.SET_OVERRIDE, data)
        return response and self._handle_response(response)
    
    def stop(self) -> bool:
        """
        立即停止机器人运动
        
        Returns:
            bool: 停止是否成功
        """
        response = self._send_command(CommandType.STOP)
        return response and self._handle_response(response)
    
    def reset(self) -> bool:
        """
        复位机器人系统
        
        Returns:
            bool: 复位是否成功
        """
        response = self._send_command(CommandType.RESET)
        return response and self._handle_response(response)
    
    def goto_pose(self, pose: List[float], speed: float = 50.0, 
                  acc: float = 50.0, radius: float = 50.0) -> bool:
        """
        运动到指定末端姿态
        
        Args:
            pose: 末端6d姿态 [X, Y, Z, Rx, Ry, Rz]
            speed: 速度
            acc: 加速度
            radius: 过渡半径
            
        Returns:
            bool: 运动是否成功
        """
        data = {
            "pose": pose,
            "speed": speed,
            "acc": acc,
            "radius": radius
        }
        response = self._send_command(CommandType.GOTO_POSE, data)
        return response and self._handle_response(response)
    
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
        data = {
            "joint_positions": joint_positions,
            "speed": speed,
            "acc": acc,
            "radius": radius
        }
        response = self._send_command(CommandType.GOTO_JOINT, data)
        return response and self._handle_response(response)
    
    def electrify(self) -> bool:
        """
        对机器人进行上电操作
        
        Returns:
            bool: 上电是否成功
        """
        response = self._send_command(CommandType.ELECTRIFY)
        return response and self._handle_response(response)
    
    def blackout(self) -> bool:
        """
        对机器人进行断电操作
        
        Returns:
            bool: 断电是否成功
        """
        response = self._send_command(CommandType.BLACKOUT)
        return response and self._handle_response(response)
    
    def get_current_state(self) -> Optional[int]:
        """
        获取机器人当前状态码
        
        Returns:
            int: 当前状态码，失败返回None
        """
        response = self._send_command(CommandType.GET_CURRENT_STATE)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("state")
        return None
    
    def get_state_description(self, state: int) -> Optional[str]:
        """
        获取机器人状态描述
        
        Args:
            state (int): 状态码
            
        Returns:
            str: 状态描述，失败返回None
        """
        data = {"state": state}
        response = self._send_command(CommandType.GET_STATE_DESCRIPTION, data)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("description")
        return None
    
    def is_ready(self) -> Optional[bool]:
        """
        检查机器人是否处于就绪状态
        
        Returns:
            bool: 是否就绪，失败返回None
        """
        response = self._send_command(CommandType.IS_READY)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("ready")
        return None
    
    def is_moving(self) -> Optional[bool]:
        """
        检查机器人是否正在运动
        
        Returns:
            bool: 是否正在运动，失败返回None
        """
        response = self._send_command(CommandType.IS_MOVING)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("moving")
        return None
    
    def wait_for_motion_done(self, timeout: float = 30.0) -> Optional[bool]:
        """
        等待机器人运动完成
        
        Args:
            timeout (float): 等待超时时间（秒）
            
        Returns:
            bool: 是否运动完成，失败返回None
        """
        data = {"timeout": timeout}
        response = self._send_command(CommandType.WAIT_FOR_MOTION_DONE, data)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("done")
        return None
    
    def get_override(self) -> Optional[float]:
        """
        获取当前速度比
        
        Returns:
            float: 当前速度比，失败返回None
        """
        response = self._send_command(CommandType.GET_OVERRIDE)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("override")
        return None
    
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
        data = {
            "delta_pose": delta_pose,
            "tcp": tcp or [0, 0, 0, 0, 0, 0],
            "ucs": ucs or [0, 0, 0, 0, 0, 0],
            "speed": speed,
            "acc": acc,
            "radius": radius
        }
        response = self._send_command(CommandType.GOTO_DELTA, data)
        return response and self._handle_response(response)
    
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
        data = {
            "delta_joints": delta_joints,
            "speed": speed,
            "acc": acc,
            "radius": radius
        }
        response = self._send_command(CommandType.GOTO_DELTA_JOINT, data)
        return response and self._handle_response(response)
    
    # ==================== 夹爪连接相关 ====================
    
    def connect_gripper(self) -> bool:
        """
        连接到夹爪设备
        
        Returns:
            bool: 连接是否成功
        """
        response = self._send_command(CommandType.CONNECT_GRIPPER)
        if response and self._handle_response(response):
            self.state = ClientState.GRIPPER_CONNECTED
            return True
        return False
    
    def disconnect_gripper(self) -> bool:
        """
        断开与夹爪的连接
        
        Returns:
            bool: 断开是否成功
        """
        response = self._send_command(CommandType.DISCONNECT_GRIPPER)
        if response and self._handle_response(response):
            if self.state == ClientState.GRIPPER_CONNECTED:
                self.state = ClientState.CONNECTED
            return True
        return False
    
    # ==================== 夹爪控制相关 ====================
    
    def set_gripper_amplitude(self, amplitude: int) -> bool:
        """
        设置夹爪开合幅度
        
        Args:
            amplitude (int): 幅度值，范围0-100
            
        Returns:
            bool: 设置是否成功
        """
        data = {"amplitude": amplitude}
        response = self._send_command(CommandType.SET_GRIPPER_AMPLITUDE, data)
        return response and self._handle_response(response)
    
    def set_gripper_force(self, force: int) -> bool:
        """
        设置夹爪抓取力度
        
        Args:
            force (int): 力度值，范围0-100
            
        Returns:
            bool: 设置是否成功
        """
        data = {"force": force}
        response = self._send_command(CommandType.SET_GRIPPER_FORCE, data)
        return response and self._handle_response(response)
    
    def get_gripper_position(self) -> Optional[int]:
        """
        获取夹爪当前位置
        
        Returns:
            int: 当前位置值，范围0-100，失败返回None
        """
        response = self._send_command(CommandType.GET_GRIPPER_POSITION)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("position")
        return None
    
    def get_gripper_torque(self) -> Optional[int]:
        """
        获取夹爪当前力矩
        
        Returns:
            int: 当前力矩值，范围0-100，失败返回None
        """
        response = self._send_command(CommandType.GET_GRIPPER_TORQUE)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("torque")
        return None
    
    def find_gripper_travel(self) -> bool:
        """
        执行夹爪找行程指令
        
        Returns:
            bool: 执行是否成功
        """
        response = self._send_command(CommandType.FIND_GRIPPER_TRAVEL)
        return response and self._handle_response(response)
    
    def is_gripper_command_completed(self) -> Optional[bool]:
        """
        检查夹爪指令是否已完成
        
        Returns:
            bool: 完成返回True，执行中返回False，失败返回None
        """
        response = self._send_command(CommandType.COMMAND_COMPLETED)
        if response and response.status == MessageStatus.SUCCESS:
            return response.data.get("completed")
        return None
    
    def is_connected(self) -> bool:
        """
        检查客户端是否已连接到服务器
        
        Returns:
            bool: 是否已连接
        """
        return self.state != ClientState.DISCONNECTED
    
    def get_state(self) -> ClientState:
        """
        获取客户端当前状态
        
        Returns:
            ClientState: 当前状态
        """
        return self.state
