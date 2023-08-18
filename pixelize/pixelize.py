import os, sys
import random
import math as m
from PIL import Image

#paths
src_path="./src_images"
dst_path="./dst_images"

#prefix
pfx="pixelized"

#creating if non-existent
if not os.path.exists(src_path):
    os.mkdir(src_path)
    print("Source directory created!")

#creating if non-existent
if not os.path.exists(dst_path):
    os.mkdir(dst_path)
    print("Destination directory created!")

#get items of directories
dlist=os.listdir(dst_path)
slist=os.listdir(src_path)

#debug and safety
if len(slist) == 0:
    res = Image.new(mode="RGB", size=(500,500), color="black")
    res.save(src_path+"/"+"dummy_source.png")
    print("No sources found! Creating dummy ...")

#get count to prevent overwrite
dest_count=len(dlist)

def square(img,x,y,ps):
    r,g,b=0,0,0 #color buffer

    xtmp=0 #init
    ytmp=0 #init

    #get all colors
    for i in range(0,ps*ps):
        c=img.getpixel((xtmp+x,ytmp+y)) #draw pixel with new color
        r+=c[0]
        g+=c[1]
        b+=c[2]
        xtmp+=1
        if xtmp >= ps:
            xtmp=0
            ytmp+=1

    xtmp=0 #reset
    ytmp=0 #reset
    r=int(r/(ps*ps))
    g=int(g/(ps*ps))
    b=int(b/(ps*ps))

    #set average
    for i in range(0,ps*ps):
        img.putpixel((xtmp+x,ytmp+y),(r,g,b)) #draw pixel with new color
        xtmp+=1
        if xtmp >= ps:
            xtmp=0
            ytmp+=1

def pixelize(img, ps):
    #boundaries
    width,height=img.size
    hor_cnt=int((width-(width%ps))/ps)
    ver_cnt=int((height-(height%ps))/ps)

    x,y=0,0

    for total in range(0,hor_cnt*ver_cnt):
        square(img,x,y,ps)
        x+=ps
        if x >= hor_cnt*ps:
            x=0
            y+=ps
            if y >= ver_cnt*ps:
                break


for index, imgpath in enumerate(slist): #go through all pictures in the source directory
    src_tag=src_path+"/"+imgpath #construct path as string
    dst_tag=dst_path+"/"+pfx+"_"+str(index+dest_count)+".png" #construct path string for destination output
    pixel_size=0 #size of pixelated area per "dot" in px

    if len(sys.argv) < 3:
        pixel_size=4
        print("-px <int 2-499> not used (defaulting to 4)")
    else:
        if sys.argv[1] == "-px" and int(sys.argv[2]) > 1 and int(sys.argv[2]) < 500:
            pixel_size=int(sys.argv[2])
            print("Using {}px mask.".format(pixel_size))
        else:
            pixel_size=4
            print("-px <int 2-499> not used (defaulting to 4)")

    img=Image.open(src_tag).convert("RGBA") #load image from source directory

    pixelize(img, pixel_size)

    img.save(dst_tag) #save image to destination directory
    print("[FINISHED] Saved image {}".format(dst_tag))