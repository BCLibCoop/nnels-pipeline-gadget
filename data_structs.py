bySCN = {}
byTitle = {}

def hasSCN(scn):
	return scn in bySCN
def hasTitle(title):
	return title in byTitle
def getSCN_fromTitle(title):
	return bySCN[title]
def getTitle_fromSCN(scn):
	return byTitle[scn]
def setTitle_fromSCN(scn, title):
	bySCN[scn] = title
def setSCN_fromTitle(title, scn):
	byTitle[title] = scn
