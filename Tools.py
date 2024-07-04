from scipy.signal import argrelextrema
import numpy as np
from stockwell import st


def FeatExtraction(signal):
    signal_2=signal*signal
    maximos = signal[argrelextrema(signal,np.greater)]
    Energy= np.sum(signal_2)
    rms = (1/np.sqrt(2))*np.sqrt(np.sum(signal_2))
    Imax = min(maximos)
    Imin = max(signal[argrelextrema(signal,np.less)])
    Nlm = len(maximos)#sum(maximos)#
    Zc = len(np.where(np.diff(np.sign(signal)))[0])
    Features = np.array([Energy,rms,Imax,Imin,Nlm,Zc])
    return Features

def build_data(data,t,fmin=0,fmax=30):
    Muestras,tSenal,_=data.shape
    db,dbl=[],[]
    df = 1/(t[-1]-t[0]) 
    for j in range(Muestras):
        for k in range (tSenal):
            y=np.zeros(tSenal)
            y[k]=1
            db.append(np.abs(st.st(data[j,k], int(fmin/df), int(fmax/df))))
            dbl.append(y)
    return np.array(db),np.array(dbl)

def build_featdata(data,labels):
    Muestras,tSenal,_=data.shape
    db,dbl=[],[]
    for j in range(Muestras):
        u=0
        for k in range (tSenal):
            db.append(FeatExtraction(data[j,k]))
            dbl.append(labels[u])
            u = u+1
    return np.array(db),np.array(dbl)
