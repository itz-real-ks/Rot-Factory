# Makes usabe for over cli, standalone py script , or can import a self sub dependencies 
# Version 1.0v
import argparse
from moviepy import VideoFileClip  

class AspectRatioCalculator: # Needs to allocate a var holding this obj calc=AspectRatioCalculator; then can call it with calc.x

    def __init__(self, file_location=None): # Here default loacation is = None
        self.file_location = file_location # self inits the var to call over the class

    def calculate_aspect_ratio(self, file_location=None):
        try:
            video_path = file_location or self.file_location
            if not video_path:
                raise ValueError("No video file path provided.")

            with VideoFileClip(video_path) as clip:
                aspect_ratio = clip.w / clip.h
                clip.close
            return aspect_ratio
        except Exception as e:
            raise Exception(f"Error calculating aspect ratio: {str(e)}")

def main():
    # CLI usage: python aspect_ratio.py <video_file_path>
    parser = argparse.ArgumentParser(description="Calculate the aspect ratio of a video file")
    parser.add_argument("video_file", help="Path to the video file")
    args = parser.parse_args()

    calculator = AspectRatioCalculator(args.video_file)
    try:
        aspect_ratio = calculator.calculate_aspect_ratio()
        print(f"Aspect ratio: {aspect_ratio:.3f}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
