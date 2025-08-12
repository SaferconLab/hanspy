# 机器人运动学接口，把运动学相关的函数和类封装在这里，便于管理和在robot_controller.py里使用。
# 调用 CPSWrapper.py 中的CPSClient类的运动学接口来实现运动学功能。

import logging
from typing import List, Union
import numpy as np

from wrapper import CPSClient


class Kinematics:
    """机器人运动学类，提供正逆运动学解算和高级运动接口"""
    
    def __init__(self, lib_wrapper: CPSClient, box_id: int = 0, robot_id: int = 0):
        """
        初始化运动学类
        
        Args:
            lib_wrapper: CPSClient实例
            box_id (int): 电箱ID，默认为0
            robot_id (int): 机器人ID，默认为0
        """
        self.lib_wrapper = lib_wrapper
        self.box_id = box_id
        self.robot_id = robot_id
    
    def inverse_kinematics(self, coord: List[float], raw_acs: List[float], 
                          tcp: List[float] = None, ucs: List[float] = None) -> List[float]:
        """
        运动学逆解，由指定用户坐标系位置和工具坐标系下的迪卡尔坐标计算对应的关节坐标位置
        
        Args:
            coord: 需要计算逆解的目标迪卡尔位置 [X, Y, Z, Rx, Ry, Rz]
            raw_acs: 参考关节坐标位置 [J1, J2, J3, J4, J5, J6]
            tcp: 工具坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            ucs: 用户坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            
        Returns:
            List[float]: 关节坐标位置 [J1, J2, J3, J4, J5, J6]
            
        Raises:
            Exception: 运动学逆解失败时抛出异常
        """
        # 设置默认值
        if tcp is None:
            tcp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if ucs is None:
            ucs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        result = []
        ret = self.lib_wrapper.HRIF_GetInverseKin(
            self.box_id, self.robot_id, coord, raw_acs, tcp, ucs, result)
        
        if ret != 0:
            raise Exception(f"运动学逆解失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("运动学逆解返回结果格式不正确")
    
    def forward_kinematics(self, raw_acs: List[float], 
                          tcp: List[float] = None, ucs: List[float] = None) -> List[float]:
        """
        运动学正解，由关节坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置
        
        Args:
            raw_acs: 关节坐标位置 [J1, J2, J3, J4, J5, J6]
            tcp: 工具坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            ucs: 用户坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            
        Returns:
            List[float]: 迪卡尔坐标位置 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 运动学正解失败时抛出异常
        """
        # 设置默认值
        if tcp is None:
            tcp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if ucs is None:
            ucs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        result = []
        ret = self.lib_wrapper.HRIF_GetForwardKin(
            self.box_id, self.robot_id, raw_acs, tcp, ucs, result)
        
        if ret != 0:
            raise Exception(f"运动学正解失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("运动学正解返回结果格式不正确")


class Calculator:
    """坐标变换计算器类"""
    
    def __init__(self, lib_wrapper: CPSClient, box_id: int = 0):
        """
        初始化计算器类
        
        Args:
            lib_wrapper: CPSClient实例
            box_id (int): 电箱ID，默认为0
        """
        self.lib_wrapper = lib_wrapper
        self.box_id = box_id
    
    def quaternion_to_rpy(self, w: float, x: float, y: float, z: float) -> List[float]:
        """
        四元素转欧拉角
        
        Args:
            w, x, y, z: 四元素分量
            
        Returns:
            List[float]: 欧拉角 [Rx, Ry, Rz]
            
        Raises:
            Exception: 转换失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_Quaternion2RPY(self.box_id, w, x, y, z, result)
        
        if ret != 0:
            raise Exception(f"四元素转欧拉角失败，错误码: {ret}")
        
        if len(result) >= 3:
            return [float(x) for x in result[0:3]]
        else:
            raise Exception("四元素转欧拉角返回结果格式不正确")
    
    def rpy_to_quaternion(self, rx: float, ry: float, rz: float) -> List[float]:
        """
        欧拉角转四元素
        
        Args:
            rx, ry, rz: 欧拉角
            
        Returns:
            List[float]: 四元素 [W, X, Y, Z]
            
        Raises:
            Exception: 转换失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_RPY2Quaternion(self.box_id, rx, ry, rz, result)
        
        if ret != 0:
            raise Exception(f"欧拉角转四元素失败，错误码: {ret}")
        
        if len(result) >= 4:
            return [float(x) for x in result[0:4]]
        else:
            raise Exception("欧拉角转四元素返回结果格式不正确")
    
    def base_to_ucs_tcp(self, coord: List[float], tcp: List[float] = None, ucs: List[float] = None) -> List[float]:
        """
        由基坐标系下的坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置
        
        Args:
            coord: 基坐标系下的坐标位置 [X, Y, Z, Rx, Ry, Rz]
            tcp: 工具坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            ucs: 用户坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            
        Returns:
            List[float]: 用户坐标系和工具坐标系下的迪卡尔坐标位置 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 坐标转换失败时抛出异常
        """
        # 设置默认值
        if tcp is None:
            tcp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if ucs is None:
            ucs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        result = []
        ret = self.lib_wrapper.HRIF_Base2UcsTcp(self.box_id, coord, tcp, ucs, result)
        
        if ret != 0:
            raise Exception(f"基坐标系转换失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("基坐标系转换返回结果格式不正确")
    
    def ucs_tcp_to_base(self, coord: List[float], tcp: List[float] = None, ucs: List[float] = None) -> List[float]:
        """
        由指定用户坐标系和工具坐标系下的迪卡尔坐标位置计算基坐标系下的坐标位置
        
        Args:
            coord: 用户坐标系和工具坐标系下的迪卡尔坐标位置 [X, Y, Z, Rx, Ry, Rz]
            tcp: 工具坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            ucs: 用户坐标系 [X, Y, Z, Rx, Ry, Rz]，默认为[0, 0, 0, 0, 0, 0]
            
        Returns:
            List[float]: 基坐标系下的坐标位置 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 坐标转换失败时抛出异常
        """
        # 设置默认值
        if tcp is None:
            tcp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if ucs is None:
            ucs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        result = []
        ret = self.lib_wrapper.HRIF_UcsTcp2Base(self.box_id, coord, tcp, ucs, result)
        
        if ret != 0:
            raise Exception(f"用户坐标系转换失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("用户坐标系转换返回结果格式不正确")
    
    def pose_add(self, pose1: List[float], pose2: List[float]) -> List[float]:
        """
        点位加法计算，使用矩阵左乘运算（第二个点左乘第一个点）
        
        Args:
            pose1: 空间坐标1 [X, Y, Z, Rx, Ry, Rz]
            pose2: 空间坐标2 [X, Y, Z, Rx, Ry, Rz]
            
        Returns:
            List[float]: 计算结果 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 计算失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_PoseAdd(self.box_id, pose1, pose2, result)
        
        if ret != 0:
            raise Exception(f"点位加法计算失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("点位加法计算返回结果格式不正确")
    
    def pose_sub(self, pose1: List[float], pose2: List[float]) -> List[float]:
        """
        点位减法计算，以第二个点为参考点
        
        Args:
            pose1: 空间坐标1 [X, Y, Z, Rx, Ry, Rz]
            pose2: 空间坐标2 [X, Y, Z, Rx, Ry, Rz]
            
        Returns:
            List[float]: 计算结果 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 计算失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_PoseSub(self.box_id, pose1, pose2, result)
        
        if ret != 0:
            raise Exception(f"点位减法计算失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("点位减法计算返回结果格式不正确")
    
    def pose_trans(self, pose1: List[float], pose2: List[float]) -> List[float]:
        """
        坐标变换
        
        Args:
            pose1: 坐标位置1 [X, Y, Z, Rx, Ry, Rz]
            pose2: 坐标位置2 [X, Y, Z, Rx, Ry, Rz]
            
        Returns:
            List[float]: 计算结果 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 计算失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_PoseTrans(self.box_id, pose1, pose2, result)
        
        if ret != 0:
            raise Exception(f"坐标变换计算失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("坐标变换计算返回结果格式不正确")
    
    def pose_inverse(self, pose: List[float]) -> List[float]:
        """
        坐标逆变换
        
        Args:
            pose: 空间坐标 [X, Y, Z, Rx, Ry, Rz]
            
        Returns:
            List[float]: 计算结果 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 计算失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_PoseInverse(self.box_id, pose, result)
        
        if ret != 0:
            raise Exception(f"坐标逆变换计算失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("坐标逆变换计算返回结果格式不正确")
    
    def pose_dist(self, pose1: List[float], pose2: List[float]) -> List[float]:
        """
        计算点位距离
        
        Args:
            pose1: 空间坐标1 [X, Y, Z, Rx, Ry, Rz]
            pose2: 空间坐标2 [X, Y, Z, Rx, Ry, Rz]
            
        Returns:
            List[float]: [点位距离(mm), 姿态距离(°)]
            
        Raises:
            Exception: 计算失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_PoseDist(self.box_id, pose1, pose2, result)
        
        if ret != 0:
            raise Exception(f"点位距离计算失败，错误码: {ret}")
        
        if len(result) >= 2:
            return [float(x) for x in result[0:2]]
        else:
            raise Exception("点位距离计算返回结果格式不正确")
    
    def pose_interpolate(self, pose1: List[float], pose2: List[float], alpha: float) -> List[float]:
        """
        空间位置直线插补计算
        
        Args:
            pose1: 空间坐标1 [X, Y, Z, Rx, Ry, Rz]
            pose2: 空间坐标2 [X, Y, Z, Rx, Ry, Rz]
            alpha: 插补比例 (0-1)
            
        Returns:
            List[float]: 计算结果 [X, Y, Z, Rx, Ry, Rz]
            
        Raises:
            Exception: 计算失败时抛出异常
        """
        result = []
        ret = self.lib_wrapper.HRIF_PoseInterpolate(self.box_id, pose1, pose2, alpha, result)
        
        if ret != 0:
            raise Exception(f"空间位置直线插补计算失败，错误码: {ret}")
        
        if len(result) >= 6:
            return [float(x) for x in result[0:6]]
        else:
            raise Exception("空间位置直线插补计算返回结果格式不正确")
