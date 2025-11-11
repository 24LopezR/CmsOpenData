import ROOT as R
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--directory','-d', dest='directory', type=str)
args = parser.parse_args()

toDefine = {
        'Dimuon_invMass', 'invMass(Muon_pt, Muon_eta, Muon_phi)',
        }

SELECT_BRANCHES = ["run","luminosityBlock","event","Muon_*","nMuon"]

if __name__=='__main__':

    book = {}

    for file in os.listdir(args.directory):
        if not file.endswith('.root'): continue
        fname = f"{args.directory}/{file}"
        print(f"Processing file {fname} ...")
        book[file] = {}
        
        # Load tree
        print("Loading tree...")
        f_read = R.TFile(str(fname),"READ")
        tree_read = f_read.Get('Events')
        tree_read.SetBranchStatus("*",0)
        for br in SELECT_BRANCHES:
            tree_read.SetBranchStatus(br,1)

        # Write new tree
        print("Writing tree...")
        with R.TFile.Open(f"{args.directory}_skimmed/{file.split('.')[0]_skimmed.root}","RECREATE") as f_write:
            tree_write = tree_read.CloneTree()
            tree_write.Write()
