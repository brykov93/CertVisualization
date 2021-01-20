# -*- coding: utf-8 -*-
import subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
def put_text_pil(img, txt,x_pos,y_pos):
    im = Image.fromarray(img)
 
    font_size = 42
    font = ImageFont.truetype('times.ttf', size=font_size)
 
    draw = ImageDraw.Draw(im)
    # здесь узнаем размеры сгенерированного блока текста
    w, h = draw.textsize(txt, font=font)

    im = Image.fromarray(img)
    draw = ImageDraw.Draw(im)
 
    # теперь можно центрировать текст
    draw.text((x_pos, y_pos), txt, fill='rgb(0, 0, 0)', font=font)
 
    img = np.asarray(im)
 
    return img
output = subprocess.check_output('"C:\Program Files\Crypto Pro\CSP\certmgr.exe"  -list -cert -store uMy')
res=output.split(b'-------')
res.pop(0)
certs=[]
for cert in res:
    a=cert.replace(b'\r',b'').split(b'\n')
    certsInfo={}
    for certInfo in a:
        b=certInfo.split(b':')
        i=0
        for c in b:
            k=c.strip()
            if b'Issuer'==k:
                s=b[i+1].decode('cp866')
                info={}
                inf=s.split(',')
                for h in inf:
                    v=h.split('=')
                    if len(v)>1:
                        info[v[0]]=v[1]
                certsInfo['Issuer']=info
            elif b'Subject'==k:
                s=b[i+1].decode('cp866')
                info={}
                inf=s.split(',')
                for h in inf:
                    v=h.split('=')
                    if len(v)>1:
                        info[v[0]]=v[1]
                certsInfo['Subject']=info
            elif b'Serial'==k:
                certsInfo['Serial']=b[i+1][3:].decode()
            elif b'Not valid before'==k:
                certsInfo['ValidFrom']=(b[i+1]+b':'+b[i+2]+b':'+b[i+3]).decode()
            elif b'Not valid after'==k:
                certsInfo['ValidFor']=(b[i+1]+b':'+b[i+2]+b':'+b[i+3]).decode()
            i=i+1
    certs.append(certsInfo)
#f=open('res.txt','w')
i=1
for cert in certs:
    print('---------------Сертификат №'+str(i)+'---------------------')
    for a in cert:
        print((a+':'+str(cert[a])))
    print('----------------------------------------------------------')
    i=i+1
a=input('Выберите сертификат для подписи: ')
cert=certs[int(a)-1]
serial=cert['Serial']
if ' T' in cert['Subject']:
    dolgn=cert['Subject'][' T']+' '
else:
    dolgn=''
dolgOrg=dolgn+cert['Subject'][' O']
FAM=cert['Subject'][' SN']+' '+cert['Subject'][' G']
ValidFrom=cert['ValidFrom']
ValidFor=cert['ValidFor']
img=Image.open('pattern.png')

img = put_text_pil(np.asarray(img), serial, 240, 280)
img = put_text_pil(np.asarray(img), dolgOrg, 210, 351)
img = put_text_pil(np.asarray(img), FAM, 210, 390)
img = put_text_pil(np.asarray(img), ValidFrom, 380, 432)
img = put_text_pil(np.asarray(img), ValidFor, 380, 475)
cv2.imshow('Result', img)
cv2.waitKey()
    
