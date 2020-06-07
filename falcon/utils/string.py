import re

def xml2Html(xml_content):
    html = xml_content.split("<en-note>")[1].replace("</en-note>", "")
    pa1 = re.compile(r"\<en\-media.*\s+hash\=\"[0-9a-z+]+\".*\<\/en\-media\>", re.M)
    re_data1  = re.findall(pa1, html)

    pa2 = re.compile(r"\<en\-media.*\s+hash\=\"[0-9a-z+]+\"/\>", re.M)
    re_data2  = re.findall(pa2, html)

    match_items = re_data1 + re_data2;
    for row in match_items:
        img = row.split("hash=")[1].split('"')[1]
        element_image = "<img src='/upload/"+img+".png'/>"
        html = html.replace(row, element_image)
    return html
