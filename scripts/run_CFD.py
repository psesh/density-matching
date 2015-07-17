#!/home/ps583/newss02/ss02/bin/python
import os
import string
import numpy as np
import threading
import time
import sys
import paths
import commands
from scipy import interpolate
#----------------------------------------------------------------------------------------
# Python script for processing 21 different Mach numbers --> np.linspace(0.6, 0.69, 21)
# Motivation is to re-investigate Figure 5 in Aggressive design paper!
# We can run a maximum of 8 SU2 runs in parallel!
#
# Pranay Seshadri
# April 2014
#----------------------------------------------------------------------------------------
def main(): 
    
    DV = get_design_parameters()

    setup_geometry_mesh(DV)

    run_cfds_in_parallel()

    run_adjointlifts_in_parallel()

    run_adjointdrag_in_parallel()

    run_gradient_projection()

    run_post_processing()

    clean_up_nonlinear()

    clean_up_adjoints()


#-------------------------------------------------------------------------------------
# This is run in serial!
def run_gradient_projection():
    
    # In each of the adjoint folders we run the gradient projection code!
    for k in range(0,21):
        adjoint_lift_folder = paths.cases+'/mach%i/adjoint_lift'%(k+1)
        adjoint_drag_folder = paths.cases+'/mach%i/adjoint_drag'%(k+1)
        lift_adjoint_command = 'SU2_GPC adjointlift.cfg'
        drag_adjoint_command = 'SU2_GPC adjointdrag.cfg'

        os.chdir(adjoint_lift_folder)
        os.system(lift_adjoint_command)

        os.chdir(adjoint_drag_folder)
        os.system(drag_adjoint_command)
        
#-------------------------------------------------------------------------------------
def run_post_processing():
    
    os.chdir(paths.code)
    no_of_uq_runs = 21
    CL = np.ones((1,no_of_uq_runs))
    CD = np.ones((1,no_of_uq_runs))
    LD = np.ones((1,no_of_uq_runs))

    # lift gradient
    dlift1 = np.ones((1,no_of_uq_runs))
    dlift2 = np.ones((1,no_of_uq_runs))
    dlift3 = np.ones((1,no_of_uq_runs))
    dlift4 = np.ones((1,no_of_uq_runs))
    dlift5 = np.ones((1,no_of_uq_runs))
    dlift6 = np.ones((1,no_of_uq_runs))
    dlift7 = np.ones((1,no_of_uq_runs))
    dlift8 = np.ones((1,no_of_uq_runs))
    dlift9 = np.ones((1,no_of_uq_runs))
    dlift10 = np.ones((1,no_of_uq_runs))
    dlift11 = np.ones((1,no_of_uq_runs))
    dlift12 = np.ones((1,no_of_uq_runs))
    dlift13 = np.ones((1,no_of_uq_runs))
    dlift14 = np.ones((1,no_of_uq_runs))
    dlift15 = np.ones((1,no_of_uq_runs))
    dlift16 = np.ones((1,no_of_uq_runs))
    
    # drag gradient
    ddrag1 = np.ones((1,no_of_uq_runs))
    ddrag2 = np.ones((1,no_of_uq_runs))
    ddrag3 = np.ones((1,no_of_uq_runs))
    ddrag4 = np.ones((1,no_of_uq_runs))
    ddrag5 = np.ones((1,no_of_uq_runs))
    ddrag6 = np.ones((1,no_of_uq_runs))
    ddrag7 = np.ones((1,no_of_uq_runs))
    ddrag8 = np.ones((1,no_of_uq_runs))
    ddrag9 = np.ones((1,no_of_uq_runs))
    ddrag10 = np.ones((1,no_of_uq_runs))
    ddrag11 = np.ones((1,no_of_uq_runs))
    ddrag12 = np.ones((1,no_of_uq_runs))
    ddrag13 = np.ones((1,no_of_uq_runs))
    ddrag14 = np.ones((1,no_of_uq_runs))
    ddrag15 = np.ones((1,no_of_uq_runs))
    ddrag16 = np.ones((1,no_of_uq_runs))
    
    # lift/drag gradient
    dlifttodrag1 = np.ones((1,no_of_uq_runs))
    dlifttodrag2 = np.ones((1,no_of_uq_runs))
    dlifttodrag3 = np.ones((1,no_of_uq_runs))
    dlifttodrag3 = np.ones((1,no_of_uq_runs))
    dlifttodrag4 = np.ones((1,no_of_uq_runs))
    dlifttodrag5 = np.ones((1,no_of_uq_runs))
    dlifttodrag6 = np.ones((1,no_of_uq_runs))
    dlifttodrag7 = np.ones((1,no_of_uq_runs))
    dlifttodrag8 = np.ones((1,no_of_uq_runs))
    dlifttodrag9 = np.ones((1,no_of_uq_runs))
    dlifttodrag10 = np.ones((1,no_of_uq_runs))
    dlifttodrag11 = np.ones((1,no_of_uq_runs))
    dlifttodrag12 = np.ones((1,no_of_uq_runs))
    dlifttodrag13 = np.ones((1,no_of_uq_runs))
    dlifttodrag14 = np.ones((1,no_of_uq_runs))
    dlifttodrag15 = np.ones((1,no_of_uq_runs))
    dlifttodrag16 = np.ones((1,no_of_uq_runs))
    
    os.system('rm MATLAB.data')
    os.chdir(paths.code)
    fmatlab = open('MATLAB.data', 'a')

    # loop over all the uq folders!
    for k in range(0,21):
    
    	# move into the right directory
    	cmd = paths.cases+'/mach%i/nonlinear'%(k+1)
    	os.chdir(cmd)

    	print cmd
    	
    	# Read objective function data
    	fileID = open("history.plt", "r")
        objective_data = fileID.readlines()
    	fileID.close()
    	lastrow = len(objective_data)-1
   	lastdata = objective_data[lastrow]
   	CL[0,k] = lastdata[13:25]
   	CD[0,k] = lastdata[27:39]
   	LD[0,k] = CL[0,k]/CD[0,k]


        # Read in adjoint-lift info!
   	cmd = paths.cases+'/mach%i/adjoint_lift'%(k+1)
    	os.chdir(cmd)
        fileIDGrad = open("of_grad.dat", "r")
   	gradient_lift = fileIDGrad.readlines()
   	fileIDGrad.close()
   	dlift1[0,k] = gradient_lift[1]
   	dlift2[0,k] = gradient_lift[2]
   	dlift3[0,k] = gradient_lift[3]
   	dlift4[0,k] = gradient_lift[4]
   	dlift5[0,k] = gradient_lift[5]
   	dlift6[0,k] = gradient_lift[6]
   	dlift7[0,k] = gradient_lift[7]
   	dlift8[0,k] = gradient_lift[8]
   	dlift9[0,k] = gradient_lift[9]
   	dlift10[0,k] = gradient_lift[10]
   	dlift11[0,k] = gradient_lift[11]
   	dlift12[0,k] = gradient_lift[12]
   	dlift13[0,k] = gradient_lift[13]
   	dlift14[0,k] = gradient_lift[14]
   	dlift15[0,k] = gradient_lift[15]
   	dlift16[0,k] = gradient_lift[16]

        # Read in adjoint-drag info!
   	cmd = paths.cases+'/mach%i/adjoint_drag'%(k+1)
    	os.chdir(cmd)
    	fileIDGrad2 = open("of_grad.dat", "r")
   	gradient_drag = fileIDGrad2.readlines()
   	fileIDGrad2.close()
   	ddrag1[0,k] = gradient_drag[1]
   	ddrag2[0,k] = gradient_drag[2]
   	ddrag3[0,k] = gradient_drag[3]
   	ddrag4[0,k] = gradient_drag[4]
   	ddrag5[0,k] = gradient_drag[5]
   	ddrag6[0,k] = gradient_drag[6]
   	ddrag7[0,k] = gradient_drag[7]
   	ddrag8[0,k] = gradient_drag[8]
   	ddrag9[0,k] = gradient_drag[9]
   	ddrag10[0,k] = gradient_drag[10]
   	ddrag11[0,k] = gradient_drag[11]
   	ddrag12[0,k] = gradient_drag[12]
   	ddrag13[0,k] = gradient_drag[13]
   	ddrag14[0,k] = gradient_drag[14]
   	ddrag15[0,k] = gradient_drag[15]
   	ddrag16[0,k] = gradient_drag[16]
   	

   	# Lift to drag ratios computed per quotient rule
 	dlifttodrag1[0,k] = ( (dlift1[0,k] * CD[0,k] ) - (CL[0,k] * ddrag1[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag2[0,k] = ( (dlift2[0,k] * CD[0,k] ) - (CL[0,k] * ddrag2[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag3[0,k] = ( (dlift3[0,k] * CD[0,k] ) - (CL[0,k] * ddrag3[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag4[0,k] = ( (dlift4[0,k] * CD[0,k] ) - (CL[0,k] * ddrag4[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag5[0,k] = ( (dlift5[0,k] * CD[0,k] ) - (CL[0,k] * ddrag5[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag6[0,k] = ( (dlift6[0,k] * CD[0,k] ) - (CL[0,k] * ddrag6[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag7[0,k] = ( (dlift7[0,k] * CD[0,k] ) - (CL[0,k] * ddrag7[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag8[0,k] = ( (dlift8[0,k] * CD[0,k] ) - (CL[0,k] * ddrag8[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag9[0,k] = ( (dlift9[0,k] * CD[0,k] ) - (CL[0,k] * ddrag9[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag10[0,k] = ( (dlift10[0,k] * CD[0,k] ) - (CL[0,k] * ddrag10[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag11[0,k] = ( (dlift11[0,k] * CD[0,k] ) - (CL[0,k] * ddrag11[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag12[0,k] = ( (dlift12[0,k] * CD[0,k] ) - (CL[0,k] * ddrag12[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag13[0,k] = ( (dlift13[0,k] * CD[0,k] ) - (CL[0,k] * ddrag13[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag14[0,k] = ( (dlift14[0,k] * CD[0,k] ) - (CL[0,k] * ddrag14[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag15[0,k] = ( (dlift15[0,k] * CD[0,k] ) - (CL[0,k] * ddrag15[0,k] ) )/(CD[0,k]**2 )
 	dlifttodrag16[0,k] = ( (dlift16[0,k] * CD[0,k] ) - (CL[0,k] * ddrag16[0,k] ) )/(CD[0,k]**2 )
 	
        os.chdir(paths.code)
        matlab_line = str(CL[0,k])+'\t'+str(CD[0,k])+'\t'+str(LD[0,k])+'\t'+str(dlifttodrag1[0,k])+'\t'+str(dlifttodrag2[0,k])+'\t'+str(dlifttodrag3[0,k])+'\t'+str(dlifttodrag4[0,k])+'\t'+str(dlifttodrag5[0,k])+'\t'+str(dlifttodrag6[0,k])+'\t'+str(dlifttodrag7[0,k])+'\t'+str(dlifttodrag8[0,k])+'\t'+str(dlifttodrag9[0,k])+'\t'+str(dlifttodrag10[0,k])+'\t'+str(dlifttodrag11[0,k])+'\t'+str(dlifttodrag12[0,k])+'\t'+str(dlifttodrag13[0,k])+'\t'+str(dlifttodrag14[0,k])+'\t'+str(dlifttodrag15[0,k])+'\t'+str(dlifttodrag16[0,k])+'\n'
        fmatlab.writelines(matlab_line)
    
    fmatlab.close()    
    

#----------------------------------------------------------------------------------------
def setup_geometry_mesh(DESIGN_VECTOR):

    # Store the design vector as variable x
    x = DESIGN_VECTOR
    
    # Open this new file and read all the data
    location = paths.geometry+'/datum_NACA0012.cfg'
    fin = open(location, "r")
    data = fin.readlines()
    fin.close()
    
    
    # Set the values for thdef e HH bump function parameters
    Hicks_data = ('DV_VALUE='+ str(x[0]) +','+ str(x[1]) +','+ str(x[2]) +','+ str(x[3]) +','+ str(x[4]) +','+ str(x[5]) +','+ str(x[6]) +','+ str(x[7])+','+ str(x[8]) +','+ str(x[9]) +','+ str(x[10]) +','+ str(x[11]) +','+ str(x[12]) +','+ str(x[13]) +','+ str(x[14]) +','+ str(x[15])+'\n')
    
    # Change output file name
    Mesh_info = 'MESH_OUT_FILENAME= perturbed_mesh.su2 \n'
    
    # Re-write the file and run the mesh deformation code on new configuration file
    os.chdir(paths.geometry)
    fout = open("input_file.cfg", "w")
    data[217] = Hicks_data
    data[257] = Mesh_info
    fout.writelines(data)
    fout.close()
   
    # Now run mesh deformation code on
    os.system('SU2_MDC input_file.cfg')

    print '******************************************************\n'
    print '****       COMPLETED MESH DEFORMATION             ****\n'
    print '******************************************************\n'

    # Now we incorporate this into the other routines!
    # So in each of the non-linear files we simply add the design parameter correction!
    for k in range(0,21):
        nonlinear_file = paths.cases+'/mach%i/nonlinear/uq.cfg'%(k+1)
        adjoint_lift_file = paths.cases+'/mach%i/adjoint_lift/adjointlift.cfg'%(k+1)
        adjoint_drag_file = paths.cases+'/mach%i/adjoint_drag/adjointdrag.cfg'%(k+1)
        write_to_file(nonlinear_file, 217, Hicks_data)
        write_to_file(adjoint_lift_file, 217, Hicks_data)
        write_to_file(adjoint_drag_file, 217, Hicks_data)
        
    
def write_to_file(filename, line_number, entry):

    filein = open(filename, 'r')
    data_all = filein.readlines()
    filein.close()
    data_all[line_number] = entry
    fout = open(filename, 'w')
    fout.writelines(data_all)
    fout.close()
    
#----------------------------------------------------------------------------------------    
def get_design_parameters():
    input_filename = 'DESIGN_PARAMETERS.txt'
    
    # Check if there is a design parameters file
    os.chdir(paths.code)
    if os.path.isfile(input_filename) == False:
        print 'Cannot find D_P_S file'
    
    fin = open(input_filename, "r")
    data = fin.readlines()
    fin.close()
    value1 = data[0][0:16]
    value2 = data[1][0:16]
    value3 = data[2][0:16]
    value4 = data[3][0:16]
    value5 = data[4][0:16]
    value6 = data[5][0:16]
    value7 = data[6][0:16]
    value8 = data[7][0:16]
    value9 = data[8][0:16]
    value10 = data[9][0:16]
    value11 = data[10][0:16]
    value12 = data[11][0:16]
    value13 = data[12][0:16]
    value14 = data[13][0:16]
    value15 = data[14][0:16]
    value16 = data[15][0:16]
    DESIGN_VECTOR = [ float(value1), float(value2),float(value3),float(value4),float(value5), float(value6), float(value7), float(value8),float(value9), float(value10),float(value11),float(value12),float(value13), float(value14), float(value15), float(value16)]
    
    return DESIGN_VECTOR


#----------------------------------------------------------------------------------------
def clean_up_adjoints():

    # lift adjoints
    clean_up_adjoints_individual(paths.UQ1_adjointlift)
    clean_up_adjoints_individual(paths.UQ2_adjointlift)
    clean_up_adjoints_individual(paths.UQ3_adjointlift)
    clean_up_adjoints_individual(paths.UQ4_adjointlift)
    clean_up_adjoints_individual(paths.UQ5_adjointlift)
    clean_up_adjoints_individual(paths.UQ6_adjointlift)
    clean_up_adjoints_individual(paths.UQ7_adjointlift)
    clean_up_adjoints_individual(paths.UQ8_adjointlift)
    clean_up_adjoints_individual(paths.UQ9_adjointlift)
    clean_up_adjoints_individual(paths.UQ10_adjointlift)
    clean_up_adjoints_individual(paths.UQ11_adjointlift)
    clean_up_adjoints_individual(paths.UQ12_adjointlift)
    clean_up_adjoints_individual(paths.UQ13_adjointlift)
    clean_up_adjoints_individual(paths.UQ14_adjointlift)
    clean_up_adjoints_individual(paths.UQ15_adjointlift)
    clean_up_adjoints_individual(paths.UQ16_adjointlift)
    clean_up_adjoints_individual(paths.UQ17_adjointlift)
    clean_up_adjoints_individual(paths.UQ18_adjointlift)
    clean_up_adjoints_individual(paths.UQ19_adjointlift)
    clean_up_adjoints_individual(paths.UQ20_adjointlift)
    clean_up_adjoints_individual(paths.UQ21_adjointlift)

    
    # drag adjoints
    clean_up_adjoints_individual(paths.UQ1_adjointdrag)
    clean_up_adjoints_individual(paths.UQ2_adjointdrag)
    clean_up_adjoints_individual(paths.UQ3_adjointdrag)
    clean_up_adjoints_individual(paths.UQ4_adjointdrag)
    clean_up_adjoints_individual(paths.UQ5_adjointdrag)
    clean_up_adjoints_individual(paths.UQ6_adjointdrag)
    clean_up_adjoints_individual(paths.UQ7_adjointdrag)
    clean_up_adjoints_individual(paths.UQ8_adjointdrag)
    clean_up_adjoints_individual(paths.UQ9_adjointdrag)
    clean_up_adjoints_individual(paths.UQ10_adjointdrag)
    clean_up_adjoints_individual(paths.UQ11_adjointdrag)
    clean_up_adjoints_individual(paths.UQ12_adjointdrag)
    clean_up_adjoints_individual(paths.UQ13_adjointdrag)
    clean_up_adjoints_individual(paths.UQ14_adjointdrag)
    clean_up_adjoints_individual(paths.UQ15_adjointdrag)
    clean_up_adjoints_individual(paths.UQ16_adjointdrag)
    clean_up_adjoints_individual(paths.UQ17_adjointdrag)
    clean_up_adjoints_individual(paths.UQ18_adjointdrag)
    clean_up_adjoints_individual(paths.UQ19_adjointdrag)
    clean_up_adjoints_individual(paths.UQ20_adjointdrag)
    clean_up_adjoints_individual(paths.UQ21_adjointdrag)
    
#----------------------------------------------------------------------------------------
def clean_up_adjoints_individual(folder_name):    
    os.chdir(folder_name)
    cmd = 'rm history.csv surface_adjoint.csv restart_adj_cd.dat adjoint.vtk surface_adjoint.vtk'
    os.chdir(paths.code)
    
#----------------------------------------------------------------------------------------
def clean_up_nonlinear():
    clean_up_nonlinear_individual(paths.UQ1_nonlinear)
    clean_up_nonlinear_individual(paths.UQ2_nonlinear)
    clean_up_nonlinear_individual(paths.UQ3_nonlinear)
    clean_up_nonlinear_individual(paths.UQ4_nonlinear)
    clean_up_nonlinear_individual(paths.UQ5_nonlinear)
    clean_up_nonlinear_individual(paths.UQ6_nonlinear)
    clean_up_nonlinear_individual(paths.UQ7_nonlinear)
    clean_up_nonlinear_individual(paths.UQ8_nonlinear)
    clean_up_nonlinear_individual(paths.UQ9_nonlinear)
    clean_up_nonlinear_individual(paths.UQ10_nonlinear)
    clean_up_nonlinear_individual(paths.UQ11_nonlinear)
    clean_up_nonlinear_individual(paths.UQ12_nonlinear)
    clean_up_nonlinear_individual(paths.UQ13_nonlinear)
    clean_up_nonlinear_individual(paths.UQ14_nonlinear)
    clean_up_nonlinear_individual(paths.UQ15_nonlinear)
    clean_up_nonlinear_individual(paths.UQ16_nonlinear)
    clean_up_nonlinear_individual(paths.UQ17_nonlinear)
    clean_up_nonlinear_individual(paths.UQ18_nonlinear)
    clean_up_nonlinear_individual(paths.UQ19_nonlinear)
    clean_up_nonlinear_individual(paths.UQ20_nonlinear)
    clean_up_nonlinear_individual(paths.UQ21_nonlinear)
    
#----------------------------------------------------------------------------------------
def clean_up_nonlinear_individual(folder_name):
    os.chdir(folder_name)
    cmd = 'rm history.plt surface_flow.csv restart_flow.dat flow.dat surface_flow.dat'
    os.chdir(paths.code)


#------------------------------------------------------------------------------------------
# CFD Threading Class
class myThreadCFD (threading.Thread):
    def __init__(self, threadID, path, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.path = path
        self.filename = filename
    
    def run(self):
	cmd = 'cd '+str(self.path)+' ; SU2_CFD '+str(self.filename)
	os.system(cmd)
        wait_to_finish_CFD(self.threadID)
           
def wait_to_finish_CFD(number):
    still_running = True
    while (still_running):
        
        output = commands.getoutput('ps -A')
        if 'SU2_CFD' in output :
        	still_running = True
        	
        else:
        	still_running = False


    time.sleep(5)



#-------------------------------------------------------------------------------------        
def run_adjointlifts_in_parallel():

    threads = []
    
    # declare the threads
    for k in range(0,7):
        path_id = paths.cases+'/mach%i/adjoint_lift'%(k+1)
        filename = 'adjointlift.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED ADJOINT-LIFT               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    #------------------------------------------------------------------
    # ADJOINT-LIFT THREAD #2
    threads = []
    
    # declare the threads
    for k in range(7,15):
        path_id = paths.cases+'/mach%i/adjoint_lift'%(k+1)
        filename = 'adjointlift.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED ADJOINT-LIFT               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    #------------------------------------------------------------------
    # ADJOINT-LIFT THREAD #3
    threads = []
    
    # declare the threads
    for k in range(15,21):
        path_id = paths.cases+'/mach%i/adjoint_lift'%(k+1)
        filename = 'adjointlift.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED ADJOINT-LIFT               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

#-------------------------------------------------------------------------------------        
def run_adjointdrag_in_parallel():

    #------------------------------------------------------------------------------
    # ADJOINT-DRAG THREAD 1
    #-------------------------------------------------------------------------------
    threads = []
    
    # declare the threads
    for k in range(0,7):
        path_id = paths.cases+'/mach%i/adjoint_drag'%(k+1)
        filename = 'adjointdrag.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED ADJOINT-DRAG               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    #------------------------------------------------------------------------------
    # ADJOINT-DRAG THREAD 2
    #-------------------------------------------------------------------------------
    threads = []
    
    # declare the threads
    for k in range(7,15):
        path_id = paths.cases+'/mach%i/adjoint_drag'%(k+1)
        filename = 'adjointdrag.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED ADJOINT-DRAG               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    #------------------------------------------------------------------------------
    # ADJOINT-DRAG THREAD 3
    #-------------------------------------------------------------------------------
    threads = []
    
    # declare the threads
    for k in range(15,21):
        path_id = paths.cases+'/mach%i/adjoint_drag'%(k+1)
        filename = 'adjointdrag.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED ADJOINT-DRAG               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t
#-------------------------------------------------------------------------------------        
def run_cfds_in_parallel():

    threads = []

    #-----------------------------------------------------------------
    # Run threads in batches of 7
    # thread 1 - [1,2,3,4,5,6,7]
    # thread 2 - [8,9,10,11,12,13,14]
    # thread 3 - [15,16,17,18,19,20,21]
    #-----------------------------------------------------------------

    # Thread part 1!
    for k in range(0,7):
        path_id = paths.cases+'/mach%i/nonlinear'%(k+1)
        filename = 'uq.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED CFD THREAD 1                ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    # Thread part 2!
    threads = []
    for k in range(7,15):
        path_id = paths.cases+'/mach%i/nonlinear'%(k+1)
        filename = 'uq.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED CFD THREAD 2               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    # Thread part 3!
    threads = []
    for k in range(15,21):
        path_id = paths.cases+'/mach%i/nonlinear'%(k+1)
        filename = 'uq.cfg'
     	thread_value = myThreadCFD(k+1, path_id, filename)
     	thread_value.start()
     	time.sleep(2)
     	threads.append(thread_value)
    
    # Wait for all threads to complete
    for t in threads:
    	t.join()
    	
    print "    \n"
    print '******************************************************\n'
    print '****		COMPLETED CFD THREAD 3               ****\n'
    print '******************************************************\n'
    
    # Get rid of some variable names
    del threads 
    del thread_value 
    del path_id
    del t

    
main()
