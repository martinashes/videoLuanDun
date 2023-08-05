# 准备材料：
1. 原始视频mp4格式，视频主画面必须在（从上往下）650像素-1250像素间
2. 标题文字，png透明底格式，1080*600大小，文件名与原始视频对应(video1, head1)
3. 背景图（可选）1080*1920大小, jpg格式

# 文件夹
- video 存放原始视频
- head 存放标题文字截图
- background 存放要替换的背景图

# 代码实现逻辑：
- 遍历文件夹中所有的视频
- 每个视频都会遍历所有背景图
- Step 1: 获取原视频的时长
- Step 2: 新建一个1080*1920的视频，并设置背景为背景图
- Step 3: 导入原视频，裁剪主画面并放置在（0，650）的位置
- Step 4: 导入标题文字放置于（0，160）的位置
- Step 5: 裁剪原视频字幕并放置在（0，1410）的位置
- Step 6: 整合所有素材并导出视频

# moviepy的一些奇怪bug
## 1.使用TextClip.list('font')时报错
**错误信息**

    UnicodeDecodeError: 'utf-8' codec can't decode byte 0x98 in position 8: invalid start byte

**解决办法**  

首先定位到moviepy\video\https://link.zhihu.com/?target=http%3A//videoclip.py/， line 1208，用编辑器打开，找到如下代码

    if arg == 'font':
        return [l.decode('UTF-8')[8:] for l in lines if l.startswith(b"  Font:")]

在Windows上decode('UTF-8')会出错，替换为ANSI编码

    if arg == 'font':
        #return [l.decode('UTF-8')[8:] for l in lines if l.startswith(b"  Font:")]
        return [l.decode('ANSI')[8:] for l in lines if l.startswith(b"  Font:")]

保存即可

## 2.使用CompositeVideoClip()时报错
**错误信息**

    ValueError: Attribute 'duration' not set

**解决办法**

定位到moviepy\video\compositing\compositevideoclip.py/, line 47，找到如下代码

    def __init__(self, clips, size=None, bg_color=None, use_bgclip=False, ismask=False)

加一个duration参数，修改为

    def __init__(self, clips, size=None, bg_color=None, use_bgclip=False,ismask=False, duration=1)

然后在当前文件line 73处附近找到

    VideoClip.__init__(self)
            
    self.size = size
    self.ismask = ismask
    self.clips = clips
    self.bg_color = bg_color

加一行self.duration = duration

    VideoClip.__init__(self)
            
    self.size = size
    self.ismask = ismask
    self.clips = clips
    self.bg_color = bg_color
    self.duration = duration
`
保存文件，并注意使用CompositeVideoClip时加上duration参数

    final_clip = CompositeVideoClip([main_clip, text_clip.set_pos(("left","top"))], duration=main_clip.duration)

# Todo list
- 解决外挂SRT字幕的问题
- 解决视频导出速度慢的问题