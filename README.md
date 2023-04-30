# Seq2seq Chatbot

## Introduction to the Project:

在利用Seq2Seq做完Abstractor之后，总感觉意犹未尽。碰巧，大创选题为"GPT4Dispatching",即“基于GPT的调度辅助决策系统”。于是，我想到了利用Seq2Seq做一个聊天机器人，作为调度辅助决策系统的一部分，也算是当作大创项目的序章了。后续，或许会将此项目作为辅助决策系统的人机交互界面（未来的事情谁说得准呢？）。

## Explain to Each Folder and File:

本项目基于Pytorch实现，Java实现了一个简单的GUI，用于与聊天机器人交互。项目结构如下：

    ChatApp/: Java GUI Project
    
    config/: 参数配置文件

    icons/: 图片库，用于Java GUI

    train_data/: 训练数据以及预处理后的数据、模型

    data.py: 数据预处理文件

    execute.py: 训练文件

    runner.py: Python模型与Java GUI的接口文件

    seq2seqModel.py: Seq2Seq模型文件

## Recommend Environment:

    Java 8, Python: 3.8.16, Pytorch: 1.12
    其它Python库，如 Flask, numpy, nltk

## Running Procedures:

如果你仅仅是为了体验该项目，在配置好相关环境后控制台输入`python runner.py`即可(我已经将训练了30轮的模型放入train_data中，说实话，我没有写分布式训练相关模块，训练起来挺慢的)。

如果你想要训练模型，那么你需要：
1. 删除train_data文件夹中的相关文件，包括：`data_model.pt`。
2. 输入`python execute.py`，开始训练。

如果你想要用自己的数据集训练模型，那么你需要：
1. 仔细阅读`data.py`中的注释，修改其中的数据预处理部分，使其适应你的数据集。
2. 仔细阅读`execute.py`中的注释，修改其中的训练部分，使其适应你的数据集。
3. 配置`seq2seq.ini`中的参数，使其适应你的数据集。
4. 输入`python data.py`，开始数据预处理。
5. 输入`python execute.py`，开始训练。

## Possible Problems:

1. 由于本项目使用了nltk库，所以可能会需要下载一些数据集，如：`nltk.download('punkt')`。
2. 由于本项目使用了SubprogressBar库，所以可能会需要将外部库的`progressbar.py`文件中的`shell=False`改为`shell=True`。
3. 由于本项目使用了Java GUI，所以请确保你的Java环境配置正确，特别是javac命令。


## TODO

- [x] 项目框架搭建
- [x] 数据预处理
- [x] 模型搭建
- [x] 模型训练
- [x] Java GUI
- [ ] 模型评估
- [ ] 分布式训练
- [ ] 前端优化
- [ ] 中文预料集

我已经将中文语料的获取方式放到了我的另一个仓库中，同时，网页版ChatBot也在开发中（本项目的dev分支），欢迎大家关注。