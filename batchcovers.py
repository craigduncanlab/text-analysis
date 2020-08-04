import sys
import review # this uses xmlutil as well
import coverpage
import os
from os import walk
# (c) Craig Duncan 2020
# bulk coverpage checks - docx legal docs classifier
# Example usage (macosx): 
# time python3 batchcovers.py ~/Documents/2020_Law/LegalPrecs
# 

def walkThru(mypath,log):
	#log=False
	f = []
	newlist=[]
	print("Getting your dir and files...")
	for (dirpath, dirnames, filenames) in walk(mypath):
	    #f.extend(dirpath,filenames)
	    f.extend(os.path.join(dirpath, filename) for filename in filenames)
	if log==True:
		print("%d files found. Filtering." % len(f))
	for i in f:
		text=i[-4:] # last few characters of filename
		# need to exclude these ~ on macosx for some reason
		passed=True
		if "~$" in i:
			passed=False
		if text=="docx" and passed==True:
			newlist.append(i)
	#print(newlist)
	print("Finished")
	print("List size %d" % len(newlist))
	#oplist=newlist[0:200] # limit to 200 documents
	filelist=newlist
	if log==True:
		print(filelist)
	classifier(filelist,log)
	
		
# function to classify document type by first page contents
# These are non-exclusive categories
# Option: rank these and select highest category
def classifier(filelist,log):
# if coverpage, then classify
	#log=False
	countflag=True
	countme=0
	count=0
	courtdocs=[]
	legaldocs=[]
	otherdocs=[]
	nocoversdocs=[]
	memodocs=[]
	for ff in filelist:
		count=count+1
		if countflag==True and count % 10==0:
			print(count)
		#print(ff)
		obs=coverpage.reportResult(ff,log)
		if obs[0]==False:
			nocoversdocs.append(ff)
			if log==True:
				nocoverreport(ff)
		if obs[1]==True:
			memodocs.append(ff)
		if obs[2]==True:
			courtdocs.append(ff)
		if obs[3]==True:
			legaldocs.append(ff)

	print("Filtered .docx files: %d" % len(filelist))
	printReport(nocoversdocs,memodocs,courtdocs,legaldocs,otherdocs)

def nocoverreport(filepath):
		reviewXML=False
		print("[XXX no cover] %s" % filepath)
		#text=review.openfilestyles(filepath)
		if reviewXML==True:
			myfile=xmlutil.getDocxContent(filepath)
			paralist=xmlutil.getParasInclusiveStyle(myfile)
			subset=paralist[0:50]
			for i in subset: # just first 50 lines
				print(i)

# dump results to std output
def printReport(nocoversdocs,memodocs,courtdocs,legaldocs,otherdocs):
	#
	print("Classifications (1st page):")
	print("general:")
	for k in nocoversdocs:
		output="[general] "+k
		print(output)
	print("---")
	print("Memo Documents:")
	for m in memodocs:
		output="[memo] "+m
		print(output)
		print("---")
	print("Court Documents:")
	for i in courtdocs:
		output="[court] "+i
		print(output)
	print("---")
	print("Agreements:")
	for p in legaldocs:
		output="[agreement] "+p
		print(output)
	print("---")
	print("Unknown summary:")
	for r in otherdocs:
		output="[unknown summary] "+r
		print(output)
	print("General Documents: %d" % len(nocoversdocs))
	print()
	print("Classified 'cover' docs")
	print()
	print("Memo Documents: %d" % len(memodocs))
	print("Court Documents: %d" % len(courtdocs))
	print("Legal Documents: %d" % len(legaldocs))
	print("Other: %d" % len(otherdocs))

	
# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
print(args)
# if this is run as the top-level stand-alone program with 1 parameter
if (args==2 and __name__ == '__main__'):
		fp=sys.argv[1]
		# request=sys.argv[2]
		if len(fp)!=0:
			# remainder is optional for now:
			print("Filepath is "+fp)
			print("Making filelist of docx files...")
			print("(This could take a few minutes)")
			walkThru(fp,True)
		else:
			print("Use python3 batchcovers.py ~/Documents")
			print("Case sensitive.  Include phrases in quotes.  Use ? to findall")
else:
	doError()