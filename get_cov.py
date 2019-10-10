#!/usr/bin/env python3
# Fabio Zanarello, JRC-Ispra, 2019


import os
import subprocess
import sys
import argparse
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--input', metavar='INPUTFILE', help='FASTA file', default="/dev/stdin")
    parser.add_argument('--ref', metavar='REF', help='Reference sequence name')
    parser.add_argument('--output', metavar='OUTPUTFILE', help='Coverage result', default="/dev/stdout")
    args = parser.parse_args()

    seqs={}

    with open (args.input) as my_fasta:
        seq_name=""

        for line in my_fasta:
            if line[0]==">":
                seq_name=line[1:].strip("\n")
                seqs[seq_name]=""
            if line[0]!=">":
                seqs[seq_name]=seqs[seq_name]+line.strip("\n")

    #print (seqs)

    reference_name=args.ref
    reference_seq=seqs[reference_name]
    reference_lenght=len(reference_seq)
    cov_dict={}

    for i in range(reference_lenght):
        cov_dict[i+1]=[0,0,0]

    for element in seqs:
        if element!=reference_name:
            if reference_lenght!=len(seqs[element]):
                print()
                print(element+" is long "+str(len(seqs[element]))+" while reference is "+str(reference_lenght))
                print ("The sequence is NOT CONSIDERED in coverage count")
                print ()
            if reference_lenght==len(seqs[element]):
                #print(element+" lenght EQUAL to reference")
                for i in range(reference_lenght):
                    #print (seqs[element][i])
                    if seqs[element][i]==reference_seq[i]:
                        cov_dict[i+1][0]+=1
                    if seqs[element][i]!=reference_seq[i] and seqs[element][i]!="-":
                        cov_dict[i+1][1]+=1

    for element in cov_dict:
        cov_dict[element][2]=cov_dict[element][0]+cov_dict[element][1]

    with open (args.output, "w") as out:
        print()
        print()
        out.write(str("POSITION")+"\t"+str("MATCH")+"\t"+str("MISMATCH")+"\t"+str("COVERAGE")+"\n")
        for element in cov_dict:
            out.write(str(element)+"\t"+str(cov_dict[element][0])+"\t"+str(cov_dict[element][1])+"\t"+str(cov_dict[element][2])+"\n")




if __name__ == "__main__":
    main()
