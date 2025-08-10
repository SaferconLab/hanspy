# 第三章 可使用接口

## 3.7 坐标转换计算指令

### 3.7.1 HRIF_Quaternion2RPY
#### 描述：四元素转欧拉角。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dQuaWW | float | - | W |
| dQuaXX | float | - | Xi |
| dQuaYY | float | - | Yj |
| dQuaZZ | float | - | Zk |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0] | string | >=-180,=<180 | 欧拉角Rx |
| result[1] | string | >=-180,=<180 | 欧拉角Ry |
| result[2] | string | >=-180,=<180 | 欧拉角Rz |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 需要转换的四元素变量
dQuaW=0dQuaX=0dQuaY=0dQuaZ=0
# 转换
nRet=cps.HRIF_Quaternion2RPY(0,dQuaW,dQuaX,dQuaY,dQuaZ,result)
# 转换后的欧拉角结果
dRx=float(result[0])dRy=float(result[1])dRz=float(result[2])
```

### 3.7.2 HRIF_RPY2Quaternion
#### 描述：欧拉角转四元素。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| Rx | float | >=-180,=<180 | 欧拉角Rx |
| Ry | float | >=-180,=<180 | 欧拉角Ry |
| Rz | float | >=-180,=<180 | 欧拉角Rz |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0] | string | - | W |
| result[1] | string | - | Xi |
| result[2] | string | - | Yj |
| result[3] | string | - | Zk |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 需要转换的转换后的欧拉角变量
dRx=0dRy=0dRz=0
# 转换
nRet=cps.HRIF_RPY2Quaternion(0,dRx,dRy,dRz,result)
# 转换后的四元素变量
dQuaW=float(result[0])dQuaX=float(result[1])
dQuaY=float(result[2])dQuaZ=float(result[3])
```

### 3.7.3 HRIF_GetInverseKin
#### 描述：运动学逆解，由指定用户坐标系位置和工具坐标系下的迪卡尔坐标计算对应的关节坐标位置。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dCoord_X-dCoord_Rz | float | - | 需要计算逆解的目标迪卡尔位置：<br>dCoord_X：X坐标，单位[mm]<br>dCoord_Y：Y坐标，单位[mm]<br>dCoord_Z：Z坐标，单位[mm]<br>dCoord_Rx：Rx坐标，单位[°]<br>dCoord_Ry：Ry坐标，单位[°]<br>dCoord_Rz：Rz坐标，单位[°] |
| dTcp_X-dTcp_Rz | float | - | 目标位置是否包含工具坐标(不包含工具坐标则所有值=0)：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] |
| dUcs_X-dUcs_Rz | float | - | 目标位置是否包含用户坐标(不包含用户坐标则所有值=0)：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] |
| dJ1-dJ6 | float | - | dJ1：关节1坐标，单位[°]<br>dJ2：关节2坐标，单位[°]<br>dJ3：关节3坐标，单位[°]<br>dJ4：关节4坐标，单位[°]<br>dJ5：关节5坐标，单位[°]<br>dJ6：关节6坐标，单位[°]<br>逆解出现多个解时需要根据参考关节坐标选取最终解 |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | dTargetJ1：关节1坐标，单位[°]<br>dTargetJ2：关节2坐标，单位[°]<br>dTargetJ3：关节3坐标，单位[°]<br>dTargetJ4：关节4坐标，单位[°]<br>dTargetJ5：关节5坐标，单位[°]<br>dTargetJ6：关节6坐标，单位[°] | 关节坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要转换的空间位置变量
dCoord=[0,0,0,0,0,0]
# 定义工具坐标变量
Tcp=[0,0,0,0,0,0]
# 定义工具坐标变量
Ucs=[0,0,0,0,0,0]
# 定义参考关节位置变量
rawACS=[0,0,0,0,0,0]
# 求逆解
nRet=cps.HRIF_GetInverseKin(0,0,dCoord,rawACS,Tcp,Ucs,result)
# 读取转换结果
dTargetJ1=float(result[0])dTargetJ2=float(result[1])dTargetJ3=float(result[2])
dTargetJ4=float(result[3])dTargetJ5=float(result[4])dTargetJ6=float(result[5])
```

### 3.7.4 HRIF_GetForwardKin
#### 描述：运动学正解，由关节坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dJ1-dJ6 | float | - | dJ1：关节1坐标，单位[°]<br>dJ2：关节2坐标，单位[°]<br>dJ3：关节3坐标，单位[°]<br>dJ4：关节4坐标，单位[°]<br>dJ5：关节5坐标，单位[°]<br>dJ6：关节6坐标，单位[°] |
| dTcp_X-dTcp_Rz | float | - | 目标位置是否包含工具坐标(不包含工具坐标则所有值=0)：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] |
| dUcs_X-dUcs_Rz | float | - | 目标位置是否包含用户坐标(不包含用户坐标则所有值=0)：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 如果正解得到的迪卡尔坐标不需要带工具坐标和用户坐标则将所有的工具坐标和用户坐标置0：<br>dTargetX：X坐标，单位[mm]<br>dTargetY：Y坐标，单位[mm]<br>dTargetZ：Z坐标，单位[mm]<br>dTargetRx：Rx坐标，单位[°]<br>dTargetRy：Ry坐标，单位[°]<br>dTargetRz：Rz坐标，单位[°] | 目标迪卡尔坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要转换的关节位置变量
rawACS=[0,0,0,0,0,0]
# 定义工具坐标变量
Tcp=[0,0,0,0,0,0]
# 定义用户坐标变量
Ucs=[0,0,0,0,0,0]
# 求正解
nRet=cps.HRIF_GetForwardKin(0,0,rawACS,Tcp,Ucs,result)
# 获取转换后的空间位置结果
dTarget_X=float(result[0])dTarget_Y=float(result[1])dTarget_Z=float(result[2])
dTarget_Rx=float(result[3])dTarget_Ry=float(result[4])dTarget_Rz=float(result[5])
```

### 3.7.5 HRIF_Base2UcsTcp
#### 描述：由基坐标系下的坐标位置计算指定用户坐标系和工具坐标系下的迪卡尔坐标位置。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dCoord_X-dCoord_Rz | float | - | 需要转换的迪卡尔位置：<br>dCoord_X：X坐标，单位[mm]<br>dCoord_Y：Y坐标，单位[mm]<br>dCoord_Z：Z坐标，单位[mm]<br>dCoord_Rx：Rx坐标，单位[°]<br>dCoord_Ry：Ry坐标，单位[°]<br>dCoord_Rz：Rz坐标，单位[°] |
| dTcp_X-dTcp_Rz | float | - | 目标位置是否包含工具坐标(不包含工具坐标则所有值=0)：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] |
| dUcs_X-dUcs_Rz | float | - | 目标位置是否包含用户坐标(不包含用户坐标则所有值=0)：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 指定用户坐标系和工具坐标系下的迪卡尔坐标位置：<br>dTargetX：X坐标，单位[mm]<br>dTargetY：Y坐标，单位[mm]<br>dTargetZ：Z坐标，单位[mm]<br>dTargetRx：Rx坐标，单位[°]<br>dTargetRy：Ry坐标，单位[°]<br>dTargetRz：Rz坐标，单位[°] | 目标迪卡尔坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要转换的空间位置变量
dCoord=[0,0,0,0,0,0]
# 定义工具坐标变量
Tcp=[0,0,0,0,0,0]
# 定义用户坐标变量
Ucs=[0,0,0,0,0,0]
# 基座坐标转换为用户坐标
nRet=cps.HRIF_Base2UcsTcp(0,dCoord,Tcp,Ucs,result)
# 定义转换后的空间位置结果
dTarget_X=float(result[0])dTarget_Y=float(result[1])dTarget_Z=float(result[2])
dTarget_Rx=float(result[3])dTarget_Ry=float(result[4])dTarget_Rz=float(result[5])
```

### 3.7.6 HRIF_UcsTcp2Base
#### 描述：由指定用户坐标系和工具坐标系下的迪卡尔坐标位置计算基坐标系下的坐标位置。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dCoord_X-dCoord_Rz | float | - | 指定用户坐标系和工具坐标系下的迪卡尔坐标位置：<br>dCoord_X：X坐标，单位[mm]<br>dCoord_Y：Y坐标，单位[mm]<br>dCoord_Z：Z坐标，单位[mm]<br>dCoord_Rx：Rx坐标，单位[°]<br>dCoord_Ry：Ry坐标，单位[°]<br>dCoord_Rz：Rz坐标，单位[°] |
| dTcp_X-dTcp_Rz | float | - | 目标位置是否包含工具坐标(不包含工具坐标则所有值=0)：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] |
| dUcs_X-dUcs_Rz | float | - | 目标位置是否包含用户坐标(不包含用户坐标则所有值=0)：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 基座坐标系下的迪卡尔坐标位置：<br>dTargetX：X坐标，单位[mm]<br>dTargetY：Y坐标，单位[mm]<br>dTargetZ：Z坐标，单位[mm]<br>dTargetRx：Rx坐标，单位[°]<br>dTargetRy：Ry坐标，单位[°]<br>dTargetRz：Rz坐标，单位[°] | 目标迪卡尔坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要转换的空间位置变量
dCoord=[0,0,0,0,0,0]
# 定义工具坐标变量
Tcp=[0,0,0,0,0,0]
# 定义用户坐标变量
Ucs=[0,0,0,0,0,0]
# 用户坐标转换为基座坐标
nRet=cps.HRIF_UcsTcp2Base(0,dCoord,Tcp,Ucs,result)
# 读取转换后的空间位置结果
dTarget_X=float(result[0])dTarget_Y=float(result[1])dTarget_Z=float(result[2])
dTarget_Rx=float(result[3])dTarget_Ry=float(result[4])dTarget_Rz=float(result[5])
```

### 3.7.7 HRIF_PoseAdd
#### 描述：点位加法计算，使用矩阵左乘运算（第二个点左乘第一个点）。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Rz | float | - | 需要计算的空间坐标1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 需要计算的空间坐标2：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算结果：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] | 计算结果 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose1=[420,0,445,180,0,180]
# 定义需要计算的空间坐标2
Pose2=[420,50,445,180,0,180]
# 计算结果
nRet=cps.HRIF_PoseAdd(0,Pose1,Pose2,result)
# 计算结果
dPose3_X=float(result[0])dPose3_Y=float(result[1])dPose3_Z=float(result[2])
dPose3_Rx=float(result[3])dPose3_Ry=float(result[4])dPose3_Rz=float(result[5])
```

### 3.7.8 HRIF_PoseSub
#### 描述：点位减法计算，以第二个点为参考点。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Rz | float | - | 需要计算的空间坐标1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 需要计算的空间坐标2：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算结果：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] | 计算坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose1=[420,0,445,180,0,180]
# 定义需要计算的空间坐标2
Pose2=[420,50,445,180,0,180]
# 计算结果
nRet=cps.HRIF_PoseSub(0,Pose1,Pose2,result)
# 计算结果
dPose3_X=float(result[0])dPose3_Y=float(result[1])dPose3_Z=float(result[2])
dPose3_Rx=float(result[3])dPose3_Ry=float(result[4])dPose3_Rz=float(result[5])
```

### 3.7.9 HRIF_PoseTrans
#### 描述：坐标变换。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Rz | float | - | 坐标位置1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 坐标位置2：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算结果：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] | 计算坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose1=[420,0,445,180,0,180]
# 定义需要计算的空间坐标2
Pose2=[420,50,445,180,0,180]
# 计算结果
nRet=cps.HRIF_PoseTrans(0,0,Pose1,Pose2,result)
# 计算结果
dPose3_X=float(result[0])dPose3_Y=float(result[1])dPose3_Z=float(result[2])
dPose3_Rx=float(result[3])dPose3_Ry=float(result[4])dPose3_Rz=float(result[5])
```

### 3.7.10 HRIF_PoseInverse
#### 描述：坐标逆变换。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Rz | float | - | 需要计算的空间坐标1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算结果：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] | 计算坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose=[420,0,445,180,0,180]
# 计算结果
nRet=cps.HRIF_PoseInverse(0,Pose,result)
# 计算结果
dPose3_X=float(result[0])dPose3_Y=float(result[1])dPose3_Z=float(result[2])
dPose3_Rx=float(result[3])dPose3_Ry=float(result[4])dPose3_Rz=float(result[5])
```

### 3.7.11 HRIF_PoseDist
#### 描述：计算点位距离。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Rz | float | - | 需要计算的空间坐标1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 需要计算的空间坐标2：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0] | float | - | 点位距离，单位[mm] |
| result[1] | float | - | 姿态距离，单位[°] |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose1=[420,0,445,180,0,180]
# 定义需要计算的空间坐标2
Pose2=[420,50,445,180,0,180]
# 计算结果
nRet=cps.HRIF_PoseDist(0,Pose1,Pose2,result)
```

### 3.7.12 HRIF_PoseInterpolate
#### 描述：空间位置直线插补计算。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Rz | float | - | 需要计算的空间坐标1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 需要计算的空间坐标2：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |
| dAlpha | float | 0-1 | 插补比例<br>dAlpha=0：dPose3=dPose1<br>dAlpha=1：dPose3=dPose2<br>0-1：按照dPose1到dPose2的位置取比例为dAlpha的位置返回dPose3 |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算结果：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] | 计算坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose1=[420,0,445,180,0,180]
# 定义需要计算的空间坐标2
Pose2=[420,50,445,180,0,180]
# 插补比例
dAlpha=0.5
# 计算结果
nRet=cps.HRIF_PoseInterpolate(0,Pose1,Pose2,dAlpha,result)
# 计算结果
dPose3_X=float(result[0])dPose3_Y=float(result[1])dPose3_Z=float(result[2])
dPose3_Rx=float(result[3])dPose3_Ry=float(result[4])dPose3_Rz=float(result[5])
```

### 3.7.13 HRIF_PoseDefdFrame
#### 描述：以轨迹中心旋转计算，p1,p2,p3为旋转前选取的轨迹的特征点，p4,p5,p6为旋转后选取的轨迹的特征点，计算结果表示为旋转特征的用户坐标系。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| dPose1_X-dPose1_Z | float | - | 需要计算的空间坐标1：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm] |
| dPose2_X-dPose2_Z | float | - | 需要计算的空间坐标2：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm] |
| dPose3_X-dPose3_Z | float | - | 需要计算的空间坐标3：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm] |
| dPose4_X-dPose4_Z | float | - | 需要计算的空间坐标4：<br>dPose4_X：X坐标，单位[mm]<br>dPose4_Y：Y坐标，单位[mm]<br>dPose4_Z：Z坐标，单位[mm] |
| dPose5_X-dPose5_Z | float | - | 需要计算的空间坐标5：<br>dPose5_X：X坐标，单位[mm]<br>dPose5_Y：Y坐标，单位[mm]<br>dPose5_Z：Z坐标，单位[mm] |
| dPose6_X-dPose6_Z | float | - | 需要计算的空间坐标6：<br>dPose6_X：X坐标，单位[mm]<br>dPose6_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算结果：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] | 计算结果 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 定义需要计算的空间坐标1
Pose1=[0,0,0]
# 定义需要计算的空间坐标2
Pose2=[0,0,0]
# 定义需要计算的空间坐标3
Pose3=[0,0,0]
# 定义需要计算的空间坐标4
Pose4=[0,0,0]
# 定义需要计算的空间坐标5
Pose5=[0,0,0]
# 定义需要计算的空间坐标6
Pose6=[0,0,0]
# 计算结果
nRet=cps.HRIF_PoseDefdFrame(0,Pose1,Pose2,Pose3,Pose4,Pose5,Pose6,result)
```

### 3.7.14 HRIF_CalUcsPlane
#### 描述：通过三点平面法计算UCS。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| dPose1_X-dPose1_Z | float | - | 点1在Base坐标系下系统默认TCP的位置：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm] |
| dPose2_X-dPose2_Z | float | - | 点2在Base坐标系下系统默认TCP的位置：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm] |
| dPose3_X-dPose3_Z | float | - | 点3在Base坐标系下系统默认TCP的位置：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算得出的UCS位姿：<br>dRetPose_X：X坐标，单位[mm]<br>dRetPose_Y：Y坐标，单位[mm]<br>dRetPose_Z：Z坐标，单位[mm]<br>dRetPose_Rx：Rx坐标，单位[°]<br>dRetPose_Ry：Ry坐标，单位[°]<br>dRetPose_Rz：Rz坐标，单位[°] | 计算结果 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 点1在Base坐标系下系统默认TCP的位置
Pose1=[10,0,0]
# 点2在Base坐标系下系统默认TCP的位置
Pose2=[0,10,0]
# 点3在Base坐标系下系统默认TCP的位置
Pose3=[0,0,10]
# 获取计算结果
nRet=cps.HRIF_CalUcsPlane(0,Pose1,Pose2,Pose3,result)
```

### 3.7.15 HRIF_CalUcsLine
#### 描述：通过两点直线法计算UCS。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| dPose1_X-dPose1_Rz | float | - | 点1在Base坐标系下系统默认TCP的位姿：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 点2在Base坐标系下系统默认TCP的位姿：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算得出的UCS位姿：<br>dRetPose_X：X坐标，单位[mm]<br>dRetPose_Y：Y坐标，单位[mm]<br>dRetPose_Z：Z坐标，单位[mm]<br>dRetPose_Rx：Rx坐标，单位[°]<br>dRetPose_Ry：Ry坐标，单位[°]<br>dRetPose_Rz：Rz坐标，单位[°] | 计算结果 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 点1在Base坐标系下系统默认TCP的位姿
Pose1=[10,0,0,10,0,0]
# 点2在Base坐标系下系统默认TCP的位姿
Pose2=[0,10,0,0,10,0]
# 获取计算结果
nRet=cps.HRIF_CalUcsLine(0,Pose1,Pose2,result)
```

### 3.7.16 HRIF_CalTcp3P
#### 描述：通过三点平面法计算TCP。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| dPose1_X-dPose1_Rz | float | - | 点1在Base坐标系下系统默认TCP的位姿：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 点2在Base坐标系下系统默认TCP的位姿：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |
| dPose3_X-dPose3_Rz | float | - | 点3在Base坐标系下系统默认TCP的位姿：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算得出的UCS位姿：<br>dRetPose_X：X坐标，单位[mm]<br>dRetPose_Y：Y坐标，单位[mm]<br>dRetPose_Z：Z坐标，单位[mm]<br>dRetPose_Rx：Rx坐标，单位[°]，一般是0<br>dRetPose_Ry：Ry坐标，单位[°]，一般是0<br>dRetPose_Rz：Rz坐标，单位[°]，一般是0 | 计算结果 |
| result[6] | string | 0/1/2 | 结果质量：<br>0：良好<br>1：差（计算结果最好不用）<br>2：异常 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 点1在Base坐标系下系统默认TCP的位置
Pose1=[10,0,0,10,0,0]
# 点2在Base坐标系下系统默认TCP的位置
Pose2=[0,10,0,0,10,0]
# 点3在Base坐标系下系统默认TCP的位置
Pose3=[0,0,10,0,0,10]
# 获取计算结果
nRet=cps.HRIF_CalTcp3P(0,Pose1,Pose2,Pose3,result)
```

### 3.7.17 HRIF_CalTcp4P
#### 描述：通过四点平面法计算TCP。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| dPose1_X-dPose1_Rz | float | - | 点1在Base坐标系下系统默认TCP的位姿：<br>dPose1_X：X坐标，单位[mm]<br>dPose1_Y：Y坐标，单位[mm]<br>dPose1_Z：Z坐标，单位[mm]<br>dPose1_Rx：Rx坐标，单位[°]<br>dPose1_Ry：Ry坐标，单位[°]<br>dPose1_Rz：Rz坐标，单位[°] |
| dPose2_X-dPose2_Rz | float | - | 点2在Base坐标系下系统默认TCP的位姿：<br>dPose2_X：X坐标，单位[mm]<br>dPose2_Y：Y坐标，单位[mm]<br>dPose2_Z：Z坐标，单位[mm]<br>dPose2_Rx：Rx坐标，单位[°]<br>dPose2_Ry：Ry坐标，单位[°]<br>dPose2_Rz：Rz坐标，单位[°] |
| dPose3_X-dPose3_Rz | float | - | 点3在Base坐标系下系统默认TCP的位置：<br>dPose3_X：X坐标，单位[mm]<br>dPose3_Y：Y坐标，单位[mm]<br>dPose3_Z：Z坐标，单位[mm]<br>dPose3_Rx：Rx坐标，单位[°]<br>dPose3_Ry：Ry坐标，单位[°]<br>dPose3_Rz：Rz坐标，单位[°] |
| dPose4_X-dPose4_Rz | float | - | 点4在Base坐标系下系统默认TCP的位置：<br>dPose4_X：X坐标，单位[mm]<br>dPose4_Y：Y坐标，单位[mm]<br>dPose4_Z：Z坐标，单位[mm]<br>dPose4_Rx：Rx坐标，单位[°]<br>dPose4_Ry：Ry坐标，单位[°]<br>dPose4_Rz：Rz坐标，单位[°] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 计算得出的UCS位姿：<br>dRetPose_X：X坐标，单位[mm]<br>dRetPose_Y：Y坐标，单位[mm]<br>dRetPose_Z：Z坐标，单位[mm]<br>dRetPose_Rx：Rx坐标，单位[°]，一般是0<br>dRetPose_Ry：Ry坐标，单位[°]，一般是0<br>dRetPose_Rz：Rz坐标，单位[°]，一般是0 | 计算结果 |
| result[6] | string | 0/1/2 | 结果质量：<br>0：良好<br>1：差（计算结果最好不用）<br>2：异常 |
| result[7]-result[10] | string | 0/1 | 源点的错误指示：<br>0：异常<br>1：正常 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 点1在Base坐标系下系统默认TCP的位置
Pose1=[10,0,0,10,0,0]
# 点2在Base坐标系下系统默认TCP的位置
Pose2=[0,10,0,0,10,0]
# 点3在Base坐标系下系统默认TCP的位置
Pose3=[0,0,10,0,0,10]
# 点4在Base坐标系下系统默认TCP的位置
Pose4=[0,0,0,0,0,0]
# 获取计算结果
nRet=cps.HRIF_CalTcp4P(0,Pose1,Pose2,Pose3,Pose4,result)
```

## 3.8 工具坐标与用户坐标读写指令

### 3.8.1 HRIF_SetTCP
#### 描述：设置当前工具坐标，不写入配置文件，重启后失效。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| dTcp_X-dTcp_Rz | float | - | 需要设置的工具坐标：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义工具坐标变量
Tcp=[0,0,0,0,0,0]
# 设置工具坐标
nRet=cps.HRIF_SetTCP(0,0,Tcp)
```

### 3.8.2 HRIF_SetUCS
#### 描述：设置当前用户坐标，不写入配置文件，重启后失效。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| dUcs_X-dUcs_Rz | float | - | 需要设置的用户坐标：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义用户坐标变量
Ucs=[0,0,0,0,0,0]
# 设置用户坐标
nRet=cps.HRIF_SetUCS(0,0,Ucs)
```

### 3.8.3 HRIF_ReadCurTCP
#### 描述：读取当前设置的工具坐标值。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 读取到的工具坐标：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] | 工具坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 读取工具坐标
nRet=cps.HRIF_ReadCurTCP(0,0,result)
# 读取工具坐标变量
dTcp_X=float(result[0])dTcp_Y=float(result[1])dTcp_Z=float(result[2])
dTcp_Rx=float(result[3])dTcp_Ry=float(result[4])dTcp_Rz=float(result[5])
```

### 3.8.4 HRIF_ReadCurUCS
#### 描述：读取当前设置的用户坐标值。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 读取到的用户坐标：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] | 用户坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 读取用户坐标
nRet=cps.HRIF_ReadCurUCS(0,0,result)
# 读取用户坐标变量
dUcs_X=float(result[0])dUcs_Y=float(result[1])dUcs_Z=float(result[2])
dUcs_Rx=float(result[3])dUcs_Ry=float(result[4])dUcs_Rz=float(result[5])
```

### 3.8.5 HRIF_SetTCPByName
#### 描述：通过名称设置工具坐标列表中的值为当前工具坐标，对应名称为示教器配置页面TCP示教的工具名称。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| sTcpName | string | - | 需要设置的工具坐标名称 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 需要下发的工具坐标名称
sTcpName="TCP"
# 设置工具坐标
nRet=cps.HRIF_SetTCPByName(0,0,sTcpName)
```

### 3.8.6 HRIF_SetUCSByName
#### 描述：通过名称设置用户坐标列表中的值为当前用户坐标，对应名称为示教器配置页面用户坐标示教的名称。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| sUcsName | string | - | 需要设置的用户坐标名称 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 需要下发的用户坐标名称
sUcsName="UCS"
# 设置用户坐标
nRet=cps.HRIF_SetUCSByName(0,0,sUcsName)
```

### 3.8.7 HRIF_ReadTCPByName
#### 描述：通过名称读取指定TCP坐标，对应名称为示教器配置页面TCP示教的工具名称。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| sTcpName | string | - | 需要读取的工具坐标名称 |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-result[5] | string | 读取到的工具坐标：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] | 工具坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 需要读取的工具坐标名称
sTcpName="TCP"
# 读取工具坐标
nRet=cps.HRIF_ReadTCPByName(0,0,sTcpName,result)
# 读取工具坐标结果变量
dTcp_X=float(result[0])dTcp_Y=float(result[1])dTcp_Z=float(result[2])
dTcp_Rx=float(result[3])dTcp_Ry=float(result[4])dTcp_Rz=float(result[5])
```

### 3.8.8 HRIF_ReadUCSByName
#### 描述：通过名称读取指定UCS坐标，对应名称为示教器配置页面用户坐标示教的用户坐标名称。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |
| sUcsName | string | - | 需要读取的用户坐标名称 |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result[0]-resutl[5] | string | 读取到的用户坐标：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] | 用户坐标 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义返回值空列表
result=[]
# 需要读取的用户坐标名称
sUcsName="UCS"
# 读取用户坐标
nRet=cps.HRIF_ReadUCSByName(0,0,sUcsName,result)
# 读取用户坐标变量
dUcs_X=0dUcs_Y=0dUcs_Z=0
dUcs_Rx=0dUcs_Ry=0dUcs_Rz=0
```

### 3.8.9 HRIF_ConfigTCP
#### 描述：新建指定名称的TCP和值。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| sTcpName | string | - | 需要新建的工具坐标名称 |
| dTcp_X-dTcp_Rz | float | - | 需要设置的工具坐标：<br>dTcp_X：X坐标，单位[mm]<br>dTcp_Y：Y坐标，单位[mm]<br>dTcp_Z：Z坐标，单位[mm]<br>dTcp_Rx：Rx坐标，单位[°]<br>dTcp_Ry：Ry坐标，单位[°]<br>dTcp_Rz：Rz坐标，单位[°] |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 需要下发的用户坐标名称
sTcpName="TCP"
# 设置工具坐标
Pose=[0,0,10,0,0,0]
# 新建Tcp
nRet=cps.HRIF_ConfigTCP(0,sTcpName,Pose)
```

### 3.8.10 HRIF_ConfigUCS
#### 描述：新建指定名称的UCS和值。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| sUcsName | string | - | 需要新建的用户坐标名称 |
| dUcs_X-dUcs_Rz | float | - | 需要设置的用户坐标：<br>dUcs_X：X坐标，单位[mm]<br>dUcs_Y：Y坐标，单位[mm]<br>dUcs_Z：Z坐标，单位[mm]<br>dUcs_Rx：Rx坐标，单位[°]<br>dUcs_Ry：Ry坐标，单位[°]<br>dUcs_Rz：Rz坐标，单位[°] |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 需要下发的用户坐标名称
sUcsName="UCS"
# 设置工具坐标
Pose=[0,0,10,0,0,0]
# 新建Ucs
nRet=cps.HRIF_ConfigUCS(0,sUcsName,Pose)
```

### 3.8.11 HRIF_ReadTCPList
#### 描述：读取系统中保存的TCP名称列表。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result | list | - | 保存读取到的所有TCP名称 | TCP名称列表 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义保存TCP列表的变量
result=[]
# 读取用户坐标系名称列表
nRet=cps.HRIF_ReadTCPList(0,0,result)
```

### 3.8.12 HRIF_ReadUCSList
#### 描述：读取系统中保存的UCS名称列表。
##### 输入变量
| 输入变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| boxID | int | 0~5 | 电箱ID号，默认值=0 |
| rbtID | int | 0~5 | 机器人ID号，默认值=0 |
| result | list | - | 传入空列表，result=[] |

##### 输出变量
| 输出变量名称 | 数据类型 | 有效范围 | 内容 |
|--------------|----------|----------|------|
| result | list | - | 保存读取到的所有UCS名称 | UCS名称列表 |

##### 返回值
| 返回值名称 | 数据类型 | 有效范围 | 内容 |
|------------|----------|----------|------|
| nRet | int | >0的整型值 | nRet=0:返回函数调用成功<br>nRet>0:返回调用失败的错误码 |

##### 示例
```python
# 定义保存UCS列表的变量
result=[]
# 读取用户坐标系名称列表
nRet=cps.HRIF_ReadUCSList(0,0,result)
