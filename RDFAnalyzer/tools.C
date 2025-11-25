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

RVec<bool> isGoodMuon(RVec<bool> cutstring) {
  return cutstring;
}

float invariantMass(RVec<float> pt, RVec<float> eta, RVec<float> phi) {
  if (pt.size()<2) return -999.;
  
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

float invariantMass(const RVec<int> &isGoodMuon,
                    const RVec<float> &pt,
                    const RVec<float> &eta,
                    const RVec<float> &phi) {
  std::vector<int> goodMuons;
  for (int i=0; i<isGoodMuon.size(); i++) {
    if (isGoodMuon[i] == 1) goodMuons.push_back(i);
  }

  if (goodMuons.size()<2) return -999.;

  int idx0 = goodMuons[0];
  int idx1 = goodMuons[1];

  float muMass = 0.105658375;

  //Calculates the dimuon mass given 4-vector components of both muons
  TLorentzVector mu1;
  TLorentzVector mu2;

  mu1.SetPtEtaPhiM(pt[idx0],eta[idx0],phi[idx0],muMass);
  mu2.SetPtEtaPhiM(pt[idx1],eta[idx1],phi[idx1],muMass);
  //Dimuon 4-Vector
  TLorentzVector dim = mu1+mu2;

  return dim.M();
}
#endif
