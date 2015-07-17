function [points, weights] = trapezoidalrule(N, bounds)

lower_bound = bounds(1);
upper_bound = bounds(2);

points = linspace(lower_bound, upper_bound, N)';
weights = (upper_bound - lower_bound)/N .*ones(1,N);
weights(1) = weights(1)/2 ; weights(end) = weights(end)/2;




end