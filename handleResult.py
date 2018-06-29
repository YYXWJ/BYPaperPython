#!/usr/bin/python
#coding=utf-8
import hashlib
import os

import re

import Constant
from Path import Path
#filesPath = "D:\\ApkIDE\\ApkIDE\\Work\\ptrace.xiaoby.com.test_flowdroid_intent\\smali\\"
#oldresultPath = "D:\\data\\shiyan\\newapk\\result\\"


#filesPath = "D:\\data\\论文\\yy论文材料\\apkResult\\起点读书\\"
sougouPath = '/Users/xiaoby/PycharmProjects/smailChange/apkResult/result/result.txt'
Paths = []

def getallSmaliFiles(path, smaliFiles):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            if '.txt' in filepath:
                smaliFiles.append(filepath)
        elif os.path.isdir(filepath):
            getallSmaliFiles(filepath,smaliFiles)
    return smaliFiles


def findAndChangeStartActivity(file):
    f = open(file, 'r')
    line = f.readline()
    while line :
        if 'startActivity' in line :
            print file.decode('gbk').encode('UTF-8')
            print line
        line = f.readline()
    f.close()


def findAndChangeStartService(file):
    f = open(file, 'r')
    line = f.readline()
    method = ''
    classname = ''
    locals = ''
    while line:
        # if '.method' in line:
        #     method = line
        #     line = f.readline()
        #     continue
        # if '.class' in line:
        #     classname = line
        #     line = f.readline()
        #     continue
        # if '.locals' in line:
        #     locals = line
        #     line = f.readline()
        #     continue
        if 'startService' in line:
            print file.decode('gbk').encode('UTF-8')
            print line
            #handleStartService(file,line)
        line = f.readline()
    f.close()

def handleStartService(filename,line = ''):
    #line = 'invoke-virtual {p0, p1, v1, v2}, Lptrace/xiaoby/com/test_flowdroid_intent/MainActivity;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;'
    print line
    intentLocal = findIntent(line)
    const = '   const/4 v3, 0x0\n\n'
    newinstance = '    new-instance v1, Lptrace/xiaoby/com/test_flowdroid_intent/SinkService;\n\n'
    invokedirect = '    invoke-direct {v1}, Lptrace/xiaoby/com/test_flowdroid_intent/SinkService;-><init>()V\n\n'
    local = '   .local v1, "sinkService":Lptrace/xiaoby/com/test_flowdroid_intent/SinkService;\n\n'
    invokevirtual = '   invoke-virtual {v1, '+intentLocal+', v3, v3}, Lptrace/xiaoby/com/test_flowdroid_intent/SinkService;->onStartCommand(Landroid/content/Intent;II)I\n\n'
    file = open(filename, "r")
    content = file.read()
    pos = content.find(line)
    if pos != -1:
        content = content[:pos] + const+newinstance+invokedirect+local+invokevirtual + content[pos:]
        file1 = open(filename, "w")
        file1.write(content)
        file1.close()

def findIntent(line = ''):
    #根据实验，测试了很多情况，startActivity或 startService或 sendBroadcast 都是第二个参数 是intent，所以可以使用相同的方法找到intent的寄存器
    start = line.find('{')
    end = line.find('}')
    locals = line[start + 1:end]
    intentLocal = locals[locals.find(',') + 1:locals.find(',') + 4]
    return intentLocal

def findAndChangeBroadcastReceiver(file):
    f = open(file, 'r')
    line = f.readline()
    method = ''
    classname = ''
    linenumber = 0;
    while line:
        # if '.method' in line:
        #     method = line
        #     line = f.readline()
        #     continue
        # if '.class' in line:
        #     classname = line
        #     line = f.readline()
        #     continue
        if 'sendBroadcast' in line:
            print file.decode('gbk').encode('UTF-8')
            print line
            print linenumber
        line = f.readline()
        linenumber = linenumber + 1
    f.close()

def getMD5(str):
    m2 = hashlib.md5()
    m2.update(str)
    return m2.hexdigest()


def findSources(file):
    f = open(file, 'r')
    line = f.readline()
    lineNumber = 0
    while line:
        for source in Constant.handler:
            if source in line:
                print file
                print line
                print lineNumber
        line = f.readline()
        lineNumber += 1
    f.close()

'''
遍历flowdroid 跑出来的结果，把每一个source-sink保存，
其中保存 ：
    source点
    source点所在的method
    sink点
    sink点所在method
    调用路径上的每一个方法和方法所在的method
'''
def getPaths(file):
    f = open(file,'r')
    line = f.readline()
    path = None
    while line:
        isreadflag = False
        if line.startswith('==========-============='):
            path = Path()
            Paths.append(path)
            path.setSink(line[line.index('The sink')+9:line.index('in method')])
            line = f.readline()
            if line:
                path.setSource(line[2:line.index('in method')])
                f.readline()
                continue
            else:
                break
        if line.startswith('===>'):#以这个字符串开头是传播语句包含所在的类和方法
            lines = []
            while line and (not line.startswith('==========-=============')):
                lines.append(line)
                line = f.readline()
                isreadflag = True
            path.handlePathNode(lines)
        if not isreadflag:
            line = f.readline()
if '__main__' == __name__ :
    #smaliFiles = getallSmaliFiles(unicode(sougouPath,"utf-8"),[])
    #decode('gbk').encode('UTF-8') 打印中文
    smaliFiles = unicode(sougouPath,"utf-8")
    getPaths(smaliFiles)
    # for path in Paths:
    #     print 'path----',path.getLeakPath()

    #
    # for path in Paths:
    #     print 'sources----',path.getSource()
    # for file in smaliFiles:
    #     getPaths(file)
        #findSources(file)
        #findAndChangeStartActivity(file)
        # findAndChangeStartService(file)
        # findAndChangeBroadcastReceiver(file)