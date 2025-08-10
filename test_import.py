"""
测试导入修复的脚本
"""

try:
    # 测试从lib包导入RobotStatusMonitor
    from lib.status_monitor import RobotStatusMonitor
    print("✓ 成功从lib.status_monitor导入RobotStatusMonitor")
    
    # 测试从lib包导入异常类
    from lib.exceptions import RobotStateError, RobotTimeoutError
    print("✓ 成功从lib.exceptions导入RobotStateError和RobotTimeoutError")
    
    # 测试通过lib包导入异常类
    from lib import RobotStateError as LibRobotStateError
    print("✓ 成功从lib导入RobotStateError")
    
    print("\n所有导入测试都通过了！导入问题已解决。")
    
except ImportError as e:
    print(f"✗ 导入失败: {e}")
except Exception as e:
    print(f"✗ 发生错误: {e}")
