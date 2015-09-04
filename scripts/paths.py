#!/usr/bin/python
import os

#-----------------------------------------
# Folder locations
#-----------------------------------------
base = '/home/ps583/Dropbox/01_Aggressive/derived_distributions'

# Geometry folder
geometry = base+'/data/geometry'
cases = base+'/data/cases'

# UQ1 folders
UQ1 = base+'/data/cases/mach1'
UQ1_adjointlift = UQ1+'/adjoint_lift'
UQ1_adjointdrag = UQ1+'/adjoint_drag'
UQ1_nonlinear = UQ1+'/nonlinear'

# UQ2 folders
UQ2 = base+'/data/cases/mach2'
UQ2_adjointlift = UQ2+'/adjoint_lift'
UQ2_adjointdrag = UQ2+'/adjoint_drag'
UQ2_nonlinear = UQ2+'/nonlinear'

# UQ3 folders
UQ3 = base+'/data/cases/mach3'
UQ3_adjointlift = UQ3+'/adjoint_lift'
UQ3_adjointdrag = UQ3+'/adjoint_drag'
UQ3_nonlinear = UQ3+'/nonlinear'

# UQ4 folders
UQ4 = base+'/data/cases/mach4'
UQ4_adjointlift = UQ4+'/adjoint_lift'
UQ4_adjointdrag = UQ4+'/adjoint_drag'
UQ4_nonlinear = UQ4+'/nonlinear'

# UQ5 folders
UQ5 = base+'/data/cases/mach5'
UQ5_adjointlift = UQ5+'/adjoint_lift'
UQ5_adjointdrag = UQ5+'/adjoint_drag'
UQ5_nonlinear = UQ5+'/nonlinear'

# UQ6 folders
UQ6 = base+'/data/cases/mach6'
UQ6_adjointlift = UQ6+'/adjoint_lift'
UQ6_adjointdrag = UQ6+'/adjoint_drag'
UQ6_nonlinear = UQ6+'/nonlinear'

# UQ7 folders
UQ7 = base+'/data/cases/mach7'
UQ7_adjointlift = UQ7+'/adjoint_lift'
UQ7_adjointdrag = UQ7+'/adjoint_drag'
UQ7_nonlinear = UQ7+'/nonlinear'

# UQ8 folders
UQ8 = base+'/data/cases/mach8'
UQ8_adjointlift = UQ8+'/adjoint_lift'
UQ8_adjointdrag = UQ8+'/adjoint_drag'
UQ8_nonlinear = UQ8+'/nonlinear'

# UQ9 folders
UQ9 = base+'/data/cases/mach9'
UQ9_adjointlift = UQ9+'/adjoint_lift'
UQ9_adjointdrag = UQ9+'/adjoint_drag'
UQ9_nonlinear = UQ9+'/nonlinear'

# UQ10 folders
UQ10 = base+'/data/cases/mach10'
UQ10_adjointlift = UQ10+'/adjoint_lift'
UQ10_adjointdrag = UQ10+'/adjoint_drag'
UQ10_nonlinear = UQ10+'/nonlinear'

# UQ11 folders
UQ11 = base+'/data/cases/mach11'
UQ11_adjointlift = UQ11+'/adjoint_lift'
UQ11_adjointdrag = UQ11+'/adjoint_drag'
UQ11_nonlinear = UQ11+'/nonlinear'

# UQ12 folders
UQ12 = base+'/data/cases/mach12'
UQ12_adjointlift = UQ12+'/adjoint_lift'
UQ12_adjointdrag = UQ12+'/adjoint_drag'
UQ12_nonlinear = UQ12+'/nonlinear'

# UQ13 folders
UQ13 = base+'/data/cases/mach13'
UQ13_adjointlift = UQ13+'/adjoint_lift'
UQ13_adjointdrag = UQ13+'/adjoint_drag'
UQ13_nonlinear = UQ13+'/nonlinear'

# UQ14 folders
UQ14 = base+'/data/cases/mach14'
UQ14_adjointlift = UQ14+'/adjoint_lift'
UQ14_adjointdrag = UQ14+'/adjoint_drag'
UQ14_nonlinear = UQ14+'/nonlinear'

# UQ15 folders
UQ15 = base+'/data/cases/mach15'
UQ15_adjointlift = UQ15+'/adjoint_lift'
UQ15_adjointdrag = UQ15+'/adjoint_drag'
UQ15_nonlinear = UQ15+'/nonlinear'

# UQ16 folders
UQ16 = base+'/data/cases/mach16'
UQ16_adjointlift = UQ16+'/adjoint_lift'
UQ16_adjointdrag = UQ1+'/adjoint_drag'
UQ16_nonlinear = UQ16+'/nonlinear'

# UQ17 folders
UQ17 = base+'/data/cases/mach17'
UQ17_adjointlift = UQ17+'/adjoint_lift'
UQ17_adjointdrag = UQ17+'/adjoint_drag'
UQ17_nonlinear = UQ17+'/nonlinear'

# UQ18 folders
UQ18 = base+'/data/cases/mach18'
UQ18_adjointlift = UQ18+'/adjoint_lift'
UQ18_adjointdrag = UQ18+'/adjoint_drag'
UQ18_nonlinear = UQ18+'/nonlinear'

# UQ19 folders
UQ19 = base+'/data/cases/mach19'
UQ19_adjointlift = UQ19+'/adjoint_lift'
UQ19_adjointdrag = UQ19+'/adjoint_drag'
UQ19_nonlinear = UQ19+'/nonlinear'

# UQ20 folders
UQ20 = base+'/data/cases/mach20'
UQ20_adjointlift = UQ20+'/adjoint_lift'
UQ20_adjointdrag = UQ20+'/adjoint_drag'
UQ20_nonlinear = UQ20+'/nonlinear'

# UQ21 folders
UQ21 = base+'/data/cases/mach21'
UQ21_adjointlift = UQ21+'/adjoint_lift'
UQ21_adjointdrag = UQ21+'/adjoint_drag'
UQ21_nonlinear = UQ21+'/nonlinear'


# Where do i drop all the files!?
code = base+'/codes'
