#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :statistics_video_time.py
# @Time      :2021/11/1 20:27
# @Author    :Chen
import struct
import os;
from moviepy.editor import VideoFileClip

#获取视频的时长
def get_video_duration(video_file):
    clip = VideoFileClip(video_file)
    duration =  clip.duration;
    print("path:%s duration:%s"%(video_file,duration))
    #关闭时长
    VideoFileClip.close(clip)
    return duration;


#遍历视频列表 获取视频时长
def get_video_list_duration(video_list):
    total_time = 0;
    for video in video_list:
        if not video:
            continue;
        total_time+=get_video_duration(video);
    return total_time;

#获取文件夹下的所有 视频文件
def get_all_video(path):
    dir_list = os.listdir(path);
    result = [];
    for dir in dir_list:
        #判断是否是视频文件
        if (".mp4" in dir) or (".flv" in dir):
            result.append(path+"/"+dir);

    return result;

#获取文件夹下的所有 文件夹
def get_all_folder(path):
    dir_list = os.listdir(path);
    result = [];
    for dir in dir_list:
        if os.path.isdir(path+"/"+dir):
            result.append(path+"/"+dir);

    return result;


#文件类
class Folder(object):

    def __init__(self,path):
        self.path = path;
        #获取文件夹列表
        self.__get_folder_list();
        #获取视频列表
        self.__get_video_list();
        #获取所有视频列表
        self.__get_all_video_list();

    #获取
    def __get_folder_list(self):
        self.folder_obj_list = [];
        folder_list = get_all_folder(self.path)
        for folder in folder_list:
            #创建Folder对象，迭代
            self.folder_obj_list.append(Folder(folder));

    def __get_video_list(self):
        self.video_list = get_all_video(self.path);

    def __get_all_video_list(self):
        #递归目录下的文件夹中的所有video
        sub_video_list = [];
        for folder in self.folder_obj_list:
            if folder.video_list:
                sub_video_list.extend(folder.video_list);
            if folder.all_video_list:
                sub_video_list.extend(folder.all_video_list)
        self.all_video_list = sub_video_list+self.video_list;

    def statistics_video_time(self):
        return get_video_list_duration(self.all_video_list);

    def __str__(self):
        return self.path;

    __repr__ = __str__


if __name__ == "__main__":
    parent_path = "F:/video/06_数据采集";
    parent_folder = Folder(parent_path);
    print("总视频数:%s"%len(parent_folder.all_video_list))
    total_second = int(parent_folder.statistics_video_time())
    total_minu = total_second/60;
    total_hour = total_second/3600;
    print("%s秒,%s分钟，%s小时"%(total_second,total_minu,total_hour))

