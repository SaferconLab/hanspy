#!/usr/bin/env python3
"""
消息协议模块
定义网络通信的消息格式
"""

import json
from typing import Dict, Any, Optional
from enum import Enum


class CommandType(Enum):
    """命令类型枚举"""
    CONNECT_ROBOT = "connect_robot"
    DISCONNECT_ROBOT = "disconnect_robot"
    ENABLE_ROBOT = "enable_robot"
    DISABLE_ROBOT = "disable_robot"
    MOVE_J = "move_j"
    MOVE_L = "move_l"
    GET_POSITION = "get_position"
    SET_OVERRIDE = "set_override"
    STOP = "stop"
    RESET = "reset"
    GOTO_POSE = "goto_pose"
    GOTO_JOINT = "goto_joint"
    CONNECT_GRIPPER = "connect_gripper"
    DISCONNECT_GRIPPER = "disconnect_gripper"
    SET_GRIPPER_AMPLITUDE = "set_gripper_amplitude"
    SET_GRIPPER_FORCE = "set_gripper_force"
    GET_GRIPPER_POSITION = "get_gripper_position"
    GET_GRIPPER_TORQUE = "get_gripper_torque"
    FIND_GRIPPER_TRAVEL = "find_gripper_travel"
    COMMAND_COMPLETED = "command_completed"
    ELECTRIFY = "electrify"
    BLACKOUT = "blackout"
    GET_CURRENT_STATE = "get_current_state"
    GET_STATE_DESCRIPTION = "get_state_description"
    IS_READY = "is_ready"
    IS_MOVING = "is_moving"
    WAIT_FOR_MOTION_DONE = "wait_for_motion_done"
    GET_OVERRIDE = "get_override"
    GOTO_DELTA = "goto_delta"
    GOTO_DELTA_JOINT = "goto_delta_joint"
    GET_CAMERAS_LIST = "get_cameras_list"
    START_CAMERA_STREAM = "start_camera_stream"
    STOP_CAMERA_STREAM = "stop_camera_stream"


class MessageStatus(Enum):
    """消息状态枚举"""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class BaseMessage:
    """基础消息类"""
    
    def __init__(self, msg_type: str, data: Optional[Dict] = None, 
                 message_id: Optional[str] = None):
        self.msg_type = msg_type
        self.data = data or {}
        self.message_id = message_id
        self.timestamp = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "type": self.msg_type,
            "data": self.data,
            "message_id": self.message_id
        }
        return result
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseMessage':
        """从字典创建消息对象"""
        return cls(
            msg_type=data.get("type"),
            data=data.get("data", {}),
            message_id=data.get("message_id")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseMessage':
        """从JSON字符串创建消息对象"""
        data = json.loads(json_str)
        # 修复：确保正确处理响应消息中的status字段
        if data.get("type") == "response":
            # 对于响应消息，我们需要特殊处理
            return ResponseMessage.from_dict(data)
        else:
            return cls.from_dict(data)


class CommandMessage(BaseMessage):
    """命令消息类"""
    
    def __init__(self, command_type: CommandType, data: Optional[Dict] = None,
                 message_id: Optional[str] = None):
        super().__init__(command_type.value, data, message_id)
        self.command_type = command_type


class ResponseMessage(BaseMessage):
    """响应消息类"""
    
    def __init__(self, status: MessageStatus, message: str, 
                 data: Optional[Dict] = None, message_id: Optional[str] = None):
        # 先调用父类构造函数
        super().__init__("response", {"status": status.value, "message": message, "data": data or {}}, message_id)
        self.status = status
        self.message = message
        self.data = data or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "type": self.msg_type,
            "status": self.status.value,  # 添加status字段到顶层
            "message": self.message,
            "data": self.data,
            "message_id": self.message_id
        }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResponseMessage':
        """从字典创建响应消息对象"""
        # 从data中提取各个字段
        status_value = data.get("status", "error")
        try:
            status = MessageStatus(status_value)
        except ValueError:
            status = MessageStatus.ERROR  # 默认错误状态
            
        message = data.get("message", "")
        data_field = data.get("data", {})
        message_id = data.get("message_id")
        
        # 创建并返回实例
        instance = cls.__new__(cls)  # 不调用__init__
        instance.status = status
        instance.message = message
        instance.data = data_field
        instance.message_id = message_id
        instance.msg_type = "response"
        return instance


def parse_message(json_str: str) -> BaseMessage:
    """
    解析JSON消息字符串
    
    Args:
        json_str (str): JSON格式的消息字符串
        
    Returns:
        BaseMessage: 解析后的消息对象
    """
    try:
        data = json.loads(json_str)
        msg_type = data.get("type")
        
        # 判断是否为响应消息
        if msg_type == "response":
            return ResponseMessage.from_dict(data)
        else:
            # 尝试转换为命令类型
            try:
                command_type = CommandType(msg_type)
                return CommandMessage(command_type, data.get("data"), data.get("message_id"))
            except ValueError:
                # 如果不是已知的命令类型，则返回基础消息
                return BaseMessage.from_dict(data)
    except json.JSONDecodeError:
        raise ValueError("无效的JSON格式")


def create_success_response(message_id: str, message: str, data: Optional[Dict] = None) -> str:
    """
    创建成功响应消息
    
    Args:
        message_id (str): 消息ID
        message (str): 响应消息内容
        data (Dict): 响应数据
        
    Returns:
        str: JSON格式的响应消息
    """
    response = ResponseMessage(MessageStatus.SUCCESS, message, data, message_id)
    return response.to_json()


def create_error_response(message_id: str, message: str, data: Optional[Dict] = None) -> str:
    """
    创建错误响应消息
    
    Args:
        message_id (str): 消息ID
        message (str): 错误消息内容
        data (Dict): 错误数据
        
    Returns:
        str: JSON格式的错误响应消息
    """
    response = ResponseMessage(MessageStatus.ERROR, message, data, message_id)
    return response.to_json()


def create_pending_response(message_id: str, message: str, data: Optional[Dict] = None) -> str:
    """
    创建待处理响应消息
    
    Args:
        message_id (str): 消息ID
        message (str): 响应消息内容
        data (Dict): 响应数据
        
    Returns:
        str: JSON格式的待处理响应消息
    """
    response = ResponseMessage(MessageStatus.PENDING, message, data, message_id)
    return response.to_json()
