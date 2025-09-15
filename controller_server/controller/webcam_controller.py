#!/usr/bin/env python3
"""
USB摄像头控制器模块
用于控制USB摄像头，包括连接、获取图像等基本功能
"""

import logging
import cv2
import subprocess
import json
from typing import List, Dict, Optional
import threading
import time
import signal


class WebcamController:
    """USB摄像头控制器类"""
    
    def __init__(self, config: dict):
        """
        初始化USB摄像头控制器
        
        Args:
            config (dict): 配置信息
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.cameras = []
        self.connected = False
        self.current_camera_index = None
        self.stream_process = None
        self.is_streaming = False
        self.stream_lock = threading.Lock()
        self._auto_started = False  # 标记是否是自动启动的流
        
        # 在初始化时列出可用摄像头
        self.list_available_cameras()
        
        # 自动启动视频流（如果配置允许）
        self.auto_start_stream()
        
    def list_available_cameras(self) -> List[Dict]:
        """
        列出所有可用的摄像头设备
        
        Returns:
            List[Dict]: 可用摄像头列表
        """
        try:
            # 使用v4l2-ctl列出设备
            cmd = ['v4l2-ctl', '--list-devices']
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            
            cameras = []
            for block in out.split('\n\n'):
                lines = block.strip().splitlines()
                if not lines:
                    continue
                name = lines[0].rstrip(':')
                for dev in lines[1:]:
                    dev = dev.strip()
                    if '/dev/video' in dev:
                        idx = int(dev.split('video')[-1])
                        # 使用OpenCV测试摄像头是否真正可用
                        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
                        if cap.read()[0]:
                            # 获取摄像头信息
                            camera_info = {
                                'index': idx,
                                'name': name,
                                'path': dev,
                                'width': cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                                'height': cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                                'fps': cap.get(cv2.CAP_PROP_FPS)
                            }
                            cameras.append(camera_info)
                        cap.release()
            
            self.cameras = cameras
            self.logger.info(f"发现 {len(cameras)} 个可用摄像头")
            return cameras
            
        except Exception as e:
            self.logger.error(f"列出摄像头失败: {e}")
            return []
    
    def connect_camera(self, camera_index: int) -> bool:
        """
        连接到指定的摄像头（仅检查摄像头是否存在）
        
        Args:
            camera_index (int): 摄像头索引
            
        Returns:
            bool: 连接是否成功
        """
        try:
            # 检查摄像头是否存在
            if not any(cam['index'] == camera_index for cam in self.cameras):
                self.logger.error(f"摄像头 {camera_index} 不存在或不可用")
                return False
            
            self.current_camera_index = camera_index
            self.connected = True
            self.logger.info(f"成功连接到摄像头 {camera_index}")
            return True
            
        except Exception as e:
            self.logger.error(f"连接摄像头 {camera_index} 失败: {e}")
            return False
    
    def disconnect_camera(self) -> bool:
        """
        断开当前摄像头连接
        
        Returns:
            bool: 断开是否成功
        """
        try:
            # 如果正在推流，先停止
            if self.is_streaming:
                self.stop_streaming()
            
            self.current_camera_index = None
            self.connected = False
            self.logger.info("摄像头连接已断开")
            return True
            
        except Exception as e:
            self.logger.error(f"断开摄像头连接失败: {e}")
            return False
    
    def is_connected(self) -> bool:
        """
        检查摄像头是否已连接
        
        Returns:
            bool: 是否已连接
        """
        return self.connected
    
    def get_camera_info(self) -> Optional[Dict]:
        """
        获取当前摄像头信息
        
        Returns:
            Optional[Dict]: 摄像头信息，失败返回None
        """
        if not self.connected or self.current_camera_index is None:
            return None
            
        try:
            # 查找对应的摄像头信息
            for cam in self.cameras:
                if cam['index'] == self.current_camera_index:
                    return cam.copy()
            return None
        except Exception as e:
            self.logger.error(f"获取摄像头信息失败: {e}")
            return None
    
    def start_streaming(self) -> bool:
        """
        使用ustreamer启动视频流
        
        Returns:
            bool: 是否成功开始流
        """
        if not self.connected or self.current_camera_index is None:
            self.logger.error("未连接到摄像头，无法开始流")
            return False
            
        try:
            # 如果已经在流中，先停止
            if self.is_streaming:
                self.stop_streaming()
            
            # 构建ustreamer命令
            width = self.config.get('width', 1280)
            height = self.config.get('height', 720)
            fps = self.config.get('fps', 30)
            
            # 获取推流端口，如果没有指定则使用默认值
            stream_port = self.config.get('stream_port', 9999)
            
            cmd = [
                'ustreamer',
                '--device', f'/dev/video{self.current_camera_index}',
                '--format', 'mjpeg',
                '-c', 'HW',  # 使用硬件编码
                '--resolution', f'{width}x{height}',
                '--desired-fps', str(fps),
                '--host', '0.0.0.0',
                '-p', str(stream_port),  # 使用配置的端口
                '--tcp-nodelay'
            ]
            
            self.logger.info(f"启动推流命令: {' '.join(cmd)}")
            
            # 启动推流进程
            self.stream_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待一段时间确认进程启动
            time.sleep(1)
            
            if self.stream_process.poll() is None:
                self.is_streaming = True
                self.logger.info(f"摄像头 {self.current_camera_index} 推流已启动")
                return True
            else:
                # 进程已经退出
                stdout, stderr = self.stream_process.communicate()
                self.logger.error(f"ustreamer启动失败: {stderr.decode()}")
                return False
                
        except Exception as e:
            self.logger.error(f"启动视频流失败: {e}")
            self.is_streaming = False
            return False
    
    def stop_streaming(self) -> bool:
        """
        停止视频流
        
        Returns:
            bool: 是否成功停止流
        """
        try:
            if self.stream_process and self.stream_process.poll() is None:
                # 发送终止信号
                self.stream_process.terminate()
                try:
                    # 等待进程结束
                    self.stream_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # 强制杀死进程
                    self.stream_process.kill()
                    self.stream_process.wait()
                
            self.is_streaming = False
            self.stream_process = None
            self.logger.info(f"停止摄像头 {self.current_camera_index} 视频流")
            return True
            
        except Exception as e:
            self.logger.error(f"停止视频流失败: {e}")
            return False
    
    def get_frame(self) -> Optional[bytes]:
        """
        获取当前帧（此方法不再使用，因为使用ustreamer推流）
        
        Returns:
            Optional[bytes]: 图像数据，失败返回None
        """
        self.logger.warning("get_frame方法不再使用，请通过网络访问推流端口获取帧")
        return None
    
    def get_camera_list(self) -> List[Dict]:
        """
        获取摄像头列表（兼容旧接口）
        
        Returns:
            List[Dict]: 摄像头列表
        """
        return self.list_available_cameras()
    
    def get_current_camera_index(self) -> Optional[int]:
        """
        获取当前连接的摄像头索引
        
        Returns:
            Optional[int]: 当前摄像头索引
        """
        return self.current_camera_index
    
    def auto_start_stream(self):
        """
        根据配置自动启动视频流
        """
        try:
            # 检查是否启用自动启动
            if not self.config.get('auto_start', False):
                self.logger.info("自动启动视频流已禁用")
                return
            
            # 获取默认摄像头索引
            default_camera_index = self.config.get('default_camera_index', 9)
            
            # 检查摄像头是否存在
            if not any(cam['index'] == default_camera_index for cam in self.cameras):
                self.logger.warning(f"默认摄像头 {default_camera_index} 不存在或不可用")
                return
            
            # 连接并启动视频流
            self.logger.info(f"自动启动摄像头 {default_camera_index} 的视频流")
            
            # 连接摄像头
            if not self.connect_camera(default_camera_index):
                self.logger.error(f"自动启动失败：无法连接到摄像头 {default_camera_index}")
                return
            
            # 启动流
            if not self.start_streaming():
                self.logger.error(f"自动启动失败：无法启动摄像头 {default_camera_index} 的流")
                # 断开连接
                self.disconnect_camera()
                return
                
            # 设置自动启动标志
            self._auto_started = True
            self.logger.info(f"成功自动启动摄像头 {default_camera_index} 的视频流")
            
        except Exception as e:
            self.logger.error(f"自动启动视频流时发生错误: {e}")
