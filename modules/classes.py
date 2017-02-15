import subprocess, os, json

########### Main Conversion CLass ############
class Conversion (object):
    def __init__(self, obj, source):
        self.language = obj['conversion']['language']
        self.name = obj['name']
        self.type = obj['type']
        self.script = os.path.abspath(obj['script'])
        self.source = os.path.abspath(source)
    
    def _process (self, call):
        def createXML (source, content):
            file = open(source,"w+") 
            file.write(content) 
            file.close()
        output = subprocess.check_output(call, shell=True)
        createXML(self.source, output)


########### Subclass Script (Conversion CLass) ############
class Script (Conversion):
    def __init__(self, obj, source):
        Conversion.__init__(self, obj, source)

    def speak (self):
        print ('SCRIPT "' + self.name + '" (' + self.type + ') via ' + self.language + ' using ' + self.script + ' on ' + self.source)
    
    def run (self):
        call = " ".join((self.language, self.script, self.source))
        self._process(call)


########### Subclass Engine (Conversion CLass) ############
class Engine (Conversion):
    def __init__(self, obj, source):
        Conversion.__init__(self, obj, source)
        self.engine = obj['conversion']['engine']
        self.path = os.path.abspath(obj['conversion']['path'])
    
    def speak (self):
        print ('ENGINE: "' + self.name + '" (' + self.type + ') via ' + self.language + ' ' + self.path + ' using ' + self.script + ' on ' + self.source)


########### Subclass Saxon (Engine CLass) ############
class Saxon (Engine):
    def __init__(self, obj, source):
        Engine.__init__(self, obj, source)
    
    def speak (self):
        print ('SAXON: "' + self.name + '" via ' + self.language + ' ' + self.path + ' using ' + self.script + ' on ' + self.source)
    
    def xslt (self):
        script = "-xsl:" + self.script
        source = "-s:" + self.source
        call = " ".join((self.language, self.path, script, source))
        self._process(call)

    def xquery (self):
        script = "-xql:" + self.script
        source = "-s:" + self.source
        call = " ".join((self.language, self.path, script, source))
        self._process(call)
    