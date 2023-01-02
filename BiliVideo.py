#-*- coding:utf-8 -*-
#本脚本仅适用于一般的简单情况(适用于大多数场景),复杂情况(如输入原始yuv文件等)建议手动调试
#H264/AVC编码,像素格式yuv420p(nv12,见"ffmpeg -pix_fmts"),关键帧至少10s一个,在"-x264-params"里bitrate单位是k
#1pass没有ACodec和Output,参数顺序:Input,VCodec,Width,Height,Fps,ACodec,Output
BaseCommand="ffmpeg -i \"%s\" %s -s %dx%d -r %s %s \"%s\""
BaseCommandPass1="ffmpeg -i \"%s\" %s -s %dx%d -r %s -pass 1 -an -f null NUL"
BaseCommandPass2="ffmpeg -i \"%s\" %s -s %dx%d -r %s -pass 2 %s \"%s\""
#每个尺寸下的参数(最大宽,最大高,最大fps,音频流编码设置(可被覆盖),视频流编码设置(可被覆盖)),应该按照从低到高排序
#注意.对于视频流编码设置,会将两个百分号及之间的内容解析为一个算式,其中"Fps"(变量名)代表Fps,使用连续的两个百分号来转义
#例如:"-vcodec libx264 -x264-params bitrate=6000:keyint=%Fps*8%:min-keyint=%Fps%"
#Fps=60,解析为:"-vcodec libx264 -x264-params bitrate=6000:keyint=480:min-keyint=60"
#最后两个参数的意思是:关键帧间隔最多8s,最少1s,此功能设计的目的就是为了关键帧间隔
#关于参数建议,预设建议placebo,为什么?因为强迫症!(),并且placebo隐含了slow-firstpass,线程不要开多了
#大部分参数让x264自己选择就好,除非追求极致的性能(超级大,并且快不了多少,还可能受到io的性能限制)/压缩(超级慢,并且只能小一点体积)
#关于这里的vbv参数,是将峰值码率限制到b站标准,属于比较保守比较通用的参数(几乎所有参数都是),想极限一点建议手动调试
Data=(
    #360p
    (640,360,30,
    "-acodec aac -ar 48000 -ab 64k",
    "-vcodec libx264 -preset placebo -threads 2 -x264-params bitrate=500:keyint=%Fps*8%:min-keyint=1 -pix_fmt nv12"
    ),
    #480p
    (854,480,30,
    "-acodec aac -ar 48000 -ab 128k",
    "-vcodec libx264 -preset placebo -threads 2 -x264-params bitrate=900:keyint=%Fps*8%:min-keyint=1 -pix_fmt nv12"
    ),
    #720p
    (1280,720,30,
    "-acodec aac -aac_coder fast -ar 48000 -ab 320k",
    "-vcodec libx264 -preset placebo -threads 2 -x264-params bitrate=2000:keyint=%Fps*8%:min-keyint=1 -pix_fmt nv12"
    ),
    #1080p,1080p+,1080p60,建议6m,峰值24m
    (1920,1080,60,
    "-acodec aac -aac_coder fast -ar 48000 -ab 320k",
    "-vcodec libx264 -preset placebo -threads 2 -x264-params bitrate=6000:keyint=%Fps*8%:min-keyint=1:vbv-maxrate=9000:vbv-bufsize=15000 -pix_fmt nv12"
    ),
    #4k,对4k的定义比较模糊,建议20m,峰值60m
    (4096,4096,120,
    "-acodec aac -aac_coder fast -ar 48000 -ab 320k",
    "-vcodec libx264 -preset placebo -threads 2 -x264-params bitrate=20000:keyint=%Fps*8%:min-keyint=1:vbv-maxrate=26000:vbv-bufsize=34000 -pix_fmt nv12"
    )
)
if __name__=="__main__":
    from sys import argv
    from os import system
    from re import sub
    #解析命令行
    Input=argv[1]
    Output=argv[2]
    Width=int(argv[3])
    Height=int(argv[4])
    Fps=int(argv[5])
    Pass2=False if argv[6]=="False" else True if argv[6]=="True" else None
    CV=argv[7] if argv[7]!="None" else None
    CA=argv[8] if argv[8]!="None" else None
    #解析VCodec用
    def Eval(Matched):
        Matched=Matched.group()
        if Matched=="%%":
            return "%"
        return str(eval(Matched[1:-1:]))
    #依次观察是否符合尺寸,注意不能区分相同分辨率不同帧率(懒,也用不到,有兴趣的可以自己写一下)
    for Now in Data:
        if Width<=Now[0] and Height<=Now[1]:
            #fps超出这个分辨率的要求,但继续编码
            if not Fps<=Now[2]:
                print("Warning:Fps is too large")
                system("pause")
            #设置acodec,vcodec
            ACodec,VCodec=Now[3::]
            if CV:
                VCodec=CV
            if CA:
                ACodec=CA
            #解析vcodec
            VCodec=sub("%[\s\S]*?%",Eval,VCodec)
            #是否2pass
            if Pass2:
                system(BaseCommandPass1%(Input,VCodec,Width,Height,Fps))
                system(BaseCommandPass2%(Input,VCodec,Width,Height,Fps,ACodec,Output))
            else:
                system(BaseCommand%(Input,VCodec,Width,Height,Fps,ACodec,Output))
            #完成
            print("====OK====")
            exit()
    #不符合所有尺寸
    print("Error:Unsupported size")
#编写/整理参数(这是重点!)花了我一个多小时(并且是未阳康状态!),支持一下吧qwq,"preset.md"里面包括了一些预设