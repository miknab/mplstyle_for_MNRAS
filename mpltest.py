import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('./MNRAS_Style.mplstyle')

print mpl.get_configdir()

x = np.linspace(0,10)
y = np.sin(x)

plt.plot(x,y)
plt.xlabel(r"$x$")
plt.ylabel(r"$\sin(x)$")
#plt.savefig("/Users/mischaknabenhans/Desktop/Papers/MyPapers/Paper1_CosmicEmulator1/CutReview_03/Test.pdf")
plt.savefig("./MNRAS_Test.pdf")  
