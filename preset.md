# x264编码参数,无损并最高压缩

-vcodec libx264 -preset placebo -threads 1 -x264-params qp=0:keyint=infinite:no-psy=1:no-scenecut=1:ref=16:merange=32:no-dct-decimate=1:partitions=all:no-fast-pskip=1:rc-lookahead=250:bframes=16:b-adapt=2

# x264编码参数,无损并最快速度

-vcodec libx264 -preset ultrafast -threads 1 -x264-params qp=0:keyint=120:no-scenecut=1:aq-mode=0:no-mbtree=1:direct=none:no-weightb=1:weightp=0:me=dia:merange=4:subme=0:no-psy=1:no-mixed-refs=1:no-chroma-me=1:no-8x8dct=1:trellis=0:bframes=0:no-cabac=1:ref=0:no-deblock=1:rc-lookahead=0

# x265编码参数,无损并最高压缩(x265新手,仅供参考),很慢(慢的超乎想象)但压缩比不错,x265还是比x264复杂太多了

-vcodec libx265 -preset placebo -threads 1 -x265-params log-level=full:pools=none:lossless=1:ref=16:rd=6:ctu=64:min-cu-size=8:qg-size=8:no-limit-modes=1:rskip=0:no-sao=1:tu-intra-depth=4:tu-inter-depth=4:max-tu-size=32:max-merge=5:me=full:subme=7:merange=32:keyint=-1:rc-lookahead=250:bframes=16:b-adapt=2

# 当然了,还是建议直接去修改"x264_param_t"结构体,比命令行直观一些

# 下面附上一些客服给我的信息

![码率上限2020.png](https://github.com/hg56th56gd6g/BiliVideo/blob/main/%E7%A0%81%E7%8E%87%E4%B8%8A%E9%99%902020.png)

![码率上限2022.png](https://github.com/hg56th56gd6g/BiliVideo/blob/main/%E7%A0%81%E7%8E%87%E4%B8%8A%E9%99%902022.png)

4K 投稿参数
推荐分辨率4096x2160(短边>=1600)最大不超过4096x4096
帧率最大支持120fps
关键帧平均至少10秒1个
视频码率建议20000kbps(H264/AVC编码)
视频峰值码率建议不超过60000kbps
色彩空间yuv420
位深8bit
音频码率最高320kbps(AAC编码)
声道数≤2
采样率=44100(48000?)

逐行扫描

8K 投稿参数
视频编码标准:H265
推荐分辨率7680x4320(短边>=3200)
帧率投稿不限制(120?)
推荐码率60000kbps
峰值码率180000kbps
色深8bit
编码H.265
