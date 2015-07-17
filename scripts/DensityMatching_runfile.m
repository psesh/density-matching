function DensityMatching_runfile()

clear; close all; clc;
%xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
%
% NACA0012 Density-Matching Case Study
% 
% Seshadri et al. (2015)
%
% MATLAB scripts for carrying out NACA0012 optimization under uncertainty
% using a new density-matching technique. This is the main file to be executed.
% This code calls a python script file that runs (in parallel) 21 CFD 2-D
% Euler solves of an airfoil using Stanford University's SU2 suite of tools.
% 
% Optimization problem:
% a) 16 design variables (Hicks-Henne bump function amplitudes on airfoil)
% b) 1 uncertainty - inlet Mach number with a beta(2,2) on [0.66,0.69]
% c) objective is the L/D ratio.
% d) adjoints for L/D computed using quotient rule

%xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
% History files
delete 'SQP_HISTORY.txt'
delete 'nohup.out'
delete 'MATLABHIST.dat'
diary('MATLABHIST.dat');
diary on;

% Optimizer setup
Aeq = [];
beq = [];
Aoo = [];
boo = [];
mycon = [];

% New testing!
initial_solution = 0.0001.*ones(1,16);

% INITIAL DESIGNS FOR STAGE 2 FOR PAPER RESULTS ---------------------------
% 
% ---- initial design for Target U[70,80] aggressive design stage 2.
%initial_solution = [ -0.0007000 	  -0.0030000 	  -0.0029485 	  0.0090000 	 0.0090000 	  0.0060000 	  -0.0030000 	  -0.0007000 	 -0.0007000 	  -0.0030000 	  -0.0070000 	  -0.0048789 	  0.0090000 	  0.0060000 	  0.0030000 	  0.0007000];

% ---- initial design for Gauss[50,10] aggressive design stage 2.
%initial_solution = [ -0.0007000 	  -0.0030000 	  0.0090000 	  0.0090000 	 0.0090000 	  -0.0004185 	  -0.0030000 	  -0.0007000 	 -0.0007000 	  -0.0030000 	  -0.0070000 	  -0.0070000 	  -0.0070000 	  0.0060000 	  0.0030000 	  0.0007000];

% ---- initial design for Beta(1.5,3.5) aggressive design stage 2.
%initial_solution = [	 -0.0007000 	  -0.0029362 	  0.0090000 	  0.0090000 	 0.0090000 	  0.0031188 	  -0.0030000 	  -0.0003639 	 -0.0007000 	  -0.0030000 	  -0.0070000 	  -0.0070000 	  0.0051584 	  0.0031188 	  0.0015594 	  0.0007000];
%
%--------------------------------------------------------------------------

% Design range for 16 parameters
design_bounds = [
-0.0007 0.0007 
-0.003 0.003 
-0.007 0.009 
-0.007 0.009 
-0.007 0.009 
-0.006 0.006 
-0.003 0.003 
-0.0007 0.0007 
-0.0007 0.0007 
-0.003 0.003 
-0.007 0.009 
-0.007 0.009 
-0.007 0.009 
-0.006 0.006 
-0.003 0.003 
-0.0007 0.0007];

% upper and lower design bounds
lower_bound = design_bounds(:,1)';
upper_bound = design_bounds(:,2)';


%----------------------- BANDWIDTH PARAMETER ------------------------------
chosen_BW = 50; % Note change to 1 for stage 2 optimization
%--------------------------------------------------------------------------

% Main function call
myfun = @(S) computeNACA(S, chosen_BW);

tic % initiate start time

% Optimization options
options = optimset('Algorithm','sqp', 'TolX', 1e-6, ...
    'Display', 'iter-detailed', ...
    'GradObj', 'on', 'MaxFunEvals', 100, 'MaxIter', 3);

[x_optimum,fval,exitflag, output] = fmincon(myfun, ...
    initial_solution, Aoo , boo,  Aeq, beq, lower_bound, upper_bound, mycon, ...
    options)

toc % end time

diary off;

end

function [Distance, Gradients, mean_value] = computeNACA(design_vector, chosen_BW)

    % Write out the file with the design_vector
    delete 'DESIGN_PARAMETERS.txt'
    delete 'nohup.out'
    fileID = fopen('DESIGN_PARAMETERS.txt', 'w');
    fprintf(fileID, '%4.7f\n', design_vector);
    fclose(fileID);
    
    % Call the python code!
    ! nohup run_CFD.py
    
    % To propgate uncertainty in Mach number
    mach_sparse = linspace(0.66, 0.69, 21); % Mach values at which CFD is computed for surrogate
    max_mach = max(mach_sparse); min_mach = min(mach_sparse);
    samples = 1e5; random_values = betarnd(2,2, [1, samples]); % dense sampling of surrogate
    mach_dense = random_values.*(max_mach - min_mach) + min_mach;

    % Quadrature rule with lower bound, upper bound and number of points
    lower_bound = -100;
    upper_bound = 200;
    N = 2500;
    [integration_points, integration_weights] =  trapezoidalrule(N, [lower_bound, upper_bound]);

    
    % Get distance and its gradient from a function that does all the
    % matrix computations
    [Distance, Gradients, mean_value, var_value, skew_value, obj_sparse, bandwidth_parameter] = MatrixComputations(mach_sparse, mach_dense, integration_points, integration_weights, chosen_BW);
    Distance = Distance * 1.0 % replace 1.0 with appropriate scalar for normalization of 1st function call during optimization
    Gradients = Gradients
    toc
    
    % save output to a file~
    fileID3 = fopen('SQP_HISTORY.txt', 'a');
    fprintf(fileID3, '%4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t  %4.7f \t %4.7f \t %4.7f \t %4.7f  \t  %4.7f \t %4.7f \t %4.7f \t %4.7f \n ', design_vector', Distance, mean_value, var_value, skew_value, obj_sparse, bandwidth_parameter);   
    fclose(fileID3);


end
