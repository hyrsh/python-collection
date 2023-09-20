import os, sys
import random, time
import math as m
from PIL import Image, ImageDraw
import multiprocessing
import numpy as np
import argparse
from halo import Halo

#paths
target="./test.jpg"
dst_path="./palettes"

#half of the available cpus (gets overwritten if -cpus is set)
cpuc=int(multiprocessing.cpu_count()/2)

#callback error for multiprocessing threads
def cbErr(e):
  print(e)

#array containing all unique colors
colorStorageArray=[[0,0,0,0,0]] #default useless value for format

#cleaned up array containing all unique colors
cleanedStorage=[[0,0,0,0,0]] #default useless value for format

#multiprocessing queue setter
def qSet(r):
  print("Processed {} entries".format(len(r)))
  for i in range(0,len(r)):
    colorStorageArray.append(r[i])

#destination directory creating if non-existent
if not os.path.exists(dst_path):
    os.mkdir(dst_path)
    print("Destination directory created!")

#cleanup given array (merge)
def cleanStorage(storage,topc):
  total=len(storage) #topc*cpuc #avoid loss if multiple parts have many different hits
  hit=False #hit scan start value
  for i in range(0,total):
    hit=False #reset hit scan
    nLen=len(cleanedStorage)
    if nLen > topc: #failsafe if cleanedStorage grows too much
      nLen=topc
    for j in range(0,nLen):
      r=storage[i][1] #color to compare
      g=storage[i][2] #color to compare
      b=storage[i][3] #color to compare
      c=storage[i][4] #count of color to compare
      p1=cleanedStorage[j][0] #new saved part to compare
      r1=cleanedStorage[j][1] #new saved color to compare
      g1=cleanedStorage[j][2] #new saved color to compare
      b1=cleanedStorage[j][3] #new saved color to compare
      c1=cleanedStorage[j][4] #count of new saved color to compare
      if r==r1 and g==g1 and b==b1:
        cleanedStorage[j][4]+=c #increase hit counter of new saved color
        r=0 #reset old color
        g=0 #reset old color
        b=0 #reset old color
        c=0 #reset old count
        hit=True #set hit scan

    if hit==False:
      cleanedStorage.append([0,r,g,b,c]) #add as new unique color
        
#fill colorStorageArray with identical colors per cpu fraction
def colorAvg(end,p,r,g,b):
  hit=False
  sLen=len(colorStorageArray)

  for i in range(0,sLen):
    if colorStorageArray[i][0]==p and colorStorageArray[i][1]==r and colorStorageArray[i][2]==g and colorStorageArray[i][3]==b:
      #print("Hit")
      colorStorageArray[i][4]+=1
      hit=True

  if hit==False:
    #print("Stored")
    colorStorageArray.append([p,r,g,b,0])

#main function to fill colorStorageArray (contains colorAvg)
def colorCount(start, end, height, part, img):
  s=start
  offsetX=start+end
  #print("Part {} started from {} to {}".format(part, s, offsetX)) #debug for part areas
  for xr in range(s,offsetX):
    for i in range(0,height):
      currentColor=img.getpixel((s,i)) #0=red, 1=green, 2=blue, 3=alpha
      r=currentColor[0]
      g=currentColor[1]
      b=currentColor[2]
      hit=False
      sLen=len(colorStorageArray)

      for i in range(0,sLen):
        if colorStorageArray[i][0]==part and colorStorageArray[i][1]==r and colorStorageArray[i][2]==g and colorStorageArray[i][3]==b:
          colorStorageArray[i][4]+=1
          hit=True
      
      if hit==False:
        colorStorageArray.append([part,r,g,b,1]) #new color with hit count 1
    s+=1
  time.sleep(0.1) #avoid racing condition for multiple array appends in callback
  return colorStorageArray

#split workload to process image faster
def processImage(img):
  h=img.height #image height
  w=img.width #image width
  tempHeight=h #left there for manual testing
  print("Image dimensions {}x{}px".format(w,h)) #debug
  offsetX_start=0 #starting point
  offsetX_failsafe=w%cpuc #get overhead
  offsetX=int((w-offsetX_failsafe)/cpuc) #offset
  prt=multiprocessing.Pool(cpuc) #multiprocessing pool

  #split workload
  for p in range(0,cpuc):
    #all other parts
    if p != 0 and p != cpuc-1:
      prt.apply_async(func=colorCount,args=(offsetX_start,offsetX,tempHeight,p+1,img,),callback=qSet,error_callback=cbErr)
    #last part
    elif p == cpuc-1:
      prt.apply_async(func=colorCount,args=(offsetX_start,offsetX+offsetX_failsafe,tempHeight,p+1,img,),callback=qSet,error_callback=cbErr)
    #first part
    else:
      prt.apply_async(func=colorCount,args=(offsetX_start,offsetX,tempHeight,p+1,img,),callback=qSet,error_callback=cbErr)
    #increment offset starting point
    offsetX_start+=offsetX

  
  prt.close() #close queue
  prt.join() #join queue threads
  #time.sleep(3)

#name tag generator for saving color palette file
def nameGen():
  amount=10 #amount of letters
  pool=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
  ret="" #return string
  for i in range(0,amount-1):
    ret+=pool[random.randrange(0,len(pool)-1)]
  return ret

def drawResult(colors, count):
  tag=nameGen() #get random tag
  name="palette_"+tag #create name
  c=[] #array that holds the "count" amount of colors
  for i in range(0,count): #fill array
    c.append((colors[i][1],colors[i][2],colors[i][3]))
  #cosmetics
  globalBorder=8 #frame thickness
  innerBorder=8 #inner distance
  paletteHeight=160 #color bar height
  background=(255,255,255) #color of all divider and borders
  img=Image.open(target).convert("RGBA") #open original picture that was analyzed
  h=img.height+(globalBorder*2)+innerBorder+paletteHeight #get height + cosmetic dimensions
  w=img.width+globalBorder+globalBorder #get width + cosmetic dimensions
  paletteWidth=int((w-((globalBorder*2)+(innerBorder*(count-1))))/count) #get maximum width of color bar
  curX=globalBorder #cursor start X axis
  curY=globalBorder+img.height+innerBorder #cursor start Y axis


  base=Image.new(mode="RGBA", size=(w,h), color=background) #create canvas
  base.paste(img,(globalBorder,globalBorder),img) #paste original onto canvas
  img.close() #close original
  base.save(dst_path+"/"+name+".png") #save canvas

  for i in range(0,count):
    base=Image.open(dst_path+"/"+name+".png").convert("RGBA") #open saved canvas
    d=ImageDraw.Draw(base) #init drawing
    shape=(curX,curY,curX+paletteWidth,curY+paletteHeight) #color bar dimensions in pixel coordinates
    d.rectangle(shape,fill=c[i]) #draw rectangle
    base.save(dst_path+"/"+name+".png") #save canvas again
    curX+=paletteWidth+innerBorder #move offset to "right"

def colorCountCorrection():
  c=0
  for i in cleanedStorage:
    if i[4]!=0:
      c+=1
  return c

if __name__ == '__main__':
  startTime=time.time() #get current time
  parser=argparse.ArgumentParser() #init cli args
  parser.add_argument('-target',default="./test.png") #flag -target
  parser.add_argument('-top',default=5) #flag -top
  parser.add_argument('-cpus',default=2) #flag -cpus
  args=parser.parse_args() #parse cli flags
  #set data from flags
  topc=int(args.top)
  target=args.target
  cpuc=int(args.cpus)

  img=Image.open(target).convert("RGBA") #open target file to analyze
  print("Using {} CPUs".format(cpuc)) #debug
  print("-----------------------") #debug
  print("Processing ...")
  #halo package
  #prfx="Processing"
  #spinner = Halo(text=prfx+" colors... ", color='red') #spinner settings
  #spinner.start() #spinner entry
  processImage(img) #main processing entrypoint
  #spinner.stop() #spinner terminate
  print("[+] Finished!") #debug
  
  #close target file handle
  img.close()

  #nice python way ! inverse sort array on value in fifth column
  s1=sorted(colorStorageArray, key=lambda tophits: tophits[4], reverse=True)
  
  cleanStorage(s1,topc) #cleaned sorted storage

  #nice python way ! inverse sort array on value in fifth column
  s=sorted(cleanedStorage, key=lambda tophits: tophits[4], reverse=True)
  
  print("-----------------------")
  print("Colors total: {}".format(colorCountCorrection()))
  print("Top{} identical colors:".format(topc))
  print("-----------------------")
  if topc > colorCountCorrection(): #failsafe to avoid array out of bounds
    topc=colorCountCorrection()
  for i in range(0,topc):
    print("#{}\t({},{},{}),\tHits: {}".format(i+1,s[i][1],s[i][2],s[i][3],s[i][4]))
  drawResult(s,topc) #call drawing
  endTime=time.time() #get time after execution
  print("-----------------------")
  print("Elapsed time {}s".format(endTime-startTime))