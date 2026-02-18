# Reachy Mini 代码框架

## 目录结构

```
code/
├── servo/           # 舵机控制
│   ├── pca9685.py   # PCA9685 驱动
│   ├── stewart.py   # Stewart 平台控制
│   └── test.py      # 测试代码
├── audio/           # 语音交互
│   ├── respeaker.py # 麦克风阵列
│   └── kws.py       # 唤醒词检测
├── vision/          # 视觉识别
│   ├── camera.py    # 摄像头控制
│   └── face.py     # 人脸追踪
├── main.py          # 主程序
└── requirements.txt # 依赖
```

---

## 舵机控制 (PCA9685)

### 安装依赖

```bash
sudo pip3 install adafruit-circuitpython-pca9685
sudo apt install python3-smbus i2c-tools
```

### PCA9685 驱动

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PCA9685 16路舵机驱动
"""

import board
import busio
from adafruit_pca9685 import PCA9685
import time

class ServoController:
    def __init__(self, i2c_address=0x40, frequency=50):
        """初始化舵机控制器
        
        Args:
            i2c_address: PCA9685 I2C地址 (默认0x40)
            frequency: PWM频率 (舵机通常50Hz)
        """
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(self.i2c, address=i2c_address)
        self.pca.frequency = frequency
        
        # 舵机角度与脉宽映射 (180度舵机)
        # 0° = 1ms = 409.6
        # 90° = 1.5ms = 2048
        # 180° = 2ms = 4096
        self.min_pulse = 409    # 0度
        self.max_pulse = 4096   # 180度
        self.mid_pulse = 2048   # 90度
    
    def angle_to_duty(self, angle):
        """角度转换为占空比
        
        Args:
            angle: 角度 (0-180)
            
        Returns:
            占空比值
        """
        return int(self.min_pulse + (self.max_pulse - self.min_pulse) * angle / 180)
    
    def set_servo(self, channel, angle):
        """设置舵机角度
        
        Args:
            channel: 通道 (0-15)
            angle: 角度 (0-180)
        """
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
            
        duty = self.angle_to_duty(angle)
        self.pca.channels[channel].duty_cycle = duty
    
    def set_servo_smooth(self, channel, target_angle, step=5, delay=0.02):
        """平滑移动舵机
        
        Args:
            channel: 通道
            target_angle: 目标角度
            step: 步进角度
            delay: 步进延迟
        """
        current = 90  # 从中位开始
        while abs(current - target_angle) > step:
            if current < target_angle:
                current += step
            else:
                current -= step
            self.set_servo(channel, current)
            time.sleep(delay)
        self.set_servo(channel, target_angle)

# 测试
if __name__ == "__main__":
    servo = ServoController()
    
    print("测试舵机...")
    for i in range(9):
        servo.set_servo(i, 90)  # 所有舵机回中位
        time.sleep(0.1)
    
    print("舵机已回中位")
```

---

## Stewart 平台控制

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stewart 平台运动学控制
基于6个舵机控制上平台姿态
"""

import math
import numpy as np
from pca9685 import ServoController

class StewartPlatform:
    def __init__(self, servo_controller):
        """初始化Stewart平台
        
        Args:
            servo_controller: ServoController实例
        """
        self.servo = servo_controller
        
        # 平台参数 (需要根据实际机械结构调整)
        self.base_radius = 50    # mm - 下平台半径
        self.top_radius = 30     # mm - 上平台半径
        self.link_length = 60   # mm - 连杆长度
        
        # 6个舵机通道对应关系
        self.channels = [1, 2, 3, 4, 5, 6]
        
        # 舵机中位角度 (度)
        self.neutral_angles = [90, 90, 90, 90, 90, 90]
    
    def inverse_kinematics(self, x, y, z, roll, pitch, yaw):
        """逆运动学 - 计算各舵机角度
        
        Args:
            x, y, z: 上平台位置 (mm)
            roll, pitch, yaw: 上平台姿态 (度)
            
        Returns:
            6个舵机的目标角度列表
        """
        # 转换角度为弧度
        roll = math.radians(roll)
        pitch = math.radians(pitch)
        yaw = math.radians(yaw)
        
        # 旋转矩阵
        R = self._rotation_matrix(roll, pitch, yaw)
        
        # 计算各支点目标位置
        angles = []
        for i in range(6):
            # 下平台安装角度
            base_angle = math.radians(60 * i)
            
            # 计算上平台对应点
            base_x = self.base_radius * math.cos(base_angle)
            base_y = self.base_radius * math.sin(base_angle)
            
            # 上平台坐标 (考虑旋转)
            top_x = self.top_radius * math.cos(base_angle + math.radians(30))
            top_y = self.top_radius * math.sin(base_angle + math.radians(30))
            
            # 应用旋转
            p = np.array([top_x, top_y, 0])
            p_rotated = R @ p
            p_final = p_rotated + np.array([x, y, z])
            
            # 计算连杆长度
            dx = base_x - p_final[0]
            dy = base_y - p_final[1]
            dz = 0 - p_final[2]
            length = math.sqrt(dx**2 + dy**2 + dz**2)
            
            # 转换为舵机角度 (简化模型)
            # 实际需要更精确的标定
            angle = 90 + (length - self.link_length) * 2
            angles.append(max(0, min(180, angle)))
        
        return angles
    
    def _rotation_matrix(self, roll, pitch, yaw):
        """计算旋转矩阵"""
        # Roll (X轴)
        R_x = np.array([
            [1, 0, 0],
            [0, math.cos(roll), -math.sin(roll)],
            [0, math.sin(roll), math.cos(roll)]
        ])
        
        # Pitch (Y轴)
        R_y = np.array([
            [math.cos(pitch), 0, math.sin(pitch)],
            [0, 1, 0],
            [-math.sin(pitch), 0, math.cos(pitch)]
        ])
        
        # Yaw (Z轴)
        R_z = np.array([
            [math.cos(yaw), -math.sin(yaw), 0],
            [math.sin(yaw), math.cos(yaw), 0],
            [0, 0, 1]
        ])
        
        return R_z @ R_y @ R_x
    
    def set_pose(self, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        """设置平台姿态
        
        Args:
            x, y, z: 位置 (mm)
            roll, pitch, yaw: 姿态 (度)
        """
        angles = self.inverse_kinematics(x, y, z, roll, pitch, yaw)
        
        for i, channel in enumerate(self.channels):
            self.servo.set_servo(channel, angles[i])
    
    def home(self):
        """回中位"""
        for i, channel in enumerate(self.channels):
            self.servo.set_servo(channel, self.neutral_angles[i])

# 测试
if __name__ == "__main__":
    servo = ServoController()
    platform = StewartPlatform(servo)
    
    print("Stewart平台回中位...")
    platform.home()
```

---

## 语音识别 (ReSpeaker)

### 安装依赖

```bash
# 麦克风驱动
git clone https://github.com/respeaker/respeaker_for_raspberrypi.git
cd respeaker_for_raspberrypi
sudo ./install.sh

# 语音识别 (替代已停服的Snowboy)
sudo pip3 install pvporcupine
```

### 唤醒词检测 (Porcupine)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音唤醒 - 使用 Porcupine (替代已停服的Snowboy)
"""

import pvporcupine
import pyaudio
import numpy as np

class WakeWordDetector:
    def __init__(self, access_key=None, keywords=["picovoice"]):
        """初始化唤醒词检测
        
        Args:
            access_key: Porcupine API Key (免费申请)
            keywords: 唤醒词列表
        """
        self.access_key = access_key or "YOUR_PORCUPINE_KEY"
        self.keywords = keywords
        
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keywords=keywords
            )
            
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.porcupine.sample_rate,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            print(f"唤醒词检测已启动，唤醒词: {keywords}")
            
        except Exception as e:
            print(f"初始化失败: {e}")
            self.porcupine = None
    
    def listen(self):
        """监听唤醒词
        
        Returns:
            True 表示检测到唤醒词
        """
        if not self.porcupine:
            return False
            
        try:
            audio_data = self.stream.read(
                self.porcupine.frame_length,
                exception_on_overflows=False
            )
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            
            result = self.porcupine.process(audio_np)
            return result >= 0
            
        except Exception as e:
            return False
    
    def wait_for_wake(self):
        """等待唤醒"""
        print("等待唤醒词...")
        while not self.listen():
            pass
        print("✓ 检测到唤醒词!")
        return True
    
    def close(self):
        """关闭"""
        if self.porcupine:
            self.porcupine.delete()
        if self.stream:
            self.stream.close()
        if self.audio:
            self.audio.terminate()

# 测试
if __name__ == "__main__":
    detector = WakeWordDetector(
        access_key="YOUR_PORCUPINE_KEY",
        keywords=["picovoice", "alexa"]
    )
    
    try:
        detector.wait_for_wake()
    finally:
        detector.close()
```

---

## 语音识别 (STT)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音转文字 (Speech to Text)
"""

import speech_recognition as sr
import time

class VoiceRecognizer:
    def __init__(self, language="zh-CN"):
        """初始化语音识别
        
        Args:
            language: 语言代码
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        
        # 环境噪声校准
        with self.microphone as source:
            print("正在校准麦克风...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("麦克风校准完成")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """监听语音
        
        Args:
            timeout: 等待说话超时时间
            phrase_time_limit: 最大录音时长
            
        Returns:
            识别到的文本，失败返回None
        """
        try:
            with self.microphone as source:
                print("请说话...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # 使用Google语音识别 (需要联网)
            text = self.recognizer.recognize_google(
                audio,
                language=self.language
            )
            print(f"识别结果: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("等待超时")
        except sr.UnknownValueError:
            print("未能识别语音")
        except sr.RequestError as e:
            print(f"识别服务错误: {e}")
        
        return None
    
    def listen_loop(self, on Recognized):
        """持续监听循环
        
        Args:
            on_recognized: 识别成功回调函数
        """
        print("开始持续监听 (Ctrl+C退出)")
        try:
            while True:
                text = self.listen()
                if text and on_recognized:
                    on_recognized(text)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n监听已停止")

# 测试
if __name__ == "__main__":
    recognizer = VoiceRecognizer(language="zh-CN")
    recognizer.listen_loop(lambda text: print(f"你说: {text}"))
```

---

## 摄像头控制

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摄像头控制 - 使用 libcamera
"""

import cv2
import numpy as np

class Camera:
    def __init__(self, width=640, height=480):
        """初始化摄像头
        
        Args:
            width, height: 分辨率
        """
        self.width = width
        self.height = height
        
        # 尝试打开摄像头
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("警告: 无法打开摄像头")
        else:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            print(f"摄像头已打开: {width}x{height}")
    
    def read(self):
        """读取帧
        
        Returns:
            numpy数组，失败返回None
        """
        if not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def detect_face(self, frame):
        """人脸检测
        
        Args:
            frame: 摄像头帧
            
        Returns:
            人脸区域列表 [(x,y,w,h), ...]
        """
        # 加载Haar级联分类器
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces
    
    def get_face_center(self, faces):
        """获取人脸中心
        
        Args:
            faces: 人脸区域列表
            
        Returns:
            (x, y) 中心坐标，无人脸返回None
        """
        if len(faces) == 0:
            return None
        
        # 取最大的人脸
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        
        return (x + w // 2, y + h // 2)
    
    def close(self):
        """关闭摄像头"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

# 测试
if __name__ == "__main__":
    camera = Camera()
    
    print("按 'q' 退出")
    while True:
        frame = camera.read()
        if frame is None:
            break
        
        # 人脸检测
        faces = camera.detect_face(frame)
        
        # 绘制人脸框
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow('Camera', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.close()
```

---

## 主程序示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reachy Mini 主程序
"""

from pca9685 import ServoController
from stewart import StewartPlatform
from voice import VoiceRecognizer
from camera import Camera
import time

def main():
    print("=" * 50)
    print("Reachy Mini 桌面机器人")
    print("=" * 50)
    
    # 初始化各模块
    print("\n[1/4] 初始化舵机控制器...")
    servo = ServoController()
    
    print("[2/4] 初始化Stewart平台...")
    platform = StewartPlatform(servo)
    platform.home()
    time.sleep(1)
    
    print("[3/4] 初始化语音识别...")
    voice = VoiceRecognizer(language="zh-CN")
    
    print("[4/4] 初始化摄像头...")
    cam = Camera()
    
    print("\n✓ 系统初始化完成!")
    print("语音指令: '你好' / '向左' / '向右' / '抬头' / '低头'")
    print("按 Ctrl+C 退出\n")
    
    # 主循环
    try:
        while True:
            # 语音识别
            text = voice.listen(timeout=3)
            
            if text:
                text = text.lower()
                
                # 处理指令
                if "你好" in text or "hello" in text:
                    platform.set_pose(z=10)
                    time.sleep(0.5)
                    platform.home()
                    
                elif "左" in text:
                    platform.set_pose(x=-20)
                    time.sleep(0.5)
                    platform.home()
                    
                elif "右" in text:
                    platform.set_pose(x=20)
                    time.sleep(0.5)
                    platform.home()
                    
                elif "上" in text or "抬头" in text:
                    platform.set_pose(pitch=-20)
                    time.sleep(0.5)
                    platform.home()
                    
                elif "下" in text or "低头" in text:
                    platform.set_pose(pitch=20)
                    time.sleep(0.5)
                    platform.home()
                
                print(f"执行: {text}")
            
            # 人脸追踪 (可选)
            frame = cam.read()
            if frame is not None:
                faces = cam.detect_face(frame)
                center = cam.get_face_center(faces)
                
                if center:
                    x, y = center
                    # 简单追踪
                    if x < 320 - 50:
                        platform.set_pose(x=-15)
                    elif x > 320 + 50:
                        platform.set_pose(x=15)
                    else:
                        platform.home()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n正在退出...")
    
    finally:
        platform.home()
        cam.close()
        print("✓ 已退出")

if __name__ == "__main__":
    main()
```

---

## 依赖安装脚本

```bash
#!/bin/bash
# install_dependencies.sh

echo "安装系统依赖..."
sudo apt update
sudo apt install -y python3-pip python3-smbus i2c-tools
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y portaudio19-dev python3-pyaudio

echo "安装Python依赖..."
pip3 install --user adafruit-circuitpython-pca9685
pip3 install --user numpy
pip3 install --user opencv-python
pip3 install --user SpeechRecognition
pip3 install --user pvporcupine

echo "启用I2C接口..."
sudo raspi-config  # 手动开启 I2C

echo "✓ 依赖安装完成"
```
