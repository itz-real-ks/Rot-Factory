from moviepy import *

class Resize:
    def __init__(self):
        pass

    def resizer(self, file):
        if file:
            clip = VideoFileClip(file)
            # Create a black background clip
            background = ColorClip(size=(720, 1280), color=(0,0,0)).with_duration(clip.duration)
            # Resize the video clip
            resized_clip = clip.resized(height=720)  # Resize to fit the width
            if resized_clip.w > 1280:  # If the width is still larger than 1280, resize based on width
                resized_clip = clip.resized(width=1280)
            # Position the resized clip at the center of the background
            position = ((720 - resized_clip.w) // 2, (1280 - resized_clip.h) // 2)
            final_clip = CompositeVideoClip([background, resized_clip.with_position(position)])
            return final_clip


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Used to force resize the video to 720x1280")
    parser.add_argument("video_file", help="Path to the video file")
    parser.add_argument("-o", "--output", help="Path to the output video file", default="resized_video.mp4")
    args = parser.parse_args()

    video_resizer = Resize()
    clip = video_resizer.resizer(args.video_file)
    clip.write_videofile(args.output, codec="libx264", audio_codec=None, threads=4, preset="ultrafast", ffmpeg_params=["-crf", "28"])
    print(f"Resized video saved to {args.output}")


if __name__ == "__main__":
    main()