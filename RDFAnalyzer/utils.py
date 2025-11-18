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
        "Muon_tightId": {
            "xlabel": "muon isTight",
            "bins": 2,
            "xmin": 0.,
            "xmax": 2.,
            "name": "Muon passes tight ID?"},
        "Muon_tkRelIso": {
            "xlabel": "muon I^{trk}_{rel}",
            "bins": 100,
            "xmin": 0.,
            "xmax": 5.,
            "name": "Muon tracker relative isolation (I/p_{T})"},
        "DiMuon_invMass": {
            "xlabel": "m_{#mu#mu} (GeV)",
            "bins": 200,
            "xmin": 0.,
            "xmax": 200.,
            "name": "Dimuon invariant mass [GeV]"},
    }

toDefine = {
        "DiMuon_invMass":  "invariantMass(Muon_pt, Muon_eta, Muon_phi)",
        "Muon_isGoodMuon": "return RVecI()",
#        "Muon_type":      "return RVecI({1*Muon_isStandalone,2*Muon_isTracker,3*Muon_isGlobal})",
    }

def loadRDF(tree, filename):
    df = R.RDataFrame(tree, filename)
    for var in toDefine:
        df = df.Define(var, toDefine[var])
    return df

colors = [R.kViolet+1, R.kOrange+1]

def plot(c, h, color=R.kViolet+1, xmin=None, xmax=None, logy=True):
    c.cd()
    if type(h)!=list: h = [h]
    for i,h_temp in enumerate(h):
        h_temp.SetLineWidth(2)
        h_temp.SetLineColor(colors[i])
        h_temp.SetFillColorAlpha(colors[i],0.3)
        if logy:
            h_temp.SetMaximum(50*h_temp.GetMaximum())
            h_temp.SetMinimum(0.5)
        else:
            h_temp.SetMaximum(1.3*h_temp.GetMaximum())
            h_temp.SetMinimum(0.)
        if xmin and xmax: h_temp.GetXaxis().SetRange(xmin,xmax)
        if i == 0:
            h_temp.Draw("HIST")
        else:
            h_temp.Draw("HIST,SAME")
    if logy: c.SetLogy(1)
    return c

def plot_with_fit(c, h, fit="gaussian", color=R.kViolet+1, xmin=None, xmax=None, logy=True):
    h_temp = h
    h_temp.SetDirectory(0)
    c.cd()
    h_temp.SetLineWidth(2)
    h_temp.SetLineColor(color)
    h_temp.SetFillColorAlpha(color,0.3)
    if logy:
        c.SetLogy(1)
        h_temp.SetMinimum(0.5)
    else:
        c.SetLogy(0)
        h_temp.SetMinimum(0.)
        h_temp.SetMaximum(1.3*h.GetMaximum())
    if xmin and xmax: h_temp.GetXaxis().SetRange(xmin,xmax)

    # Perform the fit
    if fit=="gaussian":
        f = R.TF1(fit,"gaus",60.,120.)
    elif fit=="bw":
        f = R.TF1(fit,"[0]*TMath::BreitWigner(x,[2],[1])",80.,100.)
        f.SetParameter(0, 1)
        f.SetParameter(2, 5)
        f.SetParameter(1, 91)
        f.SetParName(0,"Normalization")
        f.SetParName(1,"Z Width")
        f.SetParName(2,"Z Mass")
    elif fit=="conv":
        f = R.TF1(fit,"[3]*TMath::Voigt(x-[0],[1],[2],4)",60.,120.)
        f.SetParameter(0,h_temp.GetMean())
        f.SetParameter(1,h_temp.GetRMS())
        f.SetParameter(2,2.4)
        f.SetParameter(3,400)
        f.SetParName(0,"Z Mass")
        f.SetParName(1,"Exp. Resolution")
        f.SetParName(2,"Z Width")
        f.SetParName(3,"Normalization")
    f.SetLineWidth(2)
    f.SetLineColor(R.kRed)
    h_temp.Fit(f"{fit}")
    h_temp.Draw("HIST")
    f.Draw("SAME")
    return c
