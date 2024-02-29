import argparse, os, time, random
from PIL import Image, ImageDraw

#paths
src_dir="./src_images"
dst_dir="./dst_images"

#settings
prefix="generated"

#directory create if non-existent
if not os.path.exists(src_dir):
  os.mkdir(src_dir)
  print("Created source directory ({})".format(src_dir))

if not os.path.exists(dst_dir):
  os.mkdir(dst_dir)
  print("Created destination directory ({})".format(dst_dir))

#name tag generator for saving file
def nameGen():
  amount=10 #amount of letters
  pool=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
  ret="" #return string
  for i in range(0,amount-1):
    ret+=pool[random.randrange(0,len(pool)-1)]
  return ret

#get all images in source directory
slist=os.listdir(src_dir)
lenslist=len(slist)

#dummy picture
def createDummy(path):
  dmImg=Image.new(mode="RGB", size=(500,500), color="black")
  dmImg.save(path)
  print("[+] Created dummy picture!")

#filter for bright patterns
def filter(color):
  xtnd=30 #difference to original color (must be within 255 range)
  red=color[0] #color array position for red
  green=color[1] #color array position for green
  blue=color[2] #color array position for blue
  
  if md == "light":
    #keep within 16bit color range
    if red > (255-xtnd):
      red=255
    else:
      red=red+random.randrange(0,xtnd) #randomize within brighten range to add "used look"
    if green > (255-xtnd):
      green=255
    else:
      green=green+random.randrange(0,xtnd) #randomize within brighten range to add "used look"
    if blue > (255-xtnd):
      blue=255
    else:
      blue=blue+random.randrange(0,xtnd) #randomize within brighten range to add "used look"

  if md == "dark":
    #keep within 16bit color range
    if (red-xtnd) < 0:
      red=0
    else:
      red=red-random.randrange(0,xtnd) #randomize within darken range to add "used look"
    if (green-xtnd) < 0:
      green=0
    else:
      green=green-random.randrange(0,xtnd) #randomize within darken range to add "used look"
    if (blue-xtnd) < 0:
      blue=0
    else:
      blue=blue-random.randrange(0,xtnd) #randomize within darken range to add "used look"

  return (red,green,blue) #return new color

def patternSquare(img):
  h=img.height
  w=img.width
  offset=int(7*sca)

  for y in range(0,h):
    for x in range(0,w):
      if y%offset == 0 or x%offset == 0: #squares with 7px side length
        currentColor=img.getpixel((x,y))
        newColor=filter(currentColor)
        img.putpixel((x,y),newColor)

  img.save(dst_dir+"/"+prefix+"_squares_"+nameGen()+".png")

def patternBlock(img):
  h=img.height
  w=img.width
  offset=int(7*sca)

  for y in range(0,h):
    for x in range(0,w):
      if (y%offset != 0 and x%offset != 0) and (y%offset != 1 and x%offset != 1): #blocks with 3px side length
        currentColor=img.getpixel((x,y))
        newColor=filter(currentColor)
        img.putpixel((x,y),newColor)

  img.save(dst_dir+"/"+prefix+"_blocks_"+nameGen()+".png")

def patternHybrid(img):
  h=img.height
  w=img.width
  offset_l=int(7*sca)
  offset_b=int(3*sca)
  offset_s=int(5*sca)

  for y in range(0,h):
    for x in range(0,w):
      if (y%offset_l == 0) or ((y%offset_b != 0 and x%offset_b != 0) and (y%offset_b != 1 and x%offset_b != 1)) or (y%offset_s == 0 or x%offset_s == 0): #hybrid pattern spacing
        currentColor=img.getpixel((x,y))
        newColor=filter(currentColor)
        img.putpixel((x,y),newColor)

  img.save(dst_dir+"/"+prefix+"_hybrid_"+nameGen()+".png")

def patternLine(img):
  h=img.height
  w=img.width
  offset=int(3*sca)

  for y in range(0,h):
    for x in range(0,w):
      if y%offset == 0: #horizontal lines with 3px spacing
        currentColor=img.getpixel((x,y))
        newColor=filter(currentColor)
        img.putpixel((x,y),newColor)

  img.save(dst_dir+"/"+prefix+"_lines_"+nameGen()+".png")

#main draw pattern switch
def drawPattern(img,path):
  startTime=time.time() #get current time
  
  #switch pattern
  if pat == "square":
    patternSquare(img)
  elif pat == "hybrid":
    patternHybrid(img)
  elif pat == "line":
    patternLine(img)
  elif pat == "block":
    patternBlock(img)
  else:
    print("Pattern not recognized (try square|hybrid|line|block)")

  endTime=time.time() #get time after execution
  print("[+] Time spent for {} was {}s".format(path,endTime-startTime))

if __name__ == '__main__':
  print("[+] Image pattern filter v1.0")
  print("[+] -------------------------")
  startTime=time.time() #get current time
  parser=argparse.ArgumentParser() #init cli args
  parser.add_argument('-pattern',default="square") #flag -pattern
  parser.add_argument('-scale',default=1) #flag -scale
  parser.add_argument('-target',default="./test.png") #flag -target
  parser.add_argument('-mode',default="light") #flag -mode
  args=parser.parse_args() #parse cli flags
  #set data from flags
  pat=str(args.pattern)
  tar=str(args.target)
  sca=int(args.scale)
  md=str(args.mode)
  
  if sca > 10:
    print("[+] Set scale to 10 (was {})".format(sca))
    sca=10
  
  #switch for batch processing
  if tar == "all":
    if lenslist == 0: #if all is selected and src dir is empty create dummy
      createDummy(src_dir+"/test.png")
      img=Image.open(src_dir+"/test.png").convert("RGBA")
      drawPattern(img,src_dir+"/test.png")
      img.close() #close file handle
    else:
      print("[+] Processing all images in {}".format(src_dir))
      for i in slist:
        img=Image.open(src_dir+"/"+i).convert("RGBA")
        drawPattern(img,src_dir+"/"+i)
        img.close() #close file handle
  else:
    if not os.path.exists(tar): #create dummy if target does not exist
      createDummy(tar)
    print("[+] Processing image {}".format(tar))
    img=Image.open(tar).convert("RGBA")
    drawPattern(img,tar)
    img.close() #close file handle

  endTime=time.time() #get time after execution
  print("[+] Total elapsed time {}s".format(endTime-startTime))