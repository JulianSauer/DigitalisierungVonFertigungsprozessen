#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import _labShopLoader
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import scipy.optimize as opt

def to_local():
    ''' change to local workspace for runtime stuff '''
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

# pylint: disable = C0103
if __name__ == '__main__':
    to_local()
    FILE = "Versuchsdaten_Example.txt"
    
    if not os.path.isfile(FILE):
        print("File \"%s\" not found" % FILE)
        quit()
    LSL = _labShopLoader.LabShopLoader()
    partition=LSL.load(FILE)

func = np.load("func.npy")

m = 0.00000001 # per Annahme
c = 0.02 # per Annahme
k = 10 # per Annahme
gamma = 0.0000001 #c/(2*m) # Dämfungskonstante

omega0 = 1000 #np.sqrt(k/m) #Eigenfrequenz
omega = np.sqrt(np.power(omega0,2)-np.power(gamma,2)) #Frequenz (in den Daten)

def hOmega(omega, omega0, gamma, m):
    return 1 / (m * np.sqrt(np.power((np.power(omega0,2) - np.power(omega,2)),2)  + 4*np.power(gamma,2)*np.power(omega,2) ))

def g (x,a,b,c):
    return a * x**2 + b * x + c

#print(BetragHOmega)
popt,_ = opt.curve_fit(g,func[:int(len(func)/2),0],func[:int(len(func)/2),1],method="lm")
popt2,_ = opt.curve_fit(g,func[int(len(func)/2):,0],func[int(len(func)/2):,1],method="lm")
print("popt Werte:",popt)

c=[]
d=[]
b=[0,0]
for entry in partition:
   # print(i,val, (np.imag(1j)*val))
    if entry[0] > 2:
        val=entry[2]+entry[3]*1j
        #print(val)
        x=val/(1j*(entry[1]*2*np.pi))
        b.append(x/(1j*entry[1]*2*np.pi))
b=np.array(b)
f, axarr = plt.subplots(2, sharex=True)
def fParam(args):
    omegaH=[]
    for val in partition[:,1]:
        omegaH.append(hOmega(val,args[0],args[1],args[2])*10**6) 
    
    return np.linalg.norm(omegaH-b*10**6)**2

def frequenzantwort(omega, gamma, m, omega0):
    return np.abs(1 / (m * np.sqrt(np.power((np.power(omega0,2) - np.power(omega,2)),2)  + 4*np.power(gamma,2)*np.power(omega,2) )))

#axarr[0].plot(func[:,0],func[:,1])
##axarr[0].plot(func[:,0],zzz)
#axarr[0].plot(partition[:,1],np.angle(b))
axarr[0].plot(partition[:,1],np.abs(b)*10**6, label = "2x integriertes Zeug")
#axarr[0].plot(partition[:,1],(yyy/35))
#axarr[2].plot(partition[:,1],d, label = "Über Daten iteriert (d)")
#axarr[2].plot(partition[:,1],c, label = "Ausgedachte Daten (c)")

#popt3,_ = opt.curve_fit(frequenzantwort,partition[:,1],abs(partition[:,2]+partition[:,3]*1j),bounds=([-np.inf,-np.inf,900],[np.inf,np.inf,1100]))
omegaH=[]
for val in partition[:,1]:
    omegaH.append(hOmega(val,900,0.1,0.1)*10**6) 
#axarr[1].plot(partition[:,1],omegaH, label = "Oszillator")    
popt3 = opt.minimize(fParam,[900,0.1,0.1],method="L-BFGS-B",bounds=((0.1,np.inf),(0.1,np.inf),(0.1,np.inf)),tol=0.1)
print("popt3 Werte:",popt3)
omegaH=[]
for val in partition[:,1]:
    omegaH.append(hOmega(val,popt3.x[0],popt3.x[1],popt3.x[2])*10**6) 


axarr[0].plot(partition[:,1],omegaH, label = "OmegaH")
plt.legend()
plt.show()


zzz=[]
for (i,val) in enumerate(func):
    if(i<int(len(func)/2)):
        zzz.append(g(val[0],popt[0],popt[1],popt[2]))
    else:    
        zzz.append(g(val[0],popt2[0],popt2[1],popt2[2]))

yyy=[]
for val in partition:
    y = frequenzantwort(val[1], popt3[0],popt3[1],popt3[2])
    yyy.append(y)
yyy=np.array(yyy)



