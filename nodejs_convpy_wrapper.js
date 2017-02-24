
/*
// Load the http module to create an http server.
var http = require('http');




// Configure our HTTP server to respond with Hello World to all requests.
var server = http.createServer(function (request, response) {
    
    let json_stdin = [
        {
            "name" : "step 1",
            "xsl" : "test2.xsl"
        },
        {
            "name" : "step 2",
            "xsl" : "test2.xsl"
        }
    ]
  
    let url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw' 

    let spawn = require('child_process').spawn;
    let py = spawn('python', ['conv.py', '-url:test']);
    let dataString = '';


    // good example of child_process: http://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/


    py.stdout.setEncoding('utf8').on('data', (data) => {
        dataString += data.toString();
    });

    py.stdout.on('end', () => {
        //console.log(dataString);
        response.writeHead(200, {"Content-Type": "text/xml"});
        response.end(dataString);
    });

    //py.stdin.write('http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw');
    //py.stdin.end();
  
  
});

// Listen on port 8000, IP defaults to 127.0.0.1
server.listen(8000);

// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:8000/");
*/


let url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw' 

let json_stdin = {
                "url" : "http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw",
                "steps" : [
                    {"scenario" : "cs_nlp"},
                    {"scenario" :   "strip-space"},
                    {
                        "name"  : "cs_post-processing",
                        "desc"  : "RegEx Postprocessing to clean up the data",
                        "type"  : "regex",
                        "script": "scripts/regex/cs_post.py",
                        "language"  : "python"
                    }
                ]}

let std_in = JSON.stringify(json_stdin)

let spawn = require('child_process').spawn;
let py = spawn('python', ['convpy_json.py']);
let dataString = '';


    // good example of child_process: http://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/


py.stdout.setEncoding('utf8').on('data', (data) => {
    dataString += data.toString();
});

py.stdout.on('end', () => {
    console.log(dataString);
    //response.writeHead(200, {"Content-Type": "text/xml"});
    //response.end(dataString);
});


py.stdin.write(std_in);
py.stdin.end();