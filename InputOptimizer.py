import numpy as np

def isReal (s):
    if len(s)==0:
        return False
    return s.isdigit() or (s[0] in "+-" and s[1:].isdigit()) or (s.count(".")==1 and (s.replace(".","1")).isdigit()) or (s.count(".")==1 and (s.replace(".","1"))[0] in "+-" and (s.replace(".","1"))[1:].isdigit())

file_name=raw_input("Flow Rate Input: ")
file_name=file_name+".txt"
f_in=open(file_name,"r")
fread=f_in.read()
rows_fread=fread.split("\n")
rows_fread.remove(rows_fread[0])
rows_fread.remove(rows_fread[0])
rows_fread.remove(rows_fread[0])


Voutput=[]

for i in range(len(rows_fread)):
    row=rows_fread[i]
    if "\t" in row:
        row_splitted=row.split("\t")
        Voutput.append(row_splitted[1])

for i in range(len(Voutput)):
    Voutput[i]=float(Voutput[i])

VOutput=np.array(Voutput) #[V]
FlowRate=50.*(VOutput*2./5.-0.5)/0.4 #[cm^3/min]
FlowRate=FlowRate*10**(-6)/60. #[m^3/s]

f_out=open("Portata_Measurements.txt","w")
for i in range(len(FlowRate)-1):
    f_out.write(str(FlowRate[i]))
    f_out.write("\n")
f_out.write(str(FlowRate[len(FlowRate)-1]))
f_out.close()

#-------------------------------------------------

file_name=raw_input("Internal AlphaGUARD Data: ")
file_name=file_name+".txt"
f_in=open(file_name,"r")
fread=f_in.read()
fread=fread.replace(",","")
rows_fread=fread.split("\n")
rows_fread.remove(rows_fread[0])

datei=[]
c_radoni=[]
sigma_c_radoni=[]

for i in range(len(rows_fread)):
    row=rows_fread[i]
    if "\t" in row:
        row_splitted=row.split("\t")
        datei.append(row_splitted[0])
        c_radoni.append(row_splitted[2])
        sigma_c_radoni.append(row_splitted[3])
        
for i in range(len(datei)):
    if ":"in datei[i]:
        datei[i]=str(datei[i])
    else:
        datei.remove(datei[i])
    if isReal(c_radoni[i])==True:
        c_radoni[i]=float(c_radoni[i])
    else:
        c_radoni.remove(c_radoni[i])
    if isReal(sigma_c_radoni[i])==True:
        sigma_c_radoni[i]=float(sigma_c_radoni[i])
    else:
        sigma_c_radoni.remove(sigma_c_radoni[i])

Datei=np.array(datei) #[dd/mm/yy hh:mm]
C_radoni=np.array(c_radoni) #[Bq/m^3]
Sigma_C_radoni=np.array(sigma_c_radoni) #[Bq/m^3]

f_out=open("RadonINT_Measurements.txt","w")
for i in range(len(C_radoni)-1):
    f_out.write(str(C_radoni[i]))
    f_out.write("\t")
    f_out.write(str(Sigma_C_radoni[i]))
    f_out.write("\n")
f_out.write(str(C_radoni[len(C_radoni)-1]))
f_out.write("\t")
f_out.write(str(Sigma_C_radoni[len(Sigma_C_radoni)-1]))
f_out.close()

#-------------------------------------------------

file_name=raw_input("External AlphaGUARD Data: ")
file_name=file_name+".txt"
f_in=open(file_name,"r")
fread=f_in.read()
fread=fread.replace(",","")
rows_fread=fread.split("\n")
rows_fread.remove(rows_fread[0])

datee=[]
c_radone=[]
sigma_c_radone=[]

for i in range(len(rows_fread)):
    row=rows_fread[i]
    if "\t" in row:
        row_splitted=row.split("\t")
        datee.append(row_splitted[0])
        c_radone.append(row_splitted[2])
        sigma_c_radone.append(row_splitted[3])
        
for i in range(len(datee)):
    if ":"in datee[i]:
        datee[i]=str(datee[i])
    else:
        datee.remove(datee[i])
    if isReal(c_radone[i])==True:
        c_radone[i]=float(c_radone[i])
    else:
        c_radone.remove(c_radone[i])
    if isReal(sigma_c_radone[i])==True:
        sigma_c_radone[i]=float(sigma_c_radone[i])
    else:
        sigma_c_radone.remove(sigma_c_radone[i])

Datee=np.array(datee) #[dd/mm/yy hh:mm]
C_radone=np.array(c_radone) #[Bq/m^3]
Sigma_C_radone=np.array(sigma_c_radone) #[Bq/m^3]

f_out=open("RadonEXT_Measurements.txt","w")
for i in range(len(C_radone)-1):
    f_out.write(str(C_radone[i]))
    f_out.write("\t")
    f_out.write(str(Sigma_C_radone[i]))
    f_out.write("\n")
f_out.write(str(C_radone[len(C_radone)-1]))
f_out.write("\t")
f_out.write(str(Sigma_C_radone[len(Sigma_C_radone)-1]))
f_out.close()

if np.array_equal(Datei,Datee):
    f_out=open("Date.txt","w")
    for i in range(len(Datee)-1):
        f_out.write(str(Datee[i]))
        f_out.write("\n")
    f_out.write(str(Datee[len(Datee)-1]))
    f_out.close()

print "-------------------------------"
print "Input files correctly written."

print "-------------------------------"
if len(Datei)==len(Datee)==len(C_radoni)==len(C_radone)==len(Sigma_C_radoni)==len(Sigma_C_radone) and ((len(Datei)-1)/6*3600+1)==len(FlowRate):
    print "Data check OK."
else:
    print "Error in comparing data."
print "-------------------------------"

print "Measuring details:"
print (len(Datee)-1)/6,"hours;"
print "1","s","flow rate measuring interval;"
print "10","m","radon concentration measuring interval;"

