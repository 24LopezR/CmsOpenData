import ROOT as R
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--directory','-d', dest='directory', type=str)
parser.add_argument('--infile','-i', dest='infile', type=str)
parser.add_argument('--outfile','-o', dest='outfile', type=str)
args = parser.parse_args()

SELECT_BRANCHES = ["run","luminosityBlock","event","Muon_*","nMuon"]

if __name__=='__main__':

    book = {}

    if args.directory: filelist = [f"{args.directory}/{f}" for f in os.listdir(args.directory)]
    if args.infile:    filelist = [args.infile]
    for file in filelist:
        if not file.endswith('.root'): continue
        print(f"Processing file {file} ...")
        book[file] = {}
        
        # Load tree
        print("Loading tree...")
        f_read = R.TFile(str(file),"READ")
        tree_read = f_read.Get('Events')
        tree_read.SetBranchStatus("*",0)
        for br in SELECT_BRANCHES:
            tree_read.SetBranchStatus(br,1)

        # Write new tree
        print("Writing tree...")
        print(f"{args.outfile}")
        f_write = R.TFile.Open(f"{args.outfile}","RECREATE")
        tree_write = tree_read.CloneTree()
        tree_write.Write()
        f_write.Close()
        
        f_read.Close()