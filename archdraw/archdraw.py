import argparse, os, time, random, yaml
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

#paths
cfg_dir="./configs"
thm_dir="./themes"
out_dir="./output"
fon_dir="./fonts"

#settings
prefix="arch_" #output picture prefix
clusterpadding=50 #distance from cluster frame to frame of an item
framewidth=4 #line width of frames
fwidthoff=int(framewidth/2) #middle of the frame is pivot point
itempaddingx=12 #X distance from item frame to font
itempaddingy=14 #Y distance from item frame to font
fontsize=30 #font size, default 36
fontheight=25 #font height, default 30
itemspace=8 #distance between items (frame to frame)
fontstyle=fon_dir+"/lc.ttf" #some font you want
charsize=19 #charsize for spacing --> highly dependent on your fontsize, default 22
itembase=(framewidth*2)+(itempaddingx*2) #width of an item in px
itemheight=((framewidth*2)+(fontheight)+(itempaddingy*2)) #height in px of a single item
chead=fontheight+10 #cluster heading Y coordinate offset
lhead=fontheight+10 #layer heading Y coordinate offset

#colors default if not set
backgroundcolor=(0,0,0)
framecolor=(255,255,255)
fontcolor=(255,255,255)

#runtime settings
clusterdb=[] #multidimensional array of the whole cluster infos
clusterinfo=[] #contains all clusters [index, max chars, max items, layers]
clustersize=[] # dimensions in px [(clusterX, clusterY)]
clusterpicture="" #path to output picture

#directory create if non-existent
if not os.path.exists(cfg_dir):
  os.mkdir(cfg_dir)
  print("Created configs directory ({})".format(cfg_dir))

if not os.path.exists(out_dir):
  os.mkdir(out_dir)
  print("Created output directory ({})".format(out_dir))

if not os.path.exists(thm_dir):
  os.mkdir(thm_dir)
  print("Created themes directory ({})".format(thm_dir))

if not os.path.exists(fon_dir):
  os.mkdir(fon_dir)
  print("Created font directory ({})".format(fon_dir))

def setTheme(t):
  global backgroundcolor, framecolor, fontcolor
  backgroundcolor=t["theme"]["backgroundcolor"]
  framecolor=t["theme"]["framecolor"]
  fontcolor=t["theme"]["fontcolor"]

def clusterdimensions():
  frames=len(clusterinfo)*2 #frame amount of clusters
  btwcluster=(len(clusterinfo)-1)*clusterpadding #space between clusters
  width=(clusterpadding*2)+(clusterpadding*frames)+(framewidth*frames)+btwcluster #initial width
  layers=0
  for i in range(0,len(clusterinfo)):
    if clusterinfo[i][3] > layers:
      layers=clusterinfo[i][3] #overwrite layers always with highest number of layers to get a total height
    width+=(clusterinfo[i][1]*charsize) #maximum chars across layers
    width+=(clusterinfo[i][2]*itembase) #maximum items across layers
  layers+=1 #initial start at 0 changed to 1 AFTER counting
  clusterheight=(clusterpadding*2)+(framewidth*2)
  height=clusterheight+(itemheight*layers)+(lhead*layers)+chead
  clustersize.append((int(width),int(height)))

def paintcluster():
  x=clusterpadding #upper left X coordinate init value
  y=clusterpadding+chead #upper left Y coordinate init value
  img=Image.open(clusterpicture)
  font=ImageFont.truetype(fontstyle, fontsize)
  draw=ImageDraw.Draw(img)
  itemspacerx=0 #if only one item is present the last spacer is a clusterpadding
  itemspacery=0 #spaces between items only apply if there are more than one
  for i in range(0,len(clusterinfo)):
    if clusterinfo[i][2] > 1:
      itemspacerx=((clusterinfo[i][2]-1)*itemspace)
    if clusterinfo[i][3] > 1:
      itemspacery=((clusterinfo[i][3]-1)*itemspace)
    layers=clusterinfo[i][3]
    cx=x
    cy=y
    cx2=cx+(clusterinfo[i][1]*charsize)+(clusterinfo[i][2]*itembase)+clusterpadding+clusterpadding
    cy2=cy+(clusterpadding*2)+(itemheight*layers)+itemspacery+(lhead*(layers))
    draw.rectangle(((cx,cy),(cx2,cy2)), width=framewidth, outline=framecolor)
    x=cx2+clusterpadding
    itemspacerx=0
    itemspacery=0
  img.save(clusterpicture)
  img.close()

def paintitems(c):
  x=(clusterpadding*2)+framewidth #upper left X coordinate init value
  y=(clusterpadding*2)+framewidth+chead+lhead #upper left Y coordinate init value
  img=Image.open(clusterpicture)
  font=ImageFont.truetype(fontstyle, fontsize)
  draw=ImageDraw.Draw(img)
  cx=x #component/item reference X
  cy=y #component/item reference Y
  lx=x #layer reference X
  ly=(clusterpadding*2)+framewidth+chead #layer reference Y
  clx=clusterpadding
  cly=clusterpadding
  ccur=x #cluster cursor points to current cluster frame upper left X coordinate
  itemspacer=clusterpadding #if only one item is present the last spacer is a clusterpadding
  for i in range(0,len(clusterinfo)):
    cln=c["cluster"][i]["name"]
    draw.text((clx,cly), cln, font=font, fill=fontcolor)
    cx=ccur
    lx=ccur
    for j in range(0,len(c["cluster"][i]["layers"])):
      ln=c["cluster"][i]["layers"][j]["layer-name"]
      draw.text((lx,ly) ,ln, font=font, fill=fontcolor)
      for k in range(0,len(c["cluster"][i]["layers"][j]["components"])):
        layers=clusterinfo[i][3]
        n=c["cluster"][i]["layers"][j]["components"][k]["item"]["name"]
        clen=len(n)
        cx2=cx+(itempaddingx*2)+(clen*charsize)
        cy2=cy+(itempaddingy*2)+fontheight
        draw.text((cx+itempaddingx,cy+itempaddingy), n, font=font, fill=fontcolor)
        draw.rounded_rectangle(((cx,cy),(cx2,cy2)), outline=framecolor, width=framewidth, radius=20, corners=(1,0,1,0))
        cx=cx2+itemspace
      cy+=itemheight+itemspace+lhead #add layer offset after all items in previous layer are drawn
      ly+=itemheight+lhead+itemspace #add layer offset with layer heading size
      cx=ccur #reset X coordinate for next layer
    if clusterinfo[i][2] > 1:
      itemspacer=((clusterinfo[i][2]-1)*itemspace)
    ccur+=clusterpadding+((clusterinfo[i][1]*charsize)+(clusterinfo[i][2]*itembase)+(clusterpadding*2))
    cy=y
    ly=(clusterpadding*2)+framewidth+chead
    itemspacer=clusterpadding
    clx=ccur-clusterpadding-framewidth #subtract offsets of frame and padding to keep it on the first edge
  img.save(clusterpicture)
  img.close()

def clusterwalk(c):
  size=()
  cinfo=[]
  linfo=[]
  iinfo=[]
  for i in range(0,len(c["cluster"])):
    cwidth=0 #max character per cluster across layers
    csize=0 #amount max components across layers
    for j in range(0,len(c["cluster"][i]["layers"])):
      tl=j #total layer
      lsize=0
      for k in range(0,len(c["cluster"][i]["layers"][j]["components"])):
        s=k #last entry is max. count items
        it=c["cluster"][i]["layers"][j]["components"][k]["item"]
        cluster=i
        layer=j
        name=it["name"]
        lsize+=len(name)
        iinfo.append((name,9))
      if lsize > cwidth:
        cwidth=lsize
      if s > csize:
        csize=s
      lname=c["cluster"][i]["layers"][j]["layer-name"]
      linfo.append((lname,iinfo))
      iinfo=[]
    cname=c["cluster"][i]["name"]
    cinfo.append((cname,linfo))
    linfo=[]
    size=(i,cwidth,csize+1,tl+1)
    clusterinfo.append(size)
  clusterdb.append(cinfo)

#create picture
def createPicture(c):
  name=c["name"]
  fullpath=out_dir+"/"+prefix+name+".png"
  global clusterpicture #this keyword is nice to know
  clusterpicture=fullpath
  w=clustersize[0][0]
  h=clustersize[0][1]
  dmImg=Image.new(mode="RGB", size=(w,h), color=backgroundcolor)
  dmImg.save(fullpath)
  print("[+] Created architecture picture at {}".format(clusterpicture))

if __name__ == '__main__':
  print("[+] Architecture drawing v1.0")
  print("[+] -------------------------")
  startTime=time.time() #get current time
  parser=argparse.ArgumentParser() #init cli args
  parser.add_argument('-config',default="./configs/cluster.yml",help="[string] Path to config file")
  parser.add_argument('-theme',default="./themes/default.yml",help="[string] Path to theme file")
  args=parser.parse_args() #parse cli flags
  #set data from flags
  cfg=str(args.config)
  thm=str(args.theme)
  
  #load themes
  with open(thm, "r") as themes_raw:
    themes=yaml.safe_load(themes_raw)
  #load config
  with open(cfg, "r") as config_raw:
    config=yaml.safe_load(config_raw)

  clusterwalk(config)
  setTheme(themes)
  print("Cluster info: {}".format(clusterinfo))
  clusterdimensions()
  print("Cluster dimensions: {}".format(clustersize[0]))
  createPicture(config)
  paintcluster()
  paintitems(config)
  #print("-------------------------------------------------------")
  #INFO: DO NOT DELETE
  #clusterdb[0][0][0] #Cluster 0 name
  #clusterdb[0][0][1] #Cluster 0 layer array
  #clusterdb[0][0][1][0][1] #Cluster 0 layer 0 item array
  #print("-------------------------------------------------------")