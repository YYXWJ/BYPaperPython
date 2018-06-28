from Method import Method
import re
class Path:

    def __init__(self):
        self.__sink = ''
        self.__sinkMethod = Method()
        self.__source = ''
        self.__sourceMethod = Method()
        self.__leakPaths = []
        self.__leakPathMethods = []

    def setSink(self,sink=''):
        self.__sink = sink

    def setSinkMethod(self,sinkMethod=''):
        self.__pattrenMethod(self.__sinkMethod,sinkMethod)

    def setSource(self,source=''):
        self.__source = source

    def setSourceMethod(self,sourceMethod):
        self.__pattrenMethod(self.__sourceMethod, sourceMethod)

    def setLeakPath(self,leakPath=''):
        self.__leakPaths.append(leakPath)

    def setLeakPathMethod(self,leakPathMethod=''):
        method = Method()
        self.__pattrenMethod(self.method, leakPathMethod)
        self.__leakPathMethods.append(method)

    def getSink(self):
        return self.__sink

    def getPatternSink(self):
        matchs = re.split('(.*)<(.*)>(.*)$',self.__sink)
        return matchs[2]

    def getSinkMethod(self):
        return self.__sinkMethod

    def getSource(self):
        return self.__source

    def getSourceMethod(self):
        return self.__sourceMethod

    def getLeakPath(self):
        return self.__leakPaths

    def getLeakPathMethod(self):
        return self.__leakPathMethods


    def __pattrenMethod(self,method,str = ''):
        matchs = re.split('^<(.*):\s(.*)\s(.*)\\((.*)\\)>$', str)
        # print matchs[1]
        # print matchs[2]
        # print matchs[3]
        # print matchs[4]
        method.setClassname(matchs[1])
        method.setReturntype(matchs[2])
        method.setMethodname(matchs[3])
        method.setObjs(matchs[4].split(','))
        return matchs