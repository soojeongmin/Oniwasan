import pygame
from moviepy.editor import VideoFileClip
import time

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Video Player')

videos = [video1.mp4, video2.mp4, video3.mp4, video4.mp4]
current_video_index = 0

def play_video(video_file):
    clip = VideoFileClip(video_file)
    clip.preview()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                play_video(videos[current_video_index])
                current_video_index = (current_video_index + 1) % len(videos)

    time.sleep(0.1)

pygame.quit()

