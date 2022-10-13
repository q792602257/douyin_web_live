# 抖音web直播间([live.douyin.com](https://live.douyin.com))弹幕抓取


> ### 近期工作内容比较繁重，大概率会摸一段时间 (from:Jerry-Yan-0912)
> 
> ### 实现功能： 
> 1. 使用新版mitmproxy，使mitmproxy进程跑在主进程里，兼容Python3.10
> 2. 数据无磁盘IO，通过Queue请求传输proto数据，如果对弹幕发送时间要求较高的，可以使用消息对象中的时间 
> 3. 修改输出为组件化，后期通过配置进行启用或禁用，开发者也可以自行编写对应的保存逻辑 
> 4. 自动打开配置的房间及用户首页 
>  
> ### 对其中的修改： 
> 1. 删除了mongo相关内容（以后补吧……，重写一个也不麻烦）  
> 
> ### 待实现功能（咕）： 
> 1. 未开播时，自动刷新页面进行重新检测 
> 2. 下播事件触发及对应动作 
> 3. 上播事件触发及自动打开对应的房间 
> 4. 录播支持 
> 5. 异步输出支持 

### **如何配置**
1. 首先把`example/settings.yml`复制到根目录
2. 下载对应浏览器`WebDriver`驱动
   - [Chrome浏览器](https://chromedriver.chromium.org/downloads "官网下载") [国内镜像](https://registry.npmmirror.com/binary.html?path=chromedriver/ "淘宝镜像")
3. 配置`WebDriver`驱动可执行文件目录（根据配置注释来）
   - Chrome浏览器请配置于`webdriver.chrome.bin`
4. 配置浏览器是否需要无头`headless`模式（根据配置注释来）
   - `webdriver.headless`设置为True，浏览器打开后不会显示窗口，适合Linux服务器等无需显示的情况
   - `webdriver.headless`设置为False，浏览器打开后会显示窗口，更适合需要自己手动操作浏览器等其他需要显示情况
5. 配置输出插件(`output.use`)，可以自由搭配使用（根据配置注释来）
   - `print`：控制台打印的组件，收到弹幕信息会在控制台中输出
   - `xml`：B站弹幕姬相兼容的弹幕格式，适用于后期与视频叠加或分析
   - `debug`：开发或测试使用，会保存所有未处理的消息类型，及保留报错信息，方便后期维护排查
6. 配置默认需要打开的房间及用户主页（根据配置注释来）
   - `live.rooms`: 填写房间号（链接地址最后一串数字），或者完整链接地址
   - ~~`live.users`: 填写用户加密ID（用户首页链接地址最后一串字符串），或者完整链接地址~~ *（暂无任何用途）* 

## 运行步骤：

1. 安装依赖 `pip install -r requirements.txt`
2. 按照上述步骤进行配置
3. 运行`main.py`


## **屏幕效果截图**

![enter image description here](https://github.com/FedoraLinux1/douyin_web_live/blob/main/20220519190807.png)


### 配置文件说明

- `mitm`：mitmproxy相关配置
  - `host`：mitmproxy监听地址，_无特殊要求不建议修改_
  - `port`：mitmproxy监听端口，_无特殊要求不建议修改_
- `webdriver`：浏览器WebDriver相关配置
  - `headless`：是否开启无头模式，`True/False`
  - `use`：使用哪个浏览器，`chrome/edge`
  - `edge`：Edge浏览器相关配置，用谷歌可以不管这个
    - `bin`：webdriver可执行文件路径
  - `chrome`：Chrome浏览器相关配置，用Edge的可以不管这个
    - `bin`：webdriver可执行文件路径
    - `no_sandbox`：是否添加`--no-sandbox`启动参数，用于root用户启动浏览器，`True/False`
- `output`：输出相关配置
  - `use`：使用的输出模块，为一个数组，`print/xml/debug`
  - `xml`：XML输出模块相关配置
    - `save_path`：_预留内容，实际没有作用_
    - `file_pattern`：xml文件名称格式，现在也只有默认的这个，待后续开发
  - `debug`：Debug输出模块相关配置
    - `save_path`：保存路径相关配置
      - `error`：如果遇见错误，将错误存储在这个路径下
      - `debug`：如果遇见未处理的消息类型，将该消息存储在这个路径下
      - `known`：_预留内容，实际没有作用_
- `live`：直播间相关配置
  - `rooms`：房间号（链接地址最后一串数字），或者完整链接地址，为一个数组
  - `users`：用户加密ID（用户首页链接地址最后一串字符串），或者完整链接地址 ，为一个数组
- `api`：这个现在暂时没啥用了……
  - `userinfo`：……
