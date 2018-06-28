#!/usr/bin/python
#coding=utf-8
import os

smaliFilesPath='D:\\ApkIDE\\ApkIDE\\Work\\com.sogou.novel\\'
def getallSmaliFiles(path, smaliFiles):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            if '.smali' in filepath:
                smaliFiles.append(filepath)
        elif os.path.isdir(filepath):
            getallSmaliFiles(filepath,smaliFiles)
    return smaliFiles


def changeHandleMessage(file):
    f = open(file,'r')
    line = f.readline()
    newfile_data = ""
    while line :
        if 'Landroid/os/Handler;->sendMessage(Landroid/os/Message;)Z' in line:
            line = line.replace('Landroid/os/Handler;->sendMessage(Landroid/os/Message;)Z','Landroid/os/Handler;->handleMessage(Landroid/os/Message;)V')
        newfile_data+=line
        line = f.readline()
    with open(file, "w") as f:
        f.write(newfile_data)

if '__main__' == __name__ :
    files = getallSmaliFiles(smaliFilesPath,[])

    for file in files:
        changeHandleMessage(file)