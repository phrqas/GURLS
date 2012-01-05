function [p] = perf_macroavg(X, y, opt)

%	perf_macroavg(X,y,opt)
% 	Computes the average classification accuracy per class.
%
%	NEEDS:
%		- opt.pred

if isfield (opt,'perf')
	p = opt.perf; % lets not overwrite existing performance measures.
		      % unless they have the same name
end

T = size(y,2);
y_true = y;
y_pred = opt.pred;

if size(y,2) == 1
	predlab = sign(y_pred);

	p.acc = mean(predlab == y);
	p.forho = mean(predlab == y);
	p.forplot = mean(predlab == y);
else
	%% Assumes single label prediction.
	[dummy, predlab] = max(y_pred,[],2);
	[dummy, truelab] = max(y_true,[],2);
	[MacroAvg, PerClass] = macroavg(truelab, predlab);
	
	for t = 1:T,
		p.acc(t) = PerClass(t);
		p.forho(t) = p.acc(t);
		p.forplot(t) = p.acc(t);
	end
end


function [MacroAverage, PerClass] = macroavg(TrueY, PredY)
% Computes average of performance for each class.

% Micro
% micro = mean(Classes == YTest);
% fprintf('Micro Avg: %2.4f\n',micro);

% Macro
nClasses = max(TrueY);
for i = 1:nClasses,
    acc(i) = sum((TrueY == i) & (PredY == i))/(sum(TrueY == i) + eps);
end
PerClass = acc;
MacroAverage = mean(acc);

%fprintf('Macro Avg: %2.4f\n',macro);
