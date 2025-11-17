import cv2
import numpy as np
from moviepy import VideoFileClip, CompositeVideoClip, ColorClip


class VideoCropper:
    def __init__(self, input_video: str, output_video: str,
                 mobile_width: int = 1080, mobile_height: int = 1920):
        self.input_video = input_video
        self.output_video = output_video
        self.mobile_width = mobile_width
        self.mobile_height = mobile_height

    def load_video(self) -> VideoFileClip:
        return VideoFileClip(self.input_video)

    def calculate_aspect_ratios(self, video: VideoFileClip):
        width, height = video.size
        video_aspect_ratio = width / height
        mobile_aspect_ratio = self.mobile_width / self.mobile_height
        return video_aspect_ratio, mobile_aspect_ratio

    def create_background_with_shadow(self, duration: float, fps: int) -> VideoFileClip:
        """Creates a simple darkened background matching mobile size."""
        background = ColorClip(size=(self.mobile_width, self.mobile_height), color=(0, 0, 0))
        return background.with_duration(duration).with_opacity(0.07).with_fps(fps)

    def crop_video_to_mobile(self):
        with self.load_video() as video:
            video_ar, mobile_ar = self.calculate_aspect_ratios(video)

            # Decide how to resize based on aspect ratio
            if video_ar > mobile_ar:
                # Wide video
                resized_video = video.resized(width=self.mobile_width)
                y_pos = (self.mobile_height - resized_video.h) // 2
            else:
                # Tall or square video
                resized_video = video.resized(height=self.mobile_height)
                x_pos = (self.mobile_width - resized_video.w) // 2

            # Background (dark overlay)
            background = self.create_background_with_shadow(video.duration, video.fps)

            # Compose layers
            position = ((x_pos if video_ar <= mobile_ar else 0),
                        (y_pos if video_ar > mobile_ar else 0))
            final = CompositeVideoClip(
                [background, resized_video.with_position(position)],
                size=(self.mobile_width, self.mobile_height)
            )

            # Export
            final.write_videofile(
                self.output_video,
                fps=video.fps,
                codec="libx264",
                audio_codec="aac",
                threads=4,
                preset="medium"
            )


def main():
    input_video = r"/home/forgotten/git/git_projects/Rot-Factory/codebase/support_libs/input.mp4"
    output_video = r"/home/forgotten/git/git_projects/Rot-Factory/codebase/support_libs/output.mp4"
    cropper = VideoCropper(input_video, output_video)
    cropper.crop_video_to_mobile()


if __name__ == "__main__":
    main()
