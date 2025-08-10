"""
机器人状态监控模块
"""

import time
import threading
from typing import Optional, Callable
from wrapper import CPSClient
from .exceptions import RobotStateError, RobotTimeoutError

class RobotStatusMonitor:
    """机器人状态监控器"""
    
    # 状态机状态定义
    STATE_UNINITIALIZE = 0
    STATE_INITIALIZE = 1
    STATE_ELECTRIC_BOX_DISCONNECT = 2
    STATE_ELECTRIC_BOX_CONNECTING = 3
    STATE_EMERGENCY_STOP_HANDLING = 4
    STATE_EMERGENCY_STOP = 5
    STATE_BLACKOUTING_48V = 6
    STATE_BLACKOUT_48V = 7
    STATE_ELECTRIFYING_48V = 8
    STATE_SAFETY_GUARD_ERROR_HANDLING = 9
    STATE_SAFETY_GUARD_ERROR = 10
    STATE_SAFETY_GUARD_HANDLING = 11
    STATE_SAFETY_GUARD = 12
    STATE_CONTROLLER_DISCONNECTING = 13
    STATE_CONTROLLER_DISCONNECT = 14
    STATE_CONTROLLER_CONNECTING = 15
    STATE_CONTROLLER_VERSION_ERROR = 16
    STATE_ETHERCAT_ERROR = 17
    STATE_CONTROLLER_CHECKING = 18
    STATE_RESETING = 19
    STATE_ROBOT_OUTOF_SAFE_SPACE = 20
    STATE_ROBOT_COLLISION_STOP = 21
    STATE_ERROR = 22
    STATE_ROBOT_ENABLING = 23
    STATE_DISABLE = 24
    STATE_MOVING = 25
    STATE_LONG_JOG_MOVING = 26
    STATE_ROBOT_STOPPING = 27
    STATE_ROBOT_DISABLING = 28
    STATE_ROBOT_OPENING_FREE_DRIVER = 29
    STATE_ROBOT_CLOSING_FREE_DRIVER = 30
    STATE_FREE_DRIVER = 31
    STATE_ROBOT_HOLDING = 32
    STATE_STANDBY = 33  # 就绪状态
    STATE_SCRIPT_RUNNING = 34
    STATE_SCRIPT_HOLD_HANDLING = 35
    STATE_SCRIPT_HOLDING = 36
    STATE_SCRIPT_STOPPING = 37
    STATE_SCRIPT_STOPPED = 38
    STATE_HRAPP_DISCONNECTED = 39
    STATE_HRAPP_ERROR = 40
    STATE_ROBOT_LOAD_IDENTIFY = 41
    STATE_BRAKING = 42
    
    def __init__(self, lib_wrapper: CPSClient, box_id=0, robot_id=0):
        self.lib_wrapper = lib_wrapper
        self.box_id = box_id
        self.robot_id = robot_id
        self.current_state = None
        self.monitoring = False
        self.monitor_thread = None
        self.state_callbacks = []
    
    def get_current_state(self) -> int:
        """获取当前状态"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadCurFSMFromCPS(self.box_id, self.robot_id, result)
            if ret == 0 and result:
                self.current_state = int(result[0])
                return self.current_state
            else:
                raise RobotStateError(ret, f"获取状态失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"获取状态失败: {str(e)}")
    
    def wait_for_state(self, target_state: int, timeout: float = 30.0, 
                      check_interval: float = 0.5) -> bool:
        """等待机器人达到指定状态"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current = self.get_current_state()
            if current == target_state:
                return True
            time.sleep(check_interval)
        
        return False
    
    def wait_for_standby(self, timeout: float = 30.0) -> bool:
        """等待机器人进入就绪状态(33)"""
        return self.wait_for_state(self.STATE_STANDBY, timeout)
    
    def is_ready(self) -> bool:
        """检查机器人是否就绪"""
        try:
            state = self.get_current_state()
            return state == self.STATE_STANDBY
        except:
            return False
    
    def is_enabled(self) -> bool:
        """检查机器人是否已使能"""
        try:
            state = self.get_current_state()
            return state in [self.STATE_STANDBY, self.STATE_MOVING, 
                           self.STATE_LONG_JOG_MOVING, self.STATE_FREE_DRIVER]
        except:
            return False
    
    def is_moving(self) -> bool:
        """检查机器人是否正在运动"""
        try:
            state = self.get_current_state()
            return state in [self.STATE_MOVING, self.STATE_LONG_JOG_MOVING]
        except:
            return False
    
    def get_state_description(self, state: int) -> str:
        """获取状态描述"""
        state_map = {
            self.STATE_UNINITIALIZE: "未初始化",
            self.STATE_INITIALIZE: "初始化",
            self.STATE_ELECTRIC_BOX_DISCONNECT: "工控板与电箱的通信断开",
            self.STATE_ELECTRIC_BOX_CONNECTING: "连接电箱控制板",
            self.STATE_EMERGENCY_STOP_HANDLING: "急停处理中",
            self.STATE_EMERGENCY_STOP: "急停",
            self.STATE_BLACKOUTING_48V: "正在切断本体供电",
            self.STATE_BLACKOUT_48V: "本体供电已切断",
            self.STATE_ELECTRIFYING_48V: "正在准备给本体供电",
            self.STATE_SAFETY_GUARD_ERROR_HANDLING: "安全光幕错误处理中",
            self.STATE_SAFETY_GUARD_ERROR: "安全光幕错误",
            self.STATE_SAFETY_GUARD_HANDLING: "安全光幕处理中",
            self.STATE_SAFETY_GUARD: "安全光幕",
            self.STATE_CONTROLLER_DISCONNECTING: "正在反初始化控制器",
            self.STATE_CONTROLLER_DISCONNECT: "控制器已处于未初始化状态",
            self.STATE_CONTROLLER_CONNECTING: "正在初始化控制器",
            self.STATE_CONTROLLER_VERSION_ERROR: "控制器版本过低错误",
            self.STATE_ETHERCAT_ERROR: "EtherCAT错误",
            self.STATE_CONTROLLER_CHECKING: "控制器初始化后检查",
            self.STATE_RESETING: "正在复位机器人",
            self.STATE_ROBOT_OUTOF_SAFE_SPACE: "机器人超出安全空间",
            self.STATE_ROBOT_COLLISION_STOP: "机器人安全碰撞停车",
            self.STATE_ERROR: "机器人错误",
            self.STATE_ROBOT_ENABLING: "机器人使能中",
            self.STATE_DISABLE: "机器人去使能",
            self.STATE_MOVING: "机器人运动中",
            self.STATE_LONG_JOG_MOVING: "机器人长点动运动中",
            self.STATE_ROBOT_STOPPING: "机器人停止运动中",
            self.STATE_ROBOT_DISABLING: "机器人去使能中",
            self.STATE_ROBOT_OPENING_FREE_DRIVER: "机器人正在开启零力示教",
            self.STATE_ROBOT_CLOSING_FREE_DRIVER: "机器人正在关闭零力示教",
            self.STATE_FREE_DRIVER: "机器人处于零力示教",
            self.STATE_ROBOT_HOLDING: "机器人暂停",
            self.STATE_STANDBY: "机器人就绪",
            self.STATE_SCRIPT_RUNNING: "脚本运行中",
            self.STATE_SCRIPT_HOLD_HANDLING: "脚本暂停处理中",
            self.STATE_SCRIPT_HOLDING: "脚本暂停",
            self.STATE_SCRIPT_STOPPING: "脚本停止中",
            self.STATE_SCRIPT_STOPPED: "脚本已停止",
            self.STATE_HRAPP_DISCONNECTED: "HRApp部件断开",
            self.STATE_HRAPP_ERROR: "HRApp部件错误",
            self.STATE_ROBOT_LOAD_IDENTIFY: "负载辨识",
            self.STATE_BRAKING: "开关抱闸中",
        }
        return state_map.get(state, f"未知状态({state})")
    
    def start_monitoring(self, callback: Optional[Callable] = None, interval: float = 1.0):
        """开始状态监控"""
        if self.monitoring:
            return
        
        self.monitoring = True
        if callback:
            self.state_callbacks.append(callback)
        
        def monitor_loop():
            while self.monitoring:
                try:
                    current_state = self.get_current_state()
                    for callback in self.state_callbacks:
                        callback(current_state)
                except Exception as e:
                    print(f"状态监控异常: {e}")
                time.sleep(interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """停止状态监控"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)
        self.state_callbacks.clear()
    
    def add_state_callback(self, callback: Callable):
        """添加状态变化回调"""
        self.state_callbacks.append(callback)
    
    def remove_state_callback(self, callback: Callable):
        """移除状态变化回调"""
        if callback in self.state_callbacks:
            self.state_callbacks.remove(callback)
    
    def read_robot_flags(self) -> tuple:
        """读取机器人状态标志"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadRobotFlags(self.box_id, self.robot_id, result)
            if ret == 0:
                return tuple(result)
            else:
                raise RobotStateError(ret, f"读取机器人标志失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取机器人标志失败: {str(e)}")
    
    def read_robot_state(self) -> tuple:
        """读取机器人完整状态"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadRobotState(self.box_id, self.robot_id, result)
            if ret == 0:
                return tuple(result)
            else:
                raise RobotStateError(ret, f"读取机器人状态失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取机器人状态失败: {str(e)}")
    
    def read_current_position(self) -> tuple:
        """读取当前位置信息"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadActPos(self.box_id, self.robot_id, result)
            if ret == 0 and len(result) >= 4:
                # 根据CPSClient的HRIF_ReadActPos方法文档，返回值应包含pose, joints, tcp, ucs
                # 这里假设result是一个包含所有信息的列表，需要根据实际返回格式进行调整
                return tuple(result[:4])  # 返回前4个元素作为示例
            else:
                raise RobotStateError(ret, f"读取位置信息失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取位置信息失败: {str(e)}")
    
    def read_axis_error_code(self) -> tuple:
        """读取轴错误码"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadAxisErrorCode(self.box_id, self.robot_id, result)
            if ret == 0:
                # 根据CPSClient的HRIF_ReadAxisErrorCode方法文档，返回值应包含error_code和axis_errors
                # 这里假设result是一个包含所有信息的列表，需要根据实际返回格式进行调整
                if len(result) >= 2:
                    return result[0], result[1]  # 返回前两个元素作为示例
                else:
                    return tuple(result)  # 如果只有一个元素，直接返回
            else:
                raise RobotStateError(ret, f"读取轴错误码失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取轴错误码失败: {str(e)}")
    
    def read_current_waypoint_id(self) -> str:
        """读取当前路点ID"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadCurWaypointID(self.box_id, self.robot_id, result)
            if ret == 0 and result:
                return str(result[0])  # 返回第一个元素作为路点ID
            else:
                raise RobotStateError(ret, f"读取当前路点ID失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取当前路点ID失败: {str(e)}")
    
    def read_point_by_name(self, point_name: str) -> tuple:
        """根据点位名称读取位置信息"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadPointByName(self.box_id, self.robot_id, point_name, result)
            if ret == 0:
                # 根据CPSClient的HRIF_ReadPointByName方法文档，返回值应包含joints, pose, tcp, ucs
                # 这里假设result是一个包含所有信息的列表，需要根据实际返回格式进行调整
                if len(result) >= 4:
                    return tuple(result[:4])  # 返回前4个元素作为示例
                else:
                    return tuple(result)  # 如果元素少于4个，直接返回
            else:
                raise RobotStateError(ret, f"读取点位信息失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取点位信息失败: {str(e)}")
    
    def read_point_list(self) -> list:
        """读取点位列表"""
        try:
            result = []
            ret = self.lib_wrapper.HRIF_ReadPointList(self.box_id, self.robot_id, result)
            if ret == 0:
                return list(result)  # 返回结果列表
            else:
                raise RobotStateError(ret, f"读取点位列表失败，错误码: {ret}")
        except Exception as e:
            raise RobotStateError(-1, f"读取点位列表失败: {str(e)}")
