import cv2
from moviepy import VideoFileClip
from moviepy import CompositeAudioClip
from moviepy import AudioFileClip

import math
import moviepy.video.io.ffmpeg_tools

def mix_audio_to_video(pathVideoInput, pathVideoNonAudio, pathVideoOutput):
  audioclip = AudioFileClip("audio.mp3")
  new_audioclip = CompositeAudioClip([audioclip])
  videoclipNew = VideoFileClip(pathVideoNonAudio)
  videoclipNew.audio = new_audioclip
  videoclipNew.write_videofile(pathVideoOutput)
  return videoclipNew

def fix(file):
    cap = cv2.VideoCapture(file)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f'Checking Video {frames} Frames {frames} fps: {fps}')
    if frames < 1:
        print(f'No frames data in video {file}, trying to convert this video..')
        framecount = 0
        while True:
            ret, frame = cap.read()
            if ret is True:
                framecount += 1
            else:
                break
        cap = cv2.VideoCapture(file)
        print(framecount)
        temp = moviepy.video.io.ffmpeg_tools.ffmpeg_extract_audio(file, "audio.mp3")
        audioclip = AudioFileClip("audio.mp3")
        framerate = math.floor(framecount / audioclip.duration)

        print(framerate)
        writer = cv2.VideoWriter("fixVideo.avi", cv2.VideoWriter.fourcc(*'DIVX'),
                                 (int(framerate)),
                                 (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        i =0
        while True:
            ret, frame = cap.read()
            i += 1
            if ret is True:
                writer.write(frame)
            else:
                cap.release()
                print(f"Stopping video writer at frame {i}")
                writer.release()
                writer = None
                break
    return mix_audio_to_video(file, "fixVideo.avi", "fixVideo.mp4")
