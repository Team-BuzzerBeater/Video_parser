import os
import numpy as np
import pandas as pd
from moviepy.editor import VideoClip, VideoFileClip
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

''' make the video clip '''
start_time_list = [0, 1, 2]
end_time_list = [1, 2, 3]

# get '~.mp4' files on path
video_path = "./data/"
file_list = os.listdir(video_path)
file_list_mp4 = [file for file in file_list if file.endswith(".mp4")]

video_num = len(file_list_mp4)

print(video_num)
print ("file_list: {}".format(file_list_mp4))

try:
    extra_data = pd.read_csv('./additional_time_data.csv')
except FileNotFoundError:
    print("*** There's no csv file that matches with additional_time_data.csv ***")
    exit(1)
# 앞 5 뒤 2

for i in range(video_num):
    # 영상파일 이름과 같은 이름의 csv를 읽어서 슈팅횟수 및 슈팅시간 정보 얻기
    video_file_name = file_list_mp4[i]
    extra = extra_data.loc[i]
    first_half_min, first_half_sec, second_half_min, second_half_sec = extra['first_half_min'],extra['first_half_sec'],extra['second_half_min'],extra['second_half_sec']
    half_end = 45
    csv_file_name = video_file_name.split('.')[0] + '.csv'

    first_half = first_half_min*60 + first_half_sec
    second_half = (second_half_min - half_end)*60 + second_half_sec
    half_end *= 60

    # print(video_file_name)
    print("current file :", csv_file_name)

    csv_path = "./data/" + csv_file_name

    try:
        csv_data = pd.read_csv(csv_path,encoding='euc-kr')
    except FileNotFoundError:
        print("*** There's no csv file that matches with '%s'." %csv_file_name)
        exit(1)

    shoot_num = len(csv_data)   # 슈팅 개수

    # print(shootTime_list)
    # print(shoot_num)

    for j in range(0, shoot_num):
        row_data = csv_data.loc[j]

        shoot_time = row_data['슈팅시간']%10000
        video_sync_time = first_half if row_data['슈팅시간']//10000 < 2 else second_half
        shoot_time += int(video_sync_time)
        start_time = max(shoot_time - 2, 0)
        end_time = shoot_time + 2

        player_name = row_data['선수']

        print("입력시간 : %d    clip시작시간 : %d   clip끝나는시간 : %d" %(shoot_time, start_time, end_time))
        print("선수 : %s\n" %player_name)

        # start_time초 부터 end_time초 까지 video clip 만들기
        new_file_name = video_file_name.split('.')[0] + '_' + str(row_data['슈팅시간']) + '.mp4'
        print("file name :", new_file_name)
        new_file_name = os.path.join('./clip/',new_file_name)
        # 빠르지만 생성된 video clip의 길이가 약간 이상함
       # ffmpeg_extract_subclip(video_file_name, start_time, end_time, targetname=new_file_name)
        # 느리지만 정확
        with VideoFileClip(os.path.join('./data/',video_file_name)) as video:
            new = video.subclip(start_time, end_time)
            new.write_videofile('pycharmvideo.mp4', audio_codec='aac')
