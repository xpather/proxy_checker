import requests
import time
import threading
import os

def getSession():
    global sessions
    
    for s in sessions:
        index=s[1]
        if index>=0:
            s[1]=-1
            break
    return index
        
def cheker_proxy(proxy,index,max_errors):
    if max_errors>0:
        global proxys_work
        global sessions
        global url
        session=sessions[index][0]
        proxies = {'http': 'http://'+str(proxy),'https': 'http://'+str(proxy)}
        session.proxies.update(proxies)
        try:
            r = session.get(url,timeout=15)
            print(threading.current_thread().name," - ",proxy," - ",r.status_code)
            if str(r.status_code)=="200":
                proxys_work.append(proxy)
        except:
            cheker_proxy(proxy,index,max_errors-1) 
    sessions[index][1]=index
    
if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+"\\proxys.txt","r") as f:
        proxys= list(set(f.read().split("\n")))
    print("PROXYS IMPORT: ",len(proxys))
    
    proxys_work=[]
    max_threads=300
    max_errors=3
    url="https://api.my-ip.io/ip"
    
    sessions=[[requests.Session(),i] for i in range(max_threads)]   
    
    threads=[]
    i=0
    while i<len(proxys):
        if threading.active_count()<=max_threads:
            index=getSession()
            if index>=0:
                t=threading.Thread(target=cheker_proxy, args=(proxys[i],index,max_errors,))
                t.start()
                threads.append(t)
                i=i+1
    
    for thread in threads:
        thread.join()
    
    print("PROXYS WORKS: ",len(proxys_work))
    with open(dir_path+"\\proxys_work.txt","w") as f:
        for p in proxys_work:
            f.write(p+"\n")

    print("DONE")
    input()
