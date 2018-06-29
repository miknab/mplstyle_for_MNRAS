# mplstyle_for_MNRAS
This repository containts a matplotlib (mpl) stylesheet which (when imported) creates plots looking nice in MNRAS papers.

## WHERE TO STORE THE FILE AND HOW TO IMPORT IT
An easy way to use the file is to save it together with the python script producing the plot (in the same directory). Then,
as done in the test script `mpltest.py`, it can be imported using via

import matplotlib.pyplot as plt
plt.style.use('./MNRAS_Style.mplstyle')

Of course, you can also save the file in the default directory for matplotlib stylesheets. If you don't know the path of this
directory, just execute the commands

import matplotlib as mpl
print mpl.get_configdir()

in ipython or a python script.
