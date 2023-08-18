import os, sys, re
import random
import math as m
from PIL import Image

#paths
src_path="./src_images"
dst_path="./dst_images"

#prefix
pfx="collage"

#settings
col=2
rSizeFac=1
yshift=int(512/rSizeFac)
xshift=int(512/rSizeFac)

#creating if non-existent
if not os.path.exists(src_path):
    os.mkdir(src_path)
    print("Source directory created!")

#creating if non-existent
if not os.path.exists(dst_path):
    os.mkdir(dst_path)
    print("Destination directory created!")

def sorty(l):
    l2=[]
    prf="src_sorted_"
    for i in l:
        r=re.sub(r".*\(","",i)
        r2=re.sub(r"\).*","",r)
        r3=re.sub(r".*\_","",r2)
        r4=re.sub(r"\..*","",r3)
        #print(r4)
        #print(src_path+"/"+i, src_path+"/"+prf+r4+".png")
        os.rename(src_path+"/"+i, src_path+"/"+prf+r4+".png")
        l2.append(int(r4))
    #os.exit(1)
    l3=sorted(l2)
    idx=0
    for n in l3:
        l3[idx]=prf+str(l3[idx])+".png"
        idx+=1
    return l3
    
#get items of directories
dlist=os.listdir(dst_path)
slist=sorty(os.listdir(src_path))

#get first image dimensions
dImg=Image.open(src_path+"/"+slist[0])
yshift=int(dImg.width/rSizeFac)
xshift=int(dImg.height/rSizeFac)
dImg.close()

#get columns
if len(sys.argv) > 1:
    if int(sys.argv[1]) > 0:
        col=int(sys.argv[1])
        print("Columns set to {}".format(str(sys.argv[1])))
else:
    print("Columns set to default (2)")


def createCollageInit():
    index=len(dlist)
    name=dst_path+"/"+pfx+"_"+str(int(index))+".png"
    q=len(slist)
    if q%col == 0:
        dimX=int(xshift*int(q/col))
    else:
        r=(q+(col-(q%col)))/col
        dimX=int(xshift*r)
    dimY=int(yshift*col)
    #debug and safety
    res = Image.new(mode="RGB", size=(dimY,dimX), color="black")
    res.save(name)
    print("Created target {} with {}px x {}px".format(name,dimX,dimY))
    return name

#name of collage
cName=createCollageInit()

def svImg(collage,element,x,y):
    img=Image.open(collage).convert("RGBA")
    ele=Image.open(element).convert("RGBA")
    ele2=ele.resize((yshift,xshift))
    img.paste(ele2,(y,x),ele2)
    #img.paste(ele,(y,x),ele)
    img.save(collage)
    img.close()
    ele.close()

#starting coordinates
x=0
y=0

print("Processing {} images ...".format(len(slist)))

for index, imgpath in enumerate(slist): #go through all pictures in the source directory
    i=src_path+"/"+imgpath
    svImg(cName,i,x,y)
    print("Step {}/{}".format(index+1,len(slist)))
    if (index+1)%col == 0:
        y=0
        x+=xshift
    else:
        y+=yshift
    
