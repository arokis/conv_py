import subprocess, json, os, tempfile, sys, urllib2

#load config.json to configure conv.py
with open('config/config.json') as conv_data:
    conv_config = json.load(conv_data)

"""
#load steps.json
with open('steps.json') as steps_data:
    steps = json.load(steps_data)
    steps = steps["steps"]
"""

#xml = 'test_xml.xml'
url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'
xml_file = conv_config["tmp_file"]
saxon_path = conv_config["engines"]["saxon"]["path"]
steps = conv_config["test-steps"]

def getXml (xml):
    response = urllib2.urlopen(xml)
    xml_data = response.read()
    return xml_data

"""
# not functional yet
def readJson():
    steps = sys.stdin.readlines()
    return json.loads(steps[0])
"""

def createTempFile (tmp_file, content):
    file = open(tmp_file,"w+") 
    file.write(content) 
    file.close()

def convert(steps, xml):
    # build conversion workflow
    for step in steps:
        xml = xml
        saxon(saxon_path, step, xml)

    # when conversion is finished read the last conversion output from file and remove it
    with open(xml_file, 'r') as out:
        output = out.read()
        os.remove(xml_file)
        return output

def saxon(path, step, xml) :
    xsl = step["xsl"]
    inp = xml
    #print(inp)
    output = subprocess.check_output("java -jar " + path + " -s:" + inp + " -xsl:" + xsl, shell=True)
    createTempFile(xml_file, output)

# workflow when converting an online resource from vmr
def convertUrlResource ():
    xml_data = getXml(url)
    createTempFile(xml_file, xml_data)
    response = convert(steps, xml_file)
    print(response)


def main ():
    
    #print(conv_config)
    #print(saxon_path)
    #print(xml_file)
    #for step in steps:
    #    print step["name"] 

    
    convertUrlResource()
    


if __name__ == '__main__':
    main()

