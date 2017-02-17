# Conversion.py
# *************
# Defines the Conversion Class for each Step in a Conversion-Scenario
# IN WORK !
#

class Conversion (object):
    def __init__(self, name, type, script):
        self.name = name
        self.type = conv_type
        self.desc = desc
        self.script = os.path.abspath(script) 
        self.converter = False

    def info (self):
        print ('Converison "' + self.name + '" as ' + self.type + ' with ' + self.script + ' doing "' + self.desc + '" (Custom-Converter: ' + self.converter +')')

    def callConverter (self):
        if self.converter == False:
            if self.type == 'xslt':
                # Call Saxon.xslt()
                pass
            elif self.type == 'xquery':
                # Call Saxon.xquery()
                pass
            else: 
                print ('Type unknown')
        else:
            #Call Call.run()

