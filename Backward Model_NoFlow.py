# -*- coding: cp1252 -*-
import numpy as np
import copy as cp
import winsound as ws
import matplotlib.pyplot as plt

def isReal (s):
    if len(s)==0:
        return False
    return s.isdigit() or (s[0] in "+-" and s[1:].isdigit()) or (s.count(".")==1 and (s.replace(".","1")).isdigit()) or (s.count(".")==1 and (s.replace(".","1"))[0] in "+-" and (s.replace(".","1"))[1:].isdigit())

#------------------------------------------------------------------------------
#Defining nuclear and fluid dynamic data.

lambda_226Ra=13.73*(10**(-12)) #[s^-1]
lambda_222Rn=2.09838*(10**(-6)) #[s^-1]
lambda_218Po=3.762*(10**(-3)) #[s^-1]
lambda_214Pb=429.2*(10**(-6)) #[s^-1]
D_0=1.2*10**(-5) #[m^2 s^-1]

#------------------------------------------------------------------------------
#Defining the dimensions of the accumulation can

length=36.0 #[cm]
width=26.0 #[cm]
height=31.2 #[cm]

V_ch=length*width*height*(10**(-6)) #[m^3]

#---------------------------------------------------------------
#Defining the dimensions of hydraulic connection between
#can and room air.

d_d=0.004 #[m]
S_d=np.pi/4*d_d**2 #[m^2]
l_d=0.1 #[m]

#------------------------------------------------------------------------------
#Definizione del tempo di osservazione e degli intervalli di stampa

print("Measuring Interval Details:")
day=int(input("Days: "))
hour=int(input("Hours: "))
minute=int(input("Minutes: "))
T=day*24*3600+hour*3600+minute*60. #Measurement duration, [s].

#------------------------------------------------------------------------------
#Defining the intervals between records of radon concentration and flow-rate.

t=600. #Interval between two following CRM outputs, [s].
N=T/t #Number of t-lasting interval to cover the measurement period.
p=600 #Number of intervals between two following flow-rate outputs for each 
#t-lasting interval.

#------------------------------------------------------------------------------
#Defining the discretization details.

n=6000. #Number of computation intervals for each t-lasting interval.
deltat=t/n  #Time step used for discretization.

#------------------------------------------------------------------------------
#Reading the radon concentration records, with the corresponding uncertainties, 
#from the optimized output of the inner radon monitor.

file_input="RadonINT_Measurements.txt"
Radonin_in=open(file_input,"r")
Radonin_text=Radonin_in.read()
Radonin_list=Radonin_text.split("\n") #[Bq/m^3]

#Initializing the list of radon concentration and uncertainty values.

cin_222Rn=[]
sigmain_222Rn=[]

for i in range(len(Radonin_list)):
    raw=Radonin_list[i]
    if "\t" in raw:
        cin_222Rn.append(raw.split("\t")[0])
        sigmain_222Rn.append(raw.split("\t")[1])
    else:
        Radonin_list.remove(raw)
                
#Radon concentration and uncertainty values, read as string, are transformed 
#into float number, after a further check through the isReal function.

for i in range(len(cin_222Rn)):
    if isReal(cin_222Rn[i])==True:
        cin_222Rn[i]=float(cin_222Rn[i])
    else:
        cin_222Rn.remove(cin_222Rn[i])

for i in range(len(sigmain_222Rn)):
    if isReal(sigmain_222Rn[i])==True:
        sigmain_222Rn[i]=float(sigmain_222Rn[i])
    else:
        sigmain_222Rn.remove(sigmain_222Rn[i])

#sigmain_222Rn and cin_222Rn lists are transformed into numpay arrays.

sigmain_222Rn=np.array(sigmain_222Rn) #[Bq/m^3]        
cin_222Rn=np.array(cin_222Rn) #[Bq/m^3]

#From radon concentration the number of radon atoms array is obtained.

Min_222Rn=cin_222Rn*V_ch/lambda_222Rn #[atoms]

#If data have been properly acquired, the number of radon concentration records
#should be equal to N+1.

if len(cin_222Rn)==N+1:
    check_Radonin=True
else:
    check_Radonin=False
	
#------------------------------------------------------------------------------
#Reading the radon concentration records, with the corresponding uncertainties, 
#from the optimized output of the inner radon monitor.
#The same comments seen for the inner radon monitor identically applies to 
#the outer one.

file_input="RadonEXT_Measurements.txt"
Radonout_in=open(file_input,"r")
Radonout_text=Radonout_in.read()
Radonout_list=Radonout_text.split("\n") #[Bq/m^3]
cout_222Rn=[]
sigmaout_222Rn=[]

for i in range(len(Radonout_list)):
    raw=Radonout_list[i]
    if "\t" in raw:
        cout_222Rn.append(raw.split("\t")[0])
        sigmaout_222Rn.append(raw.split("\t")[1])
    else:
        Radonout_list.remove(raw)
                
for i in range(len(cout_222Rn)):
    if isReal(cout_222Rn[i])==True:
        cout_222Rn[i]=float(cout_222Rn[i])
    else:
        cout_222Rn.remove(cout_222Rn[i])
        
sigmaout_222Rn=np.array(sigmaout_222Rn) #[Bq/m^3]  
cout_222Rn=np.array(cout_222Rn) #[Bq/m^3]

#The outer radon concentration is used to obtain the array of
#radon atoms per unit volume.

Mout_222Rn=cout_222Rn/lambda_222Rn #[atoms/m^3]

if len(cout_222Rn)==N+1:
    check_Radonout=True
else:
    check_Radonout=False

#------------------------------------------------------------------------------
#Initializing the list radon atoms vs. time.

N_222Rn=np.ones(int(N)+1) #[atoms]
#The first array value is set equal to the radon concentration 
#measured at the beginning of the measurement by the inner detector.
N_222Rn[0]=Min_222Rn[0] 
n_222Rn=np.ones(int(n)+1)

#------------------------------------------------------------------------------
#Reading the flow rate records from the optimized output of the flow rate sensor.

file_input="Portata_Measurements.txt"
Gamma_in=open(file_input,"r")
Gamma_lista=Gamma_in.read()
Gamma_222Rn=Gamma_lista.split("\n")
for i in range(len(Gamma_222Rn)):
    if len(Gamma_222Rn)>0:
        Gamma_222Rn[i]=float(Gamma_222Rn[i])
    else:
        Gamma_222Rn.remove(Gamma_222Rn[i])
Gamma_222Rn=np.array(Gamma_222Rn) #[m^3/s]

#Being T the measurement duration (in seconds), the number of flow rate records,
#registered once a second, should be equal to T+1.

if len(Gamma_222Rn)==T+1:
	check_Gamma=True
else:
	check_Gamma=False

#------------------------------------------------------------------------------
#Defining the exhalation rate existing interval. The lower and upper boundaries
#are named r_ExInf and r_ExSup respectively. The measuring units are changed
#in agreement with the lists initialized before.

r_ExInf=200000. #[mBq/(m^2*h)]
R_ExInf=r_ExInf/1000*length*height*(10**(-4))/lambda_222Rn/3600 #[atoms_222Rn/s]
r_ExSup=500000. #[mBq/(m^2*h)]
R_ExSup=r_ExSup/1000*length*height*(10**(-4))/lambda_222Rn/3600 #[atoms_222Rn/s]

#------------------------------------------------------------------------------
#Opening the output file after having received as input the file name.

file_output=input("Results File Name: ")
f_out=open(file_output+".txtr","w")

#The exhalation rate value best fitting the radon concentration 
#trend measured is obtained through subsequent iteration. 
#The discretized differential equation governing the accumulation
#should be solved separately for R_ExInf and R_ExSup. For each 
#of the two solutions, the residual is then computed relative to
#the measured trend.

counter=1 #Counter to account for number of iterations done.
ResInf=0 #This variable will contain the "lower residual".
ResSup=0 #This variable will contain the "upper residual".

#The research of the exhalation value best-fitting the radon
#concentration trend measured is designed to end when the 
#residual is lower than a certain value or when a certain
#number of iterations has been performed.
#ResTot is a variable that equals the lowest residual 
#between ResInf and ResSup. Such a variable has to be 
#initialized at a starting value higher than the minimum
#residual such to determine the end of the exhalation rate
#research.

ResTot=1000001

#------------------------------------------------------------------------------
#Iterative process to find the radon exhalation rate best-fitting
#fitting the experimental data.

#All the acquired arrays should have passed the length check.
#The while cycle contains the two exit conditions previously
#discussed and described.
if check_Radonin==True and check_Radonout==True and check_Gamma==True:
    while (counter<=15 and ResTot>1000000.):
        #The following equations estimate the radon concentration
        #if the exhalation rate equals R_ExInf. 
        for i in range(int(N)):
            #For each interval between radon records.
            #Initializing three support variables whose
            #first value equals the measured radon 
            #concentration at the beginning of the
            #corresponding interval.
            n_222Rn[0]=N_222Rn[i]
            for k in range(int(p)):
                #For each interval between flow rate records
                #within the same radon records interval.
                for m in range(int(n/p)):
                    #For each computation interval within             
                    #the same flow rate interval.
                    Gamma_222Rn_m=(Gamma_222Rn[k+1]-Gamma_222Rn[k])/(n/p)*m+Gamma_222Rn[k]
                    Mout_222Rn_m=(Mout_222Rn[i+1]-Mout_222Rn[i])/n*(k*(n/p)+m)+Mout_222Rn[i]
                    #The flow rate measured by the sensor cannot be
                    #simultaneously positive and negative so the following
                    #if cycle chooses the proper formulation of Eq. 3.5                     
                    #relative to the flow rate sign. 
                    if Gamma_222Rn_m>=0:
                        n_222Rn[int(k*(n/p)+m+1)]=n_222Rn[int(k*(n/p)+m)]+deltat*(-lambda_222Rn*n_222Rn[int(k*(n/p)+m)]+(Gamma_222Rn_m*Mout_222Rn_m)+R_ExInf)
                    else:
                        n_222Rn[int(k*(n/p)+m+1)]=n_222Rn[int(k*(n/p)+m)]+deltat*(-lambda_222Rn*n_222Rn[int(k*(n/p)+m)]+(Gamma_222Rn_m*n_222Rn[int(k*(n/p)+m)]/V_ch)+R_ExInf)
            #The last value computed within the i-interval
            #between radon concentration records is written
            #in the i+1 value of radon concentration array.
            N_222Rn[i+1]=n_222Rn[int(n)]
        #The radon concentration array is copied.
        N_222RnInf=cp.copy(N_222Rn)
        #The following cycle computes the lower residual.
        for i in range(len(N_222RnInf)):
            ResInf+=(N_222RnInf[i]-Min_222Rn[i])**2
            
		#Con il ciclo che segue viene stimato l'andamento della concentrazione per R_ExSup
        for i in range(int(N)):
            #For each interval between radon records.
            #Initializing three support variables whose
            #first value equals the measured radon 
            #concentration at the beginning of the
            #corresponding interval.
            n_222Rn[0]=N_222Rn[i]
            for k in range(int(p)):
                #For each interval between flow rate records
                #within the same radon records interval.
                for m in range(int(n/p)):
                    #For each computation interval within             
                    #the same flow rate interval.
                    Gamma_222Rn_m=(Gamma_222Rn[k+1]-Gamma_222Rn[k])/(n/p)*m+Gamma_222Rn[k]
                    Mout_222Rn_m=(Mout_222Rn[i+1]-Mout_222Rn[i])/n*(k*(n/p)+m)+Mout_222Rn[i]
                    if Gamma_222Rn_m>=0:
                        n_222Rn[int(k*(n/p)+m+1)]=n_222Rn[int(k*(n/p)+m)]+deltat*(-lambda_222Rn*n_222Rn[int(k*(n/p)+m)]+(Gamma_222Rn_m*Mout_222Rn_m)+R_ExSup)
                    else:
                        n_222Rn[int(k*(n/p)+m+1)]=n_222Rn[int(k*(n/p)+m)]+deltat*(-lambda_222Rn*n_222Rn[int(k*(n/p)+m)]+(Gamma_222Rn_m*n_222Rn[int(k*(n/p)+m)]/V_ch)+R_ExSup)
			#The last value computed within the i-interval
            #between radon concentration records is written
            #in the i+1 value of radon concentration array.
            N_222Rn[i+1]=n_222Rn[int(n)]
        #The radon concentration array is copied.
        N_222RnSup=cp.copy(N_222Rn)
		#The following cycle computes the upper residual.
        for i in range(len(N_222RnInf)):
            ResSup+=(N_222RnSup[i]-Min_222Rn[i])**2

        #The following commands allow to print a specific report that,
        #for each iteration, displays lower and upper residuals.
        print(counter," "*(3-len(str(counter))),"|"," "*0,round(R_ExInf*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2)," "*(10-len(str(round(R_ExInf*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2)))),"|"," "*0,round(ResInf,2)," "*(20-len(str(round(ResInf,2)))),"|"," "*0,round(R_ExSup*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2)," "*(10-len(str(round(R_ExSup*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2)))),"|"," "*0,round(ResSup,2))
        f_out.write(str(counter)+" "*(3-len(str(counter)))+" "*1+"|"+" "*1+str(round(R_ExInf*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2))+" "*(10-len(str(round(R_ExInf*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2))))+" "*1+"|"+" "*1+str(round(ResInf,2))+" "*(20-len(str(round(ResInf))))+" "*1+"|"+" "*1+str(round(R_ExSup*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2))+" "*(10-len(str(round(R_ExSup*1000*lambda_222Rn*3600/(length*height*(10**(-4))),2))))+" "*1+"|"+" "*1+str(round(ResSup,2)))
        f_out.write("\n")

        #The following commands aim to define a new upper and lower
        #boundaries for the exhalation rate. Among the previous 
        #boundaries, the one characterized by the lower residual 
        #is confirmed, the other changed following the binomial 
        #goal seeking.
        if ResInf<=ResSup:
            ResTot=ResInf
            R_ExInf=R_ExInf
            R_ExSup=(R_ExSup-R_ExInf)/2+R_ExInf
            N_222Rn=N_222RnInf
            R=R_ExInf
        elif ResSup<ResInf:
            ResTot=ResSup
            R_ExSup=R_ExSup
            R_ExInf=R_ExSup-(R_ExSup-R_ExInf)/2
            N_222Rn=N_222RnSup
            R=R_ExSup
        #The residuals are zeroed and the counter increased by 1.
        ResInf=0
        ResSup=0
        counter+=1	
#Following conditions appplie in case of errors in input files.
else:
    if check_Gamma==False:
        print("Flow Rate Data Error")
    if check_Radonin==False:
        print("Internal AlphaGUARD Data Error")
    if check_Radonout==False:
        print("External AlphaGUARD Data Error")

#Reproducing a beep when the goal seeking finishes and
#printing the results on both the screen and the output
#file.
ws.Beep(400,500)
R=R*1000*lambda_222Rn*3600/(height*length*(10**(-4)))
print("The estimated radon exhalation rate is",round(R,2),"mBq/(h*m^2)")

f_out.write("\n")
f_out.write("The estimated radon exhalation rate is"+" "+str(round(R,2))+" "+"mBq/(h*m^2)")
f_out.close()

#------------------------------------------------------------------------------
#Assembling the arrays of radon activity and activity concentration.

A_222Rn=N_222Rn*lambda_222Rn #[Bq]

a_222Rn=A_222Rn/V_ch #[Bq/m^3]

#------------------------------------------------------------------------------
#Printing on a second output file the radon concentration trend
#corresponding to the returned exhalation rate.

f_out=open(file_output+".txto","w")
for i in range(len(a_222Rn)-1):
	f_out.write(str(cin_222Rn[i]))
	f_out.write(" "*(22-len(str(cin_222Rn[i]))))
	f_out.write(str(a_222Rn[i]))
	f_out.write("\n")
f_out.write(str(cin_222Rn[len(a_222Rn)-1]))
f_out.write(" "*(22-len(str(cin_222Rn[len(a_222Rn)-1]))))
f_out.write(str(a_222Rn[len(a_222Rn)-1]))
f_out.close()

#------------------------------------------------------------------------------
#The last code section is dedicated to the graphic representation
#of both the measured and the estimated radon concentration trend.

plt.figure(figsize=(10,5),dpi=200)
plt.plot(cin_222Rn,color="darkmagenta", linestyle="-",linewidth=0.7,label="Measured $^{222}$Rn concentrations")
plt.errorbar(list(range(0,len(cin_222Rn))),cin_222Rn, yerr=(sigmain_222Rn,sigmain_222Rn),color="darkmagenta",marker='.',markersize=5,markeredgewidth=0.5, linewidth=0.2, markeredgecolor='darkmagenta',markerfacecolor='magenta',ecolor='magenta',capsize=2)
plt.plot(a_222Rn,color="green",linestyle="--",linewidth=0.7,label="Estimated $^{222}$Rn concentrations")
plt.xlim(0,len(cin_222Rn)-1)
plt.ylim(0,max(cin_222Rn)*1.5)
pHours=1
plt.xticks(np.arange(0,len(cin_222Rn),pHours*6),(np.arange(0,len(cin_222Rn),pHours*6)/6).astype(int))
plt.yticks(np.arange(0,max(cin_222Rn*1.5),100))
plt.minorticks_on()
plt.grid(b=True, which='minor', color='whitesmoke', linestyle='--',linewidth=0.3)
plt.grid(b=True,which='major', color='gainsboro', linestyle='-', linewidth=0.3)


plt.xlabel(u"Measuring time (hours)")
plt.ylabel(u"$^{222}$Rn concentrations (Bq m$^{-3}$)")
plt.legend(loc="best")
plt.title("Comparison between estimated and measured trend")
plt.rcParams["font.family"] = "serif"
plt.img_output=file_output+".png"
plt.savefig(plt.img_output)
plt.show()

