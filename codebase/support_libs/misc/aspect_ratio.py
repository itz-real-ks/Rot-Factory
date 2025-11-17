from moviepy.editor import VideoFileClip

clip = VideoFileClip("input.mp4")
print(clip.w / clip.h)