import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
#plt.style.use('./MNRAS_Style.mplstyle')

matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)

mynames = [r"$\Omega_{\rm b}$", r"$\Omega_{\rm m}$",
                                        r"$\sum m_\nu$", r"$n_{\rm s}$",
                                        r"$h$", r"$w_0$", r"$w_{\rm a}$", r"$A_{\rm s}$"]

ed = pd.read_csv("EE2ED200.csv", names=mynames)

finished = [1,2,3,4,5,6,7,8,9,
			10,11,12,13,14,15,16,17,18,19,
			20,21,22,23,24,25,26,27,28,29,
			30,31,32,33,34,35,36,37,38,39,
			40,41,42,43,44,45,46,47,48,49,
			50,
			67,68,69,
			70,71,72,73,77,78,79,
			80,81,82,87,88,
			90,91,92,93,
			101,102,103,104,105,106,107,108,109,
			110,111,112]

ed_to_plot = ed.loc[finished]
#Fig, axs = plt.subplots(8,8)
#for idxA, nameA in enumerate(mynames):
#	for idxB, nameB in enumerate(mynames):
#		if nameA==nameB:
#			axs[idxA,idxB] = plt.hist(ed[nameA])
#		else:
#			axs[idxA,idxB] = plt.scatter(ed[nameA],ed[nameB])

#plt.show()
scatter_matrix1 = pd.plotting.scatter_matrix(ed)
scatter_matrix2 = pd.plotting.scatter_matrix(ed_to_plot, marker="x", c="r")

#for ax in scatter_matrix.ravel():
#    ax.set_xlabel(ax.get_xlabel(), fontsize = 16)#, rotation = 90)
#    ax.set_ylabel(ax.get_ylabel(), fontsize = 16)#, rotation = 0)
#    ax.grid(False)
plt.show()
#plt.savefig("EDScatterPlot.pdf")
