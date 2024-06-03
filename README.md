# 图书馆智能寻书系统

本项目基于 [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) 开发

项目简介：用户可以输入自己对某种图书的需求，图书知识库将自动推荐一本书，在用户指定当前位置后，便可以将用户导航到该处

### 项目结构

```
Intelligent_Library/
│
├── configs # 模型及模型的一些设置
├── server # 模型服务器
├── knowledge_base # 知识库
├── Library # 关于图书馆的一些配置文件
    ├── library.jpg # 图书馆的彩色地图
    ├── library_gray.jpg # 图书馆的灰度地图，用于导航
    ├── books.json # 书的配置文件
    ├── location.json # 书架位置的配置文件
├── README.md # 项目简介文件
├── start_up.py # Longchain_Chatchat启动脚本
├── setup_books.py # 图书配置脚本
├── setup_location.py # 位置配置脚本
└── ui_gradio.py # gradio前端启动脚本
```

其余文件与Langchain-Chatchat项目相同

### 配置

先安装必要的依赖：
```
pip install -r requirements.txt
```

之后，按照项目结构中的说明修改Library/文件夹下的内容

`location.json`的格式类似于：
```
{"0": [602, 210]} # "0"为位置编号，[602, 210] 为图像中的坐标
```
`books.json`的格式类似于：
```
{"0" : ["太白金星有点烦"]} # "0"为位置编号，["太白金星有点烦"]为图书列表
```

你可以借助`setup_books.py`和`setup_location.py`完成这一步骤

你可以借助`setup_map.py`将`Library/library.jpg`转换为二值化之后的地图。注意自适应二值化方法只是给出了一个粗糙的结果，精细调整可能需要其他的cv方法 ~~（或者直接PS）~~

### 运行

先运行
```
python3 startup.py --all-api
```

等所有服务启动完成之后，再启动一个终端，运行
```
python3 ui_gradio.py
```

你应该会在输出中看到`Running on URL: 127.0.0.1:9001`，点开即可

### 注意事项

过高的`gradio`版本会与`fastapi`冲突，如果遇到这个问题，请尝试运行
```
pip install gradio==3.33.0
```

如果你的本地具有代理环境，需要关闭代理才能正常运行