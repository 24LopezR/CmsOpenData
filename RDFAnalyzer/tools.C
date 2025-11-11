#ifndef tools
#define tools

#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <TVector3.h>
#include <TLorentzVector.h>
#include <iostream>
#include <string>
#include <TH1F.h>
#include <TMath.h>
#include <iomanip>
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"

#include <map>
#include <cmath>
#include <set>
#include <vector>
#include <regex>
#include <random>
#include <chrono>

using namespace ROOT;
using namespace ROOT::VecOps;

float invariantMass(RVecF pt, RVecF eta, RVecF phi) {
  float muMass = 0.105658375;

  //Calculates the dimuon mass given 4-vector components of both muons
  TLorentzVector mu1;
  TLorentzVector mu2;

  mu1.SetPtEtaPhiM(pt[0],eta[0],phi[0],muMass);
  mu2.SetPtEtaPhiM(pt[1],eta[1],phi[1],muMass);
  //Dimuon 4-Vector
  TLorentzVector dim = mu1+mu2;

  return dim.M();
}

#endif
