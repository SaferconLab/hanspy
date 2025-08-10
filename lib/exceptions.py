"""
HansRobot异常定义模块
"""
from wrapper.CPS_wrapper import CPSClient

class RobotError(Exception):
    """机器人通用异常"""
    def __init__(self, error_code, message=None):
        self.error_code = error_code
        self.message = message or self._get_error_message(error_code)
        super().__init__(f"机器人错误 {error_code}: {self.message}")
    
    def _get_error_message(self, error_code):
        """根据错误码获取错误信息"""
        error_map = {
            # 伺服驱动模块错误 (10000-10015)
            10000: "某个轴出现短路",
            10001: "某个轴电压超过48V",
            10002: "某个轴电压低于48V",
            10003: "某个轴速度超出限制",
            10004: "某个轴执行时报错",
            10005: "某个轴电流超出电机有效电流限制",
            10006: "某个轴编码器出现异常",
            10007: "某个轴实际位置无法跟随命令位置",
            10008: "某个轴实际速度无法跟随命令速度",
            10009: "某个轴实际位置超过负关节限位",
            10010: "某个轴实际位置超过正关节限位",
            10011: "驱动报出超出温度限制错误",
            10012: "某个轴电流超出电机最大电流限制",
            10013: "驱动报出急停错误",
            10014: "驱动报出UDM错误",
            10015: "驱动报出伺服参数错误",
            
            # 协作功能模块错误 (10016-11000)
            10016: "从站掉线",
            10017: "安全碰撞错误",
            10018: "零力示教计算错误",
            10019: "零力示教超出限制错误",
            10020: "零力示教超出最大电流限制",
            10021: "负载或安装角度设置错误",
            10022: "超出负关节安全空间",
            10023: "超出正关节安全空间",
            10024: "超出笛卡尔坐标系正向安全空间",
            10025: "超出笛卡尔坐标系负向安全空间",
            10026: "SDK错误",
            10027: "奇异点错误",
            10028: "力传感器检测到的数据超过力极限值",
            10029: "一般停止标准",
            10030: "力传感器错误",
            10031: "检测和校准之间的力差超过阈值",
            10032: "力传感器检测到的力或力矩超过力极限值",
            
            # 运动控制模块错误 (15000-16000)
            15068: "运动控制参数错误",
            15278: "轴组相关错误",
            15301: "连续路径规划错误",
            15321: "坐标变换和路径计算错误",
            15341: "轨迹规划和插补错误",
            
            # 指令执行返回错误(CPS) (20000-39999)
            20000: "基础指令错误",
            20100: "机器人状态相关错误",
            20200: "配置文件和脚本错误",
            20500: "JSON解析错误",
            20600: "脚本执行错误",
            20700: "TCP通信错误",
            20800: "插件相关错误",
            20900: "扩展设备通信错误",
            29996: "授权相关错误",
            30001: "Modbus通信错误",
            39500: "SDK连接错误",
            
            # 指令执行返回错误(CDS) (40000-40500)
            40000: "控制器状态错误",
            40051: "机器人运动状态错误",
            49502: "运动规划错误",
        }
        
        # 根据错误码范围返回通用描述
        if 10000 <= error_code <= 10015:
            return f"伺服驱动错误: {error_map.get(error_code, '未知伺服错误')}"
        elif 10016 <= error_code <= 11000:
            return f"协作功能错误: {error_map.get(error_code, '未知协作错误')}"
        elif 15000 <= error_code <= 16000:
            return f"运动控制错误: {error_map.get(error_code, '未知运动控制错误')}"
        elif 20000 <= error_code <= 39999:
            return f"CPS指令错误: {error_map.get(error_code, '未知CPS错误')}"
        elif 40000 <= error_code <= 40500:
            return f"CDS指令错误: {error_map.get(error_code, '未知CDS错误')}"
        else:
            return f"未知错误类型: 错误码 {error_code}"


class RobotConnectionError(RobotError):
    """机器人连接异常"""
    pass


class RobotStateError(RobotError):
    """机器人状态异常"""
    pass


class RobotTimeoutError(RobotError):
    """机器人超时异常"""
    pass


class ErrorCodeHelper:
    """错误码辅助类"""
    
    @staticmethod
    def get_error_message(lib_wraper: CPSClient, error_code: int, box_id: int = 0) -> str:
        """获取错误码的详细描述"""
        if not lib_wraper:
            return f"机器人库未加载，错误码: {error_code}"
        
        result = []
        ret = lib_wraper.HRIF_GetErrorCodeStr(box_id, error_code, result)
        if ret == 0 and result:
            return result[0]
        else:
            return f"获取错误信息失败，错误码: {error_code}"
    
    @staticmethod
    def get_error_category(error_code: int) -> str:
        """获取错误码类别"""
        if 10000 <= error_code <= 10015:
            return "伺服驱动错误"
        elif 10016 <= error_code <= 11000:
            return "协作功能错误"
        elif 15000 <= error_code <= 16000:
            return "运动控制错误"
        elif 20000 <= error_code <= 39999:
            return "CPS指令错误"
        elif 40000 <= error_code <= 40500:
            return "CDS指令错误"
        else:
            return "未知错误类型"
