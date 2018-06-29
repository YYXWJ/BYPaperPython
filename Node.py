#!/usr/bin/python
#coding=utf-8

'''
   一个节点用三个字段描述
   该节点所在类名
   该节点方法名
   该节点父节点
   '''
class Node:

    # def __init__(self):
    #     self.__className = ''
    #     self.__methodName = ''
    #     self.__parent = None
    #     self.__childList = []
    def __init__(self,classname = '',methodname = ''):
        self.__className = classname
        self.__methodName = methodname
        self.__parent = None
        self.__childList = []
    def equils(self,node):
        if node.getClassName() == self.__className and node.getMethodName() == self.__methodName:
            return True
        return False

    def getHash(self):
        return hash(self.__className+self.__methodName)

    def setClassName(self,className):
        self.__className = className

    def getClassName(self):
        return self.__className

    def setMethodName(self,methodName):
        self.__methodName = methodName

    def getMethodName(self):
        return self.__methodName

    def setParent(self,parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def getChildList(self):
        return self.__childList

    '''
    添加子节点 同时子节点里面添加父节点
    '''
    def addChild(self,node):
        self.__childList.append(node)
        node.setParent(self)