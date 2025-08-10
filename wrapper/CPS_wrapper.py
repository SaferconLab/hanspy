#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CPS包装器模块
为二进制CPS模块提供完整的Python源码接口包装
"""

# 导入原始的二进制模块
import sys
import os
# 添加当前目录到Python路径，以便能找到 .so 文件
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from . import CPS as _CPS #CPS是CPS.cpython-38-x86_64-linux-gnu.so

class CPSClient:
    """CPS客户端类，提供机器人控制接口"""
    
    # 类属性
    MaxBox = _CPS.CPSClient.MaxBox
    clientIP = _CPS.CPSClient.clientIP
    clientPort = _CPS.CPSClient.clientPort
    dic_FSM = _CPS.CPSClient.dic_FSM
    g_client_state = _CPS.CPSClient.g_client_state
    g_clients = _CPS.CPSClient.g_clients
    xmlrpcAddr = _CPS.CPSClient.xmlrpcAddr
    
    def __init__(self):
        """初始化CPS客户端"""
        self._client = _CPS.CPSClient()
    
    def HRIF_AddSafePlane(self, boxID, rbtID, name, UcsName, mode, display, switch):
        """
        添加虚拟墙平面；虚拟墙平面即安全平面，只是相应的功能不同，如果添加的安全平面名称已经存在，会报20006错误；最后一个参数为是否激活，如果不激活，不会检查UCS 是否存在；
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            Name：平面名称，string
            UcsName：用户坐标名称，string
            Mode：安全模式，int，0/1
            Display：显示，int，0/1
            Switch：启用，int，0/1
            
        返回值：nRet，int，>0 的整型值
            nRet = 0：返回函数调用成功
            nRet >0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义平面名称
            >>> Name = "planel"
            >>> # 定义使用的用户坐标名称
            >>> UcsName = "Plane_1"
            >>> # 定义安全模式
            >>> Mode = 0
            >>> # 定义是否显示
            >>> Display = 0
            >>> # 定义是否启用
            >>> Switch = 1
            >>> # 添加虚拟墙平面
            >>> nRet = cps.HRIF_AddSafePlane(0, 0, Name, UcsName , Mode, Display, Switch)
        """
        return self._client.HRIF_AddSafePlane(boxID, rbtID, name, UcsName, mode, display, switch)
    
    def HRIF_Base2UcsTcp(self, boxID, Base, TCP, UCS, result):
        """
        由基坐标系下的坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            Base：需要转换的迪卡尔位置，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            TCP：目标位置是否包含工具坐标(不包含工具坐标则所有值=0)，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            UCS：目标位置是否包含用户坐标(不包含用户坐标则所有值=0)，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回指定用户坐标系和工具坐标系下的迪卡尔坐标位置，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> Base = [0, 0, 0, 0, 0, 0]
            >>> Tcp = [0, 0, 0, 0, 0, 0]
            >>> Ucs = [0, 0, 0, 0, 0, 0]
            >>> ret = cps.HRIF_Base2UcsTcp(0, Base, Tcp, Ucs, result)
            >>> print(result)  # 返回转换后的坐标
        """
        return self._client.HRIF_Base2UcsTcp(boxID, Base, TCP, UCS, result)
    
    def HRIF_BlackOut(self, boxID):
        """
        机器人断电。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_BlackOut(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_BlackOut(boxID)
    
    def HRIF_CalTcp3P(self, boxID, pos1, pos2, pos3, result):
        """
        通过三点平面法计算TCP。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            pos1：点1在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            pos2：点2在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            pos3：点3在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回计算得出的TCP位姿，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]，result[6]返回结果质量(0:良好, 1:差, 2:异常)
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> pos1 = [10, 0, 0, 10, 0, 0]
            >>> pos2 = [0, 10, 0, 0, 10, 0]
            >>> pos3 = [0, 0, 10, 0, 0, 10]
            >>> ret = cps.HRIF_CalTcp3P(0, pos1, pos2, pos3, result)
            >>> print(result)  # 返回计算得出的TCP位姿及质量
        """
        return self._client.HRIF_CalTcp3P(boxID, pos1, pos2, pos3, result)
    
    def HRIF_CalTcp4P(self, boxID, pos1, pos2, pos3, pos4, result):
        """
        通过四点平面法计算TCP。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            pos1：点1在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            pos2：点2在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            pos3：点3在Base坐标系下系统默认TCP的位置，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            pos4：点4在Base坐标系下系统默认TCP的位置，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回计算得出的TCP位姿，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]，result[6]返回结果质量(0:良好, 1:差, 2:异常)，result[7]-result[10]返回源点的错误指示(0:异常, 1:正常)
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> pos1 = [10, 0, 0, 10, 0, 0]
            >>> pos2 = [0, 10, 0, 0, 10, 0]
            >>> pos3 = [0, 0, 10, 0, 0, 10]
            >>> pos4 = [0, 0, 0, 0, 0, 0]
            >>> ret = cps.HRIF_CalTcp4P(0, pos1, pos2, pos3, pos4, result)
            >>> print(result)  # 返回计算得出的TCP位姿及质量信息
        """
        return self._client.HRIF_CalTcp4P(boxID, pos1, pos2, pos3, pos4, result)
    
    def HRIF_CalUcsLine(self, boxID, pos1, pos2, result):
        """
        通过两点直线法计算UCS。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            pos1：点1在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            pos2：点2在Base坐标系下系统默认TCP的位姿，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回计算得出的UCS位姿，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> pos1 = [10, 0, 0, 10, 0, 0]
            >>> pos2 = [0, 10, 0, 0, 10, 0]
            >>> ret = cps.HRIF_CalUcsLine(0, pos1, pos2, result)
            >>> print(result)  # 返回计算得出的UCS位姿
        """
        return self._client.HRIF_CalUcsLine(boxID, pos1, pos2, result)
    
    def HRIF_CalUcsPlane(self, boxID, pos1, pos2, pos3, result):
        """
        通过三点平面法计算UCS。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            pos1：点1在Base坐标系下系统默认TCP的位置，list[float]，格式为[x,y,z]，单位[mm]
            pos2：点2在Base坐标系下系统默认TCP的位置，list[float]，格式为[x,y,z]，单位[mm]
            pos3：点3在Base坐标系下系统默认TCP的位置，list[float]，格式为[x,y,z]，单位[mm]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回计算得出的UCS位姿，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> pos1 = [10, 0, 0]
            >>> pos2 = [0, 10, 0]
            >>> pos3 = [0, 0, 10]
            >>> ret = cps.HRIF_CalUcsPlane(0, pos1, pos2, pos3, result)
            >>> print(result)  # 返回计算得出的UCS位姿
        """
        return self._client.HRIF_CalUcsPlane(boxID, pos1, pos2, pos3, result)
    
    def HRIF_CheckTemperatureUnderLow(self, boxID, rbtID, result):
        """
        检查温度是否过低
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：存储结果的列表，传入空列表，result[0]返回温度检查结果(0:正常, 1:过低)
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_CheckTemperatureUnderLow(0, 0, result)
            >>> print(result[0])  # 0表示温度正常，1表示温度过低
        """
        return self._client.HRIF_CheckTemperatureUnderLow(boxID, rbtID, result)
    
    def HRIF_CloseBrake(self, boxID, nAxisID):
        """
        抱闸。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            nAxisID：需要抱闸的目标轴ID，int，0~5，对应关节J1-J6
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_CloseBrake(0, 5)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_CloseBrake(boxID, nAxisID)
    
    def HRIF_ConfigTCP(self, boxID, name, pos):
        """
        新建指定名称的TCP和值
        
        该函数用于新建指定名称的TCP和值，将工具坐标信息保存到系统中。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            name：需要新建的工具坐标名称，string
            pos：工具坐标值，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> pos = [0, 0, 10, 0, 0, 0]
            >>> ret = cps.HRIF_ConfigTCP(0, "TCP1", pos)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_ConfigTCP(boxID, name, pos)
    
    def HRIF_ConfigUCS(self, boxID, name, pos):
        """
        新建指定名称的UCS和值
        
        该函数用于新建指定名称的UCS和值，将用户坐标信息保存到系统中。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            name：需要新建的用户坐标名称，string
            pos：用户坐标值，list[float]，格式为[x,y,z,rx,ry,rz]，单位分别为[mm]和[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> pos = [0, 0, 0, 0, 0, 0]
            >>> ret = cps.HRIF_ConfigUCS(0, "UCS1", pos)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_ConfigUCS(boxID, name, pos)
    
    def HRIF_Connect(self, boxID, hostName, nPort):
        """
        连接机器人服务器。
        
        该函数用于建立与机器人控制器的连接。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            hostName：控制器IP地址，string，根据实际设置的IP地址定义
            nPort：控制器端口，int，一般为10003
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_Connect(0, '192.168.0.10', 10003)
            >>> print(ret)  # 0表示成功
            
        See Also:
            HRIF_DisConnect: 断开连接机器人服务器。
            HRIF_IsConnected: 判断控制器是否连接。
            HRIF_Connect2Box: 连接控制器电箱。
            HRIF_Connect2Controller: 连接控制器。
        """
        return self._client.HRIF_Connect(boxID, hostName, nPort)
    
    def HRIF_Connect2Box(self, boxID):
        """
        连接控制器电箱。
        
        该函数用于连接控制器电箱，建立与电箱的通信连接。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于连接控制器电箱，建立与电箱的通信连接。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_Connect2Box(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_Connect2Box(boxID)
    
    def HRIF_Connect2Controller(self, boxID):
        """
        连接控制器，连接过程中会启动主站，初始化从站，配置参数，检查配置，完成后跳转到去使能状态。
        
        该函数用于连接控制器，连接过程中会启动主站，初始化从站，配置参数，检查配置，完成后跳转到去使能状态。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于连接控制器，连接过程中会启动主站，初始化从站，配置参数，检查配置，完成后跳转到去使能状态。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_Connect2Controller(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_Connect2Controller(boxID)
    
    def HRIF_ContinueScript(self, boxID):
        """
        继续脚本执行
        
        该函数用于继续执行之前被暂停的脚本。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于继续执行之前被暂停的脚本。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_ContinueScript(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_ContinueScript(boxID)
    
    def HRIF_DelMovePathJ(self, boxID, rbtID, trackName):
        """
        删除关节运动路径

        该函数用于删除已创建的关节运动路径。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            trackName：路径名称，string

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_DelMovePathJ(0, 0, "path1")
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_DelMovePathJ(boxID, rbtID, trackName)
    
    def HRIF_DelPath(self, boxID, rbtID, sPathName):
        """
        删除路径
        
        该函数用于删除已创建的路径。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sPathName：路径名称，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_DelPath(0, 0, "path1")
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_DelPath(boxID, rbtID, sPathName)
    
    def HRIF_DelSafePlane(self, boxID, rbtID, name):
        """
        删除安全平面
        
        该函数用于删除已创建的安全平面。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            name：安全平面名称，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_DelSafePlane(0, 0, "safe_plane1")
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_DelSafePlane(boxID, rbtID, name)
    
    def HRIF_DisConnect(self, boxID):
        """
        断开连接机器人服务器。
        
        该函数用于断开与机器人服务器的连接。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_DisConnect(0)
            >>> print(ret)  # 0表示成功
            
        See Also:
            HRIF_Connect: 连接机器人服务器。
            HRIF_IsConnected: 判断控制器是否连接。
        """
        return self._client.HRIF_DisConnect(boxID)
    
    def HRIF_Electrify(self, boxID):
        """
        机器人上电。
        
        该函数用于对机器人进行上电操作，使机器人进入可运行状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_Electrify(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_Electrify(boxID)
    
    def HRIF_EnableEndBTN(self, boxID, rbtID, state):
        """
        启用末端按钮
        
        该函数用于启用或禁用末端按钮功能。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            state：按钮状态，int，0：禁用，1：启用
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_EnableEndBTN(0, 0, 1)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_EnableEndBTN(boxID, rbtID, state)
    
    def HRIF_EndPushMovePath(self, boxID, rbtID, trackName):
        """
        结束推送运动路径
        
        该函数用于结束推送运动路径操作。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            trackName：路径名称，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_EndPushMovePath(0, 0, "path1")
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_EndPushMovePath(boxID, rbtID, trackName)
    
    def HRIF_EndPushMovePathJ(self, boxID, rbtID, trackName):
        """
        结束推送关节运动路径
        
        该函数用于结束推送关节运动路径操作。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            trackName：路径名称，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_EndPushMovePathJ(0, 0, "path1")
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_EndPushMovePathJ(boxID, rbtID, trackName)
    
    def HRIF_EndPushPathPoints(self, boxID, rbtID, sPathName):
        """
        结束向轨迹中推送点位，并开始计算轨迹。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sPathName：轨迹名称，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sPathName= "drag_01"
            >>> # 下发完成，开始计算轨迹
            >>> nRet = cps.HRIF_EndPushPathPoints(0,0, sPathName)
        """
        return self._client.HRIF_EndPushPathPoints(boxID, rbtID, sPathName)
    
    def HRIF_EnterSafetyGuard(self, boxID, rbtID, flag):
        """
        强制进入安全光幕（软急停）。
        
        该函数用于强制进入/退出安全光幕（软急停）。进入软急停后，示教器或者前端界面上看到的现象是进入了安全光幕。用此指令退出软急停后，需要在示教器或者前端界面点击"光幕恢复"。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            flag：状态标识，int，0：退出软急停，1：进入软急停
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 进入软急停
            >>> ret = cps.HRIF_EnterSafetyGuard(0, 0, 1)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_EnterSafetyGuard(boxID, rbtID, flag)
    
    def HRIF_FinishInitialize(self):
        """
        完成初始化
        
        该函数用于完成机器人系统的初始化过程。
        
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_FinishInitialize()
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_FinishInitialize()
    
    def HRIF_ForceControlContinue(self, boxID, rbtID):
        """
        继续力控运动，仅继续力控运动功能，不继续运动和脚本。（此接口功能已屏蔽）
        
        描述：继续力控运动，仅继续力控运动功能，不继续运动和脚本。（此接口功能已屏蔽）
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置力控继续运动
            >>> nRet = cps.HRIF_ForceControlContinue(0,0)
        """
        return self._client.HRIF_ForceControlContinue(boxID, rbtID)
    
    def HRIF_ForceControlInterrupt(self, boxID, rbtID):
        """
        暂停力控运动，仅暂停力控功能，不暂停运动和脚本。（此接口功能已屏蔽）
        
        描述：暂停力控运动，仅暂停力控功能，不暂停运动和脚本。（此接口功能已屏蔽）
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置力控暂停状态
            >>> nRet = cps.HRIF_ForceControlInterrupt(0,0)
        """
        return self._client.HRIF_ForceControlInterrupt(boxID, rbtID)
    
    def HRIF_GetErrorCodeStr(self, boxID, nErrorCode, result):
        """
        获取错误码解释。
        
        该函数用于获取指定错误码的具体描述说明。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            nErrorCode：错误码，int
            result：存储结果的列表，传入空列表
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_GetErrorCodeStr(0, 20018, result)
            >>> print(result[0])  # 返回错误码20018的具体描述
        """
        return self._client.HRIF_GetErrorCodeStr(boxID, nErrorCode, result)
    
    def HRIF_GetForwardKin(self, boxID, rbtID, rawACS, tcp, ucs, result):
        """
        正向运动学
        
        该函数用于计算给定关节位置下的正向运动学解。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            rawACS：关节位置，list[float]，格式为[J1,J2,J3,J4,J5,J6]，单位[°]
            tcp：工具坐标，list[float]，格式为[X,Y,Z,Rx,Ry,Rz]，单位分别为[mm]和[°]
            ucs：用户坐标，list[float]，格式为[X,Y,Z,Rx,Ry,Rz]，单位分别为[mm]和[°]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回笛卡尔坐标位置，格式为[X,Y,Z,Rx,Ry,Rz]，单位分别为[mm]和[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> rawACS = [0, 0, 0, 0, 0, 0]
            >>> tcp = [0, 0, 0, 0, 0, 0]
            >>> ucs = [0, 0, 0, 0, 0, 0]
            >>> ret = cps.HRIF_GetForwardKin(0, 0, rawACS, tcp, ucs, result)
            >>> print(result)  # 返回笛卡尔坐标位置
        """
        return self._client.HRIF_GetForwardKin(boxID, rbtID, rawACS, tcp, ucs, result)
    
    def HRIF_GetInverseKin(self, boxID, rbtID, rawPCS, rawACS, tcp, ucs, result):
        """
        逆向运动学
        
        该函数用于计算给定笛卡尔位置下的逆向运动学解。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            rawPCS：笛卡尔位置，list[float]，格式为[X,Y,Z,Rx,Ry,Rz]，单位分别为[mm]和[°]
            rawACS：关节位置，list[float]，格式为[J1,J2,J3,J4,J5,J6]，单位[°]
            tcp：工具坐标，list[float]，格式为[X,Y,Z,Rx,Ry,Rz]，单位分别为[mm]和[°]
            ucs：用户坐标，list[float]，格式为[X,Y,Z,Rx,Ry,Rz]，单位分别为[mm]和[°]
            result：存储结果的列表，传入空列表，result[0]-result[5]返回关节位置，格式为[J1,J2,J3,J4,J5,J6]，单位[°]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> rawPCS = [0, 0, 0, 0, 0, 0]
            >>> rawACS = [0, 0, 0, 0, 0, 0]
            >>> tcp = [0, 0, 0, 0, 0, 0]
            >>> ucs = [0, 0, 0, 0, 0, 0]
            >>> ret = cps.HRIF_GetInverseKin(0, 0, rawPCS, rawACS, tcp, ucs, result)
            >>> print(result)  # 返回关节位置
        """
        return self._client.HRIF_GetInverseKin(boxID, rbtID, rawPCS, rawACS, tcp, ucs, result)
    
    def HRIF_GetMovePathJOLIndex(self, rbtID, boxID, result):
        """
        获取关节运动路径索引
        
        该函数用于获取关节运动路径的索引信息。
        
        输入变量：
            rbtID：机器人 ID，int，0~5
            boxID：电箱 ID，int，0~5
            result：存储结果的列表，传入空列表，result[0]返回路径索引
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_GetMovePathJOLIndex(0, 0, result)
            >>> print(result[0])  # 返回路径索引
        """
        return self._client.HRIF_GetMovePathJOLIndex(rbtID, boxID, result)
    
    def HRIF_GrpCloseFreeDriver(self, boxID, rbtID):
        """
        机器人关闭自由驱动。
        
        该函数用于关闭机器人的自由驱动功能。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpCloseFreeDriver(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpCloseFreeDriver(boxID, rbtID)
    
    def HRIF_GrpContinue(self, boxID, rbtID):
        """
        机器人继续运动命令。
        
        该函数用于继续机器人之前被暂停的运动命令。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpContinue(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpContinue(boxID, rbtID)
    
    def HRIF_GrpDisable(self, boxID, rbtID):
        """
        机器人去使能命令。
        
        该函数用于机器人去使能命令，使机器人停止运动控制。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpDisable(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpDisable(boxID, rbtID)
    
    def HRIF_GrpEnable(self, boxID, rbtID):
        """
        机器人使能命令。
        
        该函数用于机器人使能命令，使机器人可以进行运动控制。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpEnable(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpEnable(boxID, rbtID)
    
    def HRIF_GrpInterrupt(self, boxID, rbtID):
        """
        机器人暂停运动命令。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于机器人暂停运动命令。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpInterrupt(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpInterrupt(boxID, rbtID)
    
    def HRIF_GrpOpenFreeDriver(self, boxID, rbtID):
        """
        机器人开启自由驱动。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于机器人开启自由驱动。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpOpenFreeDriver(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpOpenFreeDriver(boxID, rbtID)
    
    def HRIF_GrpReset(self, boxID, rbtID):
        """
        机器人复位命令。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于机器人复位命令，将机器人恢复到初始状态。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpReset(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpReset(boxID, rbtID)
    
    def HRIF_GrpStop(self, boxID, rbtID):
        """
        机器人停止运动命令。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于机器人停止运动命令，立即停止机器人的运动。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_GrpStop(0, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_GrpStop(boxID, rbtID)
    
    def HRIF_HRApp(self, boxID, name, cmd, param, result):
        """HR应用接口"""
        return self._client.HRIF_HRApp(boxID, name, cmd, param, result)
    
    def HRIF_HRAppCmd(self, boxID, name, cmd, param, result):
        """HR应用命令"""
        return self._client.HRIF_HRAppCmd(boxID, name, cmd, param, result)
    
    def HRIF_InitMovePathL(self, boxID, rbtID, trackName, vel, acc, jerk, ucs, tcp):
        """
        初始化空间轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            dVelocity：轨迹运动速度，float
            dAcc：轨迹运动加速度，float
            dJerk：轨迹运动加加速度，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 定义运动速度
            >>> dVelocity = 100
            >>> # 定义运动加速度
            >>> dAcc = 2500
            >>> # 定义运动加加速度
            >>> dJerk = 1000000
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 初始化关节连续轨迹运动
            >>> nRet = cps.HRIF_InitMovePathL(0,0,sTrackName, dVelocity, dAcc, dJerk, sUcsName, sTcpName)
        """
        return self._client.HRIF_InitMovePathL(boxID, rbtID, trackName, vel, acc, jerk, ucs, tcp)
    
    def HRIF_InitPath(self, boxID, rbtID, nRawDataType, sPathName, dSpeedRatio, dRadius, vel, acc, jerk, ucs, tcp):
        """
        初始化轨迹。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nRawDataType：原始点位类型，int，0/1
            sPathName：轨迹名称，string
            dSpeedRatio：轨迹运动速度比，float，0.01~1.00
            dRadius：过渡半径，float，>0
            dVelocity：轨迹运动速度，float
            dAcc：轨迹运动加速度，float
            dJerk：轨迹运动加加速度，float
            sUcsName：用户坐标名称，string
            sTcpName：工具坐标名称，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 原始点位类型
            >>> nRawDataType = 1
            >>> # 轨迹名称
            >>> trajectName = "Path_01"
            >>> # 轨迹运动速度比
            >>> dSpeedRatio = 0.3
            >>> # 过渡半径
            >>> dRadius = 20
            >>> # 轨迹运动速度
            >>> dVelocity = 100
            >>> # 轨迹运动加速度
            >>> dAcc = 500
            >>> # 轨迹运动加加速度
            >>> dJerk = 10000
            >>> # 用户坐标名称
            >>> sUcsName = "Base"
            >>> # 工具坐标名称
            >>> sTcpName = "TCP"
            >>> # 初始化直线运动轨迹
            >>> nRet = cps.HRIF_InitPath(0,0,nRawDataType,trajectName,dSpeedRatio,dRadius,dVelocity,dAcc, dJerk, sUcsName,
            >>> sTcpName)
        """
        return self._client.HRIF_InitPath(boxID, rbtID, nRawDataType, sPathName, dSpeedRatio, dRadius, vel, acc, jerk, ucs, tcp)
    
    def HRIF_InitServoEsJ(self, boxID, rbtID):
        """初始化伺服EsJ"""
        return self._client.HRIF_InitServoEsJ(boxID, rbtID)
    
    def HRIF_IsBlendingDone(self, boxID, rbtID, result):
        """
        判断路点是否运动完成。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list，传入空列表，result = [ ]
            
        输出变量：
            result[0]：返回值，bool，False/True
              - False：运动未完成，处于运动状态
              - True：运动完成，处于准备就绪状态
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 判断路点是否运动完成
            >>> nRet = cps.HRIF_IsBlendingDone(0,0,result)
            >>> # 路点运动未完成
            >>> result[0] = False
            >>> # 路点运动完成
            >>> result[0] =True
        """
        return self._client.HRIF_IsBlendingDone(boxID, rbtID, result)
    
    def HRIF_IsConnected(self, boxID):
        """
        判断控制器是否连接。
        
        该函数用于判断控制器是否连接。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            
        Returns:
            bool: True表示控制器已连接，False表示控制器未连接
            
        Note:
            该函数用于判断控制器是否连接。
            描述：判断控制器是否连接。
            该函数用于判断控制器是否连接。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_IsConnected(0)
            >>> print(ret)  # True表示已连接
            
        See Also:
            HRIF_Connect: 连接机器人服务器。
            HRIF_DisConnect: 断开连接机器人服务器。
        """
        return self._client.HRIF_IsConnected(boxID)
    
    def HRIF_IsControllerStarted(self, boxID, result):
        """
        检查控制器是否启动完成。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            result (list): 存储结果的列表，传入空列表
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于检查控制器是否启动完成。result[0]返回0表示未启动，1表示已启动。
            
        Example:
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_IsControllerStarted(0, result)
            >>> print(result[0])  # 0表示未启动，1表示已启动
        """
        return self._client.HRIF_IsControllerStarted(boxID, result)
    
    def HRIF_IsMotionDone(self, boxID, rbtID, result):
        """
        判断机器人是否处于运动状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list，传入空列表，result = [ ]
            
        输出变量：
            result[0]：返回值，bool，False/True
              - False：运动未完成，处于运动状态
              - True：运动完成，处于准备就绪状态
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 判断机器人是否处于运动状态
            >>> nRet = cps.HRIF_IsMotionDone(0,0,result)
            >>> # 机器人处于运动状态
            >>> result[0] = False
            >>> # 机器人不处于运动状态
            >>> result[0] =True
        """
        return self._client.HRIF_IsMotionDone(boxID, rbtID, result)
    
    def HRIF_IsSimulateRobot(self, boxID, result):
        """
        检查是否为模拟机器人。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            result (list): 存储结果的列表，传入空列表
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于检查是否为模拟机器人。result[0]返回0表示真实机器人，1表示模拟机器人。
            
        Example:
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_IsSimulateRobot(0, result)
            >>> print(result[0])  # 0表示真实机器人，1表示模拟机器人
        """
        return self._client.HRIF_IsSimulateRobot(boxID, result)
    
    def HRIF_MoveC(self, boxID, rbtID, StartPoint, AuxPoint, EndPoint, fixedPosure, nMoveCType, nRadLen, speed, Acc, radius, tcp, ucs, cmdID):
        """
        圆弧轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            dStartPoint：圆弧起始点位置，list[float]
            dAuxPoint：圆弧经过点位置，list[float]
            dEndPoint：圆弧结束点位置，list[float]
            nFixedPosure：是否固定姿态，int，0/1
            nMoveCType：圆弧类型，int，0/1
            dRadLen：弧长，float
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 圆弧起始点位置
            >>> dStartPoint = [420, 0, 445, 180, 0, 180]
            >>> # 圆弧经过点位置
            >>> dAuxPoint  = [420, 50, 445, 180, 0, 180]
            >>> # 圆弧结束点位置
            >>> dEndPoint = [470, 0, 445, 180, 0, 180]
            >>> # 是否固定姿态
            >>> nFixedPosure = 0
            >>> # 圆弧类型
            >>> nMoveCType = 0
            >>> # 整圆圈数
            >>> dRadLen = 1
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet = cps.HRIF_MoveC(0,0,dStartPoint , dAuxPoint, dEndPoint,
            >>> nFixedPosure, nMoveCType, dRadLen, dVelocity, dAcc, dRadius,sTcpName , sUcsName, strCmdID)
        """
        return self._client.HRIF_MoveC(boxID, rbtID, StartPoint, AuxPoint, EndPoint, fixedPosure, nMoveCType, nRadLen, speed, Acc, radius, tcp, ucs, cmdID)
    
    def HRIF_MoveCircularWeave(self, boxID, rbtID, StartPoint, AuxPoint, EndPoint, dVelocity, Acc, dRadius, nOrientMode, nMoveWhole, dMoveWholeLen, dAmplitude, dIntervalDistance, nWeaveFrameType, dElevation, dAzimuth, dCentreRise, nEnableWaiTime, nPosiTime, nNegaTime, sTcpName, sUcsName, sCmdID):
        """圆弧摆动运动"""
        return self._client.HRIF_MoveCircularWeave(boxID, rbtID, StartPoint, AuxPoint, EndPoint, dVelocity, Acc, dRadius, nOrientMode, nMoveWhole, dMoveWholeLen, dAmplitude, dIntervalDistance, nWeaveFrameType, dElevation, dAzimuth, dCentreRise, nEnableWaiTime, nPosiTime, nNegaTime, sTcpName, sUcsName, sCmdID)
    
    def HRIF_MoveE(self, boxID, rbtID, dP1, dP2, dP3, dP4, dP5, nOrientMode, nMoveType, dArcLength, dVelocity, dAcc, Radius, tcp, ucs, cmdID):
        """
        椭圆型轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            dP1-dP5：示教位置，list[float]
            nOrientMode：运动模式，int，0/1
            nMoveType：运动类型，int，0/1
            dArcLength：弧长，float
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 示教点1
            >>> dP1 = [420,0,445,180,0,180]
            >>> # 示教点2
            >>> dP2 = [460,0,445,180,0,180]
            >>> # 示教点3
            >>> dP3 = [480,10,445,180,0,180]
            >>> # 示教点4
            >>> dP4 = [460,20,445,180,0,180]
            >>> # 示教点5
            >>> dP5 = [420,20,445,180,0,180]
            >>> # 运动模式
            >>> nOrientMode = 0
            >>> # 运动类型
            >>> nMoveType = 1
            >>> # 弧长
            >>> dArcLength = 360
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 2500
            >>> # 定义过渡半径
            >>> dRadius = 5
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行椭圆运动
            >>> nRet = cps.HRIF_MoveE(0,0,dP1, dP2, dP3,dP4, dP5,
            >>> nOrientMode,nMoveType,dArcLength,dVelocity,dAcc,dRadius, sTcpName, sUcsName, strCmdID)
        """
        return self._client.HRIF_MoveE(boxID, rbtID, dP1, dP2, dP3, dP4, dP5, nOrientMode, nMoveType, dArcLength, dVelocity, dAcc, Radius, tcp, ucs, cmdID)
    
    def HRIF_MoveJ(self, boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek, bit, state, cmdID):
        """
        关节运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            dX-dRz：空间目标位置，float
            dJ1-dJ6：关节目标位置，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            nIsUseJoint：是否使用关节坐标，int，0/1
            nIsSeek：是否检测DI 停止，int，0/1
            nIOBit：检测的 DI 索引，int，0~7
            nIOState：检测的 DI 状态，int，0/1
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义空间目标位置
            >>> Point = [ 0, 0, 90, 0, 90, 0]
            >>> # 定义关节目标位置
            >>> RawACSpoints = [ 0, 0, 90, 0, 90, 0]
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义是否使用关节角度
            >>> nIsUseJoint= 1
            >>> # 定义是否使用检测DI 停止
            >>> nIsSeek = 0
            >>> # 定义检测的 DI 索引
            >>> nIOBit = 0
            >>> # 定义检测的 DI 状态
            >>> nIOState = 0
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet  =  cps.HRIF_MoveJ(0,0,  Point,  RawACSpoints,  sTcpName  ,  sUcsName,  dVelocity,  dAcc,
            >>> dRadius,nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
        """
        return self._client.HRIF_MoveJ(boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek, bit, state, cmdID)
    
    def HRIF_MoveL(self, boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isSeek, bit, state, cmdID):
        """
        直线轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            dX-dRz：空间目标位置，float
            dJ1-dJ6：关节参考位置，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            nIsSeek：是否检测DI 停止，int，0/1
            nIOBit：检测的 DI 索引，int，0~7
            nIOState：检测的 DI 状态，int，0/1
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义空间目标位置
            >>> Point = [ 420, 0, 445, 180, 0, 180]
            >>> # 定义关节目标位置
            >>> RawACSpoints = [ 0, 0, 90, 0, 90, 0]
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义是否使用检测DI停止
            >>> nIsSeek = 0
            >>> # 定义检测的DI索引
            >>> nIOBit = 0
            >>> # 定义检测的DI状态
            >>> nIOState = 0
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet = cps.HRIF_MoveL(0,0, Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,nIsSeek,
            >>> nIOBit, nIOState, strCmdID)
        """
        return self._client.HRIF_MoveL(boxID, rbtID, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isSeek, bit, state, cmdID)
    
    def HRIF_MoveLinearWeave(self, boxID, rbtID, StartPoint, EndPoint, dVelocity, Acc, dRadius, dAmplitude, dIntervalDistance, nWeaveFrameType, dElevation, dAzimuth, dCentreRise, nEnableWaiTime, nPosiTime, nNegaTime, sTcpName, sUcsName, sCmdID):
        """直线摆动运动"""
        return self._client.HRIF_MoveLinearWeave(boxID, rbtID, StartPoint, EndPoint, dVelocity, Acc, dRadius, dAmplitude, dIntervalDistance, nWeaveFrameType, dElevation, dAzimuth, dCentreRise, nEnableWaiTime, nPosiTime, nNegaTime, sTcpName, sUcsName, sCmdID)
    
    def HRIF_MovePathJ(self, boxID, rbtID, sPathName):
        """
        运动指定的轨迹。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 运动轨迹
            >>> nRet = cps.HRIF_MovePathJ(0,0,sTrackName)
        """
        return self._client.HRIF_MovePathJ(boxID, rbtID, sPathName)
    
    def HRIF_MovePathJOL(self, boxID, rbtID, dVel, dAcc, dTol, RawACSpoints, nIsSetIO, nEndDOMask, nEndDOVal, nBoxDOMask, nBoxDOVal, nBoxCOMask, nBoxCOVal, nBoxAOCH0_Mask, nBoxAOCH0_Mode, nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val):
        """
        启动在线实施规划的MovePathJ。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            dVel：关节速度，float
            dAcc：关节加速度，float
            dTol：过渡参数，float
            RawACSpoints：关节目标位置，list[float]
            nIsSetIO：各点是否设置IO，list[int]
            nEndDOMask：各个需要更改的EndDO按bit标识，list[int]
            nEndDOVal：各个需要更改的EndDO的目标状态，list[int]
            nBoxDOMask：各个需要更改的BoxDO按bit标识，list[int]
            nBoxDOVal：各个需要更改的BoxDO的目标状态，list[int]
            nBoxCOMask：需要更改的BoxCO按bit标识，list[int]
            nBoxCOVal：各个需要更改的BoxCO的目标状态，list[int]
            nBoxAOCH0_Mask：BoxAOCH0是否需要更改的标识，list[int]
            nBoxAOCH0_Mode：模式，list[int]
            nBoxAOCH1_Mask：BoxAOCH1是否需要更改的标识，list[int]
            nBoxAOCH1_Mode：模式，list[int]
            dbBoxAOCH0_Val：各点对应模拟量值，list[float]
            dbBoxAOCH1_Val：各点对应模拟量值，list[float]
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义速度
            >>> dVel = 15
            >>> # 定义加速度
            >>> dAcc = 20
            >>> # 定义过渡参数
            >>> dTol = 2
            >>> # 定义各点关节目标位置，6个一组
            >>> RawACSpoints = [0,0,90,0,90,0, 0,0,91,0,90,0, 0,0,92,0,90,0]
            >>> # 各点是否设置IO
            >>> nIsSetIO = [1,1,1]
            >>> # 需要更改的各点EndDO
            >>> nEndDOMask = [7,7,7]
            >>> # 需要更改的各点EndDO的目标状态
            >>> nEndDOVal = [2,2,2]
            >>> # 需要更改的各点BoxDO
            >>> nBoxDOMask = [86,86,86]
            >>> # 需要更改的各点BoxDO的目标状态
            >>> nBoxDOVal = [255,255,255]
            >>> # 需要更改的各点BoxCO
            >>> nBoxCOMask = [255,255,255]
            >>> # 需要更改的各点BoxCO的目标状态
            >>> nBoxCOVal = [169,169,169]
            >>> # 各点BoxAOCH0是否需要更改的标识
            >>> nBoxAOCH0_Mask = [1,1,1]
            >>> # 模式
            >>> nBoxAOCH0_Mode = [2,2,2]
            >>> # 各点BoxAOCH1是否需要更改的标识
            >>> nBoxAOCH1_Mask = [1,1,1]
            >>> # 模式
            >>> nBoxAOCH1_Mode =  [1,1,1]
            >>> # 各点对应模拟量值
            >>> dbBoxAOCH0_Val = [6.66,6.66,6.66]
            >>> # 各点对应模拟量值
            >>> dbBoxAOCH1_Val = [9.99,9.99,9.99]
            >>> # 开始运动
            >>> nRet = cps.HRIF_MovePathJOL(0,0,dVel, dAcc, dTol, RawACSpoints, nIsSetIO, nEndDOMask, nEndDOVal,
            >>> nBoxDOMask,  nBoxDOVal,  nBoxCOMask,  nBoxCOVal,  nBoxAOCH0_Mask,  nBoxAOCH0_Mode,
            >>> nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val)
        """
        return self._client.HRIF_MovePathJOL(boxID, rbtID, dVel, dAcc, dTol, RawACSpoints, nIsSetIO, nEndDOMask, nEndDOVal, nBoxDOMask, nBoxDOVal, nBoxCOMask, nBoxCOVal, nBoxAOCH0_Mask, nBoxAOCH0_Mode, nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val)
    
    def HRIF_MovePathL(self, boxID, rbtID, sPathName):
        """
        执行空间坐标轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path2"
            >>> # 开始空间连续轨迹运动
            >>> nRet = cps.HRIF_MovePathL(0,0,sTrackName)
        """
        return self._client.HRIF_MovePathL(boxID, rbtID, sPathName)
    
    def HRIF_MoveRelJ(self, boxID, rbtID, nAxis, nDirection, dDistance):
        """
        关节相对运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nAxis：轴 ID，int，0~5
            nDirection：方向，int，0/1
            dDistance：运动距离，float
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义轴ID
            >>> nAxis = 1
            >>> # 定义运动方向
            >>> nDirection = 1
            >>> # 定义运动距离
            >>> nDistance = 1
            >>> # 执行相对关节运动
            >>> nRet = cps.HRIF_MoveRelJ(0,0, nAxis, nDirection, nDistance)
        """
        return self._client.HRIF_MoveRelJ(boxID, rbtID, nAxis, nDirection, dDistance)
    
    def HRIF_MoveRelL(self, boxID, rbtID, nAxis, nDirection, dDistance, nToolMotion):
        """
        空间相对运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nAxis：轴 ID，int，0~5
            nDirection：方向，int，0/1
            dDistance：运动距离，float
            nToolMotion：运动坐标类型，int，0/1
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义轴ID
            >>> nAxis = 1
            >>> # 定义运动方向
            >>> nDirection = 1
            >>> # 定义运动距离
            >>> nDistance= 1
            >>> # 定义运动坐标类型
            >>> nToolMotion = 1
            >>> # 执行相对空间运动
            >>> nRet = cps.HRIF_MoveRelL(0,0, nAxis, nDirection, nDistance, nToolMotion)
        """
        return self._client.HRIF_MoveRelL(boxID, rbtID, nAxis, nDirection, dDistance, nToolMotion)
    
    def HRIF_MoveS(self, boxID, rbtID, dSpiralIncrement, dSpiralDiameter, dVelocity, dAcc, dRadius, sTcpName, sUcsName, cmdID):
        """螺旋运动"""
        return self._client.HRIF_MoveS(boxID, rbtID, dSpiralIncrement, dSpiralDiameter, dVelocity, dAcc, dRadius, sTcpName, sUcsName, cmdID)
    
    def HRIF_MoveToSS(self, boxID):
        """
        移动到安全位置。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于移动机器人到安全位置。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_MoveToSS(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_MoveToSS(boxID)
    
    def HRIF_MoveZ(self, boxID, rbtID, StartPoint, EndPoint, PlanePoint, Speed, Acc, WIdth, Density, EnableDensity, EnablePlane, EnableWaiTime, PosiTime, NegaTime, Radius, tcp, ucs, cmdID):
        """
        Z型轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            dStartPos：Z型起始点位置，float
            dEndPos：Z型结束点位置，float
            dPlanePos：轨迹确定平面点位置，float
            dVelocity：速度，float
            dAcc：加速度，float
            dWidth：宽度，float
            dDensity：密度，float
            nEnableDensity：是否使用密度，int
            nEnablePlane：是否使用平面点，int
            nEnableWaiTime：是否开启转折点等待时间，int
            nPosiTime：正向转折点等待时间，int
            nNegaTime：负向转折点等待时间，int
            dRadius：过渡半径，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 起始点位置
            >>> dStartPos = [420, 0, 445, 180, 0, 180]
            >>> # 结束点位置
            >>> dEndPos = [420, 100, 445, 180, 0, 180]
            >>> # 确定轨迹平面点位置
            >>> dPlanePos = [470, 50, 445, 180, 0, 180]
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 2500
            >>> # 宽度
            >>> dWidth = 50
            >>> # 密度
            >>> dDensity = 10
            >>> # 使用密度
            >>> nEnableDensity = 1
            >>> # 使用平面点
            >>> nEnablePlane = 1
            >>> # 是否在转折点等待-不等待
            >>> nEnableWaiTime = 0
            >>> # 正向转折点等待时间
            >>> nPosiTime = 0
            >>> # 负向转折点等待时间
            >>> nNegaTime = 0
            >>> # 定义过渡半径
            >>> dRadius = 5
            >>> # 定义工具坐标变量
            >>> sTcpName =  "TCP "
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet  =  cps.HRIF_MoveZ(0,0,dStartPos,  dEndPos,  dPlanePos,  dVelocity,  dAcc,  dWidth,  dDensity,
            >>> nEnableDensity, nEnablePlane, nEnableWaiTime, nPosiTime, nNegaTime, dRadius, sTcpName, sUcsName,
            >>> strCmdID)
        """
        return self._client.HRIF_MoveZ(boxID, rbtID, StartPoint, EndPoint, PlanePoint, Speed, Acc, WIdth, Density, EnableDensity, EnablePlane, EnableWaiTime, PosiTime, NegaTime, Radius, tcp, ucs, cmdID)
    
    def HRIF_OpenBrake(self, boxID, nAxisID):
        """
        松闸。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            nAxisID (int): 需要松闸的目标轴ID，范围0~5，对应关节J1-J6
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于松闸操作。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_OpenBrake(0, 5)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_OpenBrake(boxID, nAxisID)
    
    def HRIF_PauseScript(self, boxID):
        """暂停脚本"""
        return self._client.HRIF_PauseScript(boxID)
    
    def HRIF_PoseAdd(self, boxID, pos1, pos2, result):
        """姿态相加"""
        return self._client.HRIF_PoseAdd(boxID, pos1, pos2, result)
    
    def HRIF_PoseDefdFrame(self, boxID, pos1, pos2, pos3, pos4, pos5, pos6, result):
        """定义姿态框架"""
        return self._client.HRIF_PoseDefdFrame(boxID, pos1, pos2, pos3, pos4, pos5, pos6, result)
    
    def HRIF_PoseDist(self, boxID, pos1, pos2, result):
        """姿态距离"""
        return self._client.HRIF_PoseDist(boxID, pos1, pos2, result)
    
    def HRIF_PoseInterpolate(self, boxID, pos1, pos2, alpha, result):
        """姿态插值"""
        return self._client.HRIF_PoseInterpolate(boxID, pos1, pos2, alpha, result)
    
    def HRIF_PoseInverse(self, boxID, pos1, result):
        """姿态逆运算"""
        return self._client.HRIF_PoseInverse(boxID, pos1, result)
    
    def HRIF_PoseSub(self, boxID, pos1, pos2, result):
        """姿态相减"""
        return self._client.HRIF_PoseSub(boxID, pos1, pos2, result)
    
    def HRIF_PoseTrans(self, boxID, pos1, pos2, result):
        """姿态变换"""
        return self._client.HRIF_PoseTrans(boxID, pos1, pos2, result)
    
    def HRIF_PushMovePathJ(self, boxID, rbtID, trackName, paramsJ):
        """
        下发运动轨迹点位。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            paramsJ：关节点位，list[float]
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 目标关节位置
            >>> paramsJ = [0,0,90,0,0,0]
            >>> # 下发关节点位
            >>> nRet = cps.HRIF_PushMovePathJ (0,0,sTrackName, paramsJ)
        """
        return self._client.HRIF_PushMovePathJ(boxID, rbtID, trackName, paramsJ)
    
    def HRIF_PushMovePathL(self, boxID, rbtID, trackName, paramPcs):
        """
        下发运动轨迹点位。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            paramPcs：空间点位，list[float]
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 定义空间目标位置
            >>> paramPcs = [420, 0, 445, 180, 0, 180]
            >>> # 下发空间目标点位
            >>> nRet = cps.HRIF_PushMovePathL(0,0,sTrackName, paramPcs)
        """
        return self._client.HRIF_PushMovePathL(boxID, rbtID, trackName, paramPcs)
    
    def HRIF_PushMovePaths(self, boxID, rbtID, trackName, moveType, pointsSize, points):
        """
        批量下发轨迹点位，调用一次可下发多个点位数据。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            nMoveType：点位类型，int，0/1
            nPointsSize：点位数量，int
            sPoints：点位数据，list[float]
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 运动类型
            >>> nMoveType = 1
            >>> # 点位数量
            >>> nPointsSize = 6
            >>> sPoints = [420,0,445,180,0,180,420,10,445,180,0,180,420,20,445,180,0,180,
            >>> 420,30,445,180,0,180,420,40,445,180,0,180,420,50,445,180,0,180]
            >>> # 下发空间目标点位
            >>> nRet = cps.HRIF_PushMovePaths(0,0,sTrackName, nMoveType, nPointsSize, sPoints)
        """
        return self._client.HRIF_PushMovePaths(boxID, rbtID, trackName, moveType, pointsSize, points)
    
    def HRIF_PushPathPoints(self, boxID, rbtID, sPathName, sPoints):
        """
        向轨迹中批量推送原始点位（可多次调用）。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sPathName：轨迹名称，string
            sPoints：点位数据，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> trajectName = "Path_01"
            >>> # 点位数据
            >>> sPoints = [420,0,445,180,0,180, 430,10,445,180,0,180, 440,50,445,180,0,180,
            >>> 520,100,445,180,0,180, 450,50,445,180,0,180, 430,200,445,180,0,180]
            >>> # 向轨迹中批量推送原始点位
            >>> nRet = cps.HRIF_PushPathPoints(0,0, trajectName,sPoints)
        """
        return self._client.HRIF_PushPathPoints(boxID, rbtID, sPathName, sPoints)
    
    def HRIF_PushServoEsJ(self, boxID, rbtID, nPointSize, sPoints):
        """推送伺服EsJ"""
        return self._client.HRIF_PushServoEsJ(boxID, rbtID, nPointSize, sPoints)
    
    def HRIF_PushServoJ(self, boxID, rbtID, dACS):
        """推送伺服J"""
        return self._client.HRIF_PushServoJ(boxID, rbtID, dACS)
    
    def HRIF_PushServoP(self, boxID, rbtID, pose, ucs, tcp):
        """推送伺服P"""
        return self._client.HRIF_PushServoP(boxID, rbtID, pose, ucs, tcp)
    
    def HRIF_Quaternion2RPY(self, boxID, dQuaW, dQuaX, dQuaY, dQuaZ, result):
        """四元数转RPY"""
        return self._client.HRIF_Quaternion2RPY(boxID, dQuaW, dQuaX, dQuaY, dQuaZ, result)
    
    def HRIF_RPY2Quaternion(self, boxID, Rx, Ry, Rz, result):
        """RPY转四元数"""
        return self._client.HRIF_RPY2Quaternion(boxID, Rx, Ry, Rz, result)
    
    def HRIF_ReadActJointCur(self, boxID, rbtID, result):
        """读取实际关节电流"""
        return self._client.HRIF_ReadActJointCur(boxID, rbtID, result)
    
    def HRIF_ReadActJointPos(self, boxID, rbtID, result):
        """读取实际关节位置"""
        return self._client.HRIF_ReadActJointPos(boxID, rbtID, result)
    
    def HRIF_ReadActJointVel(self, boxID, rbtID, result):
        """读取实际关节速度"""
        return self._client.HRIF_ReadActJointVel(boxID, rbtID, result)
    
    def HRIF_ReadActPos(self, boxID, rbtID, result):
        """
        读取当前实际位置信息。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：关节坐标，string
              - result[0]：关节1坐标，单位[°]
              - result[1]：关节2坐标，单位[°]
              - result[2]：关节3坐标，单位[°]
              - result[3]：关节4坐标，单位[°]
              - result[4]：关节5坐标，单位[°]
              - result[5]：关节6坐标，单位[°]
            result[6]-result[11]：迪卡尔坐标，string
              - result[6]：X坐标，单位[mm]
              - result[7]：Y坐标，单位[mm]
              - result[8]：Z坐标，单位[mm]
              - result[9]：Rx坐标，单位[°]
              - result[10]：Ry坐标，单位[°]
              - result[11]：Rz坐标，单位[°]
            result[12]-result[17]：当前工具坐标，string
              - result[12]：X坐标，单位[mm]
              - result[13]：Y坐标，单位[mm]
              - result[14]：Z坐标，单位[mm]
              - result[15]：Rx坐标，单位[°]
              - result[16]：Ry坐标，单位[°]
              - result[17]：Rz坐标，单位[°]
            result[18]-result[23]：当前用户坐标，string
              - result[18]：X坐标，单位[mm]
              - result[19]：Y坐标，单位[mm]
              - result[20]：Z坐标，单位[mm]
              - result[21]：Rx坐标，单位[°]
              - result[22]：Ry坐标，单位[°]
              - result[23]：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取当前实际位置信息
            >>> nRet = cps.HRIF_ReadActPos(0,0,result)
            >>> # 读取关节位置变量
            >>> dJ1 = float(result[0])
            >>> dJ2 = float(result[1])
            >>> dJ3 = float(result[2])
            >>> dJ4 = float(result[3])
            >>> dJ5 = float(result[4])
            >>> dJ6 = float(result[5])
            >>> # 读取空间位置变量
            >>> dX = float(result[6])
            >>> dY = float(result[7])
            >>> dZ = float(result[8])
            >>> dRx = float(result[9])
            >>> dRy = float(result[10])
            >>> dRz = float(result[11])
            >>> # 读取工具坐标变量
            >>> dTcp_X = float(result[12])
            >>> dTcp_Y = float(result[13])
            >>> dTcp_Z = float(result[14])
            >>> dTcp_Rx = float(result[15])
            >>> dTcp_Ry = float(result[16])
            >>> dTcp_Rz = float(result[17])
            >>> # 读取用户坐标变量
            >>> dUcs_X = float(result[18])
            >>> dUcs_Y = float(result[19])
            >>> dUcs_Z = float(result[20])
            >>> dUcs_Rx = float(result[21])
            >>> dUcs_Ry = float(result[22])
            >>> dUcs_Rz = float(result[23])
        """
        return self._client.HRIF_ReadActPos(boxID, rbtID, result)
    
    def HRIF_ReadActTcpPos(self, boxID, rbtID, result):
        """
        读取实际TCP位置。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：TCP坐标，string
              - result[0]：X坐标，单位[mm]
              - result[1]：Y坐标，单位[mm]
              - result[2]：Z坐标，单位[mm]
              - result[3]：Rx坐标，单位[°]
              - result[4]：Ry坐标，单位[°]
              - result[5]：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取TCP实际位置
            >>> nRet = cps.HRIF_ReadActTcpPos(0,0,result)
            >>> # 读取TCP实际位置变量
            >>> dX = float(result[0])
            >>> dY = float(result[1])
            >>> dZ = float(result[2])
            >>> dRx = float(result[3])
            >>> dRy = float(result[4])
            >>> dRz = float(result[5])
        """
        return self._client.HRIF_ReadActTcpPos(boxID, rbtID, result)
    
    def HRIF_ReadActTcpVel(self, boxID, rbtID, result):
        """
        读取实际TCP速度。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：TCP速度，string
              - result[0]：X速度，单位[mm/s]
              - result[1]：Y速度，单位[mm/s]
              - result[2]：Z速度，单位[mm/s]
              - result[3]：Rx速度，单位[°/s]
              - result[4]：Ry速度，单位[°/s]
              - result[5]：Rz速度，单位[°/s]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取TCP实际速度
            >>> nRet = cps.HRIF_ReadActTcpVel(0,0,result)
            >>> # 读取TCP实际速度变量
            >>> dX = float(result[0])
            >>> dY = float(result[1])
            >>> dZ = float(result[2])
            >>> dRx = float(result[3])
            >>> dRy = float(result[4])
            >>> dRz = float(result[5])
        """
        return self._client.HRIF_ReadActTcpVel(boxID, rbtID, result)
    
    def HRIF_ReadAxisErrorCode(self, boxID, rbtID, result):
        """
        读取轴错误码。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：当前错误码，string，>=0
            result[1]：J1轴错误码，string，>=0
            result[2]：J2轴错误码，string，>=0
            result[3]：J3轴错误码，string，>=0
            result[4]：J4轴错误码，string，>=0
            result[5]：J5轴错误码，string，>=0
            result[6]：J6轴错误码，string，>=0

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取错误码
            >>> nRet = cps.HRIF_ReadAxisErrorCode(0,0,result)
        """
        return self._client.HRIF_ReadAxisErrorCode(boxID, rbtID, result)
    
    def HRIF_ReadBoxAI(self, boxID, bit, result):
        """
        读取电箱AI。

        输入变量：
            boxID：电箱 ID，int，0~5
            bit：AI通道编号，int，0~7
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：AI数值，string，单位：0~100%

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱AI
            >>> nRet = cps.HRIF_ReadBoxAI(0, 0, result)
        """
        return self._client.HRIF_ReadBoxAI(boxID, bit, result)
    
    def HRIF_ReadBoxAO(self, boxID, bit, result):
        """
        读取电箱AO。

        输入变量：
            boxID：电箱 ID，int，0~5
            bit：AO通道编号，int，0~7
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：AO数值，string，单位：0~100%

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱AO
            >>> nRet = cps.HRIF_ReadBoxAO(0, 0, result)
        """
        return self._client.HRIF_ReadBoxAO(boxID, bit, result)
    
    def HRIF_ReadBoxCI(self, boxID, bit, result):
        """
        读取电箱CI。

        输入变量：
            boxID：电箱 ID，int，0~5
            bit：CI通道编号，int，0~7
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：CI数值，string，0/1

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱CI
            >>> nRet = cps.HRIF_ReadBoxCI(0, 0, result)
        """
        return self._client.HRIF_ReadBoxCI(boxID, bit, result)
    
    def HRIF_ReadBoxCO(self, boxID, bit, result):
        """
        读取电箱CO。

        输入变量：
            boxID：电箱 ID，int，0~5
            bit：CO通道编号，int，0~7
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：CO数值，string，0/1

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱CO
            >>> nRet = cps.HRIF_ReadBoxCO(0, 0, result)
        """
        return self._client.HRIF_ReadBoxCO(boxID, bit, result)
    
    def HRIF_ReadBoxDI(self, boxID, bit, result):
        """
        读取电箱DI。

        输入变量：
            boxID：电箱 ID，int，0~5
            bit：DI通道编号，int，0~7
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：DI数值，string，0/1

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱DI
            >>> nRet = cps.HRIF_ReadBoxDI(0, 0, result)
        """
        return self._client.HRIF_ReadBoxDI(boxID, bit, result)
    
    def HRIF_ReadBoxDO(self, boxID, bit, result):
        """
        读取电箱DO。

        输入变量：
            boxID：电箱 ID，int，0~5
            bit：DO通道编号，int，0~7
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：DO数值，string，0/1

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱DO
            >>> nRet = cps.HRIF_ReadBoxDO(0, 0, result)
        """
        return self._client.HRIF_ReadBoxDO(boxID, bit, result)
    
    def HRIF_ReadBoxInfo(self, boxID, result):
        """
        读取电箱信息。

        输入变量：
            boxID：电箱 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result：返回值列表，包含电箱相关信息

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取电箱信息
            >>> nRet = cps.HRIF_ReadBoxInfo(0, result)
        """
        return self._client.HRIF_ReadBoxInfo(boxID, result)
    
    def HRIF_ReadBrakeStatus(self, boxID, result):
        """
        读取各关节松/抱闸状态。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            result (list): 存储结果的列表，传入空列表，result[0]至result[5]分别对应关节1至6的状态
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于读取各关节松/抱闸状态。result[0]至result[5]分别对应关节1至6的状态，0表示松闸，1表示抱闸。
            
        Example:
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_ReadBrakeStatus(0, result)
            >>> print(result)  # 打印各关节状态列表
        """
        return self._client.HRIF_ReadBrakeStatus(boxID, result)
    
    def HRIF_ReadCmdJointCur(self, boxID, rbtID, result):
        """
        读取关节命令电流。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：关节命令电流，string
              - result[0]：关节1命令电流，单位[A]
              - result[1]：关节2命令电流，单位[A]
              - result[2]：关节3命令电流，单位[A]
              - result[3]：关节4命令电流，单位[A]
              - result[4]：关节5命令电流，单位[A]
              - result[5]：关节6命令电流，单位[A]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取关节命令电流
            >>> nRet = cps.HRIF_ReadCmdJointCur(0,0,result)
            >>> # 读取关节命令电流变量
            >>> dJ1 = float(result[0])
            >>> dJ2 = float(result[1])
            >>> dJ3 = float(result[2])
            >>> dJ4 = float(result[3])
            >>> dJ5 = float(result[4])
            >>> dJ6 = float(result[5])
        """
        return self._client.HRIF_ReadCmdJointCur(boxID, rbtID, result)
    
    def HRIF_ReadCmdJointPos(self, boxID, rbtID, result):
        """
        读取关节命令位置。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：关节命令位置，string
              - result[0]：关节1命令位置，单位[°]
              - result[1]：关节2命令位置，单位[°]
              - result[2]：关节3命令位置，单位[°]
              - result[3]：关节4命令位置，单位[°]
              - result[4]：关节5命令位置，单位[°]
              - result[5]：关节6命令位置，单位[°]
            result[6]-result[11]：空间坐标，string
              - result[6]：X坐标，单位[mm]
              - result[7]：Y坐标，单位[mm]
              - result[8]：Z坐标，单位[mm]
              - result[9]：Rx坐标，单位[°]
              - result[10]：Ry坐标，单位[°]
              - result[11]：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取关节命令位置
            >>> nRet = cps.HRIF_ReadCmdJointPos(0,0,result)
            >>> # 读取关节命令位置变量
            >>> dJ1 = float(result[0])
            >>> dJ2 = float(result[1])
            >>> dJ3 = float(result[2])
            >>> dJ4 = float(result[3])
            >>> dJ5 = float(result[4])
            >>> dJ6 = float(result[5])
            >>> # 读取空间命令位置变量
            >>> dX = float(result[6])
            >>> dY = float(result[7])
            >>> dZ = float(result[8])
            >>> dRX = float(result[9])
            >>> dRY = float(result[10])
            >>> dRZ = float(result[11])
        """
        return self._client.HRIF_ReadCmdJointPos(boxID, rbtID, result)
    
    def HRIF_ReadCmdJointVel(self, boxID, rbtID, result):
        """
        读取关节命令速度。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：关节命令速度，string
              - result[0]：关节1命令速度，单位[°/s]
              - result[1]：关节2命令速度，单位[°/s]
              - result[2]：关节3命令速度，单位[°/s]
              - result[3]：关节4命令速度，单位[°/s]
              - result[4]：关节5命令速度，单位[°/s]
              - result[5]：关节6命令速度，单位[°/s]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取关节命令速度
            >>> nRet = cps.HRIF_ReadCmdJointVel(0,0,result)
            >>> # 读取关节命令速度变量
            >>> dJ1 = float(result[0])
            >>> dJ2 = float(result[1])
            >>> dJ3 = float(result[2])
            >>> dJ4 = float(result[3])
            >>> dJ5 = float(result[4])
            >>> dJ6 = float(result[5])
        """
        return self._client.HRIF_ReadCmdJointVel(boxID, rbtID, result)
    
    def HRIF_ReadCmdTcpPos(self, boxID, rbtID, result):
        """
        读取命令TCP位置。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：TCP坐标，string
              - result[0]：X坐标，单位[mm]
              - result[1]：Y坐标，单位[mm]
              - result[2]：Z坐标，单位[mm]
              - result[3]：Rx坐标，单位[°]
              - result[4]：Ry坐标，单位[°]
              - result[5]：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取TCP命令位置
            >>> nRet = cps.HRIF_ReadCmdTcpPos(0,0,result)
            >>> # 读取TCP命令位置
            >>> dX = float(result[0])
            >>> dY = float(result[1])
            >>> dZ = float(result[2])
            >>> dRx = float(result[3])
            >>> dRy = float(result[4])
            >>> dRz = float(result[5])
        """
        return self._client.HRIF_ReadCmdTcpPos(boxID, rbtID, result)
    
    def HRIF_ReadCmdTcpVel(self, boxID, rbtID, result):
        """
        读取命令TCP速度。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：TCP速度，string
              - result[0]：X速度，单位[mm/s]
              - result[1]：Y速度，单位[mm/s]
              - result[2]：Z速度，单位[mm/s]
              - result[3]：Rx速度，单位[°/s]
              - result[4]：Ry速度，单位[°/s]
              - result[5]：Rz速度，单位[°/s]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取TCP命令速度
            >>> nRet = cps.HRIF_ReadCmdTcpVel(0,0,result)
            >>> # 读取TCP命令速度变量
            >>> dX = float(result[0])
            >>> dY = float(result[1])
            >>> dZ = float(result[2])
            >>> dRx = float(result[3])
            >>> dRy = float(result[4])
            >>> dRz = float(result[5])
        """
        return self._client.HRIF_ReadCmdTcpVel(boxID, rbtID, result)
    
    def HRIF_ReadCurFSM(self, boxID, rbtID, result):
        """读取当前状态机"""
        return self._client.HRIF_ReadCurFSM(boxID, rbtID, result)
    
    def HRIF_ReadCurFSMFromCPS(self, boxID, rbtID, result):
        """
        从CPS读取当前状态机。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：状态机，string，>=0
              - 状态机，可以参考状态机列表

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取当前状态机
            >>> nRet = cps.HRIF_ReadCurFSMFromCPS(0,0,result)
        """
        return self._client.HRIF_ReadCurFSMFromCPS(boxID, rbtID, result)
    
    def HRIF_ReadCurTCP(self, boxID, rbtID, result):
        """
        读取当前TCP。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：TCP坐标，string
              - result[0]：X坐标，单位[mm]
              - result[1]：Y坐标，单位[mm]
              - result[2]：Z坐标，单位[mm]
              - result[3]：Rx坐标，单位[°]
              - result[4]：Ry坐标，单位[°]
              - result[5]：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取当前TCP
            >>> nRet = cps.HRIF_ReadCurTCP(0,0,result)
        """
        return self._client.HRIF_ReadCurTCP(boxID, rbtID, result)
    
    def HRIF_ReadCurUCS(self, boxID, rbtID, result):
        """
        读取当前UCS。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]-result[5]：UCS坐标，string
              - result[0]：X坐标，单位[mm]
              - result[1]：Y坐标，单位[mm]
              - result[2]：Z坐标，单位[mm]
              - result[3]：Rx坐标，单位[°]
              - result[4]：Ry坐标，单位[°]
              - result[5]：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取当前UCS
            >>> nRet = cps.HRIF_ReadCurUCS(0,0,result)
        """
        return self._client.HRIF_ReadCurUCS(boxID, rbtID, result)
    
    def HRIF_ReadCurWaypointID(self, boxID, rbtID, result):
        """
        读取WayPoint当前运动ID号。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：路点当前运动ID，string，与WayPoint,MoveJ,MoveL,MoveC里设置的路点ID一致

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取路点ID
            >>> nRet = cps.HRIF_ReadCurWaypointID(0,0,result)
        """
        return self._client.HRIF_ReadCurWaypointID(boxID, rbtID, result)
    
    def HRIF_ReadEmergencyInfo(self, boxID, result):
        """
        读取急停信息。

        输入变量：
            boxID：电箱 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：急停回路有两路，当两路信号不相同时，则认为急停回路有错误，值为1，string，0/1
            result[1]：急停信号，发生急停时，会断48V输出到本体的供电，但是不会断220V到48V的供电，string，0/1
            result[2]：安全光幕回路有两路，当两路信号不相同时，则认为安全光幕回路有错误，值为1，string，0/1
            result[3]：安全光幕信号，发生安全光幕时，会停止机器人运动，并且不再接受运动指令，不会断本体供电，string，0/1

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取急停信息
            >>> nRet = cps.HRIF_ReadEmergencyInfo(0,result)
        """
        return self._client.HRIF_ReadEmergencyInfo(boxID, result)
    
    def HRIF_ReadEndAI(self, boxID, rbtID, bit, result):
        """读取末端AI"""
        return self._client.HRIF_ReadEndAI(boxID, rbtID, bit, result)
    
    def HRIF_ReadEndBTN(self, boxID, rbtID, result):
        """读取末端按钮"""
        return self._client.HRIF_ReadEndBTN(boxID, rbtID, result)
    
    def HRIF_ReadEndDI(self, boxID, rbtID, bit, result):
        """读取末端DI"""
        return self._client.HRIF_ReadEndDI(boxID, rbtID, bit, result)
    
    def HRIF_ReadEndDO(self, boxID, rbtID, bit, result):
        """读取末端DO"""
        return self._client.HRIF_ReadEndDO(boxID, rbtID, bit, result)
    
    def HRIF_ReadEndHoldingRegisters(self, boxID, rbtID, nSlaveID, nFunction, nRegAddr, nRegCount, result):
        """读取末端保持寄存器"""
        return self._client.HRIF_ReadEndHoldingRegisters(boxID, rbtID, nSlaveID, nFunction, nRegAddr, nRegCount, result)
    
    def HRIF_ReadFTCabData(self, boxID, rbtID, result):
        """读取力传感器Cab数据"""
        return self._client.HRIF_ReadFTCabData(boxID, rbtID, result)
    
    def HRIF_ReadFTData(self, boxID, rbtID, result):
        """读取力传感器数据"""
        return self._client.HRIF_ReadFTData(boxID, rbtID, result)
    
    def HRIF_ReadFTFreeDriveSpeedMode(self, boxID, rbtID, result):
        """读取力传感器自由驱动速度模式"""
        return self._client.HRIF_ReadFTFreeDriveSpeedMode(boxID, rbtID, result)
    
    def HRIF_ReadFTMotionFreedom(self, boxID, rbtID, result):
        """读取力传感器运动自由度"""
        return self._client.HRIF_ReadFTMotionFreedom(boxID, rbtID, result)
    
    def HRIF_ReadForceControlState(self, boxID, rbtID, result):
        """
        读取当前力控状态。
        
        描述：读取当前力控状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list，传入空列表，result = [ ]
            
        输出变量：
            result[0]：力控状态，string，0~3
              - 0：关闭状态
              - 1：开力控探寻状态
              - 2：力控探寻完成状态
              - 3：力控自由驱动状态
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取力控状态
            >>> nRet = cps.HRIF_ReadForceControlState(0,0,result)
            >>> # 读取到的力控状态
            >>> nState = int(result[0])
        """
        return self._client.HRIF_ReadForceControlState(boxID, rbtID, result)
    
    def HRIF_ReadJointMaxAcc(self, boxID, rbtID, result):
        """
        读取关节最大运动加速度。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：J1轴最大加速度，string，单位[°/s^2]
            result[1]：J2轴最大加速度，string，单位[°/s^2]
            result[2]：J3轴最大加速度，string，单位[°/s^2]
            result[3]：J4轴最大加速度，string，单位[°/s^2]
            result[4]：J5轴最大加速度，string，单位[°/s^2]
            result[5]：J6轴最大加速度，string，单位[°/s^2]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取最大关节加速度
            >>> nRet = cps.HRIF_ReadJointMaxAcc(0,0,result)
        """
        return self._client.HRIF_ReadJointMaxAcc(boxID, rbtID, result)
    
    def HRIF_ReadJointMaxJerk(self, boxID, rbtID, result):
        """
        读取关节最大运动加加速度。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：J1轴最大加加速度，string，单位[°/s^3]
            result[1]：J2轴最大加加速度，string，单位[°/s^3]
            result[2]：J3轴最大加加速度，string，单位[°/s^3]
            result[3]：J4轴最大加加速度，string，单位[°/s^3]
            result[4]：J5轴最大加加速度，string，单位[°/s^3]
            result[5]：J6轴最大加加速度，string，单位[°/s^3]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取最大关节加加速度
            >>> nRet = cps.HRIF_ReadJointMaxJerk(0,0,result)
        """
        return self._client.HRIF_ReadJointMaxJerk(boxID, rbtID, result)
    
    def HRIF_ReadJointMaxVel(self, boxID, rbtID, result):
        """
        读取关节最大运动速度。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：J1轴最大速度，string，单位[°/s]
            result[1]：J2轴最大速度，string，单位[°/s]
            result[2]：J3轴最大速度，string，单位[°/s]
            result[3]：J4轴最大速度，string，单位[°/s]
            result[4]：J5轴最大速度，string，单位[°/s]
            result[5]：J6轴最大速度，string，单位[°/s]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取最大关节速度
            >>> nRet = cps.HRIF_ReadJointMaxVel(0,0,result)
        """
        return self._client.HRIF_ReadJointMaxVel(boxID, rbtID, result)
    
    def HRIF_ReadLinearMaxSpeed(self, boxID, rbtID, result):
        """
        读取直线运动最大速度参数。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：最大直线速度，string，范围0~3000，默认[500]，单位[mm/s]
            result[1]：最大直线加速度，string，范围0~2500，默认[2500]，单位[mm/s^2]
            result[2]：最大直线加加速度，string，范围0~100000，默认[100000]，单位[mm/s^3]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取最大直线速度
            >>> nRet = cps.HRIF_ReadLinearMaxSpeed(0,0,result)
        """
        return self._client.HRIF_ReadLinearMaxSpeed(boxID, rbtID, result)
    
    def HRIF_ReadMaxPayload(self, boxID, result):
        """
        读取末端最大负载。

        输入变量：
            boxID：电箱 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：末端最大负载，string，单位：kg

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取末端最大负载
            >>> nRet = cps.HRIF_ReadMaxPayload(0, result)
        """
        return self._client.HRIF_ReadMaxPayload(boxID, result)
    
    def HRIF_ReadMovePathJState(self, boxID, rbtID, trackName, result):
        """
        读取当前的轨迹状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            sTrackName：轨迹名称，string
            
        输出变量：
            result[0]：轨迹状态，string，0~5
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 读取轨迹状态
            >>> nRet = cps.HRIF_ReadMovePathJState(0,0,sTrackName, result)
            >>> # 读取到的当前轨迹状态
            >>> nState = int(result[0])
        """
        return self._client.HRIF_ReadMovePathJState(boxID, rbtID, trackName, result)
    
    def HRIF_ReadOverride(self, boxID, rbtID, result):
        """
        读取速度比。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：当前系统的速度比，string，范围0.01~1

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取速度比
            >>> nRet = cps.HRIF_ReadOverride(0,0,result)
        """
        return self._client.HRIF_ReadOverride(boxID, rbtID, result)
    
    def HRIF_ReadPathInfo(self, boxID, rbtID, sPathName, result):
        """读取路径信息"""
        return self._client.HRIF_ReadPathInfo(boxID, rbtID, sPathName, result)
    
    def HRIF_ReadPathList(self, boxID, rbtID, result):
        """
        读取轨迹列表。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result：轨迹列表，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹列表
            >>> result = [ ]
            >>> # 读取轨迹列表
            >>> nRet = cps.HRIF_ReadPathList(0,0, result)
        """
        return self._client.HRIF_ReadPathList(boxID, rbtID, result)
    
    def HRIF_ReadPathState(self, boxID, rbtID, sPathName, result):
        """
        读取当前轨迹状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sPathName：轨迹名称，string
            result：返回值，list
            
        输出变量：
            result[0]：MovePathJ的状态，string，0/1/2/3/4/5/9/10
            result[1]：MovePathJ的错误码，string
            result[2]：MovePathL的状态，string，0/1/2/3/4/5/9/10
            result[3]：MovePathL的错误码，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sPathName = "drag_01"
            >>> # MovePathJ的状态
            >>> nStateJ = 0
            >>> # MovePathJ的错误码
            >>> nErrorCodeJ = 0
            >>> # MovePathL的状态
            >>> nStateL = 0
            >>> # MovePathL的错误码
            >>> nErrorCodeL = 0
            >>> # 更新轨迹名称
            >>> nRet = cps.HRIF_ReadPathState(0,0, sPathName,nStateJ,nErrorCodeJ,nStateL,nErrorCodeL)
        """
        return self._client.HRIF_ReadPathState(boxID, rbtID, sPathName, result)
    
    def HRIF_ReadPayload(self, boxID, result):
        """
        读取当前负载参数。

        输入变量：
            boxID：电箱 ID，int，0~5
            result：返回值列表，传入空列表，result = [ ]

        输出变量：
            result[0]：负载质量，string，范围0到允许的最大负载质量，单位[kg]
            result[1]：质心X方向偏移，string，单位[mm]
            result[2]：质心Y方向偏移，string，单位[mm]
            result[3]：质心Z方向偏移，string，单位[mm]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = []
            >>> # 读取当前负载参数
            >>> nRet = cps.HRIF_ReadPayload(0, result)
        """
        return self._client.HRIF_ReadPayload(boxID, result)
    
    def HRIF_ReadPointByName(self, boxID, rbtID, pointName, result):
        """
        根据名称读取点位。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            pointName：点位名称，string
            result：返回值，list
            
        输出变量：
            result：返回值，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 点位名称
            >>> pointName = "Point1"
            >>> # 根据名称读取点位
            >>> nRet = cps.HRIF_ReadPointByName(0,0,pointName, result)
        """
        return self._client.HRIF_ReadPointByName(boxID, rbtID, pointName, result)
    
    def HRIF_ReadPointList(self, boxID, rbtID, result):
        """
        读取点位列表。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result：返回值，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取点位列表
            >>> nRet = cps.HRIF_ReadPointList(0,0, result)
        """
        return self._client.HRIF_ReadPointList(boxID, rbtID, result)
    
    def HRIF_ReadRobotFlags(self, boxID, rbtID, result):
        """
        读取机器人标志。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result：返回值，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取机器人标志
            >>> nRet = cps.HRIF_ReadRobotFlags(0,0, result)
        """
        return self._client.HRIF_ReadRobotFlags(boxID, rbtID, result)
    
    def HRIF_ReadRobotModel(self, boxID, rbtID, result):
        """
        读取机器人类型。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            result (list): 存储结果的列表，传入空列表
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于读取机器人类型。result[0]返回机器人类型字符串。
            
        Example:
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_ReadRobotModel(0, 0, result)
            >>> print(result[0])  # 打印机器人类型
        """
        return self._client.HRIF_ReadRobotModel(boxID, rbtID, result)
    
    def HRIF_ReadRobotState(self, boxID, rbtID, result):
        """
        读取机器人状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result：返回值，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取机器人状态
            >>> nRet = cps.HRIF_ReadRobotState(0,0, result)
        """
        return self._client.HRIF_ReadRobotState(boxID, rbtID, result)
    
    def HRIF_ReadSafePlane(self, boxID, rbtID, name, result):
        """
        读取安全平面。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            name：安全平面名称，string
            result：返回值，list
            
        输出变量：
            result：返回值，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义安全平面名称
            >>> name = "safe_plane1"
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取安全平面
            >>> nRet = cps.HRIF_ReadSafePlane(0,0,name, result)
        """
        return self._client.HRIF_ReadSafePlane(boxID, rbtID, name, result)
    
    def HRIF_ReadSafePlaneList(self, boxID, rbtID, result):
        """
        读取安全平面列表。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result：返回值，list
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取安全平面列表
            >>> nRet = cps.HRIF_ReadSafePlaneList(0,0, result)
        """
        return self._client.HRIF_ReadSafePlaneList(boxID, rbtID, result)
    
    def HRIF_ReadServoEsJState(self, boxID, rbtID, result):
        """
        读取当前是否可以继续下发点位信息，循环读取间隔>20ms。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result[0]：能否继续下发，string，0/1
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> result = []
            >>> # 读取
            >>> nRet = cps.HRIF_ReadServoEsJState(0,0,result)
        """
        return self._client.HRIF_ReadServoEsJState(boxID, rbtID, result)
    
    def HRIF_ReadTCPByName(self, boxID, rbtID, TCP, result):
        """根据名称读取TCP"""
        return self._client.HRIF_ReadTCPByName(boxID, rbtID, TCP, result)
    
    def HRIF_ReadTCPList(self, boxID, rbtID, result):
        """读取TCP列表"""
        return self._client.HRIF_ReadTCPList(boxID, rbtID, result)
    
    def HRIF_ReadTcpVelocity(self, boxID, rbtID, result):
        """读取TCP速度"""
        return self._client.HRIF_ReadTcpVelocity(boxID, rbtID, result)
    
    def HRIF_ReadTrackProcess(self, boxID, rbtID, result):
        """
        读取当前的轨迹运动进度。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            result：返回值，list
            
        输出变量：
            result[0]：轨迹运行进度，string，0~1
            result[1]：点位索引，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义返回值空列表
            >>> result = [ ]
            >>> # 读取轨迹状态
            >>> nRet = cps.HRIF_ReadTrackProcess(0,0,result)
            >>> # 轨迹运行进度
            >>> dProcess = float(result[0])
            >>> # 点位索引
            >>> nIndex = int(result[1])
        """
        return self._client.HRIF_ReadTrackProcess(boxID, rbtID, result)
    
    def HRIF_ReadTriStageSwitch(self, boxID, rbtID, result):
        """
        读取三段式按钮的开关以及模式。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            result (list): 存储结果的列表，传入空列表，result[0]表示开关状态(0:关闭, 1:开启)，result[1]表示模式(0:零力示教, 1:使能)
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于读取三段式按钮的开关以及模式信息。
            
        Example:
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_ReadTriStageSwitch(0, 0, result)
            >>> print(result)  # [开关状态, 模式]
        """
        return self._client.HRIF_ReadTriStageSwitch(boxID, rbtID, result)
    
    def HRIF_ReadUCSByName(self, boxID, rbtID, UCS, result):
        """根据名称读取UCS"""
        return self._client.HRIF_ReadUCSByName(boxID, rbtID, UCS, result)
    
    def HRIF_ReadUCSList(self, boxID, rbtID, result):
        """读取UCS列表"""
        return self._client.HRIF_ReadUCSList(boxID, rbtID, result)
    
    def HRIF_ReadVersion(self, boxID, rbtID, result):
        """
        读取控制器版本号。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            result (list): 存储结果的列表，传入空列表
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于读取控制器版本信息。result列表包含以下信息：
            - result[0]: CPS版本
            - result[1]: 控制器版本
            - result[2]: 电箱版本号(0:模拟电箱, 1~4:电箱版本号)
            - result[3]: 控制板固件版本
            - result[4]: 控制板固件版本
            - result[5]: 算法版本
            - result[6]: 固件版本
            - result[7]: 软件版本
            
        Example:
            >>> cps = CPSClient()
            >>> result = []
            >>> ret = cps.HRIF_ReadVersion(0, 0, result)
            >>> print(result)  # 打印版本信息列表
        """
        return self._client.HRIF_ReadVersion(boxID, rbtID, result)
    
    def HRIF_RunFunc(self, boxID, funcName, params, result):
        """运行函数"""
        return self._client.HRIF_RunFunc(boxID, funcName, params, result)
    
    def HRIF_SetBoxAOMode(self, boxID, index, pattern):
        """设置电箱AO模式"""
        return self._client.HRIF_SetBoxAOMode(boxID, index, pattern)
    
    def HRIF_SetBoxAOVal(self, boxID, index, value, pattern):
        """设置电箱AO值"""
        return self._client.HRIF_SetBoxAOVal(boxID, index, value, pattern)
    
    def HRIF_SetBoxCO(self, boxID, bit, state):
        """设置电箱CO"""
        return self._client.HRIF_SetBoxCO(boxID, bit, state)
    
    def HRIF_SetBoxDO(self, boxID, bit, state):
        """设置电箱DO"""
        return self._client.HRIF_SetBoxDO(boxID, bit, state)
    
    def HRIF_SetCollideLevel(self, boxID, nSafeLevel):
        """
        设置安全风险等级。

        输入变量：
            boxID：电箱 ID，int，0~5
            nSafeLevel：安全风险等级，int
              - 安全风险等级(0-5)
              - 0：安全风险低
              - 5：安全风险高

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义安全风险等级
            >>> nSafeLevel=3
            >>> # 设置安全风险等级
            >>> nRet=cps.HRIF_SetCollideLevel(0,nSafeLevel)
        """
        return self._client.HRIF_SetCollideLevel(boxID, nSafeLevel)
    
    def HRIF_SetControlFreedom(self, boxID, rbtID, freedom):
        """
        设置力控探寻自由度。
        
        描述：设置力控探寻自由度。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            freedom[0-5]：各方向自由度，list，0/1
              - 各轴探寻自由度开关：
              - 0：关闭
              - 1：开启
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义力控自由度状态
            >>> freedom = [0, 0, 0, 0, 0, 0]
            >>> # 设置力控自由度状态
            >>> nRet = cps.HRIF_SetControlFreedom (0,0,freedom)
        """
        return self._client.HRIF_SetControlFreedom(boxID, rbtID, freedom)
    
    def HRIF_SetControlGoal(self, boxID, rbtID, forcegoal, distance):
        """设置控制目标"""
        return self._client.HRIF_SetControlGoal(boxID, rbtID, forcegoal, distance)
    
    def HRIF_SetDampParams(self, boxID, rbtID, damp):
        """
        设置阻尼(b)控制参数。
        
        描述：设置阻尼(b)控制参数。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            damp：阻尼控制参数，list[float]
              - 阻尼控制参数：
              - dX：X 方向
              - dY：Y 方向
              - dZ：Z 方向
              - dRx：Rx方向
              - dRy：Ry方向
              - dRz：Rz方向
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置阻尼参数
            >>> Damp = [800, 800, 800, 40, 40, 40]
            >>> # 设置阻尼参数
            >>> nRet = cps.HRIF_SetDampParams(0,0,Damp)
        """
        return self._client.HRIF_SetDampParams(boxID, rbtID, damp)
    
    def HRIF_SetDepthThresholdForDampingArea(self, boxID, rbtID, depth):
        """设置阻尼区域深度阈值"""
        return self._client.HRIF_SetDepthThresholdForDampingArea(boxID, rbtID, depth)
    
    def HRIF_SetEndDO(self, boxID, rbtID, bit, state):
        """设置末端DO"""
        return self._client.HRIF_SetEndDO(boxID, rbtID, bit, state)
    
    def HRIF_SetFTFreeDriveSpeedMode(self, boxID, rbtID, mode):
        """设置力传感器自由驱动速度模式"""
        return self._client.HRIF_SetFTFreeDriveSpeedMode(boxID, rbtID, mode)
    
    def HRIF_SetFTFreeFactor(self, boxID, dLinear, dAngular):
        """设置力传感器自由因子"""
        return self._client.HRIF_SetFTFreeFactor(boxID, dLinear, dAngular)
    
    def HRIF_SetFTMovingAvgFilterParams(self, boxID, rbtID, ForceState, TorqueState, ForceLength, TorqueLength):
        """设置力传感器移动平均滤波参数"""
        return self._client.HRIF_SetFTMovingAvgFilterParams(boxID, rbtID, ForceState, TorqueState, ForceLength, TorqueLength)
    
    def HRIF_SetFTWrenchThresholds(self, boxID, rbtID, force, torque):
        """设置力传感器 wrench 阈值"""
        return self._client.HRIF_SetFTWrenchThresholds(boxID, rbtID, force, torque)
    
    def HRIF_SetForceControlGoal(self, boxID, rbtID, force_goal):
        """
        设置力控目标力。
        
        描述：设置力控目标力。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            force_goal：力控目标力，list[float]
              - 力控目标力：
              - dX：X 方向，单位[N]
              - dY：Y 方向，单位[N]
              - dZ：Z 方向，单位[N]
              - dRx：Rx方向，单位[NM]
              - dRy：Ry方向，单位[NM]
              - dRz：Rz方向，单位[NM]
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置力控目标力
            >>> Goal = [0, 0,10, 0, 0, 0]
            >>> # 设置力控目标力Z方向10N
            >>> nRet = cps.HRIF_SetForceControlGoal(0,0,Goal)
        """
        return self._client.HRIF_SetForceControlGoal(boxID, rbtID, force_goal)
    
    def HRIF_SetForceControlState(self, boxID, rbtID, state):
        """
        设置力控状态，执行命令后机器人跳转到运动状态。
        
        描述：设置力控状态，执行命令后机器人跳转到运动状态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            state：力控状态，int，0/1
              - 0：关闭力控
              - 1：开启力控
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义设置状态
            >>> nState = 1
            >>> # 设置力控状态
            >>> nRet = cps.HRIF_SetForceControlState(0,0,nState)
        """
        return self._client.HRIF_SetForceControlState(boxID, rbtID, state)
    
    def HRIF_SetForceControlStrategy(self, boxID, rbtID, strategy):
        """
        设置力控控制策略。
        
        描述：设置力控控制策略。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            strategy：控制策略，int，0~2
              - 0：恒力模式
              - 1：柔顺模式
              - 2：柔顺越障模式
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义力控策略
            >>> nState = 1
            >>> # 设置力控策略为恒力模式
            >>> nRet = cps.HRIF_SetForceControlStrategy(0,0,nState)
        """
        return self._client.HRIF_SetForceControlStrategy(boxID, rbtID, strategy)
    
    def HRIF_SetForceDataLimit(self, boxID, rbtID, max, min):
        """设置力数据限制"""
        return self._client.HRIF_SetForceDataLimit(boxID, rbtID, max, min)
    
    def HRIF_SetForceDistanceLimit(self, boxID, rbtID, allowDistance, strengthLevel):
        """设置力距离限制"""
        return self._client.HRIF_SetForceDistanceLimit(boxID, rbtID, allowDistance, strengthLevel)
    
    def HRIF_SetForceFreeDriveMode(self, boxID, rbtID, state):
        """设置力自由驱动模式"""
        return self._client.HRIF_SetForceFreeDriveMode(boxID, rbtID, state)
    
    def HRIF_SetForceToolCoordinateMotion(self, boxID, rbtID, mode):
        """
        设置力控坐标系方向为Tool坐标方向模式。
        
        描述：设置力控坐标系方向为Tool坐标方向模式。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            mode：模式，int，0/1
              - 0：关闭
              - 1：开启
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义设置状态
            >>> mode = 1
            >>> # 设置力控坐标系状态
            >>> nRet = cps.HRIF_SetForceToolCoordinateMotion(0,0,nState)
        """
        return self._client.HRIF_SetForceToolCoordinateMotion(boxID, rbtID, mode)
    
    def HRIF_SetForceZero(self, boxID, rbtID):
        """
        力控清零，在原有数据的基础上重新标定力传感器。
        
        描述：力控清零，在原有数据的基础上重新标定力传感器。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 清零力控数据
            >>> nRet = cps.HRIF_SetForceZero(0,0)
        """
        return self._client.HRIF_SetForceZero(boxID, rbtID)
    
    def HRIF_SetFreeDriveCompensateForce(self, boxID, rbtID, force, x, y, z):
        """设置自由驱动补偿力"""
        return self._client.HRIF_SetFreeDriveCompensateForce(boxID, rbtID, force, x, y, z)
    
    def HRIF_SetFreeDriveMotionFreedom(self, boxID, df):
        """设置自由驱动运动自由度"""
        return self._client.HRIF_SetFreeDriveMotionFreedom(boxID, df)
    
    def HRIF_SetFreeDrivePositionAndOrientation(self, boxID, rbtID, position):
        """
        设置力传感器中心相对于法兰盘的安装位置和姿态。
        
        描述：设置力传感器中心相对于法兰盘的安装位置和姿态。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            position：力传感器安装位置和姿态，list[float]
              - 力传感器相对于法兰盘安装位置和姿态：
              - dX：X 坐标，单位[mm]
              - dY：Y 坐标，单位[mm]
              - dZ：Z 坐标，单位[mm]
              - dRx：Rx坐标，单位[°]
              - dRy：Ry坐标，单位[°]
              - dRz：Rz坐标，单位[°]
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义力传感器安装位置和姿态
            >>> dPCS = [0, 0, 0, 0, 0, 0]
            >>> # 设置力传感器的安装位置和姿态
            >>> nRet = cps.HRIF_SetFreeDrivePositionAndOrientation(0,0,dPCS)
        """
        return self._client.HRIF_SetFreeDrivePositionAndOrientation(boxID, rbtID, position)
    
    def HRIF_SetJointMaxAcc(self, boxID, rbtID, Joint):
        """
        设置关节最大运动加速度，加速度需比速度大。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            Joint：关节加速度，list[float]
              - 各轴加速度：
              - dJ1：J1轴最大加速度，单位[°/s^2]
              - dJ2：J2轴最大加速度，单位[°/s^2]
              - dJ3：J3轴最大加速度，单位[°/s^2]
              - dJ4：J4轴最大加速度，单位[°/s^2]
              - dJ5：J5轴最大加速度，单位[°/s^2]
              - dJ6：J6轴最大加速度，单位[°/s^2]
              - *注：关节加速度有效范围需要参考具体机型。
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义需要设置的关节最大加速度
            >>> JointAcc=[20,20,20,20,20,20]
            >>> # 设置最大关节加速度
            >>> nRet=cps.HRIF_SetJointMaxAcc(0,0,JointAcc)
        """
        return self._client.HRIF_SetJointMaxAcc(boxID, rbtID, Joint)
    
    def HRIF_SetJointMaxVel(self, boxID, rbtID, Joint):
        """
        设置关节最大运动速度。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            Joint：关节速度，list[float]
              - 各轴速度：
              - dJ1：J1轴最大速度，单位[°/s]
              - dJ2：J2轴最大速度，单位[°/s]
              - dJ3：J3轴最大速度，单位[°/s]
              - dJ4：J4轴最大速度，单位[°/s]
              - dJ5：J5轴最大速度，单位[°/s]
              - dJ6：J6轴最大速度，单位[°/s]
              - *注：关节速度有效范围需要参考具体机型。
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义需要设置关节最大速度
            >>> Joint=[180,180,180,180,180,180]
            >>> # 设置最大关节速度
            >>> nRet=cps.HRIF_SetJointMaxVel(0,0,Joint)
        """
        return self._client.HRIF_SetJointMaxVel(boxID, rbtID, Joint)
    
    def HRIF_SetLinearMaxAcc(self, boxID, rbtID, MaxAcc):
        """
        设置直线运动最大加速度，加速度需比速度大。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            MaxAcc：最大直线加速度，float，范围0~2500，默认[2500]，单位[mm/s^2]
            *注：直线加速度有效范围需要参考具体机型。
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义需要设置直线最大速度
            >>> MaxAcc=2500
            >>> # 设置最大直线速度
            >>> nRet=cps.HRIF_SetLinearMaxAcc(0,0,MaxAcc)
        """
        return self._client.HRIF_SetLinearMaxAcc(boxID, rbtID, MaxAcc)
    
    def HRIF_SetLinearMaxVel(self, boxID, rbtID, MaxVel):
        """
        设置直线运动最大速度。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            MaxVel：最大直线速度，float，范围0~3000，默认[500]，单位[mm/s]
            *注：直线速度有效范围需要参考具体机型。
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义需要设置直线最大速度
            >>> MaxVel=100
            >>> # 设置最大直线速度
            >>> nRet=cps.HRIF_SetLinearMaxVel(0,0,MaxVel)
        """
        return self._client.HRIF_SetLinearMaxVel(boxID, rbtID, MaxVel)
    
    def HRIF_SetMassParams(self, boxID, rbtID, mass):
        """
        设置惯量控制参数。
        
        描述：设置惯量控制参数。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            mass：惯量控制参数，list[float]
              - 惯量控制参数：
              - dX：X 方向
              - dY：Y 方向
              - dZ：Z 方向
              - dRx：Rx方向
              - dRy：Ry方向
              - dRz：Rz方向
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置惯量控制参数
            >>> Mass = [0, 0, 0, 0, 0, 0]
            >>> nRet = cps.HRIF_SetMassParams(0,0,Mass)
        """
        return self._client.HRIF_SetMassParams(boxID, rbtID, mass)
    
    def HRIF_SetMaxAcsRange(self, boxID, rbtID, pMax, pMin):
        """
        设置关节最大运动范围。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            pMax：关节最大范围，list[float]
              - 各轴最大范围：
              - dMaxJ1：关节1最大运动范围，单位[°]
              - dMaxJ2：关节2最大运动范围，单位[°]
              - dMaxJ3：关节3最大运动范围，单位[°]
              - dMaxJ4：关节4最大运动范围，单位[°]
              - dMaxJ5：关节5最大运动范围，单位[°]
              - dMaxJ6：关节6最大运动范围，单位[°]
            pMin：关节最小范围，list[float]
              - 各轴最小范围：
              - dMinJ1：关节1最小运动范围，单位[°]
              - dMinJ2：关节2最小运动范围，单位[°]
              - dMinJ3：关节3最小运动范围，单位[°]
              - dMinJ4：关节4最小运动范围，单位[°]
              - dMinJ5：关节5最小运动范围，单位[°]
              - dMinJ6：关节6最小运动范围，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义需要设置的关节最大运动范围
            >>> dMax=[360,135,153,360,180,360]
            >>> # 定义需要设置的关节最小运动范围
            >>> dMin=[-360,-135,-153,-360,-180,-360]
            >>> # 设置关节运动范围
            >>> nRet=cps.HRIF_SetMaxAcsRange(0,0,dMax,dMin)
        """
        return self._client.HRIF_SetMaxAcsRange(boxID, rbtID, pMax, pMin)
    
    def HRIF_SetMaxFreeDriveVel(self, boxID, rbtID, vel, angular_vel):
        """设置最大自由驱动速度"""
        return self._client.HRIF_SetMaxFreeDriveVel(boxID, rbtID, vel, angular_vel)
    
    def HRIF_SetMaxPcsRange(self, boxID, rbtID, pMax, pMin, pUcs):
        """
        设置空间最大运动范围。

        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            pMax：XYZ最大范围，list[float]，单位[mm]
            pMin：XYZ最小范围，list[float]，单位[mm]
            pUcs：基于用户坐标，list[float]
              - dX：X坐标，单位[mm]
              - dY：Y坐标，单位[mm]
              - dZ：Z坐标，单位[mm]
              - dRx：Rx坐标，单位[°]
              - dRy：Ry坐标，单位[°]
              - dRz：Rz坐标，单位[°]

        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码

        示例：
            >>> cps = CPSClient()
            >>> # 定义需要设置的空间最大运动范围
            >>> dMax=[360,360,360]
            >>> # 定义需要设置的空间最小运动范围
            >>> dMin=[-360,-360,-360]
            >>> # 定义用户坐标变量
            >>> dUcs=[0,0,0,0,0,0]
            >>> # 设置关节运动范围
            >>> nRet=cps.HRIF_SetMaxPcsRange(0,0,dMax,dMin,dUcs)
        """
        return self._client.HRIF_SetMaxPcsRange(boxID, rbtID, pMax, pMin, pUcs)
    
    def HRIF_SetMaxSearchDistance(self, boxID, rbtID, AllowDistance1, AllowDistance2, AllowDistance3, AllowDistance4, AllowDistance5, AllowDistance6):
        """设置最大搜索距离"""
        return self._client.HRIF_SetMaxSearchDistance(boxID, rbtID, AllowDistance1, AllowDistance2, AllowDistance3, AllowDistance4, AllowDistance5, AllowDistance6)
    
    def HRIF_SetMaxSearchVelocities(self, boxID, rbtID, MaxLinearVelocity, MaxAngularVelocity):
        """
        设置力控探寻的最大速度。
        
        描述：设置力控探寻的最大速度。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            MaxLinearVelocity：直线速度，float，>0
            MaxAngularVelocity：姿态角速度，float，>0
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置力控探寻直线速度
            >>> dMaxLinearVelocity = 100
            >>> # 设置力控探寻姿态角速度
            >>> dMaxAngularVelocity = 50
            >>> # 设置力控探寻速度
            >>> nRet = cps.HRIF_SetMaxSearchVelocities(0,0,dMaxLinearVelocity, dMaxAngularVelocity)
        """
        return self._client.HRIF_SetMaxSearchVelocities(boxID, rbtID, MaxLinearVelocity, MaxAngularVelocity)
    
    def HRIF_SetMoveParamsAO(self, boxID, nState, nIndex, dInitAO, dWeldingAO):
        """设置运动参数AO"""
        return self._client.HRIF_SetMoveParamsAO(boxID, nState, nIndex, dInitAO, dWeldingAO)
    
    def HRIF_SetMovePathOverride(self, boxID, rbtID, MovePathOverride):
        """
        设置运动路径倍率
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            MovePathOverride (float): 运动路径倍率，范围0.01~1
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于设置运动路径的倍率，影响整个路径的执行速度。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_SetMovePathOverride(0, 0, 0.5)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_SetMovePathOverride(boxID, rbtID, MovePathOverride)
    
    def HRIF_SetMoveTraceInitParams(self, boxID, rbtID, dK, dB, maxLimit, minLimit):
        """设置运动轨迹初始参数"""
        return self._client.HRIF_SetMoveTraceInitParams(boxID, rbtID, dK, dB, maxLimit, minLimit)
    
    def HRIF_SetMoveTraceParams(self, boxID, rbtID, state, distance, dAwayVelocity, dGobackVelocity):
        """设置运动轨迹参数"""
        return self._client.HRIF_SetMoveTraceParams(boxID, rbtID, state, distance, dAwayVelocity, dGobackVelocity)
    
    def HRIF_SetMoveTraceUcs(self, boxID, rbtID, direction):
        """设置运动轨迹UCS"""
        return self._client.HRIF_SetMoveTraceUcs(boxID, rbtID, direction)
    
    def HRIF_SetOutputLog(self, output):
        """设置输出日志"""
        return self._client.HRIF_SetOutputLog(output)
    
    def HRIF_SetOverride(self, boxID, rbtID, vel):
        """
        设置速度比。
        
        描述：设置速度比。
        
        输入变量
        ----------
        boxID : int
            电箱ID号，默认值=0，范围0~5
        rbtID : int
            机器人ID号，默认值=0，范围0~5
        vel : float
            需要设置的速度比(0.01~1)
            
        返回值
        -------
        nRet : int
            nRet=0:返回函数调用成功
            nRet>0:返回调用失败的错误码
            
        示例
        ------
        >>> # 需要设置的速度比
        >>> vel=0.5
        >>> # 设置当前速度比
        >>> nRet=cps.HRIF_SetOverride(0,0,vel)
        """
        return self._client.HRIF_SetOverride(boxID, rbtID, vel)
    
    def HRIF_SetPIDControlParams(self, boxID, rbtID, fP, fI, fD, tP, tI, tD):
        """
        设置力控探寻 PID 参数。
        
        描述：设置力控探寻 PID 参数。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            fP：PID 参数 fP，float
            fI：PID 参数 fI，float
            fD：PID 参数 fD，float
            tP：PID 参数 tP，float
            tI：PID 参数 tI，float
            tD：PID 参数 tD，float
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置PID参数
            >>> dFp = 1.0 dFi= 0.1 dFd = 0
            >>> dTp = 1.0 dTi = 0.1 dTd = 0
            >>> # 设置PID参数
            >>> nRet = cps.HRIF_SetPIDControlParams(0,0,dFp, dFi, dFd, dTp, dTi, dTd)
        """
        return self._client.HRIF_SetPIDControlParams(boxID, rbtID, fP, fI, fD, tP, tI, tD)
    
    def HRIF_SetPayload(self, boxID, rbtID, Mass, Center_X, Center_Y, Center_Z):
        """
        设置当前负载参数。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            Mass：负载质量，float，范围0到允许的最大负载质量，单位[kg]
            Center_X：质心X方向偏移，单位[mm]
            Center_Y：质心Y方向偏移，单位[mm]
            Center_Z：质心Z方向偏移，单位[mm]
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 需要设置负载质量
            >>> Mass=0.5
            >>> # 需要设置负载质心X方向偏移量
            >>> Center_X=0.5
            >>> # 需要设置负载质心Y方向偏移量
            >>> Center_Y=0.5
            >>> # 需要设置负载质心Z方向偏移量
            >>> Center_Z=0.5
            >>> # 设置当前负载
            >>> nRet=cps.HRIF_SetPayload(0,0,Mass,Center_X,Center_Y,Center_Z)
        """
        return self._client.HRIF_SetPayload(boxID, rbtID, Mass, Center_X, Center_Y, Center_Z)
    
    def HRIF_SetPoseTrackingMaxMotionLimit(self, boxID, rbtID, dMaxLineVel, dMaxOriVel):
        """设置姿态跟踪最大运动限制"""
        return self._client.HRIF_SetPoseTrackingMaxMotionLimit(boxID, rbtID, dMaxLineVel, dMaxOriVel)
    
    def HRIF_SetPoseTrackingPIDParams(self, boxID, rbtID, dPosPID1, dPosPID2, dPosPID3, dOriPID1, dOriPID2, dOriPID3):
        """设置姿态跟踪PID参数"""
        return self._client.HRIF_SetPoseTrackingPIDParams(boxID, rbtID, dPosPID1, dPosPID2, dPosPID3, dOriPID1, dOriPID2, dOriPID3)
    
    def HRIF_SetPoseTrackingState(self, boxID, rbtID, nState):
        """设置姿态跟踪状态"""
        return self._client.HRIF_SetPoseTrackingState(boxID, rbtID, nState)
    
    def HRIF_SetPoseTrackingStopTimeOut(self, boxID, rbtID, dTime):
        """设置姿态跟踪停止超时"""
        return self._client.HRIF_SetPoseTrackingStopTimeOut(boxID, rbtID, dTime)
    
    def HRIF_SetPoseTrackingTargetPos(self, boxID, rbtID, dX, dY, dZ, dRx, dRy, dRz):
        """设置姿态跟踪目标位置"""
        return self._client.HRIF_SetPoseTrackingTargetPos(boxID, rbtID, dX, dY, dZ, dRx, dRy, dRz)
    
    def HRIF_SetScriptForceControlState(self, boxID, rbtID, state, FTMode, UCS, TCP, vel, forces, freedom, PID, Mass, Damp, Stiff):
        """设置脚本力控制状态"""
        return self._client.HRIF_SetScriptForceControlState(boxID, rbtID, state, FTMode, UCS, TCP, vel, forces, freedom, PID, Mass, Damp, Stiff)
    
    def HRIF_SetSimulation(self, boxID, state):
        """
        设置机器人的模拟状态。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            state (int): 模拟状态，0：真实机器人，1：模拟机器人
              注：该指令需要在机器人断电模式下才能正常调用，否则返回20018错误。
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于设置机器人的模拟状态。0表示真实机器人，1表示模拟机器人。
            注意：该指令需要在机器人断电模式下才能正常调用，否则返回20018错误。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_SetSimulation(0, 1)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_SetSimulation(boxID, state)
    
    def HRIF_SetSteadyContactDeviationRange(self, boxID, rbtID, x, y, z, rx, ry, rz, nx, ny, nz, nrx, nry, nrz):
        """设置稳定接触偏差范围"""
        return self._client.HRIF_SetSteadyContactDeviationRange(boxID, rbtID, x, y, z, rx, ry, rz, nx, ny, nz, nrx, nry, nrz)
    
    def HRIF_SetStiffParams(self, boxID, rbtID, stiff):
        """
        设置刚度(k)控制参数。
        
        描述：设置刚度(k)控制参数。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            stiff：刚度控制参数，list[float]
              - 刚度控制参数：
              - dX：X 方向
              - dY：Y 方向
              - dZ：Z 方向
              - dRx：Rx方向
              - dRy：Ry方向
              - dRz：Rz方向
              
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 设置刚度参数
            >>> Stiff = [1000, 1000, 1000, 100, 100, 100]
            >>> # 设置刚度参数
            >>> nRet = cps.HRIF_SetStiffParams(0,0,Stiff)
        """
        return self._client.HRIF_SetStiffParams(boxID, rbtID, stiff)
    
    def HRIF_SetTCP(self, boxID, rbtID, TCP):
        """设置TCP"""
        return self._client.HRIF_SetTCP(boxID, rbtID, TCP)
    
    def HRIF_SetTCPByName(self, boxID, rbtID, TcpName):
        """根据名称设置TCP"""
        return self._client.HRIF_SetTCPByName(boxID, rbtID, TcpName)
    
    def HRIF_SetTangentForceBounds(self, boxID, rbtID, Max, Min, Vel):
        """设置切向力边界"""
        return self._client.HRIF_SetTangentForceBounds(boxID, rbtID, Max, Min, Vel)
    
    def HRIF_SetToolMotion(self, boxID, rbtID, state):
        """
        开启或关闭Tool坐标系运动模式。
        
        输入变量
        ----------
        boxID : int
            电箱ID号，默认值=0，范围0~5
        rbtID : int
            机器人ID号，默认值=0，范围0~5
        state : int
            运动模式状态，0：开启，1：关闭
            
        返回值
        -------
        nRet : int
            nRet=0:返回函数调用成功
            nRet>0:返回调用失败的错误码
            
        示例
        ------
        >>> # 需要设置的Tool运动状态
        >>> state=1
        >>> # 设置Tool运动状态
        >>> nRet=cps.HRIF_SetToolMotion(0,0,state)
        """
        return self._client.HRIF_SetToolMotion(boxID, rbtID, state)
    
    def HRIF_SetTrackingState(self, boxID, rbtID, state):
        """设置跟踪状态"""
        return self._client.HRIF_SetTrackingState(boxID, rbtID, state)
    
    def HRIF_SetTriStageSwitch(self, boxID, rbtID, enable, mode):
        """
        设置三段式按钮的开关以及模式。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            rbtID (int): 机器人ID号，范围0~5，默认值=0
            enable (int): 三段式按钮开关状态，0：关闭，1：开启
            mode (int): 三段式按钮模式，0：零力示教，1：使能
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于设置三段式按钮的开关以及模式信息。
            
        Example:
            >>> cps = CPSClient()
            >>> # 开启三段式按钮并设置为零力示教模式
            >>> ret = cps.HRIF_SetTriStageSwitch(0, 0, 1, 0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_SetTriStageSwitch(boxID, rbtID, enable, mode)
    
    def HRIF_SetUCS(self, boxID, rbtID, UCS):
        """设置UCS"""
        return self._client.HRIF_SetUCS(boxID, rbtID, UCS)
    
    def HRIF_SetUCSByName(self, boxID, rbtID, UcsName):
        """根据名称设置UCS"""
        return self._client.HRIF_SetUCSByName(boxID, rbtID, UcsName)
    
    def HRIF_SetUpdateTrackingPose(self, boxID, rbtID, dX, dY, dZ, dRx, dRy, dRz):
        """设置更新跟踪姿态"""
        return self._client.HRIF_SetUpdateTrackingPose(boxID, rbtID, dX, dY, dZ, dRx, dRy, dRz)
    
    def HRIF_ShutdownRobot(self, boxID):
        """
        控制器断电（断开机器人供电，系统关机）。
        
        Args:
            boxID (int): 电箱ID号，范围0~5，默认值=0
            
        Returns:
            int: 函数调用结果，0表示成功，非0表示失败
            
        Note:
            该函数用于控制器断电，断开机器人供电并关机。
            
        Example:
            >>> cps = CPSClient()
            >>> ret = cps.HRIF_ShutdownRobot(0)
            >>> print(ret)  # 0表示成功
        """
        return self._client.HRIF_ShutdownRobot(boxID)
    
    def HRIF_SpeedJ(self, boxID, rbtID, cmdVel, acc, runtime):
        """关节速度运动"""
        return self._client.HRIF_SpeedJ(boxID, rbtID, cmdVel, acc, runtime)
    
    def HRIF_SpeedL(self, boxID, rbtID, cmdVel, linearAcc, acc, runtime):
        """直线速度运动"""
        return self._client.HRIF_SpeedL(boxID, rbtID, cmdVel, linearAcc, acc, runtime)
    
    def HRIF_StartPushMovePathJ(self, boxID, rbtID, trackName, speedRatio, radius):
        """
        初始化关节连续轨迹运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹名称，string
            dSpeedRatio：轨迹运动速度比，float，0~1
            dRadius：过渡半径，float，>=0
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 速度比
            >>> dSpeedRatio = 0.5
            >>> # 过渡半径
            >>> dRadius = 2
            >>> # 初始化关节连续轨迹运动
            >>> nRet = cps.HRIF_StartPushMovePathJ(0,0,sTrackName, dSpeedRatio, dRadius)
        """
        return self._client.HRIF_StartPushMovePathJ(boxID, rbtID, trackName, speedRatio, radius)
    
    def HRIF_StartScript(self, boxID):
        """开始脚本"""
        return self._client.HRIF_StartScript(boxID)
    
    def HRIF_StartServo(self, boxID, rbtID, servoTime, lookaheadTime):
        """开始伺服"""
        return self._client.HRIF_StartServo(boxID, rbtID, servoTime, lookaheadTime)
    
    def HRIF_StartServoEsJ(self, boxID, rbtID, dServoTime, dLookaheadTime):
        """开始伺服EsJ"""
        return self._client.HRIF_StartServoEsJ(boxID, rbtID, dServoTime, dLookaheadTime)
    
    def HRIF_StopScript(self, boxID):
        """停止脚本"""
        return self._client.HRIF_StopScript(boxID)
    
    def HRIF_UcsTcp2Base(self, boxID, UcsTcp, TCP, UCS, result):
        """UCS TCP到基坐标变换"""
        return self._client.HRIF_UcsTcp2Base(boxID, UcsTcp, TCP, UCS, result)
    
    def HRIF_UpdateMovePathJName(self, boxID, rbtID, trackName, newName):
        """
        更新指定轨迹的名称。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            sTrackName：轨迹原名称，string
            sTrackNewName：更新的轨迹名称，string
            
        返回值：nRet，int，>0 的整型值
            
        示例：
            >>> cps = CPSClient()
            >>> # 轨迹名称
            >>> sTrackName = "Path1"
            >>> # 更新的轨迹名称
            >>> sTrackNewName = "Path2"
            >>> # 重命名轨迹名称
            >>> nRet = cps.HRIF_UpdateMovePathJName(0,0,sTrackName, sTrackNewName)
        """
        return self._client.HRIF_UpdateMovePathJName(boxID, rbtID, trackName, newName)
    
    def HRIF_UpdatePathName(self, boxID, rbtID, sPathName, sPathNewName):
        """更新路径名称"""
        return self._client.HRIF_UpdatePathName(boxID, rbtID, sPathName, sPathNewName)
    
    def HRIF_UpdateSafePlane(self, boxID, rbtID, name, UcsName, mode, display, switch):
        """更新安全平面"""
        return self._client.HRIF_UpdateSafePlane(boxID, rbtID, name, UcsName, mode, display, switch)
    
    def HRIF_WayPoint(self, boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek, bit, state, cmdID):
        """
        路点运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nMoveType：运动类型，int，0/1
            dX-dRz：空间目标位置，float
            dJ1-dJ6：关节目标位置，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            nIsUseJoint：是否使用关节坐标，int，0/1
            nIsSeek：是否检测DI 停止，int，0/1
            nIOBit：检测的 DI 索引，int，0~7
            nIOState：检测的 DI 状态，int，0/1
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义运动类型
            >>> nMoveType = 0
            >>> # 定义空间目标位置
            >>> Point = [0, 0, 0, 0, 0, 0]
            >>> # 定义关节目标位置
            >>> rawACS = [0, 0, 0, 0, 0, 0]
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义是否使用关节角度
            >>> nIsUseJoint= 1
            >>> # 定义是否使用检测DI停止
            >>> nIsSeek = 0
            >>> # 定义检测的DI索引
            >>> nIOBit = 0
            >>> # 定义检测的DI状态
            >>> nIOState = 0
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet = cps.HRIF_WayPoint(0,0,nMoveType , Point, rawACS, sTcpName , sUcsName, dVelocity, dAcc,
            >>> dRadius,
            >>> nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
        """
        return self._client.HRIF_WayPoint(boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, Acc, radius, isJoint, isSeek, bit, state, cmdID)
    
    def HRIF_WayPoint2(self, boxID, rbtID, type, EndPos, AuxPos, AcsPos, Tcp, Ucs, Vel, Acc, Radius, isJoint, isSeek, bit, state, cmdID):
        """
        路点运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nMoveType：运动类型，int，0/1/2
            dEndPos_X-dEndPos_Rz：空间目标位置，float
            dAuxPos_X-dAuxPos_Rz：空间目标位置，float
            dJ1-dJ6：关节目标位置，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            nIsUseJoint：是否使用关节坐标，int，0/1
            nIsSeek：是否检测DI 停止，int，0/1
            nIOBit：检测的 DI 索引，int，0~7
            nIOState：检测的 DI 状态，int，0/1
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义运动类型
            >>> nMoveType = 0
            >>> # 定义空间目标位置
            >>> EndPos = [420, 0, 445, 180, 0, 180]
            >>> # 定义空间目标位置
            >>> AuxPos = [420, 0, 445, 180, 0, 180]
            >>> # 定义关节目标位置
            >>> AcsPose = [0, 0, 90, 0, 90, 0]
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义是否使用关节角度
            >>> nIsUseJoint= 1
            >>> # 定义是否使用检测DI停止
            >>> nIsSeek = 0
            >>> # 定义检测的DI索引
            >>> nIOBit = 0
            >>> # 定义检测的DI状态
            >>> nIOState = 0
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet = cps.HRIF_WayPoint2(0,0,nMoveType ,EndPos, AuxPos, AcsPose, sTcpName , sUcsName, dVelocity,
            >>> dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
        """
        return self._client.HRIF_WayPoint2(boxID, rbtID, type, EndPos, AuxPos, AcsPos, Tcp, Ucs, Vel, Acc, Radius, isJoint, isSeek, bit, state, cmdID)
    
    def HRIF_WayPointEx(self, boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, acc, radius, isJoint, isSeek, bit, state, cmdID):
        """
        路点运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nMoveType：运动类型，int，0/1
            dX-dRz：空间目标位置，float
            dJ1-dJ6：关节目标位置，float
            dTcp_X-dTcp_Rz：工具坐标值，float
            dUcs_X-dUcs_Rz：用户坐标值，float
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            nIsUseJoint：是否使用关节坐标，int，0/1
            nIsSeek：是否检测DI 停止，int，0/1
            nIOBit：检测的 DI 索引，int，0-7
            nIOState：检测的 DI 状态，int，0/1
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义运动类型
            >>> nMoveType = 0
            >>> # 定义空间目标位置
            >>> Point= [500, 500, 500, 500, 500, 500]
            >>> # 定义关节目标位置
            >>> RawACSpoints = [0, 0, 0, 0, 0, 0]
            >>> # 定义工具坐标变量
            >>> Tcp = [0, 0, 0, 0, 0, 0]
            >>> # 定义用户坐标变量
            >>> Ucs = [0, 0, 0, 0, 0, 0]
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义是否使用关节角度
            >>> nIsUseJoint = 1
            >>> # 定义是否使用检测DI停止
            >>> nIsSeek = 0
            >>> # 定义检测的DI索引
            >>> nIOBit = 0
            >>> # 定义检测的DI状态
            >>> nIOState = 0
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 执行路点运动
            >>> nRet = cps.HRIF_WayPointEx(0,0,nMoveType , Point, RawACSpoints, Tcp, Ucs, dVelocity, dAcc, dRadius,
            >>> nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
        """
        return self._client.HRIF_WayPointEx(boxID, rbtID, type, points, RawACSpoints, tcp, ucs, speed, acc, radius, isJoint, isSeek, bit, state, cmdID)
    
    def HRIF_WayPointRel(self, boxID, rbtID, nType, nPointList, Pos, rawACT, nrelMoveType, nAxisMask, dTarget, sTcpName, sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strcmdID):
        """
        路点相对运动。
        
        输入变量：
            boxID：电箱 ID，int，0~5
            rbtID：机器人 ID，int，0~5
            nType：运动类型，int，>0
            nPointList：是否使用列表点位，int，>1
            Pos：空间位置，list
            rawACT：关节位置，list
            nrelMoveType：相对运动类型，int
            nAxisMask：各轴是否运动，list
            nTarget：运动距离，float
            sTcpName：工具坐标名称，string
            sUcsName：用户坐标名称，string
            dVelocity：速度，float
            dAcc：加速度，float
            dRadius：过渡半径，float
            nIsUseJoint：是否使用关节角度，int
            nIsSeek：是否检测DI 停止，int，0/1
            nIOBit：检测的 DI 索引，int，0~7
            nIOState：检测的 DI 状态，int，0/1
            strCmdID：命令 ID，string
            
        返回值：nRet，int，>0 的整型值
            nRet=0：返回函数调用成功
            nRet>0：返回调用失败的错误码
            
        示例：
            >>> cps = CPSClient()
            >>> # 定义运动类型
            >>> nType = 0;
            >>> # 定义是否使用点位列表的点位
            >>> nPointList= 0;
            >>> # 定义空间目标位置
            >>> Pos = [0, 0, 0, 0, 0, 0]
            >>> # 定义关节目标位置
            >>> rawACT = [0, 0, 0, 0, 0, 0]
            >>> # 定义相对运动类型
            >>> nrelMoveType= 1;
            >>> # 定义各轴各方向是否运动
            >>> nAxisMask = [1, 1, 0, 0, 0, 0]
            >>> # 定义运动距离
            >>> nTarget = [10, -10, 0, 0, 0, 0]
            >>> # 定义工具坐标变量
            >>> sTcpName = "TCP"
            >>> # 定义用户坐标变量
            >>> sUcsName = "Base"
            >>> # 定义运动速度
            >>> dVelocity = 50
            >>> # 定义运动加速度
            >>> dAcc = 50
            >>> # 定义过渡半径
            >>> dRadius = 50
            >>> # 定义是否使用关节角度
            >>> nIsUseJoint = 0
            >>> # 定义是否使用检测DI停止
            >>> nIsSeek = 0
            >>> # 定义检测的DI索引
            >>> nIOBit = 0
            >>> # 定义检测的DI状态
            >>> nIOState = 0
            >>> # 定义路点ID
            >>> strCmdID = "0"
            >>> # 路点相对运动
            >>> nRet = cps.HRIF_WayPointRel(0,0,nType, nPointList, Pos, rawACT, nrelMoveType, nAxisMask, nTarget,
            >>> sTcpName, sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
        """
        return self._client.HRIF_WayPointRel(boxID, rbtID, nType, nPointList, Pos, rawACT, nrelMoveType, nAxisMask, dTarget, sTcpName, sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strcmdID)
    
    def HRIF_WriteEndHoldingRegisters(self, boxID, rbtID, nSlaveID, nFunction, nRegAddr, nRegCount, data):
        """写入末端保持寄存器"""
        return self._client.HRIF_WriteEndHoldingRegisters(boxID, rbtID, nSlaveID, nFunction, nRegAddr, nRegCount, data)
    
    def HRIF_cdsSetIO(self, boxID, rbtID, nEndDOMask, nEndDOVal, nBoxDOMask, nBoxDOVal, nBoxCOMask, nBoxCOVal, nBoxAOCH0_Mask, nBoxAOCH0_Mode, nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val):
        """设置IO"""
        return self._client.HRIF_cdsSetIO(boxID, rbtID, nEndDOMask, nEndDOVal, nBoxDOMask, nBoxDOVal, nBoxCOMask, nBoxCOVal, nBoxAOCH0_Mask, nBoxAOCH0_Mode, nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val)
    
    def waitBlendingDone(self, boxID, rbtID):
        """等待插补完成"""
        return self._client.waitBlendingDone(boxID, rbtID)
    
    def waitFSM(self, targetFSM, wait_timeout):
        """等待状态机"""
        return self._client.waitFSM(targetFSM, wait_timeout)
    
    def waitMoveDone(self, boxID, rbtID):
        """等待运动完成"""
        return self._client.waitMoveDone(boxID, rbtID)
    
    def waitMovementDone(self, boxID, rbtID, result):
        """等待运动完成"""
        return self._client.waitMovementDone(boxID, rbtID, result)


class RbtClient:
    """机器人客户端类"""
    
    # 类属性
    clientIP = _CPS.RbtClient.clientIP
    clientPort = _CPS.RbtClient.clientPort
    lock = _CPS.RbtClient.lock
    output_log = _CPS.RbtClient.output_log
    socket = _CPS.RbtClient.socket
    xmlrpcAddr = _CPS.RbtClient.xmlrpcAddr
    
    def __init__(self):
        """初始化机器人客户端"""
        self._client = _CPS.RbtClient()
    
    def Connect2CPS(self, hostName, nPort):
        """连接到CPS"""
        return self._client.Connect2CPS(hostName, nPort)
    
    def DisconnectFromCPS(self):
        """从CPS断开连接"""
        return self._client.DisconnectFromCPS()
    
    def sendAndRecv(self, cmd, result):
        """发送和接收数据"""
        return self._client.sendAndRecv(cmd, result)
    
    def sendHRLog(self, nLevel, msg):
        """发送HR日志"""
        return self._client.sendHRLog(nLevel, msg)
    
    def sendScriptError(self, msg):
        """发送脚本错误"""
        return self._client.sendScriptError(msg)
    
    def sendScriptFinish(self, errorCode):
        """发送脚本完成"""
        return self._client.sendScriptFinish(errorCode)
    
    def sendVarValue(self, boxID, rbtID, VarName, Value):
        """发送变量值"""
        return self._client.sendVarValue(boxID, rbtID, VarName, Value)
    
    def setOutputLog(self, output):
        """设置输出日志"""
        return self._client.setOutputLog(output)


# 重新导出枚举
RbtFSM = _CPS.RbtFSM

# 重新导出全局函数
def ReadDint(*args, **kwargs):
    """读取Dint"""
    return _CPS.ReadDint(*args, **kwargs)

def ReadFloat(*args, **kwargs):
    """读取Float"""
    return _CPS.ReadFloat(*args, **kwargs)

def WriteDint(*args, **kwargs):
    """写入Dint"""
    return _CPS.WriteDint(*args, **kwargs)

def WriteFloat(*args, **kwargs):
    """写入Float"""
    return _CPS.WriteFloat(*args, **kwargs)

# 重新导出全局变量
Double = _CPS.Double
__test__ = _CPS.__test__
dic_ErrorCode = _CPS.dic_ErrorCode
lock = _CPS.lock

# 为了确保模块可以正常工作，我们也可以添加__all__来明确导出的内容
__all__ = [
    'CPSClient',
    'RbtClient', 
    'RbtFSM',
    'ReadDint',
    'ReadFloat',
    'WriteDint',
    'WriteFloat',
    'Double',
    '__test__',
    'dic_ErrorCode',
    'lock'
]
