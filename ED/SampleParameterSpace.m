function X_LHS=SampleParameterSpace(number_of_iterations, number_of_samplepts, CosmoSampleFile)
% SAMPLEPARAMETERSPACE takes three arguments (the number of iterations, the
% number of sampling points and a file name) and writes the optimal
% sampling to the requested file.
%
% SYNOPSIS: SampleParameterSpace(number_of_iterations, number_of_samplepts, CosmoSampleFile)
%
% where 
%
% number_of_iterations .... is the number of sample iterations from which 
%                           the best one is finally chosen
% number_of_samplepts  .... the number of sample points in the sample
% CosmoSampleFile      .... file to which the sample is written

%% 1) SET UP PARAMETER SPACE
% Set the parameter space limits
ParMatrix = [ 0.04      0.06;
              0.24      0.40;
              0.0       0.15;
              0.92      1.00;
              0.61      0.73;
             -1.30     -0.70;
             -0.70       0.70;
              1.7e-9    2.5e-9];

% Declare parameter names for parameter space
ParNames = {'Omega_b' 'Omega_m' 'sum_m_nu' 'n_s' 'h' 'w_0' 'w_a' 'A_s'};

%% 2) SET UP UQlab INPUT MODEL
for ii = 1:8
    inputopts.Marginals(ii).Name = ParNames{ii};
    inputopts.Marginals(ii).Type = 'Uniform';
    inputopts.Marginals(ii).Parameters = ParMatrix(ii,:);
end

% Create input model
CosmicInput = uq_createInput(inputopts);

%% 3) PARAMETER SPACE SAMPLING

%number_of_samples = 100;
Samples = cell(1,number_of_iterations);
MinDists = zeros(1,number_of_iterations);

for jj = 1:number_of_iterations
    if mod(jj,1000)==0
        disp(jj)
    end
    %%%%%%%%%%%%% THIS IS THE CORE OF THIS SCRIPT %%%%%%%%%%%%%
    % Sample input parameter space
   
    X_LHS = uq_getSample(CosmicInput,number_of_samplepts,'LHS');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    Samples{jj} = X_LHS;
    
    md = MinDistance(X_LHS);
    MinDists(jj) = md;
end

maxindx = find(MinDists == max(MinDists(:)));

X_LHS = Samples{maxindx};

%% 5) WRITE SAMPLED POINTS TO FILE
dlmwrite(CosmoSampleFile, X_LHS, 'delimiter', ',', 'precision',9)
%fp = fopen(CosmoSampleFile, 'w');
%fprintf(fp,'%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f\n', X_LHS);
%fclose(fp);
end
