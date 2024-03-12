![](Aspose.Words.e55ab1fe-da12-4eed-b8d5-b8acd6778f25.001.png)





**JavaScript Access to Language Weaver**
1. # **Overview**
Accessing any web resource from JavaScript is likely to result in a CORS (Cross-Origin Resource Sharing) error. JavaScript is very restrictive, and blocks most cross-domain requests. Even using a server in the same domain but with a different port counts as a security violation.

To work around this, you need a server that explicitly allows calls from other domains. For security reasons, RWS can't grant CORS access to everybody, so you need some sort of proxy server you control, and set that up to allow access. Communication from the proxy server to Language Weaver is no problem: CORS only limits access from browsers.
1. # **Prerequisites**
The sample server was developed in Python 3.9 (other versions should be fine). The *requests* and *web* modules need to be installed in Python.

Python provides a simple way to run a web server with just a few lines of code, but of course you can use any server technology you are familiar with instead.
1. # **The Client Side**
User access is from a simple web page: *LanguageWeaverTest.html*. You can enter a text string and Source and Target languages ( <https://translate-api.sdlbeglobal.com/documentation/#language-codes> ). For testing, it's ok to load it from your local file system. The sample uses jquery to call the proxy API, but plain JS would work, too.

The translate string is converted to base64 before sending it, and likewise the returned translation is in base64. That is just a suggestion, you may choose to use other ways of passing data around.
1. # **The Server Side**
The server consists of two main parts:
1. ## LanguageWeaverProxy.py
This is the actual server. It implements a simple REST api with just one GET call: /translate/<text>/<sourceLng>/<targetLng>, where text is base64 encoded, for example: /translate/VGhpcyBpcyBhIHRlc3Q=/eng/spa"

It runs on port 8080 by default, if required, that can be reconfigured.

This is also where the CORS doors are opened, by adding a header value:

web.header('Access-Control-Allow-Origin', '\*')

This is the quick and easy version, open to the world. In a real life scenario, you may want to be more restrictive and only allow access from a given domain, for example:

'Access-Control-Allow-Origin', 'https://domain1.example'
## LanguageWeaverTranslator.py and LanguageWeaverUtil.py
This is the core functionality to obtain translations from Language Weaver. Since it is re-used from a standalone python sample, there is a bit more functionality then required for this demo, like file translation.
1. # **How to use**
Edit *LanguageWeaverProxy.py*, providing your own client id and secret.















![](Aspose.Words.e55ab1fe-da12-4eed-b8d5-b8acd6778f25.002.png)Assuming Python is installed, run *StartProxy.cmd*. It should open a command window displaying: http://0.0.0.0:8080/

Open *LanguageWeaverTest.html* in a browser, and you're ready to translate.

You can also open the client on a different machine than your test server, as long as your network/firewall allows communication between the machines. In that case, you need to edit the html file and change this line:

url: 'http://localhost:8080/translate/' + b64EncodeUnicode(text) + "/" + src + "/" + trg,

to this (replacing the 11.11.111.111 by the address of the proxy server):

url: 'http://11.11.111.111:8080/translate/' + b64EncodeUnicode(text) + "/" + src + "/" + trg,




![](Aspose.Words.e55ab1fe-da12-4eed-b8d5-b8acd6778f25.003.png)![](Aspose.Words.e55ab1fe-da12-4eed-b8d5-b8acd6778f25.004.png)
