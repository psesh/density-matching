function [Distance, Gradients, mean_value, var_value, skew_value, obj_sparse, bandwidth] = MatrixComputations(mach_sparse, mach_dense, obj_range, gauss_weights, bandwidthparam)


[obj_sparse, grad_sparse] = read_CFD_Adjoint_data; % Get obj_sparse values
obj_dense = least_squares_deg5(mach_sparse, obj_sparse', mach_dense);

mean_value = mean(obj_dense)
var_value = var(obj_dense)
skew_value = skewness(obj_dense)

% Distance formulation
W = getW(gauss_weights); % matrix of quadrature weights
t = getT(obj_range); % Target pdf
[Ks,bandwidth] = getKs(obj_range,  bandwidthparam);
K_prime = getKprime(obj_dense, obj_range,  bandwidthparam);
F_prime = getFprime(mach_sparse, mach_dense, grad_sparse);

xvalues = obj_sparse;
yvalues = zeros(1,21);

% Plot of pdfs
figure1 = figure;
set(gca, 'FontSize', 16, 'LineWidth', 2); hold on; box on;
area(obj_range, t, 'FaceColor', 'r'); hold on;
area(obj_range, Ks,'FaceColor', 'b');
plot(xvalues, yvalues, 'ko', 'MarkerSize', 16, 'Linewidth', 2);
xlabel('f(s,w)', 'Interpreter', 'latex');
ylabel('PDF', 'Interpreter', 'latex');
legend('Target', 'model');
xlim([-100 200]);
print('fig1', '-depsc', '-r300');
close all;

disp('here')
t = t';
Ks = Ks';

Distance = (t - Ks)' * W * (t - Ks); % Same formulation as paper!
Gradients = 2*(t - Ks)' * W * K_prime * F_prime;


clear K_prime F_prime Ks W t 

end



function grad_dense = getFprime(mach_sparse, mach_dense, grad_sparse)
[rows, cols] = size(grad_sparse);
grad_dense = zeros(numel(mach_dense), cols);

for i = 1 : cols
    grad_dense(:,i) = least_squares_deg5(mach_sparse, grad_sparse(:,i)', mach_dense)';
end


end

function K_prime = getKprime(obj_samples, obj_range, bandwidth)
K_prime = zeros(numel(obj_range), numel(obj_samples));
constant_term = (-0.1994711402)/(numel(obj_samples) * bandwidth^2);

parfor i = 1 : numel(obj_range)
    delta_f = obj_range(i) - obj_samples;
    K_prime(i,:) = constant_term * exp(-1 * (delta_f.^2)./(2 * bandwidth^2)) .* (2.*delta_f);
end

clear delta_f 
end

function [ld, grads] = read_CFD_Adjoint_data()
cfd_data = importdata('MATLAB.data');
cl = cfd_data(:,1);
cd = cfd_data(:,2);
ld = cfd_data(:,3);

% gradients:
grad1 = cfd_data(:,4);
grad2 = cfd_data(:,5);
grad3 = cfd_data(:,6);
grad4 = cfd_data(:,7);
grad5 = cfd_data(:,8);
grad6 = cfd_data(:,9);
grad7 = cfd_data(:,10);
grad8 = cfd_data(:,11);
grad9 = cfd_data(:,12);
grad10 = cfd_data(:,13);
grad11 = cfd_data(:,14);
grad12 = cfd_data(:,15);
grad13 = cfd_data(:,16);
grad14 = cfd_data(:,17);
grad15 = cfd_data(:,18);
grad16 = cfd_data(:,19);

grads = [grad1, grad2, grad3, grad4, grad5, grad6, grad7, grad8, ...
    grad9, grad10, grad11, grad12, grad13, grad14, grad15, grad16];

end



function W = getW(gauss_weights)
W = diag(gauss_weights);

end

% Compute the kernel density estimate of the quantity of interest
function [Ks,bandwidth] = getKs(obj_range,  bandwidthparam) % obj samples are dense

[obj_sparse] = read_CFD_Adjoint_data; 
mach_sparse = linspace(0.66, 0.69, 21); % Mach values at which CFD is computed
max_mach = max(mach_sparse); min_mach = min(mach_sparse);


samples = 1e5; 

random_values = betarnd(2,2, [1, samples]); 
mach_dense = random_values.*(max_mach - min_mach) + min_mach;
obj_samples = least_squares_deg5(mach_sparse, obj_sparse', mach_dense);
[Ks,vals,bandwidth] = ksdensity(obj_samples, obj_range, 'bandwidth', bandwidthparam );
Ks = Ks';

clear obj_samples mach_dense random_values 
end


% Set the target pdf here
function t = getT(obj_range) 

uniform_target = @(f) abs(f - 75) <= 5;
t = 1/(80 - 70 ).* uniform_target(obj_range)';


% -----------------------GAUSSIAN PDF--------------------------------------
% variance_val = 10; mean_val = 50;
% gaussian_dist = @(f) 1/(sqrt(2 * pi * variance_val)) .* exp( -(f - mean_val).^2 ./(2*variance_val));
% t = gaussian_dist(obj_range)';

%------------------------BETA PDF------------------------------------------
% beta pdf between [50,80] with positive skew
%a = 1.5; b = 3.5;
%for i = 1 : length(obj_range)
%    if(obj_range(i)>= 50 && obj_range(i)<=80)
%        x(i) = (obj_range(i) - 50)/(80 - 50);
%        t(i) = ( x(i)^(a - 1) * (1 - x(i) )^(b - 1) )/(beta(a,b));
%    else
%        t(i) = 0;
%    end
%end
%
%t = t./(80 - 50);

end
