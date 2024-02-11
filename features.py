import numpy as np
import matplotlib.pyplot as plt
x1=np.array([ 1.64460754e+00 , 1.36500000e+03 , 4.80112310e+07 , 3.11876256e+11,
  5.96197414e+05 ,-7.18099825e-20 ,-4.35957056e+02]).reshape(1,7)
x2=np.array([ 3.95721436e-01 , 6.02000000e+02 , 2.32698200e+06 , 1.18199592e+10,
  8.98761191e+04 ,-2.10175399e-17 ,-1.65199520e+02]).reshape(1,7)
x3=np.array([ 6.85317993e-01 , 5.03000000e+02 , 6.32819300e+06 , 6.02698378e+10,
  1.88538728e+05 ,-1.79970797e-18 ,-4.14730817e+02]).reshape(1,7)
x4=np.array([ 2.70141602e-01 , 2.27000000e+02 , 4.37096000e+05 , 6.85847031e+08,
  4.04797855e+04 ,-2.44338927e-16 ,-2.00631914e+03]).reshape(1,7)

#print(x1)
y=np.array([0,1,2,2])
#0,verde: Madera
#1,negro: Metal
#2,azul: Plástico

X=np.concatenate((x1,x2,x3,x4),axis=0)

print(X.shape)
#print(y)
plt.plot(x1.T,'g')
plt.plot(x2.T,'--k')
plt.plot(x3.T,'-b')
plt.plot(x4.T,'-b')
plt.show()
