import os
from PIL import Image

src_dir="v"
dst_dir=src_dir+"_rescaled"
prefix="rescaled_"

#resizing
rsize=True
rsizeval=512
rsizefac=3


def slicer(imgpath, index):
  src_tag=src_dir+"/"+imgpath
  dst_tag=dst_dir+"/"+prefix+str(index)+".jpg"
  
  img=Image.open(src_tag)
  w=int(img.width/rsizefac)
  h=int(img.height/rsizefac)
  print("[+] {} [{}x{}px to {}x{}px]".format(dst_tag,img.width,img.height,w,h))
  rs=img.resize((w,h))
  rs.save(dst_tag)
  #print("[SAVED] ", dst_tag)

print("\n[ Image Resizer v1.0 ]")
print("-----------------")
print("Resizing images:")
print("")

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