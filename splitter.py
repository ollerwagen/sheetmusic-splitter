import cv2
import numpy as np
import os

from cv2.typing import MatLike

def split(vid: str, threshold=500):
    output_folder = f'frames/{vid}'
    
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(f'downloads/{vid}.mp4')
    if not cap.isOpened():
        raise Exception(f'Failed to open video {vid}')
    
    frame_count = 0
    last_unique_frame: MatLike = None

    while True:
        ret, frame = cap.read()
        if not ret: break # end of video
        if last_unique_frame is None:
            save_frame(frame, frame_count, output_folder)
            last_unique_frame = frame
        else:
            if is_unique_frame(frame, last_unique_frame, threshold):
                frame_count += 1
                save_frame(frame, frame_count, output_folder)
                last_unique_frame = frame
    
    cap.release()

def save_frame(frame: MatLike, frame_count: int, output_folder: str):
    filename = os.path.join(output_folder, f'{frame_count}.jpg')
    cv2.imwrite(filename, frame)

def is_unique_frame(frame: MatLike, last_unique_frame: cv2.typing.MatLike, threshold: int):
    difference = cv2.absdiff(frame, last_unique_frame)
    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    non_zero_count = np.count_nonzero(gray_difference)
    return non_zero_count > threshold
