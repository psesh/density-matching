function Y = least_squares_deg5(x,y,X)
% least_squares_deg5
%
% A degree five polynomial fit with least squares.
%
% Inputs:
% x, training points
% y, training values, y(i) = f(x(i))
% X, approximation points
%
% Outputs:
% Y, approximate values Y(i) \approx f(X(i))

x = x(:); y = y(:); X = X(:); % make column vectors

% estimate the least-squares coefficients
n = size(x,1);
B = [ones(n,1) x x.^2 x.^3 x.^4 x.^5];
a = B\y;

% evaluate the polynomials at the approximation points
N = size(X,1);
BB = [ones(N,1) X X.^2 X.^3 X.^4 X.^5];
Y = BB*a;


