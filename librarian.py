import os
import shutil
from os import path
from datetime import datetime

# function that returns extension of a file
def get_extension(str):
    temp = ''
    for each in reversed(str):
        temp += each
        if each == '.':
            break
    return temp[::-1]

# function which returns a dictionary of extensions and counts of that files in given folder (dir stands for forders)
def get_ext_dic(str):
    ls = os.listdir(str)
    dic = {}
    for each in ls:
        if path.isdir(path.join(str,each)):
            if 'dir' not in dic.keys():
                dic['dir'] = 1
            else:
                dic['dir'] += 1
        else:
            ext = get_extension(each)
            if ext not in dic.keys():
                dic[ext] = 1
            else:
                dic[ext] += 1
    return dic

# format -> ['folder1':'extention1','extension2'...], ['folder2':'extention1','extension2'...]

folder_dic = {
    'Music':['.mp3','.wav','.MP3','.WAV'],
    'Videos':['.mp4','.mkv','.avi','.webm','.MP4','.MKV','.AVI','.WEBM'],
    'Torrents':['.torrent','.TORRENT'],
    'Images':['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG'],
    'Documents':['.PDF','.pdf','.DOC','.DOCX','.doc','.docx','.ppt','.pptx','.PPT','.PPTX'],
    'Compressed':['.zip','.ZIP','.rar','.RAR','.tar','.TAR','.gz','.GZ']
}

# any file or folder that should remain... also add new folders if added to above dictionary
exceptions = ['Music','Videos','Torrents','Images','Documents','Compressed','Others','Folders','logs.txt','librarian.py','VideoDownloader','Telegram Desktop','FireShot','Songs']

# creating required folders and log file
def init(path_str):
    for each in exceptions:
        full_path = path.join(path_str,each)
        if not path.exists(full_path):
            if '.' not in each:
                os.mkdir(full_path)
    if not path.exists(path.join(path_str,'logs.txt')):
        log_file = open(path.join(path_str,'logs.txt'),'w')
        log_file.write('<< log file created by librarian.py >>\n')
        log_file.close()
    
# function that starts organizing
def start(path_str):
    init(path_str)
    ls = os.listdir(path_str)
    log_file = open(path.join(path_str,'logs.txt'),'a')
    log_file.write('\n<< New Session Started at \"'+path_str+'\" on \"'+str(datetime.now())[:19:]+'\">>\n')
    for each in ls:
        ls = ''
        if each not in exceptions:
            full_path = path.join(path_str,each)
            log_str = '\"'+each+'\" moved to '
            if path.isdir(full_path):
                shutil.move(full_path,path.join(path_str,'Folders',each))
                log_str += 'Folders on \"'+str(datetime.now())[:19:]+'\"'
            else:
                ext = get_extension(each)
                found = False
                for key in folder_dic.keys():
                    if ext in folder_dic[key]:
                        shutil.move(full_path,path.join(path_str,key,each))
                        log_str += key+' on \"'+str(datetime.now())[:19:]+'\"'
                        found = True
                        break
                if not found:
                    shutil.move(full_path,path.join(path_str,'Others',each))
                    log_str += 'Others on \"'+str(datetime.now())[:19:]+'\"'
            log_file.write(log_str+'\n')
            print(log_str)
    log_file.write('<< Session ended on \"'+str(datetime.now())[:19:]+'\" >>\n')
    log_file.close()

# organizes the folder its in
current_path = os.getcwd()

# uncomment the below line and add your path to give a custom path
# current_path = 'path here'

start(current_path)