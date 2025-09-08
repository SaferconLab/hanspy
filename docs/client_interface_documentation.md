# 客户端接口文档

## 概述

本文档描述了控制器服务器提供的客户端接口，包括所有可用的命令、消息格式和响应结构。客户端可以通过TCP连接到服务器，并发送JSON格式的命令来控制机器人和夹爪设备。

## 服务器连接

### 连接地址
- 主机地址: `0.0.0.0`
- 端口: `8888`

### 连接流程
1. 客户端通过TCP连接到服务器
2. 服务器返回欢迎消息
3. 客户端可以开始发送命令

## 消息格式

### 命令消息格式
```json
{
  "type": "command_type",
  "data": {
    // 命令特定的数据
  },
  "message_id": "unique_id"
}
```

### 响应消息格式
```json
{
  "type": "response",
  "status": "success|error|pending",
  "message": "响应消息",
  "data": {
    // 响应特定的数据
  },
  "message_id": "unique_id"
}
```

## 命令列表

### 1. 机器人连接相关

#### 1.1 连接机器人 (connect_robot)
**描述**: 连接到机器人设备

**请求数据**:
```json
{
  "type": "connect_robot"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人连接成功",
  "data": {
    "connected": true
  }
}
```

#### 1.2 断开机器人连接 (disconnect_robot)
**描述**: 断开与机器人的连接

**请求数据**:
```json
{
  "type": "disconnect_robot"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人连接已断开",
  "data": {
    "connected": false
  }
}
```

#### 1.3 使能机器人 (enable_robot)
**描述**: 使能机器人，允许其运动

**请求数据**:
```json
{
  "type": "enable_robot"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人已使能",
  "data": {
    "enabled": true
  }
}
```

#### 1.4 去使能机器人 (disable_robot)
**描述**: 去使能机器人，禁止其运动

**请求数据**:
```json
{
  "type": "disable_robot"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人已去使能",
  "data": {
    "enabled": false
  }
}
```

### 2. 机器人运动相关

#### 2.1 关节运动 (move_j)
**描述**: 执行关节空间运动

**请求数据**:
```json
{
  "type": "move_j",
  "data": {
    "points": [X, Y, Z, Rx, Ry, Rz],
    "raw_acs_points": [J1, J2, J3, J4, J5, J6],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0,
    "timeout": 30.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "关节运动完成",
  "data": {
    "moved": true
  }
}
```

#### 2.2 直线运动 (move_l)
**描述**: 执行直线空间运动

**请求数据**:
```json
{
  "type": "move_l",
  "data": {
    "points": [X, Y, Z, Rx, Ry, Rz],
    "raw_acs_points": [J1, J2, J3, J4, J5, J6],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0,
    "timeout": 30.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "直线运动完成",
  "data": {
    "moved": true
  }
}
```

#### 2.3 获取位置 (get_position)
**描述**: 获取机器人当前位置信息

**请求数据**:
```json
{
  "type": "get_position"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "获取位置信息成功",
  "data": {
    "joint_positions": [J1, J2, J3, J4, J5, J6],
    "cartesian_positions": [X, Y, Z, Rx, Ry, Rz]
  }
}
```

#### 2.4 设置速度比 (set_override)
**描述**: 设置机器人运动速度比

**请求数据**:
```json
{
  "type": "set_override",
  "data": {
    "velocity": 0.5
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "速度比设置成功",
  "data": {
    "velocity": 0.5
  }
}
```

#### 2.5 停止运动 (stop)
**描述**: 立即停止机器人运动

**请求数据**:
```json
{
  "type": "stop"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人已停止",
  "data": {
    "stopped": true
  }
}
```

#### 2.6 复位机器人 (reset)
**描述**: 复位机器人系统

**请求数据**:
```json
{
  "type": "reset"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人已复位",
  "data": {
    "reset": true
  }
}
```

#### 2.7 运动到姿态 (goto_pose)
**描述**: 运动到指定末端姿态

**请求数据**:
```json
{
  "type": "goto_pose",
  "data": {
    "pose": [X, Y, Z, Rx, Ry, Rz],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "运动到姿态完成",
  "data": {
    "moved": true
  }
}
```

#### 2.8 运动到关节位置 (goto_joint)
**描述**: 运动到指定关节位置

**请求数据**:
```json
{
  "type": "goto_joint",
  "data": {
    "joint_positions": [J1, J2, J3, J4, J5, J6],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "运动到关节位置完成",
  "data": {
    "moved": true
  }
}
```

#### 2.9 机器人上电 (electrify)
**描述**: 对机器人进行上电操作

**请求数据**:
```json
{
  "type": "electrify"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人已成功上电",
  "data": {
    "electrified": true
  }
}
```

#### 2.10 机器人断电 (blackout)
**描述**: 对机器人进行断电操作

**请求数据**:
```json
{
  "type": "blackout"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "机器人已成功断电",
  "data": {
    "blackout": true
  }
}
```

#### 2.11 获取机器人状态 (get_current_state)
**描述**: 获取机器人当前状态码

**请求数据**:
```json
{
  "type": "get_current_state"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "获取机器人状态成功",
  "data": {
    "state": 1
  }
}
```

#### 2.12 获取状态描述 (get_state_description)
**描述**: 获取机器人状态描述

**请求数据**:
```json
{
  "type": "get_state_description",
  "data": {
    "state": 1
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "获取状态描述成功",
  "data": {
    "description": "就绪"
  }
}
```

#### 2.13 检查就绪状态 (is_ready)
**描述**: 检查机器人是否处于就绪状态

**请求数据**:
```json
{
  "type": "is_ready"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "检查就绪状态成功",
  "data": {
    "ready": true
  }
}
```

#### 2.14 检查运动状态 (is_moving)
**描述**: 检查机器人是否正在运动

**请求数据**:
```json
{
  "type": "is_moving"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "检查运动状态成功",
  "data": {
    "moving": false
  }
}
```

#### 2.15 等待运动完成 (wait_for_motion_done)
**描述**: 等待机器人运动完成

**请求数据**:
```json
{
  "type": "wait_for_motion_done",
  "data": {
    "timeout": 30.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "等待运动完成",
  "data": {
    "done": true
  }
}
```

#### 2.16 获取速度比 (get_override)
**描述**: 获取当前速度比

**请求数据**:
```json
{
  "type": "get_override"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "获取速度比成功",
  "data": {
    "override": 0.5
  }
}
```

#### 2.17 增量运动到姿态 (goto_delta)
**描述**: 运动到指定末端6d姿态的增量位置

**请求数据**:
```json
{
  "type": "goto_delta",
  "data": {
    "delta_pose": [dX, dY, dZ, dRx, dRy, dRz],
    "tcp": [X, Y, Z, Rx, Ry, Rz],
    "ucs": [X, Y, Z, Rx, Ry, Rz],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "增量运动到姿态完成",
  "data": {
    "moved": true
  }
}
```

#### 2.18 增量运动到关节位置 (goto_delta_joint)
**描述**: 运动到指定关节位置的增量位置

**请求数据**:
```json
{
  "type": "goto_delta_joint",
  "data": {
    "delta_joints": [dJ1, dJ2, dJ3, dJ4, dJ5, dJ6],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "增量运动到关节位置完成",
  "data": {
    "moved": true
  }
}
```

### 3. 夹爪连接相关

#### 3.1 连接夹爪 (connect_gripper)
**描述**: 连接到夹爪设备

**请求数据**:
```json
{
  "type": "connect_gripper"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "夹爪连接成功",
  "data": {
    "connected": true
  }
}
```

#### 3.2 断开夹爪连接 (disconnect_gripper)
**描述**: 断开与夹爪的连接

**请求数据**:
```json
{
  "type": "disconnect_gripper"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "夹爪连接已断开",
  "data": {
    "connected": false
  }
}
```

### 4. 夹爪控制相关

#### 4.1 设置夹爪幅度 (set_gripper_amplitude)
**描述**: 设置夹爪开合幅度

**请求数据**:
```json
{
  "type": "set_gripper_amplitude",
  "data": {
    "amplitude": 50
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "夹爪幅度设置成功",
  "data": {
    "amplitude": 50
  }
}
```

#### 4.2 设置夹爪力度 (set_gripper_force)
**描述**: 设置夹爪抓取力度

**请求数据**:
```json
{
  "type": "set_gripper_force",
  "data": {
    "force": 50
  }
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "夹爪力度设置成功",
  "data": {
    "force": 50
  }
}
```

#### 4.3 获取夹爪位置 (get_gripper_position)
**描述**: 获取夹爪当前位置

**请求数据**:
```json
{
  "type": "get_gripper_position"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "获取夹爪位置成功",
  "data": {
    "position": 50
  }
}
```

#### 4.4 获取夹爪力矩 (get_gripper_torque)
**描述**: 获取夹爪当前力矩

**请求数据**:
```json
{
  "type": "get_gripper_torque"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "获取夹爪力矩成功",
  "data": {
    "torque": 50
  }
}
```

#### 4.5 夹爪找行程 (find_gripper_travel)
**描述**: 执行夹爪找行程指令

**请求数据**:
```json
{
  "type": "find_gripper_travel"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "夹爪找行程指令已发送",
  "data": {
    "executed": true
  }
}
```

#### 4.6 检查夹爪指令状态 (command_completed)
**描述**: 检查夹爪指令是否已完成

**请求数据**:
```json
{
  "type": "command_completed"
}
```

**响应数据**:
```json
{
  "status": "success",
  "message": "检查夹爪指令状态成功",
  "data": {
    "completed": true
  }
}
```

## 错误处理

### 错误响应格式
```json
{
  "type": "response",
  "status": "error",
  "message": "错误消息",
  "data": {},
  "message_id": "unique_id"
}
```

### 常见错误码
- `unknown`: 未知命令类型
- `invalid_json`: 无效的JSON格式
- `connection_failed`: 连接失败
- `operation_failed`: 操作失败
- `invalid_parameter`: 参数无效

## 使用示例

### 连接机器人并使能
```json
// 请求
{
  "type": "connect_robot"
}

// 响应
{
  "status": "success",
  "message": "机器人连接成功",
  "data": {
    "connected": true
  }
}

// 请求
{
  "type": "enable_robot"
}

// 响应
{
  "status": "success",
  "message": "机器人已使能",
  "data": {
    "enabled": true
  }
}
```

### 执行关节运动
```json
// 请求
{
  "type": "move_j",
  "data": {
    "points": [0, 0, 0, 0, 0, 0],
    "raw_acs_points": [0, 0, 0, 0, 0, 0],
    "speed": 50.0,
    "acc": 50.0,
    "radius": 50.0,
    "timeout": 30.0
  }
}

// 响应
{
  "status": "success",
  "message": "关节运动完成",
  "data": {
    "moved": true
  }
}
```

## 注意事项

1. 所有命令都需要在机器人连接并使能后才能执行
2. 夹爪操作需要先连接夹爪设备
3. 建议在发送命令前检查设备连接状态
4. 所有数值参数都有合理的范围限制
5. 超时时间参数用于防止长时间阻塞
