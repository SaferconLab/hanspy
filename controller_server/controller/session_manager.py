#!/usr/bin/env python3
"""
会话管理器模块
负责管理客户端连接状态和会话信息
"""

import threading
import time
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ClientSession:
    """客户端会话信息"""
    client_id: str
    client_address: str
    connected_at: datetime
    last_activity: datetime
    robot_connected: bool = False
    gripper_connected: bool = False
    is_active: bool = True

class SessionManager:
    """会话管理器类"""
    
    def __init__(self):
        self._sessions: Dict[str, ClientSession] = {}
        self._lock = threading.Lock()
        self._session_counter = 0
    
    def create_session(self, client_address: str) -> str:
        """
        创建新的客户端会话
        
        Args:
            client_address (str): 客户端地址
            
        Returns:
            str: 会话ID
        """
        with self._lock:
            self._session_counter += 1
            client_id = f"client_{self._session_counter}"
            
            session = ClientSession(
                client_id=client_id,
                client_address=client_address,
                connected_at=datetime.now(),
                last_activity=datetime.now()
            )
            
            self._sessions[client_id] = session
            return client_id
    
    def get_session(self, client_id: str) -> Optional[ClientSession]:
        """
        获取指定会话信息
        
        Args:
            client_id (str): 会话ID
            
        Returns:
            ClientSession: 会话信息，不存在则返回None
        """
        with self._lock:
            return self._sessions.get(client_id)
    
    def update_activity(self, client_id: str):
        """
        更新会话活动时间
        
        Args:
            client_id (str): 会话ID
        """
        with self._lock:
            session = self._sessions.get(client_id)
            if session:
                session.last_activity = datetime.now()
    
    def set_robot_connection_status(self, client_id: str, connected: bool):
        """
        设置机器人连接状态
        
        Args:
            client_id (str): 会话ID
            connected (bool): 连接状态
        """
        with self._lock:
            session = self._sessions.get(client_id)
            if session:
                session.robot_connected = connected
    
    def set_gripper_connection_status(self, client_id: str, connected: bool):
        """
        设置夹爪连接状态
        
        Args:
            client_id (str): 会话ID
            connected (bool): 连接状态
        """
        with self._lock:
            session = self._sessions.get(client_id)
            if session:
                session.gripper_connected = connected

    def get_gripper_connection_status(self, client_id: str) -> bool:
        """
        获取夹爪连接状态
        
        Args:
            client_id (str): 会话ID
            
        Returns:
            bool: 夹爪连接状态
        """
        with self._lock:
            session = self._sessions.get(client_id)
            if session:
                return session.gripper_connected
            return False

    def get_robot_connection_status(self, client_id: str) -> bool:
        """
        获取机器人连接状态
        
        Args:
            client_id (str): 会话ID
            
        Returns:
            bool: 机器人连接状态
        """
        with self._lock:
            session = self._sessions.get(client_id)
            if session:
                return session.robot_connected
            return False
    
    def remove_session(self, client_id: str):
        """
        移除会话
        
        Args:
            client_id (str): 会话ID
        """
        with self._lock:
            if client_id in self._sessions:
                del self._sessions[client_id]
    
    def get_active_sessions(self) -> Dict[str, ClientSession]:
        """
        获取所有活跃会话
        
        Returns:
            Dict[str, ClientSession]: 活跃会话字典
        """
        with self._lock:
            return {k: v for k, v in self._sessions.items() if v.is_active}
    
    def cleanup_expired_sessions(self, max_age_seconds: int = 3600):
        """
        清理过期会话
        
        Args:
            max_age_seconds (int): 最大存活时间（秒）
        """
        with self._lock:
            current_time = datetime.now()
            expired_sessions = []
            
            for client_id, session in self._sessions.items():
                if (current_time - session.last_activity).seconds > max_age_seconds:
                    expired_sessions.append(client_id)
            
            for client_id in expired_sessions:
                del self._sessions[client_id]
