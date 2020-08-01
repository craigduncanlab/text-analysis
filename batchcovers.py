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

def walkThru(mypath):
	f = []
	newlist=[]
	print("Getting your dir and files...")
	for (dirpath, dirnames, filenames) in walk(mypath):
	    #f.extend(dirpath,filenames)
	    f.extend(os.path.join(dirpath, filename) for filename in filenames)
	print("%d files found. Filtering." % len(f))
	for i in f:
		text=i[-4:]
		# need to exclude these ~ on macosx for some reason
		passed=True
		if "~$" in i:
			passed=False
		if text=="docx" and passed==True:
			newlist.append(i)
	print(newlist)
	print("Finished")
	print("List size %d" % len(newlist))
	oplist=newlist[:200] # limit to 200 documents
	countme=0
	courtdocs=[]
	legaldocs=[]
	otherdocs=[]
	nocoversdocs=[]
	for ff in oplist:
		#print(ff)
		result=coverpage.parseCoverPage(ff)
		plist=coverpage.getFirst50(ff)
		if result==True:
			ccd=coverpage.checkCourtDoc(plist)
			if ccd==True:
				courtdocs.append(ff)
			else:
				cld=coverpage.checkLegalDoc(plist)
				if cld==True:
					legaldocs.append(ff)
				else:
					otherdocs.append(ff)
		else:
			nocoversdocs.append(ff)
	print("No covers Documents:")
	for k in nocoversdocs:
		print(k)
	print("---")
	print("Classified Court Documents:")
	for i in courtdocs:
		print(i)
	print("---")
	print("Classified Legal Documents:")
	for p in legaldocs:
		print(p)
	print("---")
	print("Unclassified Documents:")
	for r in otherdocs:
		print(r)

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
			walkThru(fp)
		else:
			print("Use python3 batchcovers.py ~/Documents")
			print("Case sensitive.  Include phrases in quotes.  Use ? to findall")
else:
	doError()