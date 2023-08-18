import os
from PIL import Image, ImageDraw, ImageFont

#paths
sgn_path="./src_images"
font_path="./fonts/PublicPixel.ttf"

#postfix
pfx="_sign"

#list
wlist="./wordlist.txt"

#creating if non-existent
if not os.path.exists(sgn_path):
    os.mkdir(sgn_path)
    print("Sign directory created!")

#go through word list
wlr=open(wlist,"r")
wl=wlr.readlines()

def createSign(word):
    dim_x=320
    dim_y=320
    fac=10
    font_size=int((dim_x-(dim_x%fac))/fac)
    print("Raw, Mod/7, Mod: {} {} {}".format(dim_x/fac, dim_x%fac,((dim_x-(dim_x%fac))/fac)))
    font_len=len(word)
    
    offset_x=int((dim_x)/2)-(int((font_len*font_size)/2.1))
    #offset_x=dim_x/2
    offset_y=int((dim_y)/2)-(int(font_size/2))
    #offset_y=dim_y/2
    
    #sgn = Image.new(mode="RGB", size=(dim_x,dim_y), color=(13,13,13))
    sgn = Image.new(mode="RGB", size=(dim_x,dim_y), color=(17,17,17))
    sgn.save(sgn_path+"/"+str(word)+pfx+".png")
    i = Image.open(sgn_path+"/"+str(word)+pfx+".png")
    #i = Image.open(sgn_path+"/background3.png")
    d = ImageDraw.Draw(i)
    font = ImageFont.truetype(font_path, font_size)
    d.text((offset_x,offset_y), word, fill="white", font=font,align="center")
    i.save(sgn_path+"/"+str(word)+pfx+".png")

for L in wl:
    print("Text: {}".format(L.strip()))
    createSign(L.strip())