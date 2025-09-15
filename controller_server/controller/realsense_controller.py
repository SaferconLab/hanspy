#!/usr/bin/env python3
"""
RealSense相机控制器模块
用于控制RealSense相机，包括连接、设置参数、获取图像和深度信息等功能
"""

import logging
import time
import pyrealsense2 as rs
import numpy as np
from typing import Tuple, Optional, Dict, Any
import cv2


class RealSenseController:
    """RealSense相机控制器类"""
    
    def __init__(self, config: dict):
        """
        初始化RealSense控制器
        
        Args:
            config (dict): 配置信息
        """
        self.config = config
        self.pipeline = None
        self.config_profile = None
        self.device = None
        self.depth_sensor = None
        self.color_sensor = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.depth_frame = None
        self.color_frame = None
        self.pointcloud = None
        
    def connect(self) -> bool:
        """
        连接到RealSense相机
        
        Returns:
            bool: 连接是否成功
        """
        try:
            # 创建管道对象
            self.pipeline = rs.pipeline()
            
            # 创建配置对象
            self.config_profile = rs.config()
            
            # 启用深度和颜色流
            if self.config.get('enable_depth', True):
                width = self.config.get('depth_width', 640)
                height = self.config.get('depth_height', 480)
                fps = self.config.get('depth_fps', 30)
                self.config_profile.enable_stream(
                    rs.stream.depth, 
                    rs.format.z16, 
                    fps
                )
                
            if self.config.get('enable_color', True):
                width = self.config.get('color_width', 640)
                height = self.config.get('color_height', 480)
                fps = self.config.get('color_fps', 30)
                self.config_profile.enable_stream(
                    rs.stream.color, 
                    rs.format.bgr8, 
                    fps
                )
            
            # 启动管道
            self.pipeline.start(self.config_profile)
            
            # 获取设备信息
            profile = self.pipeline.get_active_profile()
            self.device = profile.get_device()
            
            # 获取传感器信息
            sensors = list(self.device.sensors)
            for sensor in sensors:
                if sensor.get_info(rs.camera_info.name) == 'Depth Sensor':
                    self.depth_sensor = sensor
                elif sensor.get_info(rs.camera_info.name) == 'RGB Camera':
                    self.color_sensor = sensor
            
            self.connected = True
            self.logger.info("RealSense相机连接成功")
            return True
            
        except Exception as e:
            self.logger.error(f"RealSense相机连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> bool:
        """
        断开RealSense相机连接
        
        Returns:
            bool: 断开是否成功
        """
        try:
            if self.pipeline:
                self.pipeline.stop()
                self.pipeline = None
            self.connected = False
            self.logger.info("RealSense相机连接已断开")
            return True
        except Exception as e:
            self.logger.error(f"RealSense相机断开连接失败: {e}")
            return False
    
    def is_connected(self) -> bool:
        """
        检查相机是否已连接
        
        Returns:
            bool: 是否已连接
        """
        return self.connected
    
    def set_camera_parameters(self, params: Dict[str, Any]) -> bool:
        """
        设置相机参数
        
        Args:
            params (Dict[str, Any]): 参数字典
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if not self.connected:
                self.logger.error("相机未连接，无法设置参数")
                return False
                
            # 设置深度传感器参数
            if self.depth_sensor and 'depth' in params:
                depth_params = params['depth']
                for param_name, param_value in depth_params.items():
                    if hasattr(rs.option, param_name):
                        option = getattr(rs.option, param_name)
                        self.depth_sensor.set_option(option, param_value)
                        
            # 设置颜色传感器参数
            if self.color_sensor and 'color' in params:
                color_params = params['color']
                for param_name, param_value in color_params.items():
                    if hasattr(rs.option, param_name):
                        option = getattr(rs.option, param_name)
                        self.color_sensor.set_option(option, param_value)
                        
            self.logger.info("相机参数设置成功")
            return True
            
        except Exception as e:
            self.logger.error(f"相机参数设置失败: {e}")
            return False
    
    def get_depth_frame(self) -> Optional[np.ndarray]:
        """
        获取深度帧
        
        Returns:
            Optional[np.ndarray]: 深度图像数组，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("相机未连接，无法获取深度帧")
                return None
                
            # 等待帧
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            self.depth_frame = frames.get_depth_frame()
            
            if not self.depth_frame:
                return None
                
            # 转换为numpy数组
            depth_image = np.asanyarray(self.depth_frame.get_data())
            return depth_image
            
        except Exception as e:
            self.logger.error(f"获取深度帧失败: {e}")
            return None
    
    
    def get_color_frame(self) -> Optional[np.ndarray]:
        """
        获取彩色帧
        
        Returns:
            Optional[np.ndarray]: 彩色图像数组，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("相机未连接，无法获取彩色帧")
                return None
                
            # 等待帧
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            self.color_frame = frames.get_color_frame()
            
            if not self.color_frame:
                return None
                
            # 转换为numpy数组
            color_image = np.asanyarray(self.color_frame.get_data())
            return color_image
            
        except Exception as e:
            self.logger.error(f"获取彩色帧失败: {e}")
            return None
    
    def get_pointcloud(self) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        获取点云数据
        
        Returns:
            Optional[Tuple[np.ndarray, np.ndarray]]: (点云坐标, 纹理坐标)，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("相机未连接，无法获取点云数据")
                return None
                
            # 等待帧
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                return None
            
            # 创建点云对象
            if self.pointcloud is None:
                self.pointcloud = rs.pointcloud()
                self.pointcloud.map_to(color_frame)
            
            # 计算点云
            points = self.pointcloud.calculate(depth_frame)
            
            # 获取顶点和纹理坐标
            v, t = points.get_vertices(), points.get_texture_coordinates()
            verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
            texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv
            
            return (verts, texcoords)
            
        except Exception as e:
            self.logger.error(f"获取点云数据失败: {e}")
            return None
    
    def get_camera_intrinsics(self) -> Optional[Dict[str, Any]]:
        """
        获取相机内参
        
        Returns:
            Optional[Dict[str, Any]]: 相机内参信息，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("相机未连接，无法获取内参")
                return None
                
            # 获取活动配置
            profile = self.pipeline.get_active_profile()
            depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
            depth_intrinsics = depth_profile.get_intrinsics()
            
            intrinsics = {
                'width': depth_intrinsics.width,
                'height': depth_intrinsics.height,
                'fx': depth_intrinsics.fx,
                'fy': depth_intrinsics.fy,
                'ppx': depth_intrinsics.ppx,
                'ppy': depth_intrinsics.ppy,
                'model': depth_intrinsics.model.value,
                'coeffs': depth_intrinsics.coeffs
            }
            
            return intrinsics
            
        except Exception as e:
            self.logger.error(f"获取相机内参失败: {e}")
            return None
    
    def get_frame_metadata(self) -> Optional[Dict[str, Any]]:
        """
        获取帧元数据
        
        Returns:
            Optional[Dict[str, Any]]: 帧元数据，失败返回None
        """
        try:
            if not self.connected:
                self.logger.error("相机未连接，无法获取帧元数据")
                return None
                
            # 等待帧
            frames = self.pipeline.wait_for_frames(timeout_ms=1000)
            
            metadata = {}
            if self.depth_frame:
                metadata['depth_timestamp'] = self.depth_frame.get_timestamp()
                metadata['depth_frame_number'] = self.depth_frame.get_frame_number()
                
            if self.color_frame:
                metadata['color_timestamp'] = self.color_frame.get_timestamp()
                metadata['color_frame_number'] = self.color_frame.get_frame_number()
                
            return metadata
            
        except Exception as e:
            self.logger.error(f"获取帧元数据失败: {e}")
            return None
