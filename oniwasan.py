import pygame
import time
from moviepy.editor import VideoFileClip
import threading

# Pygame 초기화 및 조이스틱 초기화
pygame.init()
pygame.joystick.init()

# 동영상 파일 목록
select_videos = ['select01.mp4', 'select02.mp4', 'select03.mp4', 'select04.mp4', 'select05.mp4', 'select06.mp4']
play_videos = ['play01.mov', 'play02.mp4', 'play03.mov', 'play04.mov', 'play05.mov', 'play06.mov']
main_loop_video = 'main_loop.mp4'  # 메인 루프 영상

# 2x3 그리드에서 현재 위치(row, col)를 나타내는 변수
grid = [[0, 1, 2], [3, 4, 5]]
current_row, current_col = 0, 0  # 초기 위치는 첫 번째 행, 첫 번째 열

# 동영상 재생 스레드 및 상태 관리
video_thread = None
video_stop_event = threading.Event()
last_input_time = time.time()  # 마지막 입력 시간
trigger_buttons = {3, 2, 10, 9, 1, 0}  # 특정 버튼 리스트
in_select_mode = False  # 현재 select 모드인지 여부
in_play_mode = False  # 현재 play 모드인지 여부

# 화면 설정
screen = pygame.display.set_mode((1080, 1920))

# 동영상을 재생하는 함수
def play_video(video_file, loop=False, callback=None):
    while not video_stop_event.is_set():  # 루프를 위한 while 문
        clip = VideoFileClip(video_file)  # 동영상 클립 로드
        for frame in clip.iter_frames(fps=30, dtype="uint8"):
            if video_stop_event.is_set():  # 중단 이벤트 발생 시 중지
                break
            # 프레임을 화면에 출력
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(surface, (0, 0))
            pygame.display.update()

            # 이벤트 처리 중 종료 이벤트가 있으면 프로그램 종료
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            time.sleep(1 / 30)  # 프레임 속도에 맞춰 대기
        clip.close()  # 비디오 클립 종료

        if not loop:  # 루프가 아닌 경우 종료
            break

    if callback:  # 콜백 함수가 있으면 실행
        callback()

# 현재 재생 중인 동영상을 중단하는 함수
def stop_current_video():
    if video_thread and video_thread is not threading.current_thread():  # 수정된 부분
        video_stop_event.set()  # 비디오 중단 이벤트 설정
        video_thread.join()  # 현재 재생 중인 비디오 스레드 종료 대기
    video_stop_event.clear()  # 비디오 중단 이벤트 초기화

# 메인 루프 영상을 재생하는 함수
def play_main_loop():
    stop_current_video()  # 현재 재생 중인 비디오 중단
    global video_thread, in_select_mode, in_play_mode  # 전역 변수 수정
    in_select_mode = False  # 메인 루프 상태로 복귀
    in_play_mode = False  # play 모드 종료
    video_thread = threading.Thread(target=play_video, args=(main_loop_video, True))  # 메인 루프 영상 재생 (루프)
    video_thread.start()

# 선택된 그리드의 select 영상을 재생하는 함수
def play_select_video():
    global in_select_mode
    global last_input_time
    last_input_time = time.time()

    # 선택된 그리드의 select 영상 재생
    selected_video = grid[current_row][current_col]
    stop_current_video()
    in_select_mode = True  # 이제 select 모드임을 표시
    global video_thread
    video_thread = threading.Thread(target=play_video, args=(select_videos[selected_video], True))  # 루프 재생
    video_thread.start()

# 조이스틱이 연결된 경우 초기화
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"조이스틱 연결됨: {joystick.get_name()}")

    # 프로그램 시작 시 메인 루프 영상 재생
    video_stop_event.clear()
    video_thread = threading.Thread(target=play_video, args=(main_loop_video, True))  # 메인 루프 영상 루프 재생
    video_thread.start()

    # 메인 루프
    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료 이벤트 처리
                pygame.quit()
                quit()

            # 모든 조작(조이스틱, 버튼) 입력 시 메인 루프 중단 및 select 영상 재생
            if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION]:
                # 메인 루프 중일 때 조이스틱은 작동, 특정 버튼(3, 2, 10, 9, 1, 0)은 무시
                if not in_select_mode and not in_play_mode:
                    if event.type == pygame.JOYBUTTONDOWN and event.button not in trigger_buttons:
                        play_select_video()  # select 영상으로 이동
                last_input_time = time.time()

            # 버튼 입력에 따른 그리드 이동 처리 (상: 11, 하: 12, 좌: 13, 우: 14)
            if event.type == pygame.JOYBUTTONDOWN and event.button not in trigger_buttons:
                if event.button == 11:  # 상 방향
                    if current_row > 0:
                        current_row -= 1
                elif event.button == 12:  # 하 방향
                    if current_row < 1:
                        current_row += 1
                elif event.button == 13:  # 좌 방향
                    if current_col > 0:
                        current_col -= 1
                elif event.button == 14:  # 우 방향
                    if current_col < 2:
                        current_col += 1

                # 선택된 그리드의 select 영상 재생
                selected_video = grid[current_row][current_col]

                # 현재 재생 중인 동영상 중단 후 새로운 select 동영상 재생
                stop_current_video()
                video_thread = threading.Thread(target=play_video, args=(select_videos[selected_video], True))  # 루프 재생
                video_thread.start()

            # select 모드에서 특정 버튼(3, 2, 10, 9, 1, 0)이 눌리면 play_videos 재생
            if in_select_mode and event.type == pygame.JOYBUTTONDOWN and event.button in trigger_buttons:
                play_video_index = grid[current_row][current_col]

                # 현재 재생 중인 select 동영상 중단 후 play_videos 재생, 재생 후 메인 루프로 복귀
                stop_current_video()
                video_thread = threading.Thread(target=play_video,
                                                args=(play_videos[play_video_index], False, play_main_loop))
                video_thread.start()
                in_select_mode = False  # play_videos가 재생되면 select 모드 종료
                in_play_mode = True  # play 모드 활성화

        # play 모드를 제외한 모든 상황에서 1분 동안 입력이 없으면 메인 루프 재생
        if not in_play_mode and time.time() - last_input_time > 60:
            play_main_loop()
            last_input_time = time.time()

        # CPU 사용량을 줄이기 위한 짧은 대기 시간
        time.sleep(0.01)

# Pygame 종료
pygame.quit()
