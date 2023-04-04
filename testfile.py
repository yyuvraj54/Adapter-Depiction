from datetime import datetime
import time

fileLinks=['Apple','kela','santos','bekar']
couter=0
data = {}
lenght=len(fileLinks)
for i in range(lenght):

    # t = time.time()
    # t_ms = int(t * 1000)
    
    
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M_%S").replace('/','_')
    key=dt_string+str(couter)
    data[key]=fileLinks[i]
    couter+=1
print(data)