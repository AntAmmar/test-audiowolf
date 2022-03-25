import os
import subprocess

def execute(path, split_ranges = []):
    filename, extension = path.split(".")

    if len(split_ranges) > 0:
        ffmpeg_command = ["ffmpeg", "-i", path]
        for index, split_range in enumerate(split_ranges):
            format_filename = filename + str(index).zfill(3)
            output_path = ".".join([format_filename, extension])
            print(split_range[0], split_range[1])
            ffmpeg_command.extend(["-ss", str(split_range[0]), "-t", str(split_range[1]), "-c", "copy", output_path])
        print(ffmpeg_command)
        subprocess.call(ffmpeg_command)
    else:
        filename, extension = path.split(".")
        format_filename = filename + "%03d"
        output_path = ".".join([format_filename, extension])
        # subprocess.call(["ffmpeg", "-i", path, "-f", "segment", "-segment_time", AUDIO_SPLIT_DURATION, output_path])
    return []

execute('video.wav', [[160, 896]])
