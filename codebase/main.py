from support_libs.crop_video.aspect_ratio import AspectRatioCalculator, Resize
# from moviepy import *

def video_Ratio(video_file):
    calc = AspectRatioCalculator()
    return calc.calculate_aspect_ratio(input)

def resize_video(video_file):
    if video_Ratio(video_file) != (720/1280):
        return Resize.resizer(video_file)

