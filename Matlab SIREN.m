% clear all

% Before start, create an Excel file with the following characteristics:
% - first column reporting successive time intervals of the radon activity concentration records, e.g., for AlphaGUARD PQ2000pro with 10 minutes time intervals, the column is 10, 20, 30, etc.   
% - third column with radon activity concentration records,
% - fourth column the corresponding error associated with the radon activity concentration record,
nome_file=input('Insert the name of the excel file just described: ','s');
file_excel=[nome_file,'.xlsx'];
data=readtable(file_excel);
hours=input('how many hours does the fit last?: ');
rows=(hours*60/10)+1;

minutes=table2array(data(1:rows, 1));
concentrations=table2array(data(1:rows,4));
C0=concentrations(1);
errors=table2array(data(1:rows,5));
lambda_Rn222=2.09838*(10^(-6)); %[s-1]

%% plot
plot(minutes,concentrations,'.')
hold on
errorbar(minutes, concentrations, errors,'b')
%fit
model = fitlm(minutes, concentrations,'linear');
% The summary of the model is...
disp(model);
% The fit coefficients are...
coefficients = model.Coefficients;
a = coefficients.Estimate(2);  % angular coefficient [Bq/m3*s - dove i m3 sono riferiti a quelli della stanza]
b = coefficients.Estimate(1);  % intercept
c = coefficients.SE(2); % error on intercept

length=36.0; %[cm]
width=26.0; %[cm]
heigth=31.2; %[cm]
V_ch=length*width*heigth*(10^(-6)); %[m^3]
S=length*heigth*(10^(-4));

disp(' ');
disp(' ');
E_free=a*V_ch/60+lambda_Rn222*C0*V_ch; % [Bq/s]
E_free=E_free/S; % [Bq/m^2*s]
E_free=E_free*1000*3600; % [mBq/m^2*h]
fprintf('The surface radon exhalation rate of the building manufact is: %d mBq/m^2*h\n', E_free)
err_Efree=c*V_ch/60+lambda_Rn222*C0*V_ch; % [Bq/s]
err_Efree=err_Efree/S; % [Bq/m^2*s]
err_Efree=err_Efree*1000*3600; % [mBq/m^2*h]
fprintf('The error of the fit is: %d mBq/m^2*h\n', err_Efree)
disp(' ');
disp(' ');
hold on;
plot(minutes, model.Fitted, 'r'); 