import glob, random
from PIL import Image

def make_gif(frame_folder):
    amount=12
    ms=40
    pool=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
    ret=""
    for i in range(0,amount-1):
        ret+=pool[random.randrange(0,len(pool)-1)]

    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frame_one = frames[0]
    frame_one.save("./gifs/"+str(ms)+"ms_"+str(ret)+".gif", format="GIF", append_images=frames, save_all=True, duration=ms, loop=0)


make_gif("./dst_images")
print("GIF created!")