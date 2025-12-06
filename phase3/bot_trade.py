import numpy as np

history=[]
def make_decision(epoch,priceA,priceB):
    history.append((priceA,priceB))
    window=27
    if len(history)<window: return {"Asset A":1/3,"Asset B":1/3,"Cash":1/3}
    A,B=np.array(history).T
    ra,rb=A[-1]/A[-(window//2)]-1,B[-1]/B[-(window//2)]-1
    ra,rb=max(0,ra),max(0,rb)
    s=ra+rb
    if s==0: return {"Asset A":0,"Asset B":0,"Cash":1}
    wA,wB=ra/s*.85,rb/s*.85
    return {"Asset A":wA,"Asset B":wB,"Cash":1-wA-wB}
