import sys
import xmlutil
import review # this uses xmlutil as well
# coverpage - docx legal docs classifier
# (c) Craig Duncan 2020
# 

# input a filepath for docx
# sort a docx into buckets depending on first page contents
# if mutually exclusive then returned array can only have one 'True'
def reportResult(fp,log):
	#log=False
	# send back an array with test results (set of obs)
	isCover=False
	ismem=False
	iscrtdoc=False
	islegal=False
	plist=[]
	plist=getFirst50(fp,log)
	result=parseCoverPage(fp,log)
	# only check for Memo etc if cover page true
	if result==True:
		print("[cover] %s" % fp)
		isCover=True
		ismem=checkMemo(plist,log)
		iscrtdoc=checkCourtDoc(plist,False)
		islegal=checkLegalDoc(plist,False)
	else:
		print("Not a cover page")
	resultlist=[isCover,ismem,iscrtdoc,islegal]
	return resultlist
	
# see if the first page indicates Memorandum
# Look for title, then check for presence of introductory words (2 or more)

def checkMemo(mainlist,log):
	subset=[]
	if len(mainlist)>10:
		subset=mainlist[0:10] # should work okay with just first 5 lines
	titles=["memorandum","memo"]
	wordlist=["date","to","from","subject"]
	score=0
	count=0
	memoTitle=False
	for i in subset:
		count=count+1
		text=i[0]
		for t in titles:
			if (t.lower() in text.lower()):
				memoTitle=True
	if memoTitle==True:
		for i in subset:
			print(i)
			words=i[0].split(' ')
			for w in wordlist:
				# check first two words only
				stop=len(words)-1
				if stop>2:
					stop=2
				for t in range(0,stop):
					if w.lower() in words[t].lower():
						score=score+1
	#print(score)
	if score>2:
		print("This is a Memo")
		for i in subset:
			print(i[0])
		print(score)
		return True
	else:
		if log==True:
			print("This is not a Memo")
		return False

# test if first page is likely to be a document coverpage
def parseCoverPage(filepath,log):
	plist=getFirst50(filepath,log) # first 50 lines
	if log==True:
		print("plist OK")
		#print(plist)
		#exit()
	subset=firstpage_analysis(plist,log)
	if subset==-1:
		if log==True:
			print("no paragraphs detected.")
		return False
	result=testcoverpage(subset,log)
	if result==True:
		if log==True:
			print("Cover page detected")
		return True
	else:
		if log==True:
			print("No cover page detected")
		return False

def getFirst50(filepath,log):
	if log==True:
		print("Attempting to get first 50 paras:")
		print(filepath)
	myparastats=[]
	myparastats=review.openfilestyles(filepath,log)
	#try:
	#	myparastats=review.openfilestyles(filepath)
	#except:
	#	print("Error opening file. First 50")
	#	print (myparastats[1:3])
	#	exit()

	plist=[]
	if (len(myparastats)>50):
		plist=myparastats[0:50]
	else:
		plist=myparastats
	if log==True:
		print("plist OK with length:")
		print(len(plist))
	return plist

def checkCourtDoc(plist,log):
	#print("Checking Court Doc")
	courtList=["In the Matter of ","Between","Court","plaintiff","defendant","applicant","respondent","registry","Affidavit","Summons","CIV","Writ"]
	return checkFeaturedWords(plist,courtList,log)

def checkLegalDoc(plist,log):
	#print("Checking Legal Doc")
	docList=["Between","Parties","It is agreed","agreement"]
	result=checkFeaturedWords(plist,docList,log)
	if result==False:
		result2=checkLegalDocTitles(plist,log)
		if result2==True:
			#print("Found legal doc (by title)")
			return True
	return False

# first 50 lines will usually include front page as well
# taking in the next page will help push score over if needed
def checkLegalDocTitles(plist,log):
	#print("Checking Legal Doc Titles")
	docList=["Agreement to Lease","Lease","Assignment of Lease", "Joint Venture", "Partnership Deed", "Constitution", "Mortgage", "Deed of ", "Contract of","Consulting Agreement", "Distribution Agreement"]
	result=checkFeaturedWords(plist,docList,log)
	return result

# simple test to determine if a specific 'cover page' document or not
# Depends on what it is looking for to determine if it's likely
def checkFeaturedWords(plist,testList,log):
	courtrank=0
	count=1
	for i in plist:
		text=i[0]
		#print(text)
		#words=text.split(' ')
		for x in testList:
			#don't worry about case
			tx=text.lower().strip()
			xx=x.lower().strip()
			if tx.find(xx)!=-1:
				# print(x,text)
				courtrank=courtrank+1
		count=count+1
	result=float(courtrank/count*100)
	if log==True:
		print("Stats")
		print(courtrank,count)
	# If Court words score > 5% then we accept it is Court doc
	if result>5:
		if log==True:
			print("This is the check document. Score %s" % result)
		return True
	else:
		if log==True:
			print("Not the checked document. Score %s" % result)
		return False

# pre-req: find a region that appears to be a 'coverpage'
# i.e. do a rolling low density test for 100 lines or so
# for now, use first 50 lines in document (some old docs could be at end)
# then use this function to decide where page ends
def firstpage_analysis(plist,log):
	if log==True:
		print("---FIRST PAGE ANALYSIS---")
		# print("----Filter doc for low word density and low word count ---")
	filterlist=[]
	mainlist=[]
	breakmax=0
	pageend=0
	blocktext=0
	if len(plist)==0:
		if log==True:
			print("An empty list")
			print(plist)
		return -1
	for item in plist:
		tester=item[0][0:4]
		#if (tester=="COMM" and item[1]!="TOC1"):
			#print(item)
			#exit()
		text=item[0]
		style=item[1]
		prefix=style[0:3]
		words=item[2]
		sentences=item[3]
		index=item[4]
		density=item[5]
		pbreak=item[7]
		sbreak=item[8]
		if log==True:
			print(text)
		if pbreak==1 or sbreak==1 or blocktext==1:
			if pbreak==1:
					print(" --- page break found ---")
			if sbreak==1:
				print(" --- section break found ---")
			# we ignore it if it's in the first line or 2
			if index>3:
				pageend=1
				if breakmax==0:
					breakmax=index
			
		# filter not used
		if (density<8 and words<8):
			# can we rely on title names? or just word count?
			#if (style=="Normal" or style=="Title" and words<8):
			if (prefix!="TOC" and pageend!=1):
				filterlist.append(item)
	if breakmax==0:
		breakmax=len(plist)
	if log==True:
		print("page break at index: %d" % breakmax)
	mainlist=plist[0:breakmax] 
	if log==True:
		print("Done First Page Analysis")
		#print(mainlist)
		#print(breakmax)
	return mainlist


def testcoverpage(mainlist,log):
	total=0
	lowcount=0
	lm=len(mainlist)
	flagged=False
	wordCheck=True
	if lm>0:
		halfway=float(lm/2) #store top half marker point
		step=int(0)
		halftotal=int(0)
		for i in mainlist:
			step=int(step)+1
			text=i[0]
			flagged=False
			if ("summons" in text.lower()) and flagged==False:
				flagged=True
			words=int(i[2])
			#print(text)
			# mylist.append(i[0]) # text
			if step<halfway:
				halftotal=halftotal+words
			total=int(total)+int(words) # density
			if words<3:
				lowcount=lowcount+1 # less than 3 words in line
			if wordCheck==True:
				print("%d %d %s" % (step,words,text))
		ave=float(total/lm)
		halfave=float(halftotal/halfway)
		percentlow=float(lowcount/lm*100)
		if log==True:
			print("Total of word density: %d" % total)
			print("Ave word density: %f" % ave)
			print("Ave word density top half: %f" % halfave)
			print("Low word line pc %f" % percentlow)
		# redundant top half check:
		tophalf=False
		# was 50 for general, but make 30 to catch memos
		if (lm>10 and percentlow>30 and halfave<3):
			tophalf=True
		if log==True:
			print("%d %d %d" % (lm,percentlow,halfave))
		# check first 10 lines to see if coverpage Memo
		if (lm>10 and percentlow>30 and halfave<3):
				tophalf=True
				# checkMemo(mainlist,log)
		if total<50 or tophalf==True or ave<3 or percentlow>75:
			if log==True:
				print("Coverpage")
			return True
		else:

			if flagged==True: 
				ave=float(total/lm)
				percentlow=float(lowcount/lm*100)
				print("False negative:")
				print(text)
	return False



# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
print(args)
# if this is run as the top-level stand-alone program with 1 parameter
if (args==2 and __name__ == '__main__'):
	nbname=sys.argv[1]
	# request=sys.argv[2]
	if len(nbname)!=0:
		# remainder is optional for now:
		#
		nameonly,suffix=nbname.split('.')
		if (suffix=="docx"):
			print("Review file name is "+nbname)
			reportResult(nbname,True)
		else:
			print("This program requires .docx filename and search word i.e. python3 findphrase.py myfile.docx GST")
			print("Case sensitive.  Include phrases in quotes.  Use ? to findall")
	else:
		doError()