class Method:
    def __init__(self):
        self.classname = ''
        self.methodname = ''
        self.returntype = ''
        self.objs = []

    def setClassname(self,classname=''):
        print 'classname',classname
        self.classname = classname

    def setMethodname(self,methodname=''):
        print 'methodname',methodname
        self.methodname = methodname

    def setReturntype(self,returntype=''):
        self.returntype = returntype

    def setObjs(self,objs = []):
        self.objs = objs

    def getClassname(self):
        return self.classname

    def getMethodname(self):
        return self.methodname

    def getReturntype(self):
        return self.returntype

    def getObjs(self):
        return self.objs