import sys
import subprocess
import os

def ensure_ffmpeg():
    try:
        import imageio_ffmpeg
    except ImportError:
        print("Installing imageio-ffmpeg to get local FFmpeg binary...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
        import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def create_video(input_image, output_video, duration=10, fps=30):
    ffmpeg_exe = ensure_ffmpeg()
    
    frames = duration * fps
    
    # For a smooth zoom-in effect (Ken Burns), we scale up the image first (to avoid jittering),
    # then apply zoompan, then set the output framerate and size.
    # z='min(zoom+0.0015,1.5)': zoom in up to 1.5x
    # x and y calculations keep it centered.
    vf = f"scale=4000:-1,zoompan=z='min(zoom+0.0015,1.5)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps={fps}:s=1920x1080"
    
    cmd = [
        ffmpeg_exe,
        "-y",               # overwrite output file
        "-loop", "1",       # loop the single image
        "-framerate", str(fps), 
        "-i", input_image,  # input file
        "-vf", vf,
        "-c:v", "libx264",  # h.264 video codec
        "-t", str(duration),# limit duration
        "-pix_fmt", "yuv420p", # pixel format for compatibility
        output_video
    ]
    
    print(f"Generating smooth cinematic video... (This might take a few seconds)")
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"\nSuccessfully created {output_video}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create cinematic video from image")
    parser.add_argument("input_image", help="Path to input image")
    parser.add_argument("output_video", help="Path to output video")
    args = parser.parse_args()
    
    input_abs = os.path.abspath(args.input_image)
    output_abs = os.path.abspath(args.output_video)
    
    if not os.path.exists(input_abs):
        print(f"Error: Could not find {input_abs}")
        sys.exit(1)
        
    create_video(input_abs, output_abs)
