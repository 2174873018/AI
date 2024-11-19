#引入相关的包
import pyautogui        #引入GUI操作包
import cv2              #引入图像识别包
import keyboard         #引入键盘录入包
import time             #引入time，用于计时
import pyperclip        #引入剪切板工具
import os               #用于导入环境变量
from openai import OpenAI   #用于调用openAI大模型

#访问openai网站需要代理，但是默认openai模块不会直接使用本地已有代理
#所以需要要指定环境变量告知其代理地址。否则API连接失败
os.environ["http_proxy"]="http://127.0.0.1:33210"
os.environ["https_proxy"]="http://127.0.0.1:33210"


#创建客户端对象
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    #base_url=os.environ.get("OPENAI_API_BASE")
    #openai默认有连接api链接，除非其他情况否则无需手动设置，模块版本要和api链接匹配。
)

#将和大模型交互的内容放于函数中
restest=" ";
messages = list()
def chat(prompt,model="gpt-4o"):
    #创建客户端聊天对象，这里messages设置请求体。
    messages.append({"role": "user","content": prompt})
    messages.append({"role":"assistant","content": restest})
    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    #返回大模型回复的数据
    return chat_completion.choices[0].message.content


#获取微信窗口
mi=pyautogui.screenshot()                                     #获取当前截屏对象
mi.save("./screen.png")                                       #存为screen文件
screen=cv2.imread("./screen.png")                             #读取屏幕截图图像数据
wechat=cv2.imread("./wechat.png")                             #读取微信图标图像数据
result=cv2.matchTemplate(screen,wechat,cv2.TM_CCOEFF_NORMED)  #匹配图像，生成相似区域数据
posi=cv2.minMaxLoc(result)[3]                                 #将数据转为4个元素的元组，选择最相近区域坐标
x=int(posi[0])+int(wechat.shape[0]/2)                         #获取按钮x坐标
y=int(posi[1])+int(wechat.shape[1]/2)                         #获取按钮y坐标
pyautogui.click(x,y,)                                         #点击按钮



#点击搜索框，搜索聊天群
mi=pyautogui.screenshot()                                     #获取当前截屏对象
mi.save("./screen.png")                                       #存为screen文件
screen=cv2.imread("./screen.png")                             #读取屏幕截图图像数据
search=cv2.imread("./search.png")                             #读取搜索图标图像数据
result=cv2.matchTemplate(screen,search,cv2.TM_CCOEFF_NORMED)  #匹配图像，生成相似区域数据
posi=cv2.minMaxLoc(result)[3]                                 #将数据转为4个元素的元组，选择最相近区域坐标
x=int(posi[0])+50                                             #获取输入框x坐标
y=int(posi[1])+int(search.shape[1]/4)                         #获取输入框y坐标
pyautogui.click(x,y)                                          #点击输入框
keyboard.write("test",0.1)                         #输入搜索内容
time.sleep(1)                                                 #等待1秒
x,y=pyautogui.position()                                      #获取当前鼠标位置
pyautogui.click(x,y+100)                                      #点击搜索结果
# keyboard.write("GUI测试，无需理会",0.1)
# pyautogui.press("enter")



#每隔两秒识别是否有@自己的人,复制提问的话，然后判断和前面是否重复，如果重复则不输出内容
copy_text=str()                                                #用一个变量来存储复制的内容
while True:
    time.sleep(2)                                              #等待两秒
    mi=pyautogui.screenshot()                                  #获取当前截屏对象
    mi.save("./screen.png")                                    #存为screen文件
    screen=cv2.imread("./screen.png")                          #读取屏幕截图图像数据
    at=cv2.imread("./at.png")                                  #读取@图标图像数据
    result=cv2.matchTemplate(screen,at,cv2.TM_CCOEFF_NORMED)   #匹配图像，生成相似区域数据
    threshold=0.8                                              #设置相似度中间阈值
    if cv2.minMaxLoc(result)[1]>threshold:                     #判断相似度是否大于0.8，如果是表示屏幕中很可能有人@自己
        print("有@自己")
        posi=cv2.minMaxLoc(result)[3]                          #将数据转为4个元素的元组，选择最相近区域坐标
        pyautogui.rightClick(posi[0],posi[1])                  #右键点击
        x=int(posi[0])+30                                      #获取复制按钮x坐标
        y=int(posi[1])+30                                      #获取复制按钮y坐标
        pyautogui.click(x,y)                                   #点击复制按钮
        if copy_text == pyperclip.paste():                     #判断内容是否重复
            print("重复内容，不输出")
        else:
            copy_text=pyperclip.paste()                        #内容不重复，写入变量
            restest=chat(copy_text[5:])                        #使用分片去除@我的部分,并调用聊天函数大模型返回回答的内容
            time.sleep(1)                                      #等AI回复完成
            mi=pyautogui.screenshot()                                     #获取当前截屏对象
            mi.save("./screen.png")                                       #存为screen文件
            screen=cv2.imread("./screen.png")                             #读取屏幕截图图像数据
            press=cv2.imread("./press.png")                               #读取微信聊天框图像数据
            result=cv2.matchTemplate(screen,press,cv2.TM_CCOEFF_NORMED)   #匹配图像，生成相似区域数据
            posi=cv2.minMaxLoc(result)[3]                                 #将数据转为4个元素的元组，选择最相近区域坐标
            x=int(posi[0])+int(press.shape[0]/2)                          #获取x坐标
            y=int(posi[1])+int(press.shape[1]/2)                          #获取y坐标
            pyautogui.click(x,y)                                          #点击微信输入框
            keyboard.write(restest,0.05)                            #将大模型返回的话输入
            keyboard.press("enter")                                       #发送输入的内容
            if len(messages)==20:     #判断聊天历史记录列表是否达到20条
                messages.pop(0)       #如果有删除一条用户说的话
                messages.pop(0)       #再删除一条机器回复的话
    else:                                                      #没人@执行
        print("无@自己")