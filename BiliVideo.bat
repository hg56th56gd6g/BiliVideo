@echo off
echo path类型如果路径中带空格,两边要加双引号,bool类型只能是"True"或"False"(不带引号)
set /p a=input_video_path(path):
set /p b=output_video_path(path):
set /p c=output_video_width(int):
set /p d=output_video_height(int):
set /p e=output_video_fps(int):
set /p f=2pass(bool):
set /p g=video_codec(str/"None"):
set /p h=audio_codec(str/"None"):
python BiliVideo.py %a% %b% %c% %d% %e% %f% "%g%" "%h%"
pause
exit