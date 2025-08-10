# 第三章 可使用接口（续）

## 3.9 力控控制指令

### 3.9.1 HRIF_SetForceControlState
描述：设置力控状态，执行命令后机器人跳转到运动状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nState：力控状态，int，0/1
    - 0：关闭力控
    - 1：开启力控
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义设置状态
nState = 1
# 设置力控状态
nRet = cps.HRIF_SetForceControlState(0,0,nState)
```

### 3.9.2 HRIF_ReadForceControlState
描述：读取当前力控状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list，传入空列表，result = [ ]
- 输出变量：
  - result[0]：力控状态，string，0~3
    - 0：关闭状态
    - 1：开力控探寻状态
    - 2：力控探寻完成状态
    - 3：力控自由驱动状态
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义返回值空列表
result = [ ]
# 读取力控状态
nRet = cps.HRIF_ReadForceControlState(0,0,result)
# 读取到的力控状态
nState = int(result[0])
```

### 3.9.3 HRIF_SetForceToolCoordinateMotion
描述：设置力控坐标系方向为Tool坐标方向模式。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nMode：模式，int，0/1
    - 0：关闭
    - 1：开启
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义设置状态
mode = 1
# 设置力控坐标系状态
nRet = cps.HRIF_SetForceToolCoordinateMotion(0,0,nState)
```

### 3.9.4 HRIF_ForceControlInterrupt
描述：暂停力控运动，仅暂停力控功能，不暂停运动和脚本。（此接口功能已屏蔽）
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置力控暂停状态
nRet = cps.HRIF_ForceControlInterrupt(0,0)
```

### 3.9.5 HRIF_ForceControlContinue
描述：继续力控运动，仅继续力控运动功能，不继续运动和脚本。（此接口功能已屏蔽）
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置力控继续运动
nRet = cps.HRIF_ForceControlContinue(0,0)
```

### 3.9.6 HRIF_SetForceZero
描述：力控清零，在原有数据的基础上重新标定力传感器。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 清零力控数据
nRet = cps.HRIF_SetForceZero(0,0)
```

### 3.9.7 HRIF_SetMaxSearchVelocities
描述：设置力控探寻的最大速度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dMaxLinearVelocity：直线速度，float，>0
  - dMaxAngularVelocity：姿态角速度，float，>0
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置力控探寻直线速度
dMaxLinearVelocity = 100
# 设置力控探寻姿态角速度
dMaxAngularVelocity = 50
# 设置力控探寻速度
nRet = cps.HRIF_SetMaxSearchVelocities(0,0,dMaxLinearVelocity, dMaxAngularVelocity)
```

### 3.9.8 HRIF_SetControlFreedom
描述：设置力控探寻自由度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - freedom[0-5]：各方向自由度，list，0/1
    - 各轴探寻自由度开关：
    - 0：关闭
    - 1：开启
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义力控自由度状态
freedom = [0, 0, 0, 0, 0, 0]
# 设置力控自由度状态
nRet = cps.HRIF_SetControlFreedom (0,0,freedom)
```

### 3.9.9 HRIF_SetForceControlStrategy
描述：设置力控控制策略。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nState：控制策略，int，0~2
    - 0：恒力模式
    - 1：柔顺模式
    - 2：柔顺越障模式
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义力控策略
nState = 1
# 设置力控策略为恒力模式
nRet = cps.HRIF_SetForceControlStrategy(0,0,nState)
```

### 3.9.10 HRIF_SetFreeDrivePositionAndOrientation
描述：设置力传感器中心相对于法兰盘的安装位置和姿态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：迪卡尔坐标，float
    - 力传感器相对于法兰盘安装位置和姿态：
    - dX：X 坐标，单位[mm]
    - dY：Y 坐标，单位[mm]
    - dZ：Z 坐标，单位[mm]
    - dRx：Rx坐标，单位[°]
    - dRy：Ry坐标，单位[°]
    - dRz：Rz坐标，单位[°]
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义力传感器安装位置和姿态
dPCS = [0, 0, 0, 0, 0, 0]
# 设置力传感器的安装位置和姿态
nRet = cps.HRIF_SetFreeDrivePositionAndOrientation(0,0,dPCS)
```

### 3.9.11 HRIF_SetPIDControlParams
描述：设置力控探寻 PID 参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dFp：PID 参数 fP，float
  - dFi：PID 参数 fI，float
  - dFd：PID 参数 fD，float
  - dTp：PID 参数 tP，float
  - dTi：PID 参数 tI，float
  - dTd：PID 参数 tD，float
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置PID参数
dFp = 1.0 dFi= 0.1 dFd = 0
dTp = 1.0 dTi = 0.1 dTd = 0
# 设置PID参数
nRet = cps.HRIF_SetPIDControlParams(0,0,dFp, dFi, dFd, dTp, dTi, dTd)
```

### 3.9.12 HRIF_SetMassParams
描述：设置惯量控制参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：惯量控制参数，float
    - 惯量控制参数：
    - dX：X 方向
    - dY：Y 方向
    - dZ：Z 方向
    - dRx：Rx方向
    - dRy：Ry方向
    - dRz：Rz方向
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置惯量控制参数
Mass = [0, 0, 0, 0, 0, 0]
nRet = cps.HRIF_SetMassParams(0,0,Mass)
```

### 3.9.13 HRIF_SetDampParams
描述：设置阻尼(b)控制参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：阻尼控制参数，float
    - 阻尼控制参数：
    - dX：X 方向
    - dY：Y 方向
    - dZ：Z 方向
    - dRx：Rx方向
    - dRy：Ry方向
    - dRz：Rz方向
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置阻尼参数
Damp = [800, 800, 800, 40, 40, 40]
# 设置阻尼参数
nRet = cps.HRIF_SetDampParams(0,0,Damp)
```

### 3.9.14 HRIF_SetStiffParams
描述：设置刚度(k)控制参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：刚度控制参数，float
    - 刚度控制参数：
    - dX：X 方向
    - dY：Y 方向
    - dZ：Z 方向
    - dRx：Rx方向
    - dRy：Ry方向
    - dRz：Rz方向
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置刚度参数
Stiff = [1000, 1000, 1000, 100, 100, 100]
# 设置刚度参数
nRet = cps.HRIF_SetStiffParams(0,0,Stiff)
```

### 3.9.15 HRIF_SetForceControlGoal
描述：设置力控目标力。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：力控目标力，float
    - 力控目标力：
    - dX：X 方向，单位[N]
    - dY：Y 方向，单位[N]
    - dZ：Z 方向，单位[N]
    - dRx：Rx方向，单位[NM]
    - dRy：Ry方向，单位[NM]
    - dRz：Rz方向，单位[NM]
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置力控目标力
Goal = [0, 0,10, 0, 0, 0]
# 设置力控目标力Z方向10N
nRet = cps.HRIF_SetForceControlGoal(0,0,Goal)
```

### 3.9.16 HRIF_SetControlGoal
描述：设置力控目标力和目标距离(0,0,力控目标距离暂未启用)。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dWrench_X-dWrench_Rz：力控目标力，float
    - 力控目标力：
    - dWrenchX：X 方向，单位[N]
    - dWrenchY：Y 方向，单位[N]
    - dWrenchZ：Z 方向，单位[N]
    - dWrenchRx：Rx方向，单位[NM]
    - dWrenchRy：Ry方向，单位[NM]
    - dWrenchRz：Rz方向，单位[NM]
  - dDistance_X-dDistance_Rz：力控目标距离，float
    - 力控目标距离：
    - dDistanceX：X 方向，单位[N]
    - dDistanceY：Y 方向，单位[N]
    - dDistanceZ：Z 方向，单位[N]
    - dDistanceRx：Rx方向，单位[NM]
    - dDistanceRy：Ry方向，单位[NM]
    - dDistanceRz：Rz方向，单位[NM]
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置力控目标力
Wrench = [0, 0,10, 0, 0, 0]
# 设置力控目标距离
Distance = [0, 0, 0, 0, 0, 0]
# 设置力控目标力Z方向10N
nRet = cps.HRIF_SetControlGoal (0,0,Wrench, Distance)
```

### 3.9.17 HRIF_SetForceDataLimit
描述：设置力控限制范围，力传感器超过此范围后控制器断电。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dMax_X-dMax_Rz：力最大范围，float
    - 力最大范围：
    - dMax_X：X 方向，单位[N]
    - dMax_Y：Y 方向，单位[N]
    - dMax_Z：Z 方向，单位[N]
    - dMax_Rx：Rx方向，单位[NM]
    - dMax_Ry：Ry方向，单位[NM]
    - dMax_Rz：Rz方向，单位[NM]
  - dMin_X-dMin_Rz：力最小范围，float
    - 力最小范围：
    - dMin_X：X 方向，单位[N]
    - dMin_Y：Y 方向，单位[N]
    - dMin_Z：Z 方向，单位[N]
    - dMin_Rx：Rx方向，单位[NM]
    - dMin_Ry：Ry方向，单位[NM]
    - dMin_Rz：Rz方向，单位[NM]
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置力最大值
dMax = [500, 500, 500, 500, 500, 500]
# 设置力最小值
dMin = [-500, -500, -500, -500, -500, -500]
# 设置力传感器数据限制范围
nRet = cps.HRIF_SetForceDataLimit(0,0, dMax, dMin)
```

### 3.9.18 HRIF_SetForceDistanceLimit
描述：设置力控形变范围。（此接口功能已弃用）
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dAllowDistance：允许最大距离，float
  - dStrengthLevel：位置与边界设置偏离距离的幂次项，float，2/3
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置允许最大距离
dAllowDistance = 10
# 设置位置与边界设置偏离距离的幂次项
dStrengthLevel = 2
# 设置力控形变范围
nRet = cps.HRIF_SetForceDistanceLimit(0,0, dAllowDistance, dStrengthLevel)
```

### 3.9.19 HRIF_SetForceFreeDriveMode
描述：设置开启或者关闭力控自由驱动模式。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nMode：是否开启，int，0/1
    - 0：关闭
    - 1：开启
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 设置开启力控自由驱动
nMode = 1
# 设置开启力控自由驱动
nRet = cps.HRIF_SetForceFreeDriveMode(0,0,nMode )
```

### 3.9.20 HRIF_SetFTFreeDriveSpeedMode
描述：设置自由驱动的速度模式。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nMode：速度模式，int，0~3
    - 0：正常速度模式
    - 1：慢速模式
    - 2：快速模式
    - 3：焊接模式
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
nMode = 3
# 设置速度模式为焊接模式
nRet = cps.HRIF_SetFTFreeDriveSpeedMode(0,0,nMode)
```

### 3.9.21 HRIF_ReadFTFreeDriveSpeedMode
描述：读取设定后的自由驱动速度模式。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list，传入空列表，result = [ ]
- 输出变量：
  - result[0]：速度模式，string，0~3
    - 0：正常速度模式
    - 1：慢速模式
    - 2：快速模式
    - 3：焊接模式
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
result = 0
# 读取设定的自由驱动速度模式
nRet = cps.HRIF_ReadFTFreeDriveSpeedMode(0,0, result)
mode = int(result[0])
```

### 3.9.22 HRIF_ReadFTCabData
描述：读取标定后的力传感器数据。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list，传入空列表，result = [ ]
- 输出变量：
  - result[0]-result[5]：标定后的力传感器数据，string
    - dX：X 坐标，单位[N]
    - dY：Y 坐标，单位[N]
    - dZ：Z 坐标，单位[N]
    - dRx：Rx坐标，单位[NM]
    - dRy：Ry坐标，单位[NM]
    - dRz：Rz坐标，单位[NM]
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义返回值空列表
result = [ ]
# 读取力传感器数据
nRet = cps.HRIF_ReadFTCabData(0,0,result)
# 读取到力传感器数据
dX = float(result[0]) dY = float(result[1]) dZ = float(result[2])
dRx = float(result[3]) dRy = float(result[4]) dRz = float(result[5])
```

### 3.9.23 HRIF_SetFreeDriveMotionFreedom
描述：设置力控自由驱动末端自由度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - nX-nRz：各方向自由度，int，0/1
    - 各方向探寻自由度开关：
    - 0：关闭
    - 1：开启
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义力控自由驱动自由度状态,nX-nRz
df = [0, 0, 1, 0, 0, 0]
# 设置力控自由驱动自由度状态
nRet = cps.HRIF_SetFreeDriveMotionFreedom(0,df)
```

### 3.9.24 HRIF_SetFTFreeFactor
描述：设置平移柔顺度和旋转柔顺度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - dLinear：平移柔顺度，float，0~100
  - dAngular：旋转柔顺度，float，0~100
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义平移柔顺度
dLinear = 50
# 定义旋转柔顺度
dAngular = 50
# 设置力控自由驱动平移柔顺度和旋转柔顺度
nRet = cps.HRIF_SetFTFreeFactor(0, dLinear, dAngular)
```

### 3.9.25 HRIF_SetTangentForceBounds
描述：设置X/Y方向切向力最大值、最小值和最大上抬速度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dMax：最大值，float，0~500
  - dMin：最小值，float，0~500
  - dVel：抬升速度，float，0~100
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义X/Y方向切向力最大值
dMax = 25
# 定义X/Y方向切向力最小值
dMin = 15
# 定义越障上抬最大速度
dVel = 30
# 设置X/Y方向切向力最大值、最小值和上抬最大速度
nRet = cps.HRIF_SetTangentForceBounds(0,0, dMax, dMin, dVel)
```

### 3.9.26 HRIF_SetFreeDriveCompensateForce
描述：设置FreeDrive模式下的定向补偿力大小及矢量方向。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dForce：补偿力，float，0~500
  - dX-dZ：力方向向量，float
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义补偿力大小
dForce = 10
# 定义补偿力在基坐标系下的矢量方向
dX = 0
dY = 0
dZ = 0
# 设置FreeDrive模式下的定向补偿力大小和矢量方向[x,y,z]
nRet = cps.HRIF_SetFreeDriveCompensateForce(0,0,dForce,dX,dY,dZ);
```

### 3.9.27 HRIF_SetFTWrenchThresholds
描述：设置力控自由驱动启动阈值（力与力矩）。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dForceThreshold：力，float，0~100
  - dTorqueThreshold：力矩，float，0~10
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义力阈值
dForceThreshold=10
# 定义力矩阈值
dTorqueThreshold=10
# 设置力控自由驱动启动阈值（力与力矩）
nRet = cps.HRIF_SetFTWrenchThresholds(0,0,dForceThreshold,dTorqueThreshold)
```

### 3.9.28 HRIF_SetMaxFreeDriveVel
描述：设置力控自由驱动最大直线速度及姿态角速度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dMaxLinearVelocity：直线速度，float，1~1000
  - dMaxAngularVelocity：姿态角速度，float，1~50
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义自由驱动最大直线速度
dMaxLinearVelocity=100
# 定义自由驱动最大角速度
dMaxAngularVelocity=10
# 设置力控自由驱动最大直线速度及姿态角速度
nRet = cps.HRIF_SetMaxFreeDriveVel(0,0,dMaxLinearVelocity,dMaxAngularVelocity)
```

### 3.9.29 HRIF_ReadFTMotionFreedom
描述：读取力控自由驱动的末端自由度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list，传入空列表，result = [ ]
- 输出变量：
  - result[0-5]：各方向自由度，string，0/1
    - 各方向探寻自由度开关：
    - 0：关闭
    - 1：开启
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
result = []
# 读取力控自由驱动的末端自由度
nRet = cps.HRIF_ReadFTMotionFreedom(0,0,result)
nx = int(result[0])
ny = int(result[1])
nz = int(result[2])
nRx = int(result[3])
nRy = int(result[4])
nRz = int(result[5])
```

### 3.9.30 HRIF_SetMaxSearchDistance
描述：设置各自由度力控探寻最大距离。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - Dis_X：X方向探寻边界，float，-X方向探寻边界，单位：mm
  - Dis_Y：Y方向探寻边界，float，-Y方向探寻边界，单位：mm
  - Dis_Z：Z方向探寻边界，float，-Z方向探寻边界，单位：mm
  - Dis_RX：RX方向探寻边界，float，-RX方向探寻边界，单位：°
  - Dis_RY：RY方向探寻边界，float，-RY方向探寻边界，单位：°
  - Dis_RZ：RZ方向探寻边界，float，-RZ方向探寻边界，单位：°
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义各自由度力控探寻最大距离
Dis_X = 300
Dis_Y = 300
Dis_Z = 300
Dis_RX = 20
Dis_RY = 20
Dis_RZ = 20
# 设置各自由度力控探寻最大距离
nRet = cps.HRIF_SetMaxSearchDistance(0,0,Dis_X,Dis_Y,Dis_Z,Dis_RX,Dis_RY,Dis_RZ)
```

### 3.9.31 HRIF_SetSteadyContactDeviationRange
描述：设置恒力控稳定阶段边界。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - Pos_X~Dis_RZ：正方向边界，float，>0
  - Neg_X ~ Neg_RZ：负方向边界，float，<0
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
Pos_X = 100
Pos_Y = 100
Pos_Z = 100
Pos_RX = 20
Pos_RY = 20
Pos_RZ = 20
Neg_X = -100
Neg_Y = -100
Neg_Z = -100
Neg_RX = -20
Neg_RY = -2
Neg_RZ = -20
# 设置恒力控稳定阶段边界
nRet = cps.HRIF_SetSteadyContactDeviationRange(0,0,Pos_X,Pos_Y,Pos_Z,Pos_RX,Pos_RY,Pos_RZ,
Neg_X,Neg_Y,Neg_Z,Neg_RX,Neg_RY,Neg_RZ)
```

### 3.9.32 HRIF_SetDepthThresholdForDampingArea
描述：设置虚拟墙开始产生阻尼时的距离阈值。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dDepth：阈值大小，float
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义阈值大小
dDepth = 100
# 设置虚拟墙开始产生阻尼时的距离阈值
nRet = cps.HRIF_SetDepthThresholdForDampingArea(0, 0, dDepth)
```

### 3.9.33 HRIF_AddSafePlane
描述：添加虚拟墙平面；虚拟墙平面即安全平面，只是相应的功能不同，如果添加的安全平面名称已经存在，会报20006错误；最后一个参数为是否激活，如果不激活，不会检查UCS 是否存在；
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - Name：平面名称，string
  - UcsName：用户坐标名称，string
  - Mode：安全模式，int，0/1
  - Display：显示，int，0/1
  - Switch：启用，int，0/1
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义平面名称
Name = "planel"
# 定义使用的用户坐标名称
UcsName = "Plane_1"
# 定义安全模式
Mode = 0
# 定义是否显示
Display = 0
# 定义是否启用
Switch = 1
# 添加虚拟墙平面
nRet = cps.HRIF_AddSafePlane(0, 0, Name, UcsName , Mode, Display, Switch)
```

### 3.9.34 HRIF_UpdateSafePlane
描述：修改更新虚拟墙平面属性；虚拟墙平面即安全平面，只是相应的功能不同；最后一个参数为是否激活，如果不激活，不会检查UCS 是否存在；
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - Name：平面名称，string
  - UcsName：用户坐标名称，string
  - Mode：安全模式，int，0/1
  - Display：显示，int，0/1
  - Switch：启用，int，0/1
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义平面名称
Name = "planel"
# 定义使用的用户坐标名称
UcsName = "Plane_1"
# 定义安全模式
Mode = 0
# 定义是否显示
Display = 0
# 定义是否启用
Switch = 1
# 修改虚拟墙平面
nRet = cps.HRIF_UpdateSafePlane(0, 0, Name, UcsName , Mode, Display, Switch)
```

### 3.9.35 HRIF_DelSafePlane
描述：删除虚拟墙平面；虚拟墙平面即安全平面，只是相应的功能不同，如果指定的安全平面名称不存在，报20006错误；
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - Name：平面名称，string
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义要删除的平面名称
Name = "planel"
# 删除虚拟墙平面
nRet = cps.HRIF_DelSafePlane(0, 0, Name )
```

### 3.9.36 HRIF_ReadSafePlaneList
描述：返回结果为所有安全平面的名字清单，虚拟墙平面即安全平面，只是相应的功能不同；
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
- 输出变量：
  - result：所有虚拟墙平面名称，list[string]
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
# 定义接收所有虚拟墙平面名称的列表
result = []
# 读取当前所有的虚拟墙平面名称
nRet = cps.HRIF_ReadSafePlaneList(0, 0, result )
```

### 3.9.37 HRIF_ReadSafePlane
描述：返回结果为指定安全平面的详细参数；虚拟墙平面即安全平面，只是相应的功能不同，如果指定的安全平面不存在，返回结果为空；
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - Name：平面名称，string
- 输出变量：
  - result[0]：用户坐标名称，string
  - result[1]：安全模式，string，0/1
  - result[2]：显示，string，0/1
  - result[3]：启用，string，0/1
- 返回值：nRet，int，>0 的整型值
  - nRet = 0：返回函数调用成功
  - nRet >0：返回调用失败的错误码

示例：
```python
result = []
# 定义要读取的平面名称
BorderName = "planel"
# 读取目标虚拟墙平面的详细信息
nRet = cps.HRIF_ReadSafePlane(0, 0, BorderName,result)
```

## 3.10 通用运动类控制指令

### 3.10.1 HRIF_MoveRelJ
描述：关节相对运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nAxis：轴 ID，int，0~5
  - nDirection：方向，int，0/1
  - dDistance：运动距离，float
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义轴ID
nAxis = 1
# 定义运动方向
nDirection = 1
# 定义运动距离
nDistance = 1
# 执行相对关节运动
nRet = cps.HRIF_MoveRelJ(0,0, nAxis, nDirection, nDistance)
```

### 3.10.2 HRIF_MoveRelL
描述：空间相对运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nAxis：轴 ID，int，0~5
  - nDirection：方向，int，0/1
  - dDistance：运动距离，float
  - nToolMotion：运动坐标类型，int，0/1
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义轴ID
nAxis = 1
# 定义运动方向
nDirection = 1
# 定义运动距离
nDistance= 1
# 定义运动坐标类型
nToolMotion = 1
# 执行相对空间运动
nRet = cps.HRIF_MoveRelL(0,0, nAxis, nDirection, nDistance, nToolMotion)
```

### 3.10.3 HRIF_WayPointRel
描述：路点相对运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nType：运动类型，int，>0
  - nPointList：是否使用列表点位，int，>1
  - Pos：空间位置，list
  - rawACT：关节位置，list
  - nrelMoveType：相对运动类型，int
  - nAxisMask：各轴是否运动，list
  - nTarget：运动距离，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nIsUseJoint：是否使用关节角度，int
  - nIsSeek：是否检测DI 停止，int，0/1
  - nIOBit：检测的 DI 索引，int，0~7
  - nIOState：检测的 DI 状态，int，0/1
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义运动类型
nType = 0;
# 定义是否使用点位列表的点位
nPointList= 0;
# 定义空间目标位置
Pos = [0, 0, 0, 0, 0, 0]
# 定义关节目标位置
rawACT = [0, 0, 0, 0, 0, 0]
# 定义相对运动类型
nrelMoveType= 1;
# 定义各轴各方向是否运动
nAxisMask = [1, 1, 0, 0, 0, 0]
# 定义运动距离
nTarget = [10, -10, 0, 0, 0, 0]
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义是否使用关节角度
nIsUseJoint = 0
# 定义是否使用检测DI停止
nIsSeek = 0
# 定义检测的DI索引
nIOBit = 0
# 定义检测的DI状态
nIOState = 0
# 定义路点ID
strCmdID = "0"
# 路点相对运动
nRet = cps.HRIF_WayPointRel(0,0,nType, nPointList, Pos, rawACT, nrelMoveType, nAxisMask, nTarget,
sTcpName, sUcsName, dVelocity, dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
```

### 3.10.4 HRIF_IsMotionDone
描述：判断机器人是否处于运动状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list，传入空列表，result = [ ]
- 输出变量：
  - result[0]：返回值，bool，False/True
    - False：运动未完成，处于运动状态
    - True：运动完成，处于准备就绪状态
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义返回值空列表
result = [ ]
# 判断机器人是否处于运动状态
nRet = cps.HRIF_IsMotionDone(0,0,result)
# 机器人处于运动状态
result[0] = False
# 机器人不处于运动状态
result[0] =True
```

### 3.10.5 HRIF_IsBlendingDone
描述：判断路点是否运动完成。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list，传入空列表，result = [ ]
- 输出变量：
  - result[0]：返回值，bool，False/True
    - False：运动未完成，处于运动状态
    - True：运动完成，处于准备就绪状态
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义返回值空列表
result = [ ]
# 判断路点是否运动完成
nRet = cps.HRIF_IsBlendingDone(0,0,result)
# 路点运动未完成
result[0] = False
# 路点运动完成
result[0] =True
```

### 3.10.6 HRIF_WayPointEx
描述：路点运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nMoveType：运动类型，int，0/1
  - dX-dRz：空间目标位置，float
  - dJ1-dJ6：关节目标位置，float
  - dTcp_X-dTcp_Rz：工具坐标值，float
  - dUcs_X-dUcs_Rz：用户坐标值，float
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nIsUseJoint：是否使用关节坐标，int，0/1
  - nIsSeek：是否检测DI 停止，int，0/1
  - nIOBit：检测的 DI 索引，int，0-7
  - nIOState：检测的 DI 状态，int，0/1
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义运动类型
nMoveType = 0
# 定义空间目标位置
Point= [500, 500, 500, 500, 500, 500]
# 定义关节目标位置
RawACSpoints = [0, 0, 0, 0, 0, 0]
# 定义工具坐标变量
Tcp = [0, 0, 0, 0, 0, 0]
# 定义用户坐标变量
Ucs = [0, 0, 0, 0, 0, 0]
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义是否使用关节角度
nIsUseJoint = 1
# 定义是否使用检测DI停止
nIsSeek = 0
# 定义检测的DI索引
nIOBit = 0
# 定义检测的DI状态
nIOState = 0
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet = cps.HRIF_WayPointEx(0,0,nMoveType , Point, RawACSpoints, Tcp, Ucs, dVelocity, dAcc, dRadius,
nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
```

### 3.10.7 HRIF_WayPoint
描述：路点运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nMoveType：运动类型，int，0/1
  - dX-dRz：空间目标位置，float
  - dJ1-dJ6：关节目标位置，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nIsUseJoint：是否使用关节坐标，int，0/1
  - nIsSeek：是否检测DI 停止，int，0/1
  - nIOBit：检测的 DI 索引，int，0~7
  - nIOState：检测的 DI 状态，int，0/1
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义运动类型
nMoveType = 0
# 定义空间目标位置
Point = [0, 0, 0, 0, 0, 0]
# 定义关节目标位置
rawACS = [0, 0, 0, 0, 0, 0]
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义是否使用关节角度
nIsUseJoint= 1
# 定义是否使用检测DI停止
nIsSeek = 0
# 定义检测的DI索引
nIOBit = 0
# 定义检测的DI状态
nIOState = 0
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet = cps.HRIF_WayPoint(0,0,nMoveType , Point, rawACS, sTcpName , sUcsName, dVelocity, dAcc,
dRadius,
nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
```

### 3.10.8 HRIF_WayPoint2
描述：路点运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nMoveType：运动类型，int，0/1/2
  - dEndPos_X-dEndPos_Rz：空间目标位置，float
  - dAuxPos_X-dAuxPos_Rz：空间目标位置，float
  - dJ1-dJ6：关节目标位置，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nIsUseJoint：是否使用关节坐标，int，0/1
  - nIsSeek：是否检测DI 停止，int，0/1
  - nIOBit：检测的 DI 索引，int，0~7
  - nIOState：检测的 DI 状态，int，0/1
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义运动类型
nMoveType = 0
# 定义空间目标位置
EndPos = [420, 0, 445, 180, 0, 0, 180]
# 定义空间目标位置
AuxPos = [420, 0, 445, 180, 0, 0, 180]
# 定义关节目标位置
AcsPose = [0, 0, 90, 0, 90, 0]
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义是否使用关节角度
nIsUseJoint= 1
# 定义是否使用检测DI停止
nIsSeek = 0
# 定义检测的DI索引
nIOBit = 0
# 定义检测的DI状态
nIOState = 0
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet = cps.HRIF_WayPoint2(0,0,nMoveType ,EndPos, AuxPos, AcsPose, sTcpName , sUcsName, dVelocity,
dAcc, dRadius, nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
```

### 3.10.9 HRIF_MoveJ
描述：关节运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：空间目标位置，float
  - dJ1-dJ6：关节目标位置，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nIsUseJoint：是否使用关节坐标，int，0/1
  - nIsSeek：是否检测DI 停止，int，0/1
  - nIOBit：检测的 DI 索引，int，0~7
  - nIOState：检测的 DI 状态，int，0/1
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义空间目标位置
Point = [ 0, 0, 90, 0, 90, 0]
# 定义关节目标位置
RawACSpoints = [ 0, 0, 90, 0, 90, 0]
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义是否使用关节角度
nIsUseJoint= 1
# 定义是否使用检测DI停止
nIsSeek = 0
# 定义检测的DI索引
nIOBit = 0
# 定义检测的DI状态
nIOState = 0
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet  =  cps.HRIF_MoveJ(0,0,  Point,  RawACSpoints,  sTcpName  ,  sUcsName,  dVelocity,  dAcc,
dRadius,nIsUseJoint, nIsSeek, nIOBit, nIOState, strCmdID)
```

### 3.10.10 HRIF_MoveL
描述：直线轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX-dRz：空间目标位置，float
  - dJ1-dJ6：关节参考位置，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nIsSeek：是否检测DI 停止，int，0/1
  - nIOBit：检测的 DI 索引，int，0~7
  - nIOState：检测的 DI 状态，int，0/1
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义空间目标位置
Point = [ 420, 0, 445, 180, 0, 180]
# 定义关节目标位置
RawACSpoints = [ 0, 0, 90, 0, 90, 0]
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义是否使用检测DI停止
nIsSeek = 0
# 定义检测的DI索引
nIOBit = 0
# 定义检测的DI状态
nIOState = 0
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet = cps.HRIF_MoveL(0,0, Point, RawACSpoints, sTcpName, sUcsName, dVelocity, dAcc, dRadius,nIsSeek,
nIOBit, nIOState, strCmdID)
```

### 3.10.11 HRIF_MoveC
描述：圆弧轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dStartPoint：圆弧起始点位置，list[float]
  - dAuxPoint：圆弧经过点位置，list[float]
  - dEndPoint：圆弧结束点位置，list[float]
  - nFixedPosure：是否固定姿态，int，0/1
  - nMoveCType：圆弧类型，int，0/1
  - dRadLen：弧长，float
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 圆弧起始点位置
dStartPoint = [420, 0, 445, 180, 0, 180]
# 圆弧经过点位置
dAuxPoint  = [420, 50, 445, 180, 0, 180]
# 圆弧结束点位置
dEndPoint = [470, 0, 445, 180, 0, 180]
# 是否固定姿态
nFixedPosure = 0
# 圆弧类型
nMoveCType = 0
# 整圆圈数
dRadLen = 1
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet = cps.HRIF_MoveC(0,0,dStartPoint , dAuxPoint, dEndPoint,
nFixedPosure, nMoveCType, dRadLen, dVelocity, dAcc, dRadius,sTcpName , sUcsName, strCmdID)
```

### 3.10.12 HRIF_MoveZ
描述：Z型轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dStartPos：Z型起始点位置，float
  - dEndPos：Z型结束点位置，float
  - dPlanePos：轨迹确定平面点位置，float
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dWidth：宽度，float
  - dDensity：密度，float
  - nEnableDensity：是否使用密度，int
  - nEnablePlane：是否使用平面点，int
  - nEnableWaiTime：是否开启转折点等待时间，int
  - nPosiTime：正向转折点等待时间，int
  - nNegaTime：负向转折点等待时间，int
  - dRadius：过渡半径，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 起始点位置
dStartPos = [420, 0, 445, 180, 0, 180]
# 结束点位置
dEndPos = [420, 100, 445, 180, 0, 180]
# 确定轨迹平面点位置
dPlanePos = [470, 50, 445, 180, 0, 180]
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 2500
# 宽度
dWidth = 50
# 密度
dDensity = 10
# 使用密度
nEnableDensity = 1
# 使用平面点
nEnablePlane = 1
# 是否在转折点等待-不等待
nEnableWaiTime = 0
# 正向转折点等待时间
nPosiTime = 0
# 负向转折点等待时间
nNegaTime = 0
# 定义过渡半径
dRadius = 5
# 定义工具坐标变量
sTcpName =  "TCP "
# 定义用户坐标变量
sUcsName = "Base"
# 定义路点ID
strCmdID = "0"
# 执行路点运动
nRet  =  cps.HRIF_MoveZ(0,0,dStartPos,  dEndPos,  dPlanePos,  dVelocity,  dAcc,  dWidth,  dDensity,
nEnableDensity, nEnablePlane, nEnableWaiTime, nPosiTime, nNegaTime, dRadius, sTcpName, sUcsName,
strCmdID)
```

### 3.10.13 HRIF_MoveE
描述：椭圆型轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dP1-dP5：示教位置，list[float]
  - nOrientMode：运动模式，int，0/1
  - nMoveType：运动类型，int，0/1
  - dArcLength：弧长，float
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 示教点1
dP1 = [420,0,445,180,0,180]
# 示教点2
dP2 = [460,0,445,180,0,180]
# 示教点3
dP3 = [480,10,445,180,0,180]
# 示教点4
dP4 = [460,20,445,180,0,180]
# 示教点5
dP5 = [420,20,445,180,0,180]
# 运动模式
nOrientMode = 0
# 运动类型
nMoveType = 1
# 弧长
dArcLength = 360
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 2500
# 定义过渡半径
dRadius = 5
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义路点ID
strCmdID = "0"
# 执行椭圆运动
nRet = cps.HRIF_MoveE(0,0,dP1, dP2, dP3,dP4, dP5,
nOrientMode,nMoveType,dArcLength,dVelocity,dAcc,dRadius, sTcpName, sUcsName, strCmdID)
```

### 3.10.14 HRIF_MoveS
描述：阿基米德螺旋线运动，初始半径为固定1mm。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dSpiralIncrement：增量半径，float，>0
  - dSpiralDiameter：结束半径，float，>1
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义增量半径
dSpiralIncrement = 1
# 定义结束半径
dSpiralDiameter = 5
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义路点ID
strCmdID = "0"
# 执行螺旋轨迹运动
nRet= cps.HRIF_MoveS(0,0, dSpiralIncrement, dSpiralDiameter, dVelocity, dAcc, dRadius, sTcpName,
sUcsName, sCmdID)
```

### 3.10.15 HRIF_MoveLinearWeave
描述：直线摆焊运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - StartPoint：开始点位置，list[float]
  - EndPoint：结束点位置，list[float]
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - dAmplitude：宽度，float
  - dInterValDistance：间距，float
  - nWeaveFrameType：选择方式，int，0/1
  - dElevation：仰角，float
  - dAzimuth：方向角，float
  - dCentreRise：中心隆起量，float
  - nEnableWaitTime：是否等待，int，0/1
  - nPosiTime：正等待时间，float
  - nNegaTime：负等待时间，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义开始点位置
StartPoint = [420, 0, 445, 180, 0, 180]
# 定义结束点位置
EndPoint = [470, 0, 445, 180, 0, 180]
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义宽度
dAmplitude = 10
# 定义间距
dInterValDistance = 10
# 定义方式
nWeaveFrameType = 0
# 定义仰角
dElevation = 10
# 定义方向角
dAzimuth = 10
# 定义中心隆起量
dCentreRise = 5
# 定义是否等待
nEnableWaitTime = 0
# 定义正向转折点等待时间
nPosiTime = 10
# 定义负向转折点等待时间
nNegaTime = 50
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义路点ID
sCmdID = "0"
# 执行直线摆焊运动
nRet=cps.HRIF_MoveLinearWeave(0, 0, StartPoint, EndPoint, dVelocity, dAcc, dRadius, dAmplitude,
dInterValDistance, nWeaveFrameType, dElevation, dAzimuth, dCentreRise, nEnableWaitTime, nPosiTime,
nNegaTime, sTcpName, sUcsName, sCmdID)
```

### 3.10.16 HRIF_MoveCircularWeave
描述：圆弧摆焊运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - StartPoint：开始点位置，list[float]
  - AuxPoint：经过点位置，list[float]
  - EndPoint：结束点位置，list[float]
  - dVelocity：速度，float
  - dAcc：加速度，float
  - dRadius：过渡半径，float
  - nOrientMode：是否使用固定姿态，int，0/1
  - nMoveWhole：轨迹，int，0/1
  - nMoveWholeLen：圈数，int
  - dAmplitude：宽度，float
  - dInterValDistance：间距，float
  - nWeaveFrameType：选择方式，int，0/1
  - dElevation：仰角，float
  - dAzimuth：方向角，float
  - dCentreRise：中心隆起量，float
  - nEnableWaitTime：是否等待，int，0/1
  - nPosiTime：正等待时间，float
  - nNegaTime：负等待时间，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
  - strCmdID：命令 ID，string
- 返回值：nRet，int，>0 的整型值
  - nRet=0：返回函数调用成功
  - nRet>0：返回调用失败的错误码

示例：
```python
# 定义开始点位置
StartPoint = [420, 0, 445, 180, 0, 180]
# 定义经过点位置
AuxPoint = [420, 50, 445, 180, 0, 180]
# 定义结束点位置
EndPoint = [470, 0, 445, 180, 0, 180]
# 定义运动速度
dVelocity = 50
# 定义运动加速度
dAcc = 50
# 定义过渡半径
dRadius = 50
# 定义固定姿态
nOrientMode = 0
# 定义轨迹
nMoveWhole = 0
# 定义圈数
nMoveWholeLen = 10
# 定义宽度
dAmplitude = 10
# 定义间距
dInterValDistance = 10
# 定义方式
nWeaveFrameType = 0
# 定义仰角
dElevation = 10
# 定义方向角
dAzimuth = 10
# 定义中心隆起量
dCentreRise = 5
# 定义是否等待
nEnableWaitTime = 0
# 定义正向转折点等待时间
nPosiTime = 10
# 定义负向转折点等待时间
nNegaTime = 50
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 定义路点ID
sCmdID = "0"
# 执行圆弧摆焊运动
nRet=cps.HRIF_MoveCircularWeave(0, 0, StartPoint, AuxPoint, EndPoint, dVelocity, dAcc, dRadius,
nOrientMode, nMoveWhole, nMoveWholeLen, dAmplitude, dInterValDistance, nWeaveFrameType, dElevation,
dAzimuth, dCentreRise, nEnableWaitTime, nPosiTime, nNegaTime, sTcpName, sUcsName, sCmdID)
