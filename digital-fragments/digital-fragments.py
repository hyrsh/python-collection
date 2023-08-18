import os, sys
import random
import math as m
from PIL import Image
from wand.image import Image as wimg

#paths
src_path="./src_images"
dst_path="./dst_images"

#prefix
pfx="fragmented"

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

#inits
x_pos=0
y_pos=0

shift_y_pos=0
shift_x_pos=0

#recursion limit for large pictures
sys.setrecursionlimit(1500)

def chColor(color, rnd):
    target=(0,0,0)
    nhc=10 #color enhancer value


    #change color filter
    if rnd == 0: #red
        target=(color[0]+int(nhc*1.1),color[1],color[2])
    if rnd == 1: #green
        target=(color[0],color[1]+int(nhc*1.5),color[2])
    if rnd == 2: #blue
        target=(color[0],color[1],color[2]+int(nhc*1.5))
    if rnd == 3: #r+g
        target=(color[0]+nhc,color[1]+nhc,color[2])
    if rnd == 4: #g+b
        target=(color[0],color[1]+nhc,color[2]+nhc)
    if rnd == 5: #r+b
        target=(color[0]+nhc,color[1],color[2]+nhc)
    if rnd == 6: #red filter
        target=(color[0]+10,color[1]-3,color[2]-3)
    #if rnd == 6: #purple filter
    #    target=(color[0]+10,color[1]-3,color[0]+30)
    if rnd == 7: #lightblue filter
        target=(color[0]-2,color[1]+10,color[2]+10)
    #if rnd == 7: #green filter
    #    target=(color[0],color[1]+30,color[2])
    if rnd == 8: #darken
        target=(color[0]-nhc,color[1]-nhc,color[2]-nhc)
    
    #capture exceeding values    
    if target[0] > 255:
        target=(255,target[1],target[2])
    if target[1] > 255:
        target=(target[0],255,target[2])
    if target[2] > 255:
        target=(target[0],target[1],255)
    if target[0] < 0:
        target=(0,target[1],target[2])
    if target[1] < 0:
        target=(target[0],0,target[2])
    if target[2] < 0:
        target=(target[0],target[1],0)
        
    return target

def drawQdr(start_x,start_y,end_x,end_y,img,bDir):
    #get pixel amount to get total pixels for loop
    xlen=end_x-start_x
    ylen=end_y-start_y
    ttl=xlen*ylen

    #bars start from left or right
    if bDir == "left":
        x=start_x
    if bDir == "right":
        x=width-1
    
    y=start_y
    
    #get a random number for filter color choice
    #filterColor=random.randrange(0,9)
    filterColor=random.randrange(6,8) #we do not use all color filters for now (6,7,8 are sufficient)
    
    #go through all pixels in the square and adjust the pixel color to a new color (dependent on the random filter)
    for i in range(0,ttl):
        if bDir == "left": #bar direction starting from left
            if x < end_x:
                currentColor=img.getpixel((x,y)) #get current pixel color
                newColor=chColor(currentColor,filterColor) #get new color after applying the filter
                img.putpixel((x,y),newColor) #draw pixel with new color
                x+=1
            else:
                x=start_x
                y+=1
        if bDir == "right": #bar direction starting from right
            if x > width-end_x:
                currentColor=img.getpixel((x,y)) #get current pixel color
                newColor=chColor(currentColor,filterColor) #get new color after applying the filter
                img.putpixel((x,y),newColor) #draw pixel with new color
                x-=1
            else:
                x=width-1
                y+=1

def ripQdr(start_x,start_y,end_x,end_y,img):
    #get pixel amount to get total pixels for loop
    xlen=end_x-start_x
    ylen=end_y-start_y
    ttl=xlen*ylen

    #get a random number ripping (this is the distance pixels will jump to the right)
    ripRange=random.randrange(0,14)

    if end_x <= img.width:
        x=end_x
    else:
        x=width-(ripRange+1)


    y=start_y
    if y < img.height-1:
        y=start_y
    else:
        y=img.height-1


    #go through all pixels in the square and shift them by the rip range
    for i in range(0,ttl):
        if x > start_x+ripRange:
            #print("{}x/{}y".format(x-ripRange,y)) #debug, can be deleted
            shiftColor=img.getpixel((x-ripRange,y)) #get shifted (offset) pixel color
            img.putpixel((x,y),shiftColor) #draw pixel with new shifted color
            x-=1
        else:
            if end_x <= img.width:
                x=end_x
            else:
                x=width-(ripRange+1)
            if y < img.height-1:
                y+=1
            else:
                y=img.height-1

def rip(shift_x_pos,shift_y_pos,width,height,img):
    #get square coordinates for upper x, upper y, lower x and lower y
    offset_x=random.randrange(0,int(width/3)) #offset from the left edge
    offset_y=random.randrange(-2,2) #offset on the y axis
    start_x=shift_x_pos+offset_x #upper x coordinate
    start_y=shift_y_pos+offset_y #upper y coordinate
    end_x=start_x+random.randrange(int(width/8),width-offset_x) #lower x coordinate
    end_y=start_y+random.randrange(1,20) #lower y coordinate

    shift_y_pos=end_y #set current lower y for the next square to take in as upper y (see line with upper y coordinate)

    if end_x > width: #prevent out of bounds if next step would be wider than the picture
        end_x=width
    if start_y < 0: #prevent out of bounds if the y axis starting point would be above the first pixel (e.g. -1)
        start_y=0

    if shift_y_pos <= height: #prevent out of bounds for the last drawn bar (highest y coordinate value)
        ripQdr(start_x,start_y,end_x,end_y,img)
        rip(shift_x_pos,shift_y_pos,width,height,img)

def qdr(x_pos,y_pos,width,height,img,bDir):
    #get square coordinates for upper x, upper y, lower x and lower y
    offset_x=0 #offset from the left edge
    offset_y=random.randrange(-10,5) #offset on  the y axis
    start_x=x_pos+offset_x #upper x coordinate
    start_y=y_pos+offset_y # upper y coordinate
    end_x=start_x+random.randrange(5,width) #lower x coordinate
    end_y=start_y+random.randrange(1,10) #lower y coordinate

    y_pos=end_y #set current lower y for the next square to take in as upper y (see line with upper y coordinate)

    if end_x > width: #prevent out of bounds if next step would be wider than the picture
        end_x=width
    if start_y < 0: #prevent out of bounds if the y axis starting point would be above the first pixel (e.g. -1)
        start_y=0

    if y_pos <= height: #prevent out of bounds for the last drawn bar (highest y coordinate value)
        drawQdr(start_x,start_y,end_x,end_y,img,bDir)
        qdr(x_pos,y_pos,width,height,img,bDir)

def rndstr(amount):
    pool=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
    ret=""
    for i in range(0,amount-1):
        ret+=pool[random.randrange(0,len(pool)-1)]

    return ret

for index, imgpath in enumerate(slist): #go through all pictures in the source directory
    rid=rndstr(9)
    src_tag=src_path+"/"+imgpath #construct path as string
    dst_tag=dst_path+"/"+pfx+"_"+str(index+dest_count)+"_"+str(rid)+".png" #construct path string for destination output
    dst_green=dst_path+"/"+pfx+"_tinted_green_"+str(index+dest_count)+".png" #construct path string for destination output
    dst_red=dst_path+"/"+pfx+"_tinted_red_"+str(index+dest_count)+".png" #construct path string for destination output
    
    img=Image.open(src_tag).convert("RGBA") #load image from source directory
    width,height=img.size #get image height and width
    
    #color shift distance for overlays in pixel
    shift_len=8
    
    #overlay transperancy
    tp=255
    
    #shifting threshold (green/red overlays; only bright spots get shifted)
    threshold=180
    
    print("[+] Processing ...")
        
    #create green tinted image
    print("[1/5] Creating green tint ...")
    xgreen=0
    ygreen=0
    with wimg(filename=src_tag) as wi:
        #wi.tint(color="rgb(50,255,255)", alpha="rgb(10%,100%,100%)")
        wi.save(filename=dst_green)
    
    imgg=Image.open(dst_green).convert("RGBA")
    ite=(imgg.width-1)*(imgg.height-1)
    for i in range(0,ite):
        pc=imgg.getpixel((xgreen,ygreen)) #get pixel color
        avg=int((pc[0]+pc[1]+pc[2])/3) #average brightness
        if avg > threshold:
            imgg.putpixel((xgreen,ygreen),(0,200,200))
            
        xgreen+=1
        if xgreen >= imgg.width:
                ygreen+=1
                xgreen=0
                
    imgg.save(dst_green) #save overlay

    #create red tinted image
    print("[2/5] Creating red tint ...")
    xred=0
    yred=0

    with wimg(filename=src_tag) as wi:
        #wi.tint(color="rgb(255,80,80)", alpha="rgb(100%,30%,30%)")
        wi.save(filename=dst_red)
        
    imgr=Image.open(dst_red).convert("RGBA")
    ite=(imgr.width-1)*(imgr.height-1)
    for i in range(0,ite):
        pc=imgr.getpixel((xred,yred)) #get pixel color
        avg=int((pc[0]+pc[1]+pc[2])/3) #average brightness
        if avg > threshold:
            imgr.putpixel((xred,yred),(255,80,80))

        xred+=1
        if xred >= imgr.width:
                yred+=1
                xred=0

    imgr.save(dst_red) #save overlay
    
    #paste green tinted image as overlay (shifted -5px on the x-axis)
    print("[3/5] Overlay green tint ...")
    ov_green=Image.open(dst_green).convert("RGBA")
    ov_green.putalpha(tp) #transparency
    img.paste(ov_green,(int(random.randrange(1,shift_len))*-1,int(random.randrange(1,shift_len))*-1),ov_green)
    os.remove(dst_green) #delete after paste
    
    #paste red tinted image as overlay (shifted 5px on the x-axis)
    print("[4/5] Overlay red tint ...")
    ov_red=Image.open(dst_red).convert("RGBA")
    ov_red.putalpha(int(tp/2)) #transparency
    img.paste(ov_red,(int(random.randrange(1,shift_len))*-1,int(random.randrange(1,shift_len))*-1),ov_red)
    os.remove(dst_red) #delete after paste

    print("[5/7] Left bars ...")
    qdr(x_pos,y_pos,width,height,img,"left") #call left hand drawing func
    print("[6/7] Right bars ...")
    qdr(x_pos,y_pos,width,height,img,"right") #call right hand drawing func
    
    ov_org=Image.open(src_tag).convert("RGBA")
    ov_org.putalpha(50)
    img.paste(ov_org,(0,0),ov_org)
    
    print("[7/7] Ripping ...")
    rip(shift_x_pos,shift_y_pos,width,height,img) #call ripping func
    
    
    
    img.save(dst_tag) #save image to destination directory
    print("[FINISHED] Saved image {}".format(dst_tag))