import os, argparse
from PIL import Image, ImageDraw, ImageFont

mainsign="./main_res/Main_Sign.png"
f_res="./faceit_ranks"
dst="./result/main_sign_edit.png"

def fSymbol(selector):
  if selector == 1:
    return f_res+"/f_1.png"
  if selector == 2:
    return f_res+"/f_2.png"
  if selector == 3:
    return f_res+"/f_3.png"
  if selector == 4:
    return f_res+"/f_4.png"
  if selector == 5:
    return f_res+"/f_5.png"
  if selector == 6:
    return f_res+"/f_6.png"
  if selector == 7:
    return f_res+"/f_7.png"
  if selector == 8:
    return f_res+"/f_8.png"
  if selector == 9:
    return f_res+"/f_9.png"
  if selector == 10:
    return f_res+"/f_10.png"

def pColor(selector):
  if selector <= 4999:
    return (0,213,255)
  if selector > 4999 and selector <= 9999:
    return (0,128,255)
  if selector > 9999 and selector <= 14999:
    return (0,42,255)
  if selector > 14999 and selector <= 19999:
    return (191,0,230)
  if selector > 19999 and selector <= 24999:
    return (255,0,255)
  if selector > 24999 and selector <= 29999:
    return (255,0,43)
  if selector > 29999:
    return (230,191,0)


if __name__ == '__main__':
  parser=argparse.ArgumentParser() #init cli args
  parser.add_argument('-faceit',default=1) #flag -faceit
  parser.add_argument('-prime',default="11,000") #flag -prime
  args=parser.parse_args() #parse cli flags
  #set data from flags
  fc=int(args.faceit)
  pr=int(args.prime)
  fontColor=pColor(pr)
  img=Image.open(mainsign).convert("RGBA")
  fr=Image.open(fSymbol(fc)).convert("RGBA")
  w=int(fr.width/1.5)
  h=int(fr.height/1.5)
  rs=fr.resize((w,h))
  img.paste(rs,(180,20),rs)
  font = ImageFont.truetype("./main_res/lc.ttf", 48)
  draw = ImageDraw.Draw(img)
  draw.rounded_rectangle(((112,107),(332,184)), fill=(20,20,20), radius=20, outline=fontColor, width=4, corners=(1,0,1,0))
  draw.text((135, 125),str(format(pr, ",d")),fontColor, font=font, stroke_width=2, stroke_fill=(100,100,100))
  #draw.rectangle(((111,106),(333,185)), outline=(255, 255, 255))
  fr.close()
  img.save(dst)
  img.close()
  print("Done")