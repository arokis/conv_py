import json 
import os
import sys
import urllib2
from shutil import rmtree

# ConvPy-Module "Conversion.py"
import Conversion
# ConvPy-Module "Converter.py"
from Converter import Saxon, Call


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


def clean_tmp (file_path):
    """
    cleans all temporary files and folders being created during convPY working 
    
    ARGS:
    * path: path of tmp-file to be deleted inkl. it's parent directory 
    """
    try:
        rmtree(os.path.dirname(file_path))
    except:
        print ('[convPY:WARNING] Could not clean up tmp-file "' + file_path +'". Maybe you should clean it manually!')
        sys.exit(0)


def create_file (path, content, option='w+'):
    """
    creates files with params 
    
    ARGS:
    * path: path of file being created
    * content: content being writen in file
    * options (optional): writing mode (no string-controll!), default: 'w+' 
    """
    try:
        fo = open( path, option ) 
        fo.write( content ) 
        fo.close()
    except:
        print ('[convPY:ERROR] Failed while creating File "' + path +'". Exit!')
        sys.exit(1)


def convert (flow, convpy):
    """
    main conversion routine which creates Conversion-Instances and call the Converter-Instances

    ARGS:
    * flow: the givern conversion-workflow which should to be done
    * convpy: The actual configured convPY Instance
    
    TO-DO:
    - decouple Conversion from Converter
    - "pathify" Saxon-Class (Converter.py) -> and make the Classes smooth ... they are a mess right now
    - make Conversion-Class smooth !
    """
    #print os.path.join(convpy.home, convpy.engines['Saxon']['xslt']['path'])
    for step in flow:
        conversion = Conversion.Conversion(convpy)
        conversion.scenarioise(step)
        #print convpy.scripts_path
        #conversion.info()
        
        if conversion.type == 'xslt':
            language = convpy.engines['Saxon']['xslt']['language']
            engine = os.path.join(convpy.home, convpy.engines['Saxon']['xslt']['path'])
            Saxon(language, engine).xslt(conversion.script)
        elif conversion.type == 'xquery':
            language = convpy.engines['Saxon']['xquery']['language']
            engine = os.path.join(convpy.home, convpy.engines['Saxon']['xquery']['path'])
            Saxon(language, engine).xquery()
        else:
            Call(conversion.language).run(conversion.script)


def finish (tmp_file, output_file=False, clean=True):
    """
    convPY's result:  
    * return last conversion's output from tmp-file and clean-up
    
    ARGS:
    * tmp_file [STRING]: The temporary files going to be cleaned up
    * output_file [STRING]: An optional output directory
    * clean [BOOLEAN]: If True clean up, if False don't and keep all tmp-files and directories

    TO-DO:
    * save last conversion's output from tmp-file in user-defined output-folder
    """
    output = open_file (tmp_file)
    if output_file != False:
        create_file(output_file, output)
    print(output)
    if clean == True:
        clean_tmp(tmp_file)
    sys.exit(0)


def open_file (path):
    """
    opens files and reads it in with params 

    ARGS:
    * path: path of file being opened 

    RETURN:
    * content of a file or sys.exit(1)
    """
    try:
        with open(path, 'r') as out:
            output = out.read()
        return output
    except:
        print ('[convPY:ERROR] Failed in reading in file "' + path +'". Exit!')
        sys.exit(1)


def preset (data, tmp_file):
    """
    starts convPY's workflow by creating the essential file-system for temporary file
    """

    def create_tmp_essentials (tmp_file, data):
        os.makedirs( os.path.dirname( tmp_file ) )
        create_file( tmp_file, data )

    tmp_file = tmp_file
    tmp_dir = os.path.dirname( tmp_file )
    try:
        if not os.path.exists( tmp_dir ):
            create_tmp_essentials(tmp_file, data)
        else:
            clean_tmp(tmp_file)
            create_tmp_essentials(tmp_file, data)
    except:
        print ('[convPY:ERROR] Failed in creating essential file "' + tmp_file +'". Exit!')
        sys.exit(1)


def read_JSON_file (json_file):
    """
    reads a JSON File

    ARGS:
    *json_file (STR): Path to a JSON File

    RETURN:
    * content of a JSON file
    """
    return json.load(open_file(json_file))


def retrieve (path):
    """
    input handler which loads the input data and decides if File or URL and returns the data
    
    ARGS:
    * path: file-path or url which should be read in
    """
    try:
        if path.startswith('http'):
            return request(path)
        elif os.path.exists(path) and os.path.isfile(path):
            return open_file(path)
    except:
        print ('[convPY:ERROR] Failed in reading inpu-data "' + path +'". Exit!')    
        sys.exit(1)


def request (url):
    """
    requests data from url 
    
    ARGS:
    * url: url whose data is going do be responded (well ... when server resonds)
    """
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        return data
    except:
        print ('[convPY:ERROR] Failed retrieving data from url "' + url +'" Exit!')
        sys.exit(1)



    
