# 第三章 可使用接口 (3.11-3.15节)

## 3.11 连续轨迹运动类控制指令

### 3.11.1 HRIF_StartPushMovePathJ
描述：初始化关节连续轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
  - dSpeedRatio：轨迹运动速度比，float，0~1
  - dRadius：过渡半径，float，>=0
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 速度比
dSpeedRatio = 0.5
# 过渡半径
dRadius = 2
# 初始化关节连续轨迹运动
nRet = cps.HRIF_StartPushMovePathJ(0,0,sTrackName, dSpeedRatio, dRadius)
```

### 3.11.2 HRIF_PushMovePathJ
描述：下发运动轨迹点位。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
  - paramsJ：关节点位，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 目标关节位置
paramsJ = [0,0,90,0,0,0]
# 下发关节点位
nRet = cps.HRIF_PushMovePathJ (0,0,sTrackName, paramsJ)
```

### 3.11.3 HRIF_EndPushMovePathJ
描述：轨迹下发完成并开始计算轨迹。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 下发完成，开始计算轨迹
nRet = cps.HRIF_EndPushMovePathJ(0,0,sTrackName)
```

### 3.11.4 HRIF_MovePathJ
描述：运动指定的轨迹。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 运动轨迹
nRet = cps.HRIF_MovePathJ(0,0,sTrackName)
```

### 3.11.5 HRIF_ReadMovePathJState
描述：读取当前的轨迹状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list
  - sTrackName：轨迹名称，string
- 输出变量：
  - result[0]：轨迹状态，string，0~5
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 定义返回值空列表
result = [ ]
# 轨迹名称
sTrackName = "Path1"
# 读取轨迹状态
nRet = cps.HRIF_ReadMovePathJState(0,0,sTrackName, result)
# 读取到的当前轨迹状态
nState = int(result[0])
```

### 3.11.6 HRIF_UpdateMovePathJName
描述：更新指定轨迹的名称。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹原名称，string
  - sTrackNewName：更新的轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 更新的轨迹名称
sTrackNewName = "Path2"
# 重命名轨迹名称
nRet = cps.HRIF_UpdateMovePathJName(0,0,sTrackName, sTrackNewName)
```

### 3.11.7 HRIF_DelMovePathJ
描述：删除指定轨迹。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 删除轨迹
nRet = cps.HRIF_DelMovePathJ(0,0,sTrackName)
```

### 3.11.8 HRIF_ReadTrackProcess
描述：读取当前的轨迹运动进度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list
- 输出变量：
  - result[0]：轨迹运行进度，string，0~1
  - result[1]：点位索引，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 定义返回值空列表
result = [ ]
# 读取轨迹状态
nRet = cps.HRIF_ReadTrackProcess(0,0,result)
# 轨迹运行进度
dProcess = float(result[0])
# 点位索引
nIndex = int(result[1])
```

### 3.11.9 HRIF_InitMovePathL
描述：初始化空间轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
  - dVelocity：轨迹运动速度，float
  - dAcc：轨迹运动加速度，float
  - dJerk：轨迹运动加加速度，float
  - sTcpName：工具坐标名称，string
  - sUcsName：用户坐标名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 定义运动速度
dVelocity = 100
# 定义运动加速度
dAcc = 2500
# 定义运动加加速度
dJerk = 1000000
# 定义工具坐标变量
sTcpName = "TCP"
# 定义用户坐标变量
sUcsName = "Base"
# 初始化关节连续轨迹运动
nRet = cps.HRIF_InitMovePathL(0,0,sTrackName, dVelocity, dAcc, dJerk, sUcsName, sTcpName)
```

### 3.11.10 HRIF_PushMovePathL
描述：下发运动轨迹点位。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
  - paramPcs：空间点位，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 定义空间目标位置
paramPcs = [420, 0, 445, 180, 0, 180]
# 下发空间目标点位
nRet = cps.HRIF_PushMovePathL(0,0,sTrackName, paramPcs)
```

### 3.11.11 HRIF_PushMovePaths
描述：批量下发轨迹点位，调用一次可下发多个点位数据。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
  - nMoveType：点位类型，int，0/1
  - nPointsSize：点位数量，int
  - sPoints：点位数据，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path1"
# 运动类型
nMoveType = 1
# 点位数量
nPointsSize = 6
sPoints = [420,0,445,180,0,180,420,10,445,180,0,180,420,20,445,180,0,180,
420,30,445,180,0,180,420,40,445,180,0,180,420,50,445,180,0,180]
# 下发空间目标点位
nRet = cps.HRIF_PushMovePaths(0,0,sTrackName, nMoveType, nPointsSize, sPoints)
```

### 3.11.12 HRIF_MovePathL
描述：执行空间坐标轨迹运动。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sTrackName：轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sTrackName = "Path2"
# 开始空间连续轨迹运动
nRet = cps.HRIF_MovePathL(0,0,sTrackName)
```

### 3.11.13 HRIF_MovePathJOL
描述：启动在线实施规划的MovePathJ。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dVel：关节速度，float
  - dAcc：关节加速度，float
  - dTol：过渡参数，float
  - RawACSpoints：关节目标位置，list[float]
  - nIsSetIO：各点是否设置IO，list[int]
  - nEndDOMask：各个需要更改的EndDO按bit标识，list[int]
  - nEndDOVal：各个需要更改的EndDO的目标状态，list[int]
  - nBoxDOMask：各个需要更改的BoxDO按bit标识，list[int]
  - nBoxDOVal：各个需要更改的BoxDO的目标状态，list[int]
  - nBoxCOMask：需要更改的BoxCO按bit标识，list[int]
  - nBoxCOVal：各个需要更改的BoxCO的目标状态，list[int]
  - nBoxAOCH0_Mask：BoxAOCH0是否需要更改的标识，list[int]
  - nBoxAOCH0_Mode：模式，list[int]
  - nBoxAOCH1_Mask：BoxAOCH1是否需要更改的标识，list[int]
  - nBoxAOCH1_Mode：模式，list[int]
  - dbBoxAOCH0_Val：各点对应模拟量值，list[float]
  - dbBoxAOCH1_Val：各点对应模拟量值，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 定义速度
dVel = 15
# 定义加速度
dAcc = 20
# 定义过渡参数
dTol = 2
# 定义各点关节目标位置，6个一组
RawACSpoints = [0,0,90,0,90,0, 0,0,91,0,90,0, 0,0,92,0,90,0]
# 各点是否设置IO
nIsSetIO = [1,1,1]
# 需要更改的各点EndDO
nEndDOMask = [7,7,7]
# 需要更改的各点EndDO的目标状态
nEndDOVal = [2,2,2]
# 需要更改的各点BoxDO
nBoxDOMask = [86,86,86]
# 需要更改的各点BoxDO的目标状态
nBoxDOVal = [255,255,255]
# 需要更改的各点BoxCO
nBoxCOMask = [255,255,255]
# 需要更改的各点BoxCO的目标状态
nBoxCOVal = [169,169,169]
# 各点BoxAOCH0是否需要更改的标识
nBoxAOCH0_Mask = [1,1,1]
# 模式
nBoxAOCH0_Mode = [2,2,2]
# 各点BoxAOCH1是否需要更改的标识
nBoxAOCH1_Mask = [1,1,1]
# 模式
nBoxAOCH1_Mode =  [1,1,1]
# 各点对应模拟量值
dbBoxAOCH0_Val = [6.66,6.66,6.66]
# 各点对应模拟量值
dbBoxAOCH1_Val = [9.99,9.99,9.99]
# 开始运动
nRet = cps.HRIF_MovePathJOL(0,0,dVel, dAcc, dTol, RawACSpoints, nIsSetIO, nEndDOMask, nEndDOVal,
nBoxDOMask,  nBoxDOVal,  nBoxCOMask,  nBoxCOVal,  nBoxAOCH0_Mask,  nBoxAOCH0_Mode,
nBoxAOCH1_Mask, nBoxAOCH1_Mode, dbBoxAOCH0_Val, dbBoxAOCH1_Val)
```

### 3.11.14 HRIF_GetMovePathJOLIndex
描述：获取MovePathJOL运动当前的点位索引号及轨迹运动所有点总数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list
- 输出变量：
  - result[0]：点位索引号，string
  - result[1]：点总数，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
result = []
# 读取点位索引号与总数
nRet = cps.HRIF_GetMovePathJOLIndex(0,0,result)
```

### 3.11.15 HRIF_SetMovePathOverride
描述：设置MovePath速度比，MovePath运动中设置有效。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - MovePathOverride：设置速度比，float，0.01~1
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 速度比
MovePathOverride= 0.01
# 设置MovePath速度比
nRet = cps.HRIF_SetMovePathOverride(0,0,MovePathOverride)
```

### 3.11.16 HRIF_InitPath
描述：初始化轨迹。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nRawDataType：原始点位类型，int，0/1
  - sPathName：轨迹名称，string
  - dSpeedRatio：轨迹运动速度比，float，0.01~1.00
  - dRadius：过渡半径，float，>0
  - dVelocity：轨迹运动速度，float
  - dAcc：轨迹运动加速度，float
  - dJerk：轨迹运动加加速度，float
  - sUcsName：用户坐标名称，string
  - sTcpName：工具坐标名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 原始点位类型
nRawDataType = 1
# 轨迹名称
trajectName = "Path_01"
# 轨迹运动速度比
dSpeedRatio = 0.3
# 过渡半径
dRadius = 20
# 轨迹运动速度
dVelocity = 100
# 轨迹运动加速度
dAcc = 500
# 轨迹运动加加速度
dJerk = 10000
# 用户坐标名称
sUcsName = "Base"
# 工具坐标名称
sTcpName = "TCP"
# 初始化直线运动轨迹
nRet = cps.HRIF_InitPath(0,0,nRawDataType,trajectName,dSpeedRatio,dRadius,dVelocity,dAcc, dJerk, sUcsName,
sTcpName)
```

### 3.11.17 HRIF_PushPathPoints
描述：向轨迹中批量推送原始点位（可多次调用）。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sPathName：轨迹名称，string
  - sPoints：点位数据，list
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
trajectName = "Path_01"
# 点位数据
sPoints = [420,0,445,180,0,180, 430,10,445,180,0,180, 440,50,445,180,0,180,
520,100,445,180,0,180, 450,50,445,180,0,180, 430,200,445,180,0,180]
# 向轨迹中批量推送原始点位
nRet = cps.HRIF_PushPathPoints(0,0, trajectName,sPoints)
```

### 3.11.18 HRIF_EndPushPathPoints
描述：结束向轨迹中推送点位，并开始计算轨迹。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sPathName：轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sPathName= "drag_01"
# 下发完成，开始计算轨迹
nRet = cps.HRIF_EndPushPathPoints(0,0, sPathName)
```

### 3.11.19 HRIF_DelPath
描述：删除指定名称的轨迹。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sPathName：轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sPathName = "drag_03"
# 删除轨迹
nRet = cps.HRIF_DelPath(0,0, sPathName)
```

### 3.11.20 HRIF_ReadPathList
描述：读取轨迹列表。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list
- 输出变量：
  - result：轨迹列表，list
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹列表
result = [ ]
# 读取轨迹列表
nRet = cps.HRIF_ReadPathList(0,0, result)
```

### 3.11.21 HRIF_ReadPathInfo
描述：读取指定名称轨迹的信息。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sPathName：轨迹名称，string
  - result：返回值，list
- 输出变量：
  - result[0]：原始点位类型，string
  - result[1]：MovePathJ的状态，string
  - result[2]：错误码，string
  - result[3]：MovePathL的状态，string
  - result[4]：错误码，string
  - result[5]：轨迹运动速度比，string
  - result[6]：过渡半径，string
  - result[7]：轨迹运动速度，string
  - result[8]：轨迹运动加速度，string
  - result[9]：轨迹运动加加速度，string
  - result[10]：用户坐标，string
  - result[11]：工具坐标，string
  - result[12]：原始点位个数，string
  - result[13]：第一个原始点位坐标，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sPathName = "Path_01"
# 轨迹信息
result = [ ]
# 读取指定名称轨迹的信息
nRet = cps.HRIF_ReadPathInfo(0,0, sPathName, result)
```

### 3.11.22 HRIF_UpdatePathName
描述：更新轨迹名称。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sPathName：轨迹原名称，string
  - sPathNewName：新轨迹名称，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹原名称
sPathName = "drag_01"
# 新轨迹名称
sPathNewName = "drag_02"
# 更新轨迹名称
nRet = cps.HRIF_UpdatePathName(0,0, sPathName, sPathNewName)
```

### 3.11.23 HRIF_ReadPathState
描述：读取当前轨迹状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sPathName：轨迹名称，string
  - result：返回值，list
- 输出变量：
  - result[0]：MovePathJ的状态，string，0/1/2/3/4/5/9/10
  - result[1]：MovePathJ的错误码，string
  - result[2]：MovePathL的状态，string，0/1/2/3/4/5/9/10
  - result[3]：MovePathL的错误码，string
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 轨迹名称
sPathName = "drag_01"
# MovePathJ的状态
nStateJ = 0
# MovePathJ的错误码
nErrorCodeJ = 0
# MovePathL的状态
nStateL = 0
# MovePathL的错误码
nErrorCodeL = 0
# 更新轨迹名称
nRet = cps.HRIF_ReadPathState(0,0, sPathName,nStateJ,nErrorCodeJ,nStateL,nErrorCodeL)
```

## 3.12 Servo运动类控制指令

### 3.12.1 HRIF_StartServo
描述：启动机器人在线控制（ServoJ或 ServoP）时，设定位置固定更新的周期和前瞻时间。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dServoTime：更新周期，float，>0
  - dLookaheadTime：前瞻时间，float，>0
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 周期
dServoTime = 0.02
# 前瞻时间
dLookaheadTime = 0.2
# 启动机器人在线控制
nRet = cps.HRIF_StartServo(0,0,dServoTime, dLookaheadTime)
```

### 3.12.2 HRIF_PushServoJ
描述：在线关节位置命令控制，以StartServo设定的固定更新时间发送关节位置，机器人将实时的跟踪关节位置指令。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dAcs：关节点位，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 目标关节位置
dAcs = [0, 0, 0, 0, 0, 0]
# 在线关节位置命令控制
nRet = cps.HRIF_PushServoJ(0,0, dAcs )
```

### 3.12.3 HRIF_PushServoP
描述：在线末端TCP位置命令控制，以StartServo设定的固定更新时间发送TCP位置，机器人将实时的跟踪目标TCP位置逆运算转换后的关节位置指令。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dPcs：空间点位，list[float]
  - dTcp：工具坐标，list[float]
  - dUcs：用户坐标，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 空间目标位置
dPcs = [420, 0, 445, 180, 0, 180]
# 定义工具坐标变量
dTcp = [0, 0, 0, 0, 0, 0]
# 定义用户坐标变量
dUcs = [0, 0, 0, 0, 0, 0]
# 在线空间位置命令控制
nRet = cps.HRIF_PushServoP(0,0,dPcs, dTcp, dUcs)
```

### 3.12.4 HRIF_SpeedJ
描述：在线关节运动速度伺服控制，以该指令中指定的各个关节的速度和加速度运动指定的时长。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - cmdVel：命令关节速度，list[float]
  - acc：加速度，float
  - runtime：运行时间，float
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 命令关节速度
cmdVel = [5,5,5,2,2,2]
# 定义关节加速度
acc = 20
# 定义运行时间
runtime = 2
# 下发关节命令速度指令
nRet = cps.HRIF_SpeedJ(0,0,cmdVel, acc, runtime)
```

### 3.12.5 HRIF_SpeedL
描述：在线空间运动速度伺服控制，以该指令中指定的位姿各个坐标的速度和加速度运动指定的时长。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - cmdVel：坐标命令速度，list[float]
  - LinearAcc：X/Y/Z加速度，float
  - AngularAcc：RX/RY/RZ加速度，float
  - runtime：运行时间，float
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 命令空间速度
cmdVel = [-1,1,1,0,1,2]
# 定义X/Y/Z加速度
LinearAcc = 100
# 定义RX/RY/RZ加速度
AngularAcc = 200
# 定义运行时间
runtime = 2
# 下发空间命令速度指令
nRet = cps.HRIF_SpeedL(0,0,cmdVel, LinearAcc , AngularAcc, runtime)
```

### 3.12.6 HRIF_ReadServoEsJState
描述：读取当前是否可以继续下发点位信息，循环读取间隔>20ms。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list
- 输出变量：
  - result[0]：能否继续下发，string，0/1
- 返回值：nRet，int，>0 的整型值

示例：
```python
result = []
# 读取
nRet = cps.HRIF_ReadServoEsJState(0,0,result)
```

## 3.13 相对跟踪运动类控制指令

### 3.13.1 HRIF_SetMoveTraceParams
描述：设置相对跟踪运动控制参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nState：跟踪状态，int，0/1
  - dDistance：相对跟踪运动保持的相对距离，float，>0
  - dAwayVelocity：相对跟踪的运动的远离探寻速度，float，>0
  - dBackVelocity：相对跟踪的运动的靠近探寻速度，float，>0
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置跟踪状态和保持的相对距离
nState = 1
dDistance = 100
# 相对跟踪的运动的探寻速度
dAwayVelocity = 50
dBackVelocity = 50
# 设置相对跟踪运动控制参数并开启相对跟踪运动
nRet = cps.HRIF_SetMoveTraceParams(0,0,nState, dDistance,dAwayVelocity,dBackVelocity)
```

### 3.13.2 HRIF_SetMoveTraceInitParams
描述：设置相对跟踪运动初始化参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dK：传感器计算参数，float
  - dB：传感器计算参数，float
  - dMaxLimit：激光传感器检测距离最大值，float
  - dMinLimit：激光传感器检测距离最小值，float
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 传感器计算参数
dK= -14
# 传感器计算参数
dB= 135
# 激光传感器检测距离最大值
dMaxLimit = 130
# 激光传感器检测距离最小值
dMinLimit = 65
# 设置跟踪状态初始化参数
nRet = cps.HRIF_SetMoveTraceInitParams(0,0,dK, dB, dMaxLimit, dMinLimit)
```

### 3.13.3 HRIF_SetMoveTraceUcs
描述：设置相对跟踪运动的跟踪探寻方向。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - direction：跟踪探寻方向，list[float]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置跟踪方向
direction = [420, 0, 445, 180, 0, 180]
# 设置跟踪方向
nRet = cps.HRIF_SetMoveTraceUcs(0,0,direction)
```

### 3.13.4 HRIF_SetTrackingState
描述：设置传送带跟踪运动状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nState：跟踪状态，int，0/1
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置传送带跟踪开启
nState = 1
# 开启传送带跟踪
nRet = cps.HRIF_SetTrackingState(0,0,nState)
```

## 3.14 位置跟随运动类控制指令

### 3.14.1 HRIF_SetPoseTrackingMaxMotionLimit
描述：设置位置跟随的最大跟随速度。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dMaxLineVel：直线最大速度，float，>0
  - dMaxOriVel：姿态最大速度，float，>0
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置直线最大速度
dMaxLineVel = 100
# 设置姿态最大速度
dMaxOriVel = 1
# 发送信息
nRet = cps.HRIF_SetPoseTrackingMaxMotionLimit(0,0,dMaxLineVel,dMaxOriVel)
```

### 3.14.2 HRIF_SetPoseTrackingStopTimeOut
描述：设置位置跟踪超时停止时间。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dTime：超时时间，float，>=0
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 超时时间
dTime = 10
# 设置位置跟踪超时停止时间
nRet = cps.HRIF_SetPoseTrackingStopTimeOut(0,0,dTime)
```

### 3.14.3 HRIF_SetPoseTrackingPIDParams
描述：设置PID参数。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dPosPID1：位置跟随PID，float
  - dPosPID2：位置跟随PID，float
  - dPosPID3：位置跟随PID，float
  - dOriPID1：姿态跟随PID，float
  - dOriPID2：姿态跟随PID，float
  - dOriPID3：姿态跟随PID，float
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置位置跟随PID和姿态跟随PID
dPosPID1= 5
dPosPID2 = 0.1
dPosPID3= 0
dOriPID1 = 5
dOriPID2 = 0.1
dOriPID3 = 0
# 发送信息
nRet = cps.HRIF_SetPoseTrackingPIDParams(0,0,dPosPID1,dPosPID2,dPosPID3,dOriPID1,dOriPID2,dOriPID3)
```

### 3.14.4 HRIF_SetPoseTrackingTargetPos
描述：设置位置跟随的目标位置。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX：X 方向保持的距离，float
  - dY：Y 方向保持的距离，float
  - dZ：Z 方向保持的距离，float
  - dRx：Rx 方向保持的距离，float
  - dRy：Ry 方向保持的距离，float
  - dRz：Rz 方向保持的距离，float
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置目标位置
dX = 0dY = 0  dZ= 100dRx = 0  dRy= 0dRz = 0
# 发送信息
nRet = cps.HRIF_SetPoseTrackingTargetPos(0,0,dX ,dY ,dZ,dRx,dRy,dRz)
```

### 3.14.5 HRIF_SetPoseTrackingState
描述：设置位置跟随状态。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nState：位置跟随状态，int，0/1
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 开启位置跟随
nState = 1
# 发送信息
nRet = cps.HRIF_SetPoseTrackingState(0,0,nState)
```

### 3.14.6 HRIF_SetUpdateTrackingPose
描述：设置实时更新传感器位置信息。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - dX：检测到的X方向的距离，float
  - dY：检测到的Y方向的距离，float
  - dZ：检测到的Z方向的距离，float
  - dRx：检测到的Rx方向的距离，float
  - dRy：检测到的Ry方向的距离，float
  - dRz：检测到的Rz方向的距离，float
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置检测到的位置信息
dX = 0dY = 0  dZ= 100dRx = 0  dRy= 0dRz = 0
# 发送信息
nRet = cps.HRIF_SetUpdateTrackingPose(0,0,dX ,dY ,dZ,dRx,dRy,dRz)
```

## 3.15 其他指令

### 3.15.1 HRIF_HRApp
描述：执行插件App命令。(推荐使用HRIF_HRAppCmd）
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sCmdName：命令名称，string
  - sParams：参数列表，list
  - result：返回值，list
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 定义返回值空列表
result = [ ]
# 插件名称
sCmdName = 'FT_Plugin'
# 插件指令与参数
sParams = ['FT_reset']
# 发送插件命令
nRet = cps.HRIF_HRApp(0,0,sCmdName, sParams, result)
```

### 3.15.2 HRIF_HRAppCmd
描述：执行插件App命令。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - sCmdName：命令名称，string
  - sParams：参数列表，list
  - result：返回值，list
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 定义返回值空列表
result = [ ]
# 插件名称
sCmdName = 'FT_Plugin'
# 插件指令与参数
sParams = ['FT_reset']
# 发送插件命令
nRet = cps.HRIF_HRAppCmd(0,0,sCmdName, sParams, result)
```

### 3.15.3 HRIF_WriteEndHoldingRegisters
描述：写末端连接的Modbus从站寄存器。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - nSlaveID：从站 ID，int，1~255
  - nFunction：功能码，int，>0
  - nRegAddr：寄存器地址，int，>0
  - nRegCount：寄存器数量，int，>0
  - nData：寄存器数据，list[int]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置从站ID=1
nSlaveID = 1
# 设置功能码
nFunction = 16
# 设置寄存器起始地址
nRegAddr = 100
# 设置寄存器数量
nRegCount = 2
# 设置寄存器数据
nData=[196,34465]
nRet = cps.HRIF_WriteEndHoldingRegisters(0,0,nSlaveID, nFunction, nRegAddr, nRegCount, nData)
```

### 3.15.4 HRIF_ReadEndHoldingRegisters
描述：读末端连接的Modbus从站寄存器。
- 输入变量：
  - boxID：电箱 ID，int，0~5
  - rbtID：机器人 ID，int，0~5
  - result：返回值，list
  - nSlaveID：从站 ID，int，1~255
  - nFunction：功能码，int，>0
  - nRegAddr：寄存器地址，int，>0
  - nRegCount：寄存器数量，int，>0
- 输出变量：
  - result：寄存器数据，list[int]
- 返回值：nRet，int，>0 的整型值

示例：
```python
# 设置从站ID=1
nSlaveID = 1
# 设置功能码
nFunction = 3
# 设置寄存器起始地址
nRegAddr = 100
# 设置寄存器数量
nRegCount = 4
# 定义返回值空列表
result = [ ]
# 读取寄存器数据
nRet = cps.HRIF_ReadEndHoldingRegisters(0,0,nSlaveID, nFunction, nRegAddr, nRegCount, result)
for i in range(len(result)):
    print(result[i])
