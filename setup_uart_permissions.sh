#!/bin/bash
# 设置串口设备权限脚本

echo "设置串口设备权限..."

# 添加用户到dialout组
sudo usermod -a -G dialout $USER

# 创建udev规则文件
sudo tee /etc/udev/rules.d/99-usb-serial.rules > /dev/null <<EOF
# USB串口设备权限规则
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", KERNEL=="ttyUSB*", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", KERNEL=="ttyACM*", MODE="0666", GROUP="dialout"
EOF

# 重新加载udev规则
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "串口设备权限设置完成"
echo "请重新登录或重启系统以使组权限生效"