import subprocess, os, json

################## Conversion Classes #########################

class Conversion (object):
    def __init__(self, obj, source):
        #self.script = obj['script']
        self.script = os.path.abspath(obj['script'])
        self.language = obj['language']
        self.type = os.path.abspath(obj['type'])
        self.engine = False
        if obj['engine'] != False:
            self.engine = os.path.abspath(obj['engine'])
            
        self.name = obj['name']
        self.source = os.path.abspath(source)
    
    def speak (self):
        print('I am the ' + self.name + '!')
        print ('Conversion "' + self.name + '" via ' + self.language + ':' + str(self.engine) + ' using ' + self.script + ' on ' + self.source)

    def createXML (self, content):
        file = open(self.source,"w+") 
        file.write(content) 
        file.close()
    
    def call (self):
        return " ".join((self.language, self.script, self.source))

    def run (self):
        output = subprocess.check_output(self.call(), shell=True)
        self.createXML(output)

#************ XSLT ***********
class Xslt (Conversion):
    def call (self):
        script = "-xsl:" + self.script
        source = "-s:" + self.source
        return " ".join((self.language, self.engine, script, source))

#************ XQUERY *********
class Xquery (Conversion):
    def call (self):
        script = "-xquery:" + self.script
        source = "-s:" + self.source
        return " ".join((self.language, self.engine, script, source))

# Prototyping Saxon as Class
#************ saxon *********
class Saxon (object):
    def __init__(self, obj, source):
        #self.script = obj['script']
        self.script = os.path.abspath(obj['script'])
        self.type = obj['type']
        self.language = obj['language']
        self.type = os.path.abspath(obj['type'])
        self.engine = False
        if obj['engine'] != False:
            self.engine = os.path.abspath(obj['engine'])
            
        self.name = obj['name']
        self.source = os.path.abspath(source)
    
    def speak (self):
        print('I am the ' + self.name + '!')
        print ('Conversion "' + self.name + '" via ' + self.language + ':' + str(self.engine) + ' using ' + self.script + ' on ' + self.source)

    def createXML (self, content):
        file = open(self.source,"w+") 
        file.write(content) 
        file.close()
    
    def call (self):
        return " ".join((self.language, self.script, self.source))

    def run (self):
        output = subprocess.check_output(self.call(), shell=True)
        self.createXML(output)