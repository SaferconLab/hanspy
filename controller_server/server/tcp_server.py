#!/usr/bin/env python3
"""
TCP服务器模块
负责监听网络连接并处理来自上位机B的指令
"""

import socket
import threading
import json
import time
import logging
from typing import Dict, Any, Optional
from controller.session_manager import SessionManager
from controller.robot_controller import RobotControllerWrapper
from controller.gripper_controller import GripperControllerWrapper
from protocol.message_protocol import (
    parse_message, CommandMessage, ResponseMessage, 
    MessageStatus, CommandType, create_success_response, 
    create_error_response, create_pending_response, BaseMessage
)


class ControllerServer:
    """控制器服务器类"""
    
    def __init__(self, config: dict):
        """
        初始化控制器服务器
        
        Args:
            config (dict): 配置信息
        """
        self.config = config
        self.host = config['server']['host']
        self.port = config['server']['port']
        self.max_connections = config['server']['max_connections']
        
        # 初始化组件
        self.session_manager = SessionManager()
        self.robot_controller = RobotControllerWrapper(config['robot'])
        self.gripper_controller = GripperControllerWrapper(config['gripper'])
        
        # 服务器相关
        self.server_socket = None
        self.running = False
        self.clients: Dict[str, socket.socket] = {}
        self.client_threads: Dict[str, threading.Thread] = {}
        
        # 日志配置
        self.logger = logging.getLogger(__name__)
        
        # 初始化日志
        logging.basicConfig(
            level=getattr(logging, config['logging']['level']),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=config['logging']['file'],
            filemode='a'
        )
    
    def start(self):
        """启动服务器"""
        try:
            self.logger.info(f"启动控制器服务器 {self.host}:{self.port}")
            
            # 创建socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 绑定地址和端口
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
            
            self.running = True
            
            # 启动监听线程
            listen_thread = threading.Thread(target=self._listen_for_clients)
            listen_thread.daemon = True
            listen_thread.start()
            
            self.logger.info("控制器服务器已启动")
            
        except Exception as e:
            self.logger.error(f"启动服务器失败: {e}")
            raise
    
    def stop(self):
        """停止服务器"""
        self.logger.info("正在停止控制器服务器...")
        self.running = False
        
        # 关闭所有客户端连接
        for client_id, client_socket in list(self.clients.items()):
            try:
                client_socket.close()
                self.session_manager.remove_session(client_id)
            except Exception as e:
                self.logger.error(f"关闭客户端连接失败 {client_id}: {e}")
        
        # 关闭服务器socket
        if self.server_socket:
            self.server_socket.close()
        
        # 等待所有客户端线程结束
        for thread in self.client_threads.values():
            if thread.is_alive():
                thread.join(timeout=1)
        
        self.logger.info("控制器服务器已停止")
    
    def _listen_for_clients(self):
        """监听客户端连接"""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.logger.info(f"新客户端连接: {client_address}")
                
                # 创建会话
                client_id = self.session_manager.create_session(str(client_address))
                
                # 保存客户端连接
                self.clients[client_id] = client_socket
                
                # 为每个客户端启动处理线程
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_id, client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
                self.client_threads[client_id] = client_thread
                
            except Exception as e:
                if self.running:
                    self.logger.error(f"接受客户端连接失败: {e}")
    
    def _handle_client(self, client_id: str, client_socket: socket.socket, 
                       client_address: str):
        """处理单个客户端的请求"""
        try:
            # 发送欢迎消息
            welcome_msg = create_success_response(
                "welcome", 
                "连接成功，控制器服务器已就绪",
                {"client_id": client_id}
            )
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # 处理客户端消息循环
            while self.running:
                try:
                    # 接收消息
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    
                    # 解析消息
                    message_str = data.decode('utf-8')
                    message = parse_message(message_str)
                    
                    # 更新会话活动时间
                    self.session_manager.update_activity(client_id)
                    
                    # 处理消息
                    response = self._process_message(client_id, message)
                    
                    # 发送响应
                    if response:
                        client_socket.send(response.encode('utf-8'))
                        
                except json.JSONDecodeError:
                    error_msg = create_error_response(
                        "unknown", 
                        "无效的JSON格式消息"
                    )
                    client_socket.send(error_msg.encode('utf-8'))
                except Exception as e:
                    self.logger.error(f"处理客户端消息失败 {client_id}: {e}")
                    error_msg = create_error_response(
                        "unknown", 
                        f"处理消息时发生错误: {str(e)}"
                    )
                    client_socket.send(error_msg.encode('utf-8'))
                    
        except Exception as e:
            self.logger.error(f"客户端处理线程异常 {client_id}: {e}")
        finally:
            # 清理客户端资源
            self._cleanup_client(client_id, client_socket)
    
    def _process_message(self, client_id: str, message: BaseMessage) -> Optional[str]:
        """处理接收到的消息"""
        try:
            if isinstance(message, CommandMessage):
                command_type = message.command_type
                
                # 根据命令类型处理
                if command_type == CommandType.CONNECT_ROBOT:
                    return self._handle_connect_robot(client_id, message)
                elif command_type == CommandType.DISCONNECT_ROBOT:
                    return self._handle_disconnect_robot(client_id, message)
                elif command_type == CommandType.ENABLE_ROBOT:
                    return self._handle_enable_robot(client_id, message)
                elif command_type == CommandType.DISABLE_ROBOT:
                    return self._handle_disable_robot(client_id, message)
                elif command_type == CommandType.MOVE_J:
                    return self._handle_move_j(client_id, message)
                elif command_type == CommandType.MOVE_L:
                    return self._handle_move_l(client_id, message)
                elif command_type == CommandType.GET_POSITION:
                    return self._handle_get_position(client_id, message)
                elif command_type == CommandType.SET_OVERRIDE:
                    return self._handle_set_override(client_id, message)
                elif command_type == CommandType.STOP:
                    return self._handle_stop(client_id, message)
                elif command_type == CommandType.RESET:
                    return self._handle_reset(client_id, message)
                elif command_type == CommandType.GOTO_POSE:
                    return self._handle_goto_pose(client_id, message)
                elif command_type == CommandType.GOTO_JOINT:
                    return self._handle_goto_joint(client_id, message)
                elif command_type == CommandType.CONNECT_GRIPPER:
                    return self._handle_connect_gripper(client_id, message)
                elif command_type == CommandType.DISCONNECT_GRIPPER:
                    return self._handle_disconnect_gripper(client_id, message)
                elif command_type == CommandType.SET_GRIPPER_AMPLITUDE:
                    return self._handle_set_gripper_amplitude(client_id, message)
                elif command_type == CommandType.SET_GRIPPER_FORCE:
                    return self._handle_set_gripper_force(client_id, message)
                elif command_type == CommandType.GET_GRIPPER_POSITION:
                    return self._handle_get_gripper_position(client_id, message)
                elif command_type == CommandType.GET_GRIPPER_TORQUE:
                    return self._handle_get_gripper_torque(client_id, message)
                elif command_type == CommandType.FIND_GRIPPER_TRAVEL:
                    return self._handle_find_gripper_travel(client_id, message)
                elif command_type == CommandType.COMMAND_COMPLETED:
                    return self._handle_command_completed(client_id, message)
                elif command_type == CommandType.GOTO_DELTA_JOINT:
                    return self._handle_goto_delta_joint(client_id, message)
                elif command_type == CommandType.IS_CONNECTED:
                    return self._handle_is_connected(client_id, message)
                elif command_type == CommandType.GET_CURRENT_JOINT_POSITIONS:
                    return self._handle_get_current_joint_positions(client_id, message)
                elif command_type == CommandType.ELECTRIFY:
                    return self._handle_electrify(client_id, message)
                elif command_type == CommandType.BLACKOUT:
                    return self._handle_blackout(client_id, message)
                elif command_type == CommandType.GET_CURRENT_STATE:
                    return self._handle_get_current_state(client_id, message)
                elif command_type == CommandType.GET_STATE_DESCRIPTION:
                    return self._handle_get_state_description(client_id, message)
                elif command_type == CommandType.IS_READY:
                    return self._handle_is_ready(client_id, message)
                elif command_type == CommandType.IS_MOVING:
                    return self._handle_is_moving(client_id, message)
                elif command_type == CommandType.WAIT_FOR_MOTION_DONE:
                    return self._handle_wait_for_motion_done(client_id, message)
                elif command_type == CommandType.GET_OVERRIDE:
                    return self._handle_get_override(client_id, message)
                elif command_type == CommandType.GOTO_DELTA:
                    return self._handle_goto_delta(client_id, message)
                else:
                    return create_error_response(
                        message.message_id or "unknown",
                        f"未知的命令类型: {command_type.value}"
                    )
            else:
                # 处理响应消息或其他类型消息
                return create_error_response(
                    message.message_id or "unknown",
                    "不支持的消息类型"
                )
                
        except Exception as e:
            self.logger.error(f"处理消息时发生错误: {e}")
            return create_error_response(
                message.message_id or "unknown",
                f"处理消息时发生错误: {str(e)}"
            )
    
    def _handle_connect_robot(self, client_id: str, message: CommandMessage) -> str:
        """处理连接机器人命令"""
        try:
            self.logger.info(f"开始处理连接机器人命令，客户端ID: {client_id}")
            result = self.robot_controller.connect()
            self.session_manager.set_robot_connection_status(client_id, result)
            
            self.logger.info(f"机器人连接结果: {result}")
            
            if result:
                response = create_success_response(
                    message.message_id or "unknown",
                    "机器人连接成功",
                    {"connected": True}
                )
                self.logger.info(f"返回成功响应: {response}")
                return response
            else:
                response = create_error_response(
                    message.message_id or "unknown",
                    "机器人连接失败"
                )
                self.logger.info(f"返回错误响应: {response}")
                return response
        except Exception as e:
            error_msg = f"连接机器人时发生错误: {str(e)}"
            self.logger.error(error_msg)
            return create_error_response(
                message.message_id or "unknown",
                error_msg
            )
    
    def _handle_disconnect_robot(self, client_id: str, message: CommandMessage) -> str:
        """处理断开机器人连接命令"""
        try:
            result = self.robot_controller.disconnect()
            self.session_manager.set_robot_connection_status(client_id, False)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人连接已断开",
                    {"connected": False}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "断开机器人连接失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"断开机器人连接时发生错误: {str(e)}"
            )
    
    def _handle_enable_robot(self, client_id: str, message: CommandMessage) -> str:
        """处理使能机器人命令"""
        try:
            result = self.robot_controller.enable()
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人已使能",
                    {"enabled": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "机器人使能失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"使能机器人时发生错误: {str(e)}"
            )
    
    def _handle_disable_robot(self, client_id: str, message: CommandMessage) -> str:
        """处理去使能机器人命令"""
        try:
            result = self.robot_controller.disable()
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人已去使能",
                    {"enabled": False}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "机器人去使能失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"去使能机器人时发生错误: {str(e)}"
            )
    
    def _handle_move_j(self, client_id: str, message: CommandMessage) -> str:
        """处理关节运动命令"""
        try:
            data = message.data
            points = data.get('points', [])
            raw_acs_points = data.get('raw_acs_points', [])
            speed = data.get('speed', 50.0)
            acc = data.get('acc', 50.0)
            radius = data.get('radius', 50.0)
            timeout = data.get('timeout', 30.0)
            
            result = self.robot_controller.move_j(
                points, raw_acs_points, speed, acc, radius, timeout
            )
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "关节运动完成",
                    {"moved": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "关节运动失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"关节运动时发生错误: {str(e)}"
            )
    
    def _handle_move_l(self, client_id: str, message: CommandMessage) -> str:
        """处理直线运动命令"""
        try:
            data = message.data
            points = data.get('points', [])
            raw_acs_points = data.get('raw_acs_points', [])
            speed = data.get('speed', 50.0)
            acc = data.get('acc', 50.0)
            radius = data.get('radius', 50.0)
            timeout = data.get('timeout', 30.0)
            
            result = self.robot_controller.move_l(
                points, raw_acs_points, speed, acc, radius, timeout
            )
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "直线运动完成",
                    {"moved": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "直线运动失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"直线运动时发生错误: {str(e)}"
            )
    
    def _handle_get_position(self, client_id: str, message: CommandMessage) -> str:
        """处理获取位置命令"""
        try:
            joint_pos, cartesian_pos = self.robot_controller.get_current_position()
            
            if joint_pos and cartesian_pos:
                return create_success_response(
                    message.message_id or "unknown",
                    "获取位置信息成功",
                    {
                        "joint_positions": joint_pos,
                        "cartesian_positions": cartesian_pos
                    }
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "获取位置信息失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取位置信息时发生错误: {str(e)}"
            )
    
    def _handle_set_override(self, client_id: str, message: CommandMessage) -> str:
        """处理设置速度比命令"""
        try:
            data = message.data
            velocity = data.get('velocity', 0.5)
            
            result = self.robot_controller.set_override(velocity)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "速度比设置成功",
                    {"velocity": velocity}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "速度比设置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"设置速度比时发生错误: {str(e)}"
            )
    
    def _handle_stop(self, client_id: str, message: CommandMessage) -> str:
        """处理停止命令"""
        try:
            result = self.robot_controller.stop()
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人已停止",
                    {"stopped": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "停止机器人失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"停止机器人时发生错误: {str(e)}"
            )
    
    def _handle_reset(self, client_id: str, message: CommandMessage) -> str:
        """处理复位命令"""
        try:
            result = self.robot_controller.reset()
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人已复位",
                    {"reset": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "机器人复位失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"复位机器人时发生错误: {str(e)}"
            )
    
    def _handle_goto_pose(self, client_id: str, message: CommandMessage) -> str:
        """处理运动到姿态命令"""
        try:
            data = message.data
            pose = data.get('pose', [])
            speed = data.get('speed', 50.0)
            acc = data.get('acc', 50.0)
            radius = data.get('radius', 50.0)
            
            result = self.robot_controller.goto_pose(pose, speed, acc, radius)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "运动到姿态完成",
                    {"moved": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "运动到姿态失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"运动到姿态时发生错误: {str(e)}"
            )
    
    def _handle_goto_joint(self, client_id: str, message: CommandMessage) -> str:
        """处理运动到关节位置命令"""
        try:
            data = message.data
            joint_positions = data.get('joint_positions', [])
            speed = data.get('speed', 50.0)
            acc = data.get('acc', 50.0)
            radius = data.get('radius', 50.0)
            
            result = self.robot_controller.goto_joint(joint_positions, speed, acc, radius)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "运动到关节位置完成",
                    {"moved": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "运动到关节位置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"运动到关节位置时发生错误: {str(e)}"
            )
    
    def _handle_connect_gripper(self, client_id: str, message: CommandMessage) -> str:
        """处理连接夹爪命令"""
        try:
            result = self.gripper_controller.connect()
            self.session_manager.set_gripper_connection_status(client_id, result)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "夹爪连接成功",
                    {"connected": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "夹爪连接失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"连接夹爪时发生错误: {str(e)}"
            )
    
    def _handle_disconnect_gripper(self, client_id: str, message: CommandMessage) -> str:
        """处理断开夹爪连接命令"""
        try:
            result = self.gripper_controller.disconnect()
            self.session_manager.set_gripper_connection_status(client_id, False)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "夹爪连接已断开",
                    {"connected": False}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "断开夹爪连接失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"断开夹爪连接时发生错误: {str(e)}"
            )
    
    def _handle_set_gripper_amplitude(self, client_id: str, message: CommandMessage) -> str:
        """处理设置夹爪幅度命令"""
        try:
            data = message.data
            amplitude = data.get('amplitude', 0)
            
            result = self.gripper_controller.set_amplitude(amplitude)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "夹爪幅度设置成功",
                    {"amplitude": amplitude}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "夹爪幅度设置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"设置夹爪幅度时发生错误: {str(e)}"
            )
    
    def _handle_set_gripper_force(self, client_id: str, message: CommandMessage) -> str:
        """处理设置夹爪力度命令"""
        try:
            data = message.data
            force = data.get('force', 0)
            
            result = self.gripper_controller.set_force(force)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "夹爪力度设置成功",
                    {"force": force}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "夹爪力度设置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"设置夹爪力度时发生错误: {str(e)}"
            )
    
    def _handle_get_gripper_position(self, client_id: str, message: CommandMessage) -> str:
        """处理获取夹爪位置命令"""
        try:
            position = self.gripper_controller.get_position()
            
            if position is not None:
                return create_success_response(
                    message.message_id or "unknown",
                    "获取夹爪位置成功",
                    {"position": position}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "获取夹爪位置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取夹爪位置时发生错误: {str(e)}"
            )
    
    def _handle_get_gripper_torque(self, client_id: str, message: CommandMessage) -> str:
        """处理获取夹爪力矩命令"""
        try:
            torque = self.gripper_controller.get_torque()
            
            if torque is not None:
                return create_success_response(
                    message.message_id or "unknown",
                    "获取夹爪力矩成功",
                    {"torque": torque}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "获取夹爪力矩失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取夹爪力矩时发生错误: {str(e)}"
            )
    
    def _handle_goto_delta_joint(self, client_id: str, message: CommandMessage) -> str:
        """处理运动到关节位置增量命令"""
        try:
            data = message.data
            delta_joints = data.get('delta_joints', [])
            speed = data.get('speed', 50.0)
            acc = data.get('acc', 50.0)
            radius = data.get('radius', 50.0)
            
            result = self.robot_controller.goto_delta_joint(delta_joints, speed, acc, radius)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "增量运动到关节位置完成",
                    {"moved": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "增量运动到关节位置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"增量运动到关节位置时发生错误: {str(e)}"
            )

    def _handle_is_connected(self, client_id: str, message: CommandMessage) -> str:
        """处理检查机器人是否连接命令"""
        try:
            result = self.robot_controller.is_connected()
            return create_success_response(
                message.message_id or "unknown",
                "检查连接状态成功",
                {"connected": result}
            )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"检查连接状态时发生错误: {str(e)}"
            )

    def _handle_get_current_joint_positions(self, client_id: str, message: CommandMessage) -> str:
        """处理获取当前关节位置命令"""
        try:
            result = self.robot_controller.get_current_joint_positions()
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "获取关节位置成功",
                    {"joint_positions": result}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "获取关节位置失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取关节位置时发生错误: {str(e)}"
            )

    def _handle_electrify(self, client_id: str, message: CommandMessage) -> str:
        """处理机器人上电命令"""
        try:
            result = self.robot_controller.electrify()
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人上电成功",
                    {"electrified": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "机器人上电失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"机器人上电时发生错误: {str(e)}"
            )

    def _handle_blackout(self, client_id: str, message: CommandMessage) -> str:
        """处理机器人断电命令"""
        try:
            result = self.robot_controller.blackout()
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "机器人断电成功",
                    {"blackout": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "机器人断电失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"机器人断电时发生错误: {str(e)}"
            )

    def _handle_get_current_state(self, client_id: str, message: CommandMessage) -> str:
        """处理获取机器人当前状态命令"""
        try:
            result = self.robot_controller.get_current_state()
            return create_success_response(
                message.message_id or "unknown",
                "获取机器人状态成功",
                {"state": result}
            )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取机器人状态时发生错误: {str(e)}"
            )

    def _handle_get_state_description(self, client_id: str, message: CommandMessage) -> str:
        """处理获取状态描述命令"""
        try:
            data = message.data
            state = data.get('state', -1)
            result = self.robot_controller.get_state_description(state)
            return create_success_response(
                message.message_id or "unknown",
                "获取状态描述成功",
                {"description": result}
            )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取状态描述时发生错误: {str(e)}"
            )

    def _handle_is_ready(self, client_id: str, message: CommandMessage) -> str:
        """处理检查机器人是否就绪命令"""
        try:
            result = self.robot_controller.is_ready()
            return create_success_response(
                message.message_id or "unknown",
                "检查就绪状态成功",
                {"ready": result}
            )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"检查就绪状态时发生错误: {str(e)}"
            )

    def _handle_is_moving(self, client_id: str, message: CommandMessage) -> str:
        """处理检查机器人是否正在运动命令"""
        try:
            result = self.robot_controller.is_moving()
            return create_success_response(
                message.message_id or "unknown",
                "检查运动状态成功",
                {"moving": result}
            )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"检查运动状态时发生错误: {str(e)}"
            )

    def _handle_wait_for_motion_done(self, client_id: str, message: CommandMessage) -> str:
        """处理等待机器人运动完成命令"""
        try:
            data = message.data
            timeout = data.get('timeout', 30.0)
            result = self.robot_controller.wait_for_motion_done(timeout)
            return create_success_response(
                message.message_id or "unknown",
                "等待运动完成成功",
                {"done": result}
            )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"等待运动完成时发生错误: {str(e)}"
            )

    def _handle_get_override(self, client_id: str, message: CommandMessage) -> str:
        """处理获取当前速度比命令"""
        try:
            result = self.robot_controller.get_override()
            if result != -1.0:
                return create_success_response(
                    message.message_id or "unknown",
                    "获取速度比成功",
                    {"override": result}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "获取速度比失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"获取速度比时发生错误: {str(e)}"
            )

    def _handle_goto_delta(self, client_id: str, message: CommandMessage) -> str:
        """处理运动到指定末端6d姿态的增量位置命令"""
        try:
            data = message.data
            delta_pose = data.get('delta_pose', [])
            tcp = data.get('tcp', None)
            ucs = data.get('ucs', None)
            speed = data.get('speed', 50.0)
            acc = data.get('acc', 50.0)
            radius = data.get('radius', 50.0)
            
            result = self.robot_controller.goto_delta(delta_pose, tcp, ucs, speed, acc, radius)
            
            if result:
                return create_success_response(
                    message.message_id or "unknown",
                    "增量运动到姿态完成",
                    {"moved": True}
                )
            else:
                return create_error_response(
                    message.message_id or "unknown",
                    "增量运动到姿态失败"
                )
        except Exception as e:
            return create_error_response(
                message.message_id or "unknown",
                f"增量运动到姿态时发生错误: {str(e)}"
            )

    def _cleanup_client(self, client_id: str, client_socket: socket.socket):
        """清理客户端资源"""
        try:
            # 先去使能机器人（如果连接了机器人）
            try:
                robot_connected = self.session_manager.get_robot_connection_status(client_id)
                if robot_connected:
                    # 先尝试去使能机器人
                    self.robot_controller.disable()
                    self.logger.info(f"客户端 {client_id} 的机器人已去使能")
            except Exception as e:
                self.logger.error(f"机器人去使能时发生错误: {e}")
            
            # 断开机器人连接
            try:
                robot_connected = self.session_manager.get_robot_connection_status(client_id)
                if robot_connected:
                    self.robot_controller.disconnect()
                    self.session_manager.set_robot_connection_status(client_id, False)
                    self.logger.info(f"客户端 {client_id} 的机器人连接已断开")
            except Exception as e:
                self.logger.error(f"断开客户端 {client_id} 机器人连接时发生错误: {e}")
            
            # 断开夹爪连接
            try:
                gripper_connected = self.session_manager.get_gripper_connection_status(client_id)
                if gripper_connected:
                    self.gripper_controller.disconnect()
                    self.session_manager.set_gripper_connection_status(client_id, False)
                    self.logger.info(f"客户端 {client_id} 的夹爪连接已断开")
            except Exception as e:
                self.logger.error(f"断开客户端 {client_id} 夹爪连接时发生错误: {e}")
            
            # 从客户端列表中移除
            if client_id in self.clients:
                del self.clients[client_id]
            
            # 从客户端线程列表中移除
            if client_id in self.client_threads:
                del self.client_threads[client_id]
            
            # 从会话管理器中移除会话
            self.session_manager.remove_session(client_id)
            
            # 关闭客户端socket
            if client_socket:
                client_socket.close()
                
            self.logger.info(f"客户端 {client_id} 资源已清理")
            
        except Exception as e:
            self.logger.error(f"清理客户端 {client_id} 资源时发生错误: {e}")
