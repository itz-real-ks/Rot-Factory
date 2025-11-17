# 2Version@

from moviepy import VideoFileClip
from pathlib import Path
import argparse


class VideoProcessor:
    """
    A lightweight video processing utility using MoviePy.
    Can be imported as a library or used standalone.
    """

    def __init__(self, input_path: str, output_path: str = None, audio: bool = False):
        self.input_path = Path(input_path).expanduser().resolve()
        self.output_path = Path(output_path) if output_path else self._default_output_path()
        self.audio = audio
        self.clip = None

    def _default_output_path(self) -> Path:
        """Generate default output path (e.g., input_cropped.mp4)."""
        return self.input_path.with_name(self.input_path.stem + "_cropped.mp4")

    def load(self, start_time: float = 0, end_time: float = None):
        """Load and optionally subclip the video."""
        clip = VideoFileClip(str(self.input_path), audio=self.audio)
        if end_time is not None:
            clip = clip.subclipped(start_time, end_time)
        self.clip = clip
        return self

    def export(self, preset: str = "ultrafast", threads: int = 4, overwrite: bool = True):
        """Write processed clip to file."""
        if self.clip is None:
            
            raise RuntimeError("No video loaded. Call load() first.")

        output_path = str(self.output_path)
        if not overwrite and Path(output_path).exists():
            raise FileExistsError(f"Output file already exists: {output_path}")

        self.clip.write_videofile(
            output_path,
            fps=self.clip.fps,
            codec="libx264",
            audio=self.audio,
            threads=threads,
            preset=preset,
            logger=None  # disable progress bar for faster, cleaner runs
        )
        return output_path

    def close(self):
        """Safely close the clip to free resources."""
        if self.clip:
            self.clip.close()
            self.clip = None


def main():
    parser = argparse.ArgumentParser(
        description="Video cropping and exporting utility using MoviePy."
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: input_cropped.mp4)"
    )
    parser.add_argument(
        "-s", "--start", type=float, default=0, help="Start time in seconds"
    )
    parser.add_argument(
        "-e", "--end", type=float, help="End time in seconds"
    )
    parser.add_argument(
        "-a", "--audio", action="store_true", help="Enable audio export"
    )
    parser.add_argument(
        "-p", "--preset", default="ultrafast", help="Encoding preset (default: ultrafast)"
    )
    args = parser.parse_args()

    processor = VideoProcessor(args.input, args.output, audio=args.audio)
    processor.load(start_time=args.start, end_time=args.end)
    output_path = processor.export(preset=args.preset)
    processor.close()

    print(f"✅ Exported successfully to: {output_path}")


if __name__ == "__main__":
    main()
