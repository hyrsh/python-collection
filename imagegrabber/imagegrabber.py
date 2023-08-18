from PIL import Image, ImageGrab
from win32gui import FindWindow, GetWindowRect, GetDC, SetPixel
from multiprocessing import Process
import win32api
import os
import time

#PowerShell command to get all processes
#Get-Process

#PowerShell command to get all main window title
#Get-Process | ? {$_.MainWindowHandle} | Select ProcessName, @{Name="AppTitle";Expression= {($_.MainWindowTitle)}}

#PowerShell command to manually get window handle
#(Get-Process <NAME>).mainWindowHandle


wndName=None
wndClass=None
mHandle=3146974

target1 = (255,255,255) #white default
target2 = (0,255,0)

#pr0
plus=178
minus=152

if wndName == None and wndClass == None and mHandle != None:
    wndHandle = mHandle
else:
    wndHandle = FindWindow(wndClass, wndName)
wndRect = GetWindowRect(wndHandle)

x_top=wndRect[0]
y_top=wndRect[1]
x_bottom=wndRect[2]
y_bottom=wndRect[3]

width = x_bottom - x_top
height = y_bottom - y_top

dim = width*height

offset = 50

x1=(x_top+int(width/2))-offset
x2=(x_top+int(width/2))+offset
y1=(y_top+int(height/2))-offset
y2=(y_top+int(height/2))+offset

dc = GetDC(0)

def rct(dc,x1,x2,y1,y2):
    print("Drawing scope.")
    clr=win32api.RGB(0,255,0)
    while True:
        xr=x1
        yr=y1
        for w in range(0,offset):
            SetPixel(dc,xr,y1,clr)
            SetPixel(dc,xr,y2,clr)
            SetPixel(dc,x1,yr,clr)
            SetPixel(dc,x2,yr,clr)
            xr+=2
            yr+=2
        time.sleep(0.001)
        
def pixCount():
    print("Analyzing scope.")
    for j in range(0,5000):
        x=0
        y=0
        
        counter=0
        t1c=0
        
        im = ImageGrab.grab(bbox=(x1,y1,x2,y2))
        
        #st = time.time()
        for i in range(0,(offset*2)*(offset*2)):
            #print(x,y,i)
            r,g,b = im.getpixel((x,y))
            if r<20 and g<20 and b<20:
                counter+=1
            elif r==target1[0] and g==target1[1] and b==target1[2]:
                t1c+=1
    
            if x == (offset*2)-1:
                y+=1
                x=0
            else:
                x+=1
    
        #et = (time.time() - st)
        #print("Time cycle:",str(et),"seconds")
    
        #os.system("cls")                
        print("<DARK: ", counter)
        print("<WHITE: ", t1c)
        #rct(dc,x1,x2,y1,y2,xr,yr,clr)
        time.sleep(0.1)

if __name__ == '__main__':
    pc = Process(target=pixCount(),)
    box = Process(target=rct(dc,x1,x2,y1,y2),)
    
    
    pc.start()
    box.start()
    
    #pixCount()
    
    
    print("Routine finished")
    #print("Window "+wndName+" rectangle", wndRect)
    #im.show()