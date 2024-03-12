import os
import base64
import json

## parse API response data
def GetNamedNode(res, name):
    jRes = json.loads(res)
    return jRes[name]

## map file types

def GetFileType(path):
    filename, file_extension = os.path.splitext(path)
    file_extension = file_extension[1:].lower()
    types = {
    "doc":"DOC",
    "docx":"DOCX",
    "xls":"XLS",
    "xlsx":"XLSX",
    "ppt":"PPT",
    "pptx":"PPTX",
    "odt":"ODT",
    "odp":"ODP",
    "ods":"ODS",
    "rtf":"RTF",
    "xml":"XML",
    "xliff":"XLIFF",
    "xlf":"XLIFF",
    "sdlxliff":"XLIFF",
    "tmx":"TMX",
    "htm":"HTML",
    "html":"text/html",
    "pdf":"PDF"
    }
    if (file_extension in types):
        return types[file_extension];
    else:
        return "PLAIN"
