#!/usr/bin/env python3
"""
夹爪控制器模块 - 串口通信版本
封装了常用的夹爪控制功能接口，使用标准串口通信
"""

import time
import sys
import logging
import serial
import serial.tools.list_ports
from typing import Optional, List, Tuple

# 作为模块时只导出GripperController类
__all__ = ['GripperController']

# 自定义Logger类，用于捕获日志
class LogCaptureLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET, log_history=None):
        super().__init__(name, level)
        self.log_history = log_history or []
    
    def handle(self, record):
        # 将日志记录到历史记录列表中
        self.log_history.append(str(record.getMessage()))
        # 调用父类的handle方法以确保日志正常输出
        super().handle(record)

# 注册自定义logger
logging.setLoggerClass(LogCaptureLogger)

# 配置根日志记录器，使日志能输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Modbus RTU参数
BAUDRATE = 115200
WORD_LENGTH = 8
STOP_BITS = 1
PARITY = serial.PARITY_NONE
TIMEOUT = 2.0

class GripperController:
    """
    夹爪控制器类 - 串口通信版本
    封装了常用的夹爪控制功能接口
    """
    
    def __init__(self, device_index: int = 0, device_name: str = "/dev/ttyUSB0", device_address: int = 1):
        """
        初始化夹爪控制器
        
        Args:
            device_index (int): 设备索引，为了兼容原版本，默认为0
            device_name (str): 串口设备名，默认为/dev/ttyUSB0
            device_address (int): 设备Modbus地址，默认为1
        """
        self.serial_port = None
        self.device_index = device_index  # 保留设备索引参数以兼容原版本
        self.device_name = device_name
        self.device_address = device_address
        self._log_history = []  # 存储历史日志
        # 为这个实例创建一个logger，使用自定义的LogCaptureLogger类
        self.logger = logging.getLogger(f"GripperController_{id(self)}")
        self.logger.log_history = self._log_history
        
    @property
    def log_history(self):
        """
        获取历史日志的属性
        
        Returns:
            list: 包含所有日志条目的列表
        """
        return self._log_history
        
    def get_log_history(self):
        """
        获取历史日志的方法
        
        Returns:
            list: 包含所有日志条目的列表
        """
        return self._log_history
        
    def clear_log_history(self):
        """
        清空历史日志
        """
        self._log_history.clear()
        
    @staticmethod
    def list_available_ports() -> List[Tuple[str, str, str]]:
        """
        列出所有可用的串口设备
        
        Returns:
            List[Tuple[str, str, str]]: 包含(设备名, 描述, 硬件ID)的元组列表
        """
        ports = serial.tools.list_ports.comports()
        return [(port.device, port.description, port.hwid) for port in ports]
        
    def open_device(self) -> bool:
        """
        打开串口设备
        
        Returns:
            bool: 成功返回True，失败返回False
        """
        try:
            self.serial_port = serial.Serial(
                port=self.device_name,
                baudrate=BAUDRATE,
                bytesize=WORD_LENGTH,
                parity=PARITY,
                stopbits=STOP_BITS,
                timeout=TIMEOUT,
                write_timeout=TIMEOUT
            )
            
            if self.serial_port.is_open:
                self.logger.info(f"成功打开串口设备: {self.device_name}")
                return True
            else:
                self.logger.error(f"无法打开串口设备: {self.device_name}")
                return False
                
        except serial.SerialException as e:
            error_msg = str(e)
            if "Permission denied" in error_msg or "PermissionError" in error_msg:
                self.logger.error(f"串口设备权限不足: {self.device_name}")
                self.logger.error("请尝试以下解决方案:")
                self.logger.error("1. 运行 'sudo chmod 666 /dev/ttyUSB0' 临时设置权限")
                self.logger.error("2. 运行 'sudo usermod -a -G dialout $USER' 添加用户到dialout组")
                self.logger.error("3. 运行 'bash setup_uart_permissions.sh' 设置永久权限")
                self.logger.error("4. 重新登录或重启系统使组权限生效")
            else:
                self.logger.error(f"打开串口设备失败: {e}")
            return False
        except Exception as e:
            self.logger.error(f"未知错误: {e}")
            return False
            
    def set_baudrate(self) -> bool:
        """
        设置波特率 - 兼容原版本接口
        
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not self.serial_port or not self.serial_port.is_open:
            self.logger.error("设备未打开")
            return False
            
        try:
            self.serial_port.baudrate = BAUDRATE
            self.logger.info(f"波特率设置为 {BAUDRATE}")
            return True
        except Exception as e:
            self.logger.error(f"设置波特率失败: {e}")
            return False
            
    def set_data_characteristics(self) -> bool:
        """
        设置数据特性 (8N1格式) - 兼容原版本接口
        
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not self.serial_port or not self.serial_port.is_open:
            self.logger.error("设备未打开")
            return False
            
        try:
            self.serial_port.bytesize = WORD_LENGTH
            self.serial_port.parity = PARITY
            self.serial_port.stopbits = STOP_BITS
            self.logger.info(f"数据特性设置成功: {WORD_LENGTH}位数据, {STOP_BITS}个停止位, {PARITY}个奇偶校验")
            return True
        except Exception as e:
            self.logger.error(f"设置数据特性失败: {e}")
            return False
            
    def set_timeouts(self, read_timeout: int = 2000, write_timeout: int = 2000) -> bool:
        """
        设置超时时间 - 兼容原版本接口
        
        Args:
            read_timeout (int): 读取超时时间(毫秒)
            write_timeout (int): 写入超时时间(毫秒)
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not self.serial_port or not self.serial_port.is_open:
            self.logger.error("设备未打开")
            return False
            
        try:
            self.serial_port.timeout = read_timeout / 1000.0
            self.serial_port.write_timeout = write_timeout / 1000.0
            self.logger.info(f"超时设置成功: 读取{read_timeout}ms, 写入{write_timeout}ms")
            return True
        except Exception as e:
            self.logger.error(f"设置超时失败: {e}")
            return False
            
    def close_device(self):
        """
        关闭串口设备
        """
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.logger.info("串口设备已关闭")
            
    def flush_buffers(self) -> bool:
        """
        清空缓冲区
        
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not self.serial_port or not self.serial_port.is_open:
            self.logger.error("设备未打开")
            return False
            
        try:
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()
            self.logger.info("缓冲区已清空")
            return True
        except Exception as e:
            self.logger.error(f"清空缓冲区失败: {e}")
            return False
            
    def send_command(self, command: bytes, debug: bool = False) -> bool:
        """
        发送命令到夹爪
        
        Args:
            command (bytes): 要发送的命令
            debug (bool): 是否显示调试信息
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not self.serial_port or not self.serial_port.is_open:
            self.logger.error("设备未打开")
            return False
            
        try:
            bytes_written = self.serial_port.write(command)
            self.serial_port.flush()
            
            if debug:
                self.logger.debug(f"发送命令: {command.hex()} ({bytes_written} 字节)")
            else:
                self.logger.info(f"成功发送命令: {command.hex()} ({bytes_written} 字节)")
            return True
        except Exception as e:
            self.logger.error(f"发送命令失败: {e}")
            return False
            
    def read_response(self, buffer_size: int = 1024, timeout_ms: int = 2000, debug: bool = False) -> bytes:
        """
        从夹爪读取响应
        
        Args:
            buffer_size (int): 缓冲区大小
            timeout_ms (int): 超时时间(毫秒)
            debug (bool): 是否显示调试信息
            
        Returns:
            bytes: 响应数据
        """
        if not self.serial_port or not self.serial_port.is_open:
            self.logger.error("设备未打开")
            return b''
            
        try:
            # 设置读取超时
            original_timeout = self.serial_port.timeout
            self.serial_port.timeout = timeout_ms / 1000.0
            
            response = self.serial_port.read(buffer_size)
            
            # 恢复原始超时设置
            self.serial_port.timeout = original_timeout
            
            if response:
                if debug:
                    self.logger.debug(f"读取到 {len(response)} 字节: {response.hex()}")
                else:
                    self.logger.info(f"读取到 {len(response)} 字节: {response.hex()}")
            else:
                self.logger.warning("未收到响应")
            return response
        except Exception as e:
            self.logger.error(f"读取响应失败: {e}")
            return b''

    def _parse_specific_response(self, response: bytes, expected_address: int, expected_function: int) -> bytes:
        """
        解析特定的响应，从多个响应中提取我们需要的那个
        
        Args:
            response (bytes): 原始响应数据
            expected_address (int): 期望的设备地址
            expected_function (int): 期望的功能码
            
        Returns:
            bytes: 解析后的响应数据，如果未找到则返回空bytes
        """
        if not response:
            return b''
            
        # 标准响应格式: [地址][功能码][字节数][数据1][数据2][CRC_L][CRC_H]
        # 对于读取寄存器(0x03)响应，数据部分应为2字节(1个字)
        expected_length = 7  # 1+1+1+2+2
        
        # 查找标准响应格式
        for i in range(len(response) - expected_length + 1):
            if (response[i] == expected_address and 
                response[i+1] == expected_function and
                response[i+2] == 0x02):  # 字节数=2
                
                # 验证CRC
                parsed_response = response[i:i+expected_length]
                if self._validate_crc(parsed_response):
                    return parsed_response
                    
        # 如果没有找到匹配的响应，返回原始响应
        self.logger.debug("未找到标准响应，返回原始响应")
        return response

    def set_gripper_amplitude(self, amplitude: int) -> bool:
        """
        设置夹爪幅度(开合程度)
        
        Args:
            amplitude (int): 幅度值，范围0-100
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not 0 <= amplitude <= 100:
            self.logger.error("幅度值必须在0-100范围内")
            return False
            
        # 构造Modbus RTU命令
        # 地址: 0x9C40 (40000)
        # 功能码: 0x10 (写多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        # 字节数: 0x02 (2字节)
        # 数据: 幅度值的高低字节
        
        # 将幅度值转换为两个字节
        high_byte = (amplitude >> 8) & 0xFF
        low_byte = amplitude & 0xFF
        
        # 构建命令
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x40,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            high_byte,            # 幅度值高字节
            low_byte,             # 幅度值低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        result = self.send_command(command, debug=True)
        if result:
            self.logger.info(f"夹爪幅度设置为 {amplitude}%")
            response = self.read_response(timeout_ms=3000, debug=True)
        else:
            self.logger.error("发送设置夹爪幅度命令失败")
        return result
    
    def set_gripper_force(self, force: int) -> bool:
        """
        设置夹爪力度
        
        Args:
            force (int): 力度值，范围0-100
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not 0 <= force <= 100:
            self.logger.error("力度值必须在0-100范围内")
            return False
            
        # 构造Modbus RTU命令
        # 地址: 0x9C41 (40001)
        # 功能码: 0x10 (写多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        # 字节数: 0x02 (2字节)
        # 数据: 力度值的高低字节
        
        # 将力度值转换为两个字节
        high_byte = (force >> 8) & 0xFF
        low_byte = force & 0xFF
        
        # 构建命令
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x41,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            high_byte,            # 力度值高字节
            low_byte,             # 力度值低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        result = self.send_command(command, debug=True)
        if result:
            self.logger.info(f"夹爪力度设置为 {force}%")
            response = self.read_response(timeout_ms=3000, debug=True)
        else:
            self.logger.error("发送设置夹爪力度命令失败")
        return result
    
    def get_gripper_position(self) -> int:
        """
        获取夹爪当前位置
        
        Returns:
            int: 当前位置值，范围0-100，失败返回-1
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C45 (40005)
        # 功能码: 0x03 (读多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x03,                 # 功能码: 读多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x45,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        # 发送命令并读取响应
        # 必须请求两次！第二次是真实值
        # 第一次请求
        try:
            result = self.send_command(command, debug=False)
            if not result:
                self.logger.error("第一次发送读取位置命令失败")
                return -1
            response = self.read_response(timeout_ms=2000, debug=False)
        except Exception as e:
            self.logger.error(f"第一次请求位置失败: {e}")
            return -1
        
        # 第二次请求
        try:
            result = self.send_command(command, debug=True)
        except Exception as e:
            self.logger.error(f"第二次发送读取位置命令失败: {e}")
            return -1
        if not result:
            self.logger.error("第二次发送读取位置命令失败")
            return -1
            
        # 读取响应
        response = self.read_response(timeout_ms=3000, debug=True)
        if not response or len(response) < 5:
            self.logger.error("读取响应失败或响应不完整")
            return -1
            
        # 解析特定响应
        parsed_response = self._parse_specific_response(response, self.device_address, 0x03)
        if len(parsed_response) < 7:  # 标准响应应为7字节
            self.logger.error("解析响应失败")
            return -1
            
        # 解析响应中的位置值
        # 响应格式: [地址][功能码][字节数][数据1][数据2][CRC_L][CRC_H]
        self.logger.debug(f"完整响应数据: {parsed_response.hex()}")
        self.logger.debug(f"数据字节1: {parsed_response[3]:02x}, 数据字节2: {parsed_response[4]:02x}")
        # 组合两个字节的值 (高位在前)
        position = (parsed_response[3] << 8) | parsed_response[4]
        if position < 0 or position > 100:
            self.logger.error(f"无效的位置值: {position}%")
            return -1
        self.logger.debug(f"读取位置值: {position}%")
        return position
    
    def get_gripper_torque(self) -> int:
        """
        获取夹爪当前力矩
        
        Returns:
            int: 当前力矩值，范围0-100，失败返回-1
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C46 (40006)
        # 功能码: 0x03 (读多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x03,                 # 功能码: 读多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x46,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        # 发送命令并读取响应
        # 必须请求两次！第二次是真实值
        # 第一次请求
        try:
            result = self.send_command(command, debug=False)
            if not result:
                self.logger.error("第一次发送读取力矩命令失败")
                return -1
            response = self.read_response(timeout_ms=2000, debug=False)
        except Exception as e:
            self.logger.error(f"第一次请求力矩失败: {e}")
            return -1
        
        # 第二次请求
        try:
            result = self.send_command(command, debug=True)
            if not result:
                self.logger.error("第二次发送读取力矩命令失败")
                return -1
        except Exception as e:
            self.logger.error(f"第二次发送读取力矩命令失败: {e}")
            return -1

        # 读取响应
        try:
            response = self.read_response(timeout_ms=3000, debug=True)
            if not response or len(response) < 5:
                self.logger.error("读取响应失败或响应不完整")
                return -1
        except Exception as e:
            self.logger.error(f"读取响应失败: {e}")
            return -1
            
        # 解析特定响应
        parsed_response = self._parse_specific_response(response, self.device_address, 0x03)
        if len(parsed_response) < 7:  # 标准响应应为7字节
            self.logger.error("解析响应失败")
            return -1
            
        # 解析响应中的力矩值
        # 响应格式: [地址][功能码][字节数][数据1][数据2][CRC_L][CRC_H]
        self.logger.debug(f"完整响应数据: {parsed_response.hex()}")
        self.logger.debug(f"数据字节1: {parsed_response[3]:02x}, 数据字节2: {parsed_response[4]:02x}")
        # 组合两个字节的值 (高位在前)
        torque = (parsed_response[3] << 8) | parsed_response[4]
        if torque < 0 or torque > 100:
            self.logger.error(f"无效的力矩值: {torque}%")
            return -1
        self.logger.debug(f"读取力矩值: {torque}%")
        return torque
    
    def find_travel(self) -> bool:
        """
        执行找行程指令
        
        Returns:
            bool: 成功返回True，失败返回False
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C48 (40008)
        # 功能码: 0x10 (写多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        # 字节数: 0x02 (2字节)
        # 数据: 0x0001 (执行找行程)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x48,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            0x00,                 # 数据高字节
            0x01,                 # 数据低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        return self.send_command(command, debug=True)
        
    def is_command_completed(self) -> bool:
        """
        检查指令是否执行完成
        
        Returns:
            bool: 完成返回True，执行中返回False，失败返回None
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C47 (40007)
        # 功能码: 0x03 (读多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x03,                 # 功能码: 读多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x47,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        # 发送命令并读取响应
        # 必须请求两次！第二次是真实值
        # 第一次请求
        try:
            result = self.send_command(command, debug=False)
            if not result:
                self.logger.error("第一次发送读取指令完成状态命令失败")
                return None
            response = self.read_response(timeout_ms=2000, debug=False)
        except Exception as e:
            self.logger.error(f"第一次请求指令完成状态失败: {e}")
            return None
        
        # 第二次请求
        try:
            result = self.send_command(command, debug=True)
            if not result:
                self.logger.error("第二次发送读取指令完成状态命令失败")
                return None
        except Exception as e:
            self.logger.error(f"第二次发送读取指令完成状态命令失败: {e}")
            return None
        
        # 读取响应
        try:
            response = self.read_response(timeout_ms=3000, debug=True)
            if not response or len(response) < 5:
                self.logger.error("读取响应失败或响应不完整")
                return None
        except Exception as e:
            self.logger.error(f"读取响应失败: {e}")
            return None
            
        # 解析特定响应
        parsed_response = self._parse_specific_response(response, self.device_address, 0x03)
        if len(parsed_response) < 5:
            self.logger.error("解析响应失败")
            return None
            
        # 解析响应中的状态值
        # 响应格式: [地址][功能码][字节数][数据1][数据2][CRC_L][CRC_H]
        status = (parsed_response[3] << 8) | parsed_response[4]
        return bool(status)
    
    def disable_auto_find_travel(self, save_to_flash: bool = False) -> bool:
        """
        关闭自动找行程指令
        
        Args:
            save_to_flash (bool): 是否保存到闪存，默认为False
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C9A (40090)
        # 功能码: 0x10 (写多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        # 字节数: 0x02 (2字节)
        # 数据: 0x0001 (关闭自动找行程) 或 0x0002 (关闭自动找行程且断电保存)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x9A,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            0x00,                 # 数据高字节
            0x02 if save_to_flash else 0x01,  # 数据低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        result = self.send_command(command, debug=True)
        if result:
            action = "关闭自动找行程并保存到闪存" if save_to_flash else "关闭自动找行程"
            self.logger.info(f"{action}命令发送成功")
            response = self.read_response(timeout_ms=3000, debug=True)
        else:
            self.logger.error("发送关闭自动找行程命令失败")
        return result
    
    def enable_auto_find_travel(self, save_to_flash: bool = False) -> bool:
        """
        恢复自动找行程指令
        
        Args:
            save_to_flash (bool): 是否保存到闪存，默认为False
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C9A (40090)
        # 功能码: 0x10 (写多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        # 字节数: 0x02 (2字节)
        # 数据: 0x0003 (恢复自动找行程且断电保存)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x9A,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            0x00,                 # 数据高字节
            0x03,                 # 数据低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        result = self.send_command(command, debug=True)
        if result:
            action = "恢复自动找行程并保存到闪存" if save_to_flash else "恢复自动找行程"
            self.logger.info(f"{action}命令发送成功")
            response = self.read_response(timeout_ms=3000, debug=True)
        else:
            self.logger.error("发送恢复自动找行程命令失败")
        return result
    
    def set_gripper_speed(self, speed: int, save_to_flash: bool = False) -> bool:
        """
        设置夹爪开合速度
        
        Args:
            speed (int): 速度值，范围0-100
            save_to_flash (bool): 是否保存到闪存，默认为False
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not 0 <= speed <= 100:
            self.logger.error("速度值必须在0-100范围内")
            return False
            
        # 选择寄存器地址
        # 40010 (0x9C4A): 设置夹爪开合速度
        # 40011 (0x9C4B): 保存夹爪开合速度，断电保留
        register_address = 0x9C4B if save_to_flash else 0x9C4A
        
        # 构造Modbus RTU命令
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            (register_address >> 8) & 0xFF,  # 寄存器地址高字节
            register_address & 0xFF,         # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            (speed >> 8) & 0xFF,  # 速度值高字节
            speed & 0xFF,         # 速度值低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        result = self.send_command(command, debug=True)
        if result:
            action = "设置夹爪速度并保存到闪存" if save_to_flash else "设置夹爪速度"
            self.logger.info(f"{action}为 {speed}%")
            response = self.read_response(timeout_ms=3000, debug=True)
        else:
            self.logger.error("发送设置夹爪速度命令失败")
        return result
    
    def set_device_address(self, address: int) -> bool:
        """
        设置夹爪地址
        
        Args:
            address (int): 新地址，范围1-10000
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        if not 1 <= address <= 10000:
            self.logger.error("地址值必须在1-10000范围内")
            return False
            
        # 构造Modbus RTU命令
        # 地址: 0x9C9B (40091)
        # 功能码: 0x10 (写多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        # 字节数: 0x02 (2字节)
        # 数据: 新地址
        
        command = bytes([
            self.device_address,  # 设备地址
            0x10,                 # 功能码: 写多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x9B,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
            0x02,                 # 字节数
            (address >> 8) & 0xFF,  # 地址值高字节
            address & 0xFF,         # 地址值低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        result = self.send_command(command, debug=True)
        if result:
            self.logger.info(f"夹爪地址设置为 {address}")
            self.device_address = address  # 更新本地地址
            response = self.read_response(timeout_ms=3000, debug=True)
        else:
            self.logger.error("发送设置夹爪地址命令失败")
        return result
    
    def is_travel_not_found(self) -> bool:
        """
        检查夹爪是否未找行程
        
        Returns:
            bool: 未找行程返回True，找行程完成返回False，失败返回None
        """
        # 构造Modbus RTU命令
        # 地址: 0x9C49 (40009)
        # 功能码: 0x03 (读多个寄存器)
        # 寄存器数量: 0x0001 (1个寄存器)
        
        command = bytes([
            self.device_address,  # 设备地址
            0x03,                 # 功能码: 读多个寄存器
            0x9C,                 # 寄存器地址高字节
            0x49,                 # 寄存器地址低字节
            0x00,                 # 寄存器数量高字节
            0x01,                 # 寄存器数量低字节
        ])
        
        # 计算CRC校验
        crc = self._calculate_crc(command)
        command += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
        
        # 发送命令并读取响应
        # 必须请求两次！第二次是真实值
        # 第一次请求
        try:
            result = self.send_command(command, debug=False)
            if not result:
                self.logger.error("第一次发送读取找行程状态命令失败")
                return None
            response = self.read_response(timeout_ms=2000, debug=False)
        except Exception as e:
            self.logger.error(f"第一次请求找行程状态失败: {e}")
            return None
        
        # 第二次请求
        try:
            result = self.send_command(command, debug=True)
            if not result:
                self.logger.error("第二次发送读取找行程状态命令失败")
                return None
        except Exception as e:
            self.logger.error(f"第二次发送读取找行程状态命令失败: {e}")
            return None
        
        # 读取响应
        try:
            response = self.read_response(timeout_ms=3000, debug=True)
            if not response or len(response) < 5:
                self.logger.error("读取响应失败或响应不完整")
                return None
        except Exception as e:
            self.logger.error(f"读取响应失败: {e}")
            return None
            
        # 解析特定响应
        parsed_response = self._parse_specific_response(response, self.device_address, 0x03)
        if len(parsed_response) < 5:
            self.logger.error("解析响应失败")
            return None
            
        # 解析响应中的状态值
        # 响应格式: [地址][功能码][字节数][数据1][数据2][CRC_L][CRC_H]
        status = (parsed_response[3] << 8) | parsed_response[4]
        return bool(status)  # 1表示未找行程，0表示找行程完成
    
    def _calculate_crc(self, data: bytes) -> int:
        """
        计算Modbus RTU CRC校验值
        
        Args:
            data (bytes): 要计算CRC的数据
            
        Returns:
            int: CRC校验值
        """
        # Modbus CRC计算表
        crc_table = [
            0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
            0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
            0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
            0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
            0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
            0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
            0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
            0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
            0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
            0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
            0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
            0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
            0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
            0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
            0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
            0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
            0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
            0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
            0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
            0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
            0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
            0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
            0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
            0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
            0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
            0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
            0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
            0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
            0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
            0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
            0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
            0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
        ]
        
        crc = 0xFFFF
        for byte in data:
            crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
        return crc

    def _validate_crc(self, response: bytes) -> bool:
        """
        验证Modbus RTU响应的CRC校验
        
        Args:
            response (bytes): 带CRC的响应数据
            
        Returns:
            bool: CRC校验通过返回True，否则返回False
        """
        if len(response) < 3:
            return False
            
        # 提取数据部分（除了CRC）
        data_to_check = response[:-2]
        # 提取接收到的CRC
        received_crc = (response[-1] << 8) | response[-2]
        # 计算CRC
        calculated_crc = self._calculate_crc(data_to_check)
        
        return received_crc == calculated_crc

# 测试代码
if __name__ == "__main__":
    """
    基础测试代码
    """
    print("=" * 50)
    print("夹爪控制器基础测试 - 串口版本")
    print("=" * 50)
    
    # 列出可用串口
    print("\n可用串口设备:")
    available_ports = GripperController.list_available_ports()
    for i, (device, desc, hwid) in enumerate(available_ports):
        print(f"{i}: {device} - {desc} ({hwid})")
    
    # 创建夹爪控制器
    gripper = GripperController()
    
    try:
        # 打开设备
        if not gripper.open_device():
            print("无法打开设备，请检查连接和权限")
            exit(1)
            
        # 清空缓冲区
        gripper.flush_buffers()
        
        # 测试获取夹爪位置
        print("\n1. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试设置夹爪幅度
        print("\n2. 测试设置夹爪幅度...")
        if gripper.set_gripper_amplitude(0):
            print("✓ 设置夹爪幅度0%成功")
        else:
            print("✗ 设置夹爪幅度0%失败")
            
        time.sleep(3)
        
        # 测试设置夹爪幅度
        print("\n3. 测试设置夹爪幅度...")
        if gripper.set_gripper_amplitude(50):
            print("✓ 设置夹爪幅度50%成功")
        else:
            print("✗ 设置夹爪幅度50%失败")
            
        time.sleep(3)

        # 测试获取夹爪位置
        print("\n4. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试设置夹爪幅度
        print("\n5. 测试设置夹爪幅度...")
        if gripper.set_gripper_amplitude(100):
            print("✓ 设置夹爪幅度100%成功")
        else:
            print("✗ 设置夹爪幅度100%失败")
            
        time.sleep(2)

        # 测试获取夹爪位置
        print("\n6. 测试获取夹爪位置...")
        position = gripper.get_gripper_position()
        if position >= 0:
            print(f"✓ 夹爪当前位置: {position}%")
        else:
            print("✗ 获取夹爪位置失败")
            
        time.sleep(1)

        # 测试获取夹爪力矩
        print("\n7. 测试获取夹爪力矩...")
        torque = gripper.get_gripper_torque()
        if torque >= 0:
            print(f"✓ 夹爪当前力矩: {torque}%")
        else:
            print("✗ 获取夹爪力矩失败")
            
        time.sleep(1)

        # 测试设置夹爪力度
        print("\n8. 测试设置夹爪力度...")
        if gripper.set_gripper_force(50):
            print("✓ 设置夹爪力度50%成功")
        else:
            print("✗ 设置夹爪力度50%失败")
            
        time.sleep(1)
        
        # 测试获取夹爪力矩
        print("\n9. 测试获取夹爪力矩...")
        torque = gripper.get_gripper_torque()
        if torque >= 0:
            print(f"✓ 夹爪当前力矩: {torque}%")
        else:
            print("✗ 获取夹爪力矩失败")
            
        time.sleep(1)
        
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭设备
        gripper.close_device()
        print("\n程序结束")