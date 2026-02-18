# Reachy Mini 9自由度桌面机器人

🤖 一个基于树莓派 + Arduino 的低成本桌面机器人项目

## 项目简介

Reachy Mini 是一个9自由度桌面机器人，具备以下特性：
- **6自由度颈部** - 斯图尔特平台结构
- **1自由度360°旋转** - 机身底座
- **2自由度天线** - 独立摇头/点头

## 硬件配置

| 模块 | 规格 | 数量 |
|------|------|------|
| 主控 | 树莓派 4B (4GB) | 1 |
| 摄像头 | 1200万像素广角 (120°) | 1 |
| 麦克风 | 4麦阵列 (声源定位) | 1 |
| 舵机 (颈部) | DS3231MG 金属舵机 | 6 |
| 舵机 (旋转) | DS5160 大扭矩舵机 | 1 |
| 舵机 (天线) | SG90 微型舵机 | 2 |
| 电池 | 7.4V 2S 锂电池 | 1 |
| 降压模块 | LM2596 5V/3A | 1 |

## 成本估算

| 类别 | 成本 (RMB) |
|------|-----------|
| 主控与感知 | 650-870元 |
| 运动系统 | 740-1020元 |
| 音频与输出 | 30-70元 |
| 电源与结构 | 250-410元 |
| 辅料 | 50-80元 |
| **总计** | **1660-2370元** |

## 项目结构

```
ReachyMini/
├── docs/               # 文档
│   ├── BOM.md         # 采购清单
│   └── assembly.md    # 组装指南
├── code/               # 代码
│   ├── servo/         # 舵机控制
│   ├── audio/         # 语音交互
│   └── vision/        # 视觉识别
├── images/            # 图片
└── README.md
```

## 功能特性

- 🎤 语音交互 (4麦阵列)
- 👀 视觉跟随 (1200万摄像头)
- 🦾 9自由度运动控制
- 🔊 音频输出 (5W扬声器)
- 📡 声源定位

## 快速开始

### 1. 硬件组装

详见 [组装指南](./docs/assembly.md)

### 2. 系统烧录

```bash
# 使用 Raspberry Pi Imager 烧录系统
# 选择 Raspberry Pi OS (64-bit) Desktop

# 开启 SSH
touch ssh

# 配置 WiFi
```

### 3. 安装依赖

```bash
# 舵机驱动
sudo pip3 install adafruit-circuitpython-pca9685

# 语音识别
sudo apt install pocketsphinx
```

## 开发指南

### 舵机控制

```python
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# 设置舵机角度
pca.channels[0].duty_cycle = 0x4000  # 中位
```

### 语音识别

```python
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)
    text = r.recognize_google(audio)
```

## 参考资料

- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [PCA9685 Driver](https://circuitpython.readthedocs.io/projects/pca9685/en/latest/)
- [ReSpeaker 4-Mic Array](https://wiki.seeedstudio.com/ReSpeaker_4-Mic_Array_for_Raspberry_Pi/)

## 许可证

MIT License
