""" Get PDF metadata """

import re
import PyPDF2

def pdfinfo(fnm):
    with open(fnm, "rb") as f:
        pdf = PyPDF2.PdfFileReader(f)
        info = pdf.documentInfo
    author = info.get("/Author", None)
    title = info.get("/Title", None)
    keywords = info.get("/Title", None)
    datestr = info.get("/CreationDate", "")
    match = re.search("[0-9]{4}", datestr)
    if match:
        date = match.group()
    else:
        date = None
    return {"title":title, "author":author, "keywords":keywords, "date":date}

def asbibtex(info):
    pass

