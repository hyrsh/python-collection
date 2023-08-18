import os, requests, time, argparse

m="./metrics.txt"
murl="http://localhost:2112/metrics"

def recalc(s):
  #byte to KB --> 1024 base
  kb=float(s)/1024
  #KB to MB --> 1024 base
  mb=kb/1024
  return round(float(mb),2)

def largenumber(s):
  return round(float(s))

def mapper(k,v):
  tokens=[
  ["go_goroutines",                   "Go routines       ", "normal"],
  ["go_memstats_sys_bytes",           "All memory        ", "exponential"],
  ["go_threads",                      "Threads           ", "normal"],
  ["process_open_fds",                "Open FDs          ", "normal"],
  ["process_max_fds",                 "System FD capacity", "large"],
  ["go_memstats_heap_alloc_bytes",    "Heap allocated    ", "exponential"],
  ["go_memstats_heap_idle_bytes",     "Heap idle         ", "exponential"],
  ["go_memstats_heap_inuse_bytes",    "Heap in use       ", "exponential"],
  ["go_memstats_heap_released_bytes", "Heap released     ", "exponential"],
  ["go_memstats_heap_sys_bytes",      "Heap system       ", "exponential"],
  ["process_virtual_memory_bytes",    "Virtual memory    ", "exponential"],
  ["process_resident_memory_bytes",   "RSS memory        ", "exponential"],
  ]
  for i in tokens:
    if i[0] == k:
      if i[2] == "normal":
        print("{} {}".format(i[1], v))
      elif i[2] == "exponential":
        ret=recalc(v)
        print("{} {}MB".format(i[1], ret))
      elif i[2] == "large":
        ret=largenumber(v)
        print("{} {}".format(i[1], ret))

parser=argparse.ArgumentParser() #init cli args
parser.add_argument('-duration',default=5) #flag -target
args=parser.parse_args() #parse cli flags

rt=int(args.duration)

for i in range(0,rt):
  print("Prometheus GoLang Prettifier v1.0")
  print("---------------------------------")
  print("[+] Running for {} seconds ({}/{})".format(rt,i+1,rt))
  print("---------------------------------")
  rsp=requests.get(murl)
  m2=rsp.text
  
  with open(m, "w") as file:
    file.write(m2)
  
  with open(m) as metrics:
    lines=metrics.readlines()
  
  for k,line in enumerate(lines):
    ct=line.split(" ",1)
    #print(ct[0])
    if ct[0] != "#":
      mapper(ct[0],ct[1])
  time.sleep(1)
  if i < rt-1:
    os.system("clear")