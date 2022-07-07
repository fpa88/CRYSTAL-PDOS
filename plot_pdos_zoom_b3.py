#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np
import json
import matplotlib.pyplot as plt
import os
import sys
from io import StringIO
import re
import matplotlib.patches as mpatches
import matplotlib as mpt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)

LX=True
#LX=False
HtoeV=27.211396132  # eV both1.f line 1844
nba=4
nbb=2
NBPTS=20000
nbl=NBPTS+2

# system case without extension
SYSTEMCASE=sys.argv[1]

EMIN=-8
EMAX=8

TXTSPG="Pm$\\bar{3}$m (221)"
# FROM OUTPUT of CRYSTAL, replace values on the 2 following lines 
EFERMI=-1.4364177E-01 #  TOP OF VALENCE BANDS - ALPHA      ELECTRONS
GAP=4.5698

xl_G1 = 0
xr_G1 = GAP
y_G1  = 1
XLABEL=True
YLABEL=True

EMIN=EMIN/HtoeV
EMAX=EMAX/HtoeV

EMAX=EMAX+EFERMI
EMIN=EMIN+EFERMI


TXT = """PPAN
NEWK
40 40 
1 1
66 505
DOSS
"""
TXT = TXT +"%d %d %d %d %d %d %d %d\n%10.5f %10.5f\n" % (5 ,NBPTS, -1 ,-71 , 1,  14,  0, 2,EMIN,EMAX)
TXT = TXT + """-2 1 2                    # all Mn atomic orbitals (AO)
-6 3 4 5 6 7 8                           # all O  AO
-2 9 10                                  # all K  AO
 8 18 22 23 27 45 49 50 54               # all Mn  eg AO
 12 19 20 21 24 25 26 46 47 48 51 52 53  # all Mn t2g AO
END
END"""

with open (SYSTEMCASE+".d3","w+") as f:
  f.write(TXT)

# HERE YOU MUST RUN YOUR CRYSTAL CALCULATION properties with the .d3 input written in the previous line

data = np.loadtxt(SYSTEMCASE+".DOSS",skiprows=nba,max_rows=nbl+1,dtype=float)
datb = np.loadtxt(SYSTEMCASE+".DOSS",skiprows=nbl+nba+nbb,max_rows=nbl+1,dtype=float)


# FFFFFFF
# F
# FFF          PLOT GRAPH
# F
# F

fig,(axes1)  = plt.subplots(nrows=1, ncols=1,figsize=[8,8],dpi=100, sharex=True)

def add_arrow(ax,startx=-1,starty=1,endx=-2,arrow_width=1,head_width=40):
  w=arrow_width
  x1=startx
  y1=starty
  x2=endx
  z=head_width
  ax.arrow(x1+w , y1, x2-(x1+w), 0, head_width=z+0.2, head_length=w, linewidth=w+1, color='black', length_includes_head=True)
  ax.arrow(x2-w, y1, x1-x2+w, 0, head_width=z+0.2, head_length=w, linewidth=w+1, color='black', length_includes_head=True)

def add_arrow_zoom(ax,startx=-1,starty=1,endx=-2,arrow_width=1,head_width=40):
  w=arrow_width
  x1=startx
  y1=starty
  x2=endx
  z=head_width
  ax.arrow(x1+w , y1, x2-(x1+w), 0, head_width=z+0.02, head_length=w, linewidth=w+1, color='black', length_includes_head=True)
  ax.arrow(x2-w, y1, x1-x2+w, 0, head_width=z+0.02, head_length=w, linewidth=w+1, color='black', length_includes_head=True)

font = {'family' : 'sans', # cursive', 'fantasy', 'monospace', 'sans', 'sans serif', 'sans-serif', 'serif'
        'weight' : 'normal', # 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight'
        'size'   : 20}

mpt.rc('font', **font)

unit="eV"
if YLABEL :
  axes1.set_ylabel(r'Density of states (states/eV/cell)',fontsize=20)
if XLABEL :
  axes1.set_xlabel(r'Energy (eV)',fontsize=20)
FAC=HtoeV

DATA1 = data[:,2]
DATA2 = DATA1 + data[:,4]
DATA3 = DATA2 + data[:,5]

DATB1 = datb[:,2]
DATB2 = DATB1 + datb[:,4]
DATB3 = DATB2 + datb[:,5]

axes1.fill_between(data[:,0]*FAC,DATA1/FAC,0                  , alpha=0.6 , color='blue',label='F')#,hatch='/')
axes1.fill_between(data[:,0]*FAC,DATA1/FAC,DATA2/FAC, alpha=0.5,color='red',label='Mn $e_g$')#,hatch='x')
axes1.fill_between(data[:,0]*FAC,DATA2/FAC,DATA3/FAC, alpha=0.5,color="green",label="Mn $t_{2g}$")#,hatch='+')

axes1.fill_between(datb[:,0]*FAC,DATB1/FAC,0        ,alpha=0.6,color="blue")#,hatch='/')
axes1.fill_between(datb[:,0]*FAC,DATB1/FAC,DATB2/FAC,alpha=0.5,color="red")#,hatch='x')
axes1.fill_between(datb[:,0]*FAC,DATB2/FAC,DATB3/FAC,alpha=0.5,color="green")#,hatch='+')

axes1.legend(loc='lower left')


axes1.tick_params(which='both',direction='in', length=6, width=0.5, colors='black', grid_color='r', grid_alpha=0.5)

if LX:
  axes1.yaxis.set_ticklabels([])
  axes1.set_yticks([])
  axes1.set_xlim([-3.0,8])
  XRANGE=np.arange(-0,9,4)
  axes1.set_xticks(XRANGE)
  axes1.set_xticklabels(XRANGE, fontsize=20)

axes1.text(0.95*axes1.get_xlim()[0],0.96*axes1.get_ylim()[1],TXTSPG,fontsize=20)

X1=0.85*(axes1.get_xlim()[1]-axes1.get_xlim()[0])+axes1.get_xlim()[0]
axes1.text(X1,0.95*axes1.get_ylim()[1],"Spin $\\alpha$",fontsize=20)
axes1.text(X1,0.95*axes1.get_ylim()[0],"Spin $\\beta$",fontsize=20)

axes1.plot([GAP/2,GAP/2],axes1.get_ylim(),color="red", marker='',fillstyle='none',linestyle='dashed')

##
#   GAP ARROW
##

# first gap 
add_arrow(axes1, startx=xl_G1 , starty= y_G1 , endx=xr_G1  , arrow_width=0.2,head_width=0.02)
axes1.text( xl_G1+(xr_G1-xl_G1)/2 , y_G1+0.5 ,"%.1f eV" % np.round(abs(xl_G1-xr_G1),1),horizontalalignment='center')

plt.savefig(SYSTEMCASE+"_doss.jpg" )
plt.show( )
