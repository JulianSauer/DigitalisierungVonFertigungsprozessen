import matplotlib.pyplot as plt
import numpy as np
import math
plt.Circle((0,0),8)


nx=[]
ny=[]
circle=[]
quantel=16
for i in range(0,quantel+1):
    circle.append([math.sin((i/quantel)*2*np.pi),math.cos((i/quantel) *2*np.pi)])
    ny.append(math.cos((i/quantel) *2*np.pi))
    nx.append(math.sin((i/quantel) *2*np.pi))


nx=np.array(nx)
ny=np.array(ny)
circle=np.array(circle)*8

plt.quiver(circle[:,0],circle[:,1],nx,ny)
plt.quiver(circle[:,0],circle[:,1],ny,-nx)
plt.plot(circle[:,0],circle[:,1])
plt.axis('scaled')
plt.show()
