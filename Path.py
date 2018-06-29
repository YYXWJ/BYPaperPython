#!/usr/bin/python
#coding=utf-8
from Method import Method
import re
from Node import Node
class Path:

    def __init__(self):
        self.__sink = Node()
        self.__source = Node()
        self.__nodes = {}
    '''
        处理一条泄露路径
        lines ： 一条完整的泄露路径
        
    '''
    def handlePathNode(self,lines=[]):
        print lines
        for index in range(len(lines)):
            if lines[index].startswith('===>'):
                classname ,methodname = self.__patternMethod(lines[index][4:])
                # print classname
                # print methodname
                parentNode = Node(classname,methodname)
                if parentNode.getHash() not in self.__nodes:
                    self.__nodes[parentNode.getHash()] = parentNode
                    # for key in self.__nodes.keys():
                    #     print self.__nodes[key].getClassName()
                    #     print self.__nodes[key].getMethodName()
                    #     print self.__nodes[key].getChildList()
                else:
                    parentNode = self.__nodes[parentNode.getHash()]
                childstate = lines[index+1]
                if 'invoke' not in childstate:#没有invoke认为赋值语句
                    if 'return' in childstate:#如果是return 说明return的上一句是return下一句的父节点
                        # print childstate
                        childchildstate = lines[index + 2]
                        classname, methodname = self.__patternMethod(childchildstate[4:])
                        gradepaNode = Node(classname, methodname)
                        if gradepaNode.getHash() not in self.__nodes:
                            self.__nodes[gradepaNode.getHash()] = gradepaNode
                            gradepaNode.addChild(parentNode)
                        else:
                            gradepaNode = self.__nodes[gradepaNode.getHash()]
                            gradepaNode.addChild(parentNode)
                else:
                    temp = self.__patternNode(childstate[7:])
                    if temp is None:
                        continue
                    classname ,methodname = self.__splitNodestr(temp)
                    # print classname
                    # print methodname
                    childNode = Node(classname,methodname)
                    self.__nodes[childNode.getHash()] = childNode
                    parentNode.addChild(childNode)
            if lines[index].startswith('------>'):
                pass
        for key in self.__nodes.keys():
            print self.__nodes[key].getClassName(),self.__nodes[key].getMethodName()
            for nnode in self.__nodes[key].getChildList():
                print 'child----',nnode.getClassName(),nnode.getMethodName()

    def setSink(self,sink):
        temp = self.__patternNode( sink)
        classname , methodname = self.__splitNodestr(temp)
        self.__sink.setClassName(classname)
        self.__sink.setMethodName(methodname)
        # self.__sink = sink

    def getSink(self):
        return self.__sink

    def setSource(self,source):
        temp = self.__patternNode(source)
        classname, methodname =  self.__splitNodestr(temp)
        self.__source.setClassName(classname)
        self.__source.setMethodName(methodname)
        # self.__source = source

    def getSource(self):
        return self.__source

    def getNodeList(self):
        return self.__nodeList

    '''
    针对method做正则
    如：
    <com.aaa.bbb: void func(args1,args2)>
    
    这里的method是Node类型
    '''
    def __patternMethod(self,str = ''):
        matchs = re.split('^<(.*):\s(.*)\s(.*)\\((.*)\\)>$', str)
        # print matchs[1]
        # print matchs[2]
        # print matchs[3]
        # print matchs[4]
        # method.setClassName(matchs[1])
        # method.setMethodName(matchs[3])
        return matchs[1],matchs[3]

    '''
    针对语句进行正则
    
    '''
    def __patternNode(self,str):
        if str.index('<') > -1:
            matchs = re.split('<(.*)>',str)
            return matchs[1]
        else:
            return None

    def __splitNodestr(self,str = ''):
        classname = str[:str.index(':')]
        # print classname
        if '(' in str:
            methodname = str[self.__find_last(str,' ')+1:str.index('(')]
        else:
            methodname = str[self.__find_last(str,' ')+1:]
        # print methodname
        return classname,methodname

    def __find_last(self,string,str):
        last_position = -1
        while True:
            position = string.find(str, last_position + 1)
            if position == -1:
                return last_position
            last_position = position