## 项目细节简述:

设备：NVIDIA Jetson NANO 

神经网路：Yolov4-tiny

使用框架：Darknet

数据来源：戴口罩、不戴口罩和不正确佩戴口罩，一共800多张(已标注数据集https://pan.changchen.cc/%E5%9B%BE%E7%89%87/images.zip)

## 准备工作：

安装Darknet框架（教程：https://www.jianshu.com/p/813342202837）

```
git clone https://github.com/AlexeyAB/darknet.git
```

```
cd darknet
vim Makefile
```

修改下面三个参数（记得把自己cuda加进环境变量）

![](https://cdn.jsdelivr.net/gh/kevinchangg/BlogImage/20211202212553.png)


```
   make
```

等待一段时间后，我们测试一下,下载官方训练完毕的权重

```
wget https://pjreddie.com/media/files/yolov3-tiny.weights
```

```
./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/dog.jpg
```

你会看到以下效果:

![](https://cdn.jsdelivr.net/gh/kevinchangg/BlogImage/20211203154735.png)

自此darknet安装完毕

点击 https://pjreddie.com/media/files/darknet53.conv.74 下载 darknet53.conv.74模型（153MB）到darknet安装目录

将项目克隆到 jetson nano


```
   git clone https://github.com/kevinchangg/maskDetection_jetson.git
```

## 执行步骤：

```
cd maskDetection_jetson
```

将我提供给的数据集，解压并且重新命名为dataset，并放在当前目录下(xml+jpg)

执行下面指令，会协助您执行三件工作：

- 将所有 .xml 格式的标注，转换成 darkent 可识别的 .txt 格式
- 建立模型训练的图像列表 train.txt ，需要用完整路径
- 建立模型训练的测试列表 test.txt ，需要用完整路径

```
./0_dataDispatch.py
```

修改 mask.data 文件，提供每个设定文件的正确绝对路径

从 Darknet 目录（根据实际路径调整指令）复制yolov4-tiny-custom.cfg 到本目录

- 这里可以选择不同的 .cfg 设定文件，修改变量的方式雷同

```
cp ~/darknet/cfg/yolov4-tiny-custom.cfg .
```

修改以下三个变量值：

- 第 220行 与 269行：**classes=80 改成 classes=3**
- 第 212行 与 263行：**filters=255 改成 filters=24**
- 第 20行：**max_batches=500200 改成 max_batches=5000**，便于在 Jetson 直接模型训练

要在Jetson上执行模型训练，请修改的 batch与subdivisions 的值，如下：

- batch=16, subdivisions=2

修改 train_mask.sh 里面 DARKNET 与 PRJ_PATH 的绝对路径，例如

- export DARKNET=$HOME/darknet
- export PRJ_PATH=$HOME/maskDetection_jetson
- 存档后执行下面指令进行模型训练，**在 Jetson Nano 4GB 下大约 90分钟**

```
./1_trainMask.sh
```

训练好模型之后，依旧需要用 yolov4-tiny-custom.cfg 配置文件进行推理计算，修改下面两处参数

- batch=1, subdivisions=1

  存档后执行下面指令进行推理

  ```
  ./2_demoMask.sh
  ```

  

  请自行调整 2_demoMash.sh 脚本最后的数据源，可以是视频、CSI摄像头、USB摄像头

  如果是调用csi摄像头

  ```
  ./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, width=1280, height=720, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink"
  ```

  

关于其他参考文章：

https://zhuanlan.zhihu.com/p/363839453

https://zhuanlan.zhihu.com/p/357438016

https://blog.csdn.net/weixin_44198954/article/details/106785299
