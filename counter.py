import os
import re


def counter(path):
    datapath = str(path)
    typestr = str(re.split('/', datapath)[-1][0:3])
    datatype = ""
    if typestr == "10X":
        datatype = '10X'
    elif typestr == 'bio':
        datatype = 'BioNano'
    elif typestr == 'Bio':
        datatype = 'BioNano'
    elif typestr == 'pac':
        datatype = 'PacBio'
    elif typestr == 'Pac':
        datatype = 'PacBio'
    elif typestr == 'ill':
        datatype = 'illumina'
    elif typestr == 'HiC':
        datatype = 'HiC'

    if datatype == "BioNano":
        print(datapath)
        print('BioNano DEL count:')
        os.system("awk '{print $17}'" + f" {datapath} | grep 'DEL' | wc -l")
        print('BioNano INS count:')
        os.system("awk '{print $17}'" + f" {datapath} | grep 'INS' | wc -l")
        print('BioNano TRA count:')
        os.system("awk '{print $17}'" + f" {datapath} | grep 'TRA' | wc -l")
        print('BioNano INV count:')
        os.system("awk '{print $17}'" + f" {datapath} | grep 'INV' | wc -l")
        print('BioNano DUP count:')
        os.system("awk '{print $17}'" + f" {datapath} | grep 'DUP' | wc -l")
        print('\n')
        print('\n')
        print('\n')
    elif datatype == "HiC":
        print(datapath)
        print("HiC does not support SV type calling")
    elif datatype == "10X":
        print(datapath)
        print('10X DEL count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep 'TYPE=DEL' | wc -l")
        print('10X INS count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep 'TYPE=INS' | wc -l")
        print('10X TRA count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep 'TYPE=TRA' | wc -l")
        print('10X INV count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep 'TYPE=INV' | wc -l")
        print('10X UNK count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep 'TYPE=UNK' | wc -l")
        print('\n')
        print('\n')
        print('\n')
    elif datatype == "illumina":
        print(datapath)
        print('Illumina inversion count:')
        os.system("awk '{print $18}'"+f" {datapath} | grep 'inversion' | wc -l")
        print('Illumina deletion count:')
        os.system("awk '{print $18}'"+f" {datapath} | grep 'deletion' | wc -l")
        print('Illumina tandem-duplication count:')
        os.system("awk '{print $18}'"+f" {datapath} | grep 'tandem-duplication' | wc -l")
        print('Illumina translocation count:')
        os.system("awk '{print $18}'"+f" {datapath} | grep 'translocation' | wc -l")
        print('\n')
        print('\n')
        print('\n')
    elif datatype == "PacBio":
        print(datapath)
        print('PacBio <TRA> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<TRA>' | wc -l")
        print('PacBio <DUP> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<DUP>' | wc -l")
        print('PacBio <DEL> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<DEL>' | wc -l")
        print('PacBio <INS> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<INS>' | wc -l")
        print('PacBio <INV> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<INV>' | wc -l")
        print('PacBio <INVDUP> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<INVDUP>' | wc -l")
        print('PacBio <DUP/INS> count:')
        os.system("awk '{print $18}'" + f" {datapath} | grep '<DUP/INS>' | wc -l")
        print('\n')
        print('\n')
        print('\n')
    else:
        print(f"{datatype} is not a valid type")
    return datatype


if __name__ == "__main__":
    inp = input('SV type counter (Path to input file), separate multiple inputs with ", "\n')
    sep_output = inp.split(", ")
    for item in sep_output:
        a = counter(item)
        print(f"Done with {a}")
