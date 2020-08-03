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
	log=True
	f = []
	newlist=[]
	print("Getting your dir and files...")
	for (dirpath, dirnames, filenames) in walk(mypath):
	    #f.extend(dirpath,filenames)
	    f.extend(os.path.join(dirpath, filename) for filename in filenames)
	if log==True:
		print("%d files found. Filtering." % len(f))
	for i in f:
		text=i[-4:]
		# need to exclude these ~ on macosx for some reason
		passed=True
		if "~$" in i:
			passed=False
		if text=="docx" and passed==True:
			newlist.append(i)
	#print(newlist)
	print("Finished")
	print("List size %d" % len(newlist))
	oplist=newlist[0:200] # limit to 200 documents
	if log==True:
		print(oplist)
	countme=0
	courtdocs=[]
	legaldocs=[]
	otherdocs=[]
	nocoversdocs=[]
	count=0
	for ff in oplist:
		count=count+1
		if log==True:
			print(count)
		#print(ff)
		# if coverpage, then classify
		result=coverpage.parseCoverPage(ff,True) # No log
		if log==True:
			print(result)
		plist=coverpage.getFirst50(ff,log)
		if log==True:
			print(plist)
		if result==True:
			ccd=coverpage.checkCourtDoc(plist,False)
			if ccd==True:
				courtdocs.append(ff)
			else:
				cld=coverpage.checkLegalDoc(plist,False)
				if cld==True:
					legaldocs.append(ff)
				else:
					otherdocs.append(ff)
		else:
			nocoversdocs.append(ff)
	for r in otherdocs:
		print(r)
	print("No covers Documents:")
	for k in nocoversdocs:
		output="[no cover] "+k
		print(output)
	print("---")
	print("Classified Court Documents:")
	for i in courtdocs:
		output="[court] "+i
		print(output)
	print("---")
	print("Classified Legal Documents:")
	for p in legaldocs:
		output="[legal] "+p
		print(output)
	print("---")
	print("Unclassified Documents:")
	for r in otherdocs:
		output="[unclassified] "+r
		print(output)
	print("Filtered .docx files: %d" % len(oplist))
	print("No covers Documents: %d" % len(nocoversdocs))
	print("Classified Court Documents: %d" % len(courtdocs))
	print("Classified Legal Documents: %d" % len(legaldocs))
	print("Unclassified Documents: %d" % len(otherdocs))
	

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