import os
from PIL import Image

dst_dir="sliced_images"
src_dir="raw_images"
prefix="r_"

#resizing
rsize=False
rsizeval=512

#upper left corner coordinates
x1=0
y1=1080
#lower right corner coordinates
x2=1919
y2=2159

def slicer(imgpath, index):
  src_tag=src_dir+"/"+imgpath
  dst_tag=dst_dir+"/"+prefix+str(index)+".png"
  
  img=Image.open(src_tag)
  crop=img.crop((x1,y1,x2,y2))
  if rsize == True:
    rs=crop.resize((rsizeval,rsizeval))
    rs.save(dst_tag)
  else:
    crop.save(dst_tag)
  print("[SAVED] ", dst_tag)

print("\n[ Image Slicer v1.0 ]")
print("-----------------")
print("Images get cropped to:")
print(" - Upper left [{}x{}]".format(x1,y1))
print(" - Lower right [{}x{}]".format(x2,y2))
print("")
print("Progress:\n")

if os.path.exists(dst_dir):
  print("[+] Destination directory exists. Skipping")
else:
  os.mkdir(dst_dir)
  print("[+] Created destination directory")

if os.path.exists(src_dir):
  print("[+] Source directory exists. Skipping")
else:
  os.mkdir(src_dir)
  print("[+] Created source directory")

dlist=os.listdir(dst_dir)
slist=os.listdir(src_dir)

if len(slist) != 0:
  print("[!] Processing")
  for index, i in enumerate(slist):
    slicer(i, index+len(dlist))
  print("\nFinished!")
else:
  print("[!] Make sure your DST is empty and your SRC is full")
  print("[+] DST = ",dst_dir)
  print("[+] SRC = ",src_dir)
  print("Aborting ...")
  



