import os
import re
import reportlab
import arabic_reshaper
from bidi.algorithm import get_display

import pandas as pd
import qrcode

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import utils
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    Paragraph, 
    Frame, 
    Image, 
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# def get_excel_data(excel_path):
#     data = pd.read_excel(excel_path).dropna()

#     records = data.to_dict("index") 
    
#     return records


def image_creator(book_name, book_link):    
    qr = qrcode.QRCode(
        version = 1,
        box_size = 10,
        border = 5
    ) 

    #* Adding data to the instance 'qr'
    qr.add_data(book_link)
    
    qr.make(fit=True)
    img = qr.make_image(fill_color='blue',
                        back_color='white')

    img.save('img/' + str(book_name) + '.png')

    return img

#* important for Arabic language 
reportlab.rl_config.TTFSearchPath.append('/home/gold/projects/fonts/')  # must use BASE_DIR path
# must use BASE_DIR path
pdfmetrics.registerFont(TTFont('KFGQPC Uthman Taha Naskh Regular', '/home/gold/projects/fonts/Traditional_Arabic.ttf')) 


def get_image(path, width=1):
    """ 
        #*: help in pass the image to the frame in reportlab  
    """
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))



def create_pdf(author_name, book_name, book_link):
    #* Assign a path for created pdf covers
    pdf = Canvas("book_covers/{}.pdf".format(book_name))
    image_frame = Frame(100, 300, 400, 400, showBoundary=0, leftPadding=1, rightPadding=1, bottomPadding=1, topPadding=1)

    text_frame = Frame(100, 100, 400, 200, showBoundary=0, leftPadding=1, rightPadding=1, bottomPadding=1, topPadding=1)
        
    directory = 'img/'

    #* save image to directory
    image_creator(book_name=book_name, book_link=book_link)
    
    code = []
    code.append(get_image(directory + book_name + '.png', width=150))
    
    #* add image to the frame
    image_frame.addFromList(code, pdf)

    #* Drawing the image
    pdf.drawInlineImage(directory + book_name + '.png', 100, 300, 400, 400)

    #* add link to the frame (rectangle)
    pdf.linkURL(book_link, rect=(145, 335, 455, 655), relative=5)


    text_list = []
    styles = getSampleStyleSheet()
    style = styles['Title']

    text_1 = arabic_reshaper.reshape(u"اسم الكتاب: {}".format(book_name))
    text_1 = get_display(text_1)
    text_2 = arabic_reshaper.reshape(u"اسم المؤلف: {}".format(author_name))
    text_2 = get_display(text_2)
    text = re.sub(r'\n\n', '<br/><br/>', (text_1 + '\n\n\n\n' + text_2))

    text_list.append(Paragraph(text, 
            ParagraphStyle(
                name='', fontName='KFGQPC Uthman Taha Naskh Regular', 
                fontSize=18, textColor='black', alignment=TA_CENTER
            ), 
            encoding='utf8'
        )
    )

    #* add text to the new frame 
    text_frame.addFromList(text_list, pdf)

    #* save the file 
    pdf.save()

    return pdf


def generate_books_cover(excel_path):
    data = pd.read_excel(excel_path).dropna()
    
    records = data.to_dict("index")
    keys = [key for key in records][1:]
    for key in keys:
        author_name = records[key]['المؤلف']
        book_name = records[key]['الرواية']
        book_link = records[key]['رابط الكتاب']
        create_pdf(author_name, book_name, book_link)




# if __name__ == '__main__':
#     generate_books_cover('data.xlsx')


