import ROOT as R
R.gROOT.ProcessLine(".L tools.C")

histpars = {
        "nMuon":    {
            "xlabel": "N muons",
            "bins": 10,
            "xmin": 0,
            "xmax": 10,
            "name": "Number of muons in the event"},
        "Muon_dxy":    {
            "xlabel": "muon d_{xy} (cm)",
            "bins": 100,
            "xmin": 0.,
            "xmax": 15.,
            "name": "Muon impact parameter in the XY plane [GeV]"},
        "Muon_dz":     {
            "xlabel": "muon d_{z} (cm)",
            "bins": 100,
            "xmin": 0.,
            "xmax": 15.,
            "name": "Muon impact parameter in the Z axis [GeV]"},
        "Muon_eta": {
            "xlabel": "muon #eta",
            "bins": 100,
            "xmin": -3.,
            "xmax": 3.,
            "name": "Muon trajectory pseudorrapidity (#eta)"},
        "Muon_phi": {
            "xlabel": "muon #phi",
            "bins": 100,
            "xmin": -3.2,
            "xmax": 3.2,
            "name": "Muon trajectory #phi coordinate"},
        "Muon_pt":  {
            "xlabel": "muon p_{T} (GeV)",
            "bins": 100,
            "xmin": 0.,
            "xmax": 200.,
            "name": "Muon transverse momentum (p_{T}) [GeV]"},
        "Muon_charge": {
            "xlabel": "muon q",
            "bins": 3,
            "xmin": -1.,
            "xmax": 2.,
            "name": "Muon charge"},
        "Muon_isTracker": {
            "xlabel": "muon isTracker",
            "bins": 2,
            "xmin": 0.,
            "xmax": 2.,
            "name": "Muon is reconstructed by tracker algorithm?"},
        "Muon_isStandalone": {
            "xlabel": "muon isStandalone",
            "bins": 2,
            "xmin": 0.,
            "xmax": 2.,
            "name": "Muon is reconstructed by standalone algorithm?"},
        "Muon_isGlobal": {
            "xlabel": "muon isGlobal",
            "bins": 2,
            "xmin": 0.,
            "xmax": 2.,
            "name": "Muon is reconstructed by global algorithm?"},
        "DiMuon_invMass": {
            "xlabel": "m_{#mu#mu} (GeV)",
            "bins": 200,
            "xmin": 0.,
            "xmax": 200.,
            "name": "Dimuon invariant mass [GeV]"},
    }

toDefine = {
        "DiMuon_invMass": "invariantMass(Muon_pt, Muon_eta, Muon_phi)",
#        "Muon_type":      "return RVecI({1*Muon_isStandalone,2*Muon_isTracker,3*Muon_isGlobal})",
    }

def loadRDF(tree, filename):
    df = R.RDataFrame(tree, filename)
    for var in toDefine:
        df = df.Define(var, toDefine[var])
    return df

def plot(c, h, color=R.kViolet+1, xmin=None, xmax=None):
    c.cd()
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetFillColorAlpha(color,0.3)
    h.SetMaximum(50*h.GetMaximum())
    h.SetMinimum(0.5)
    if xmin and xmax: h.GetXaxis().SetRange(xmin,xmax)
    h.Draw("HIST")
    c.SetLogy(1)
    return c
