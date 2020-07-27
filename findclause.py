import sys
import review # this uses xmlutil as well
# findclause - docx legal clause finder
# (c) Craig Duncan 2020
# 
# a utility function that works with the review.py
# inputs: 
# it requires generation of 'sentence list' from the docx document using review.py
# 'request' is the search phrase

def finder(paralist,request):
	count=0
	notcount=0
	print("============================")
	print("clause finder %s:" % request)
	print("============================")
	findClauses(paralist,request)


# the input argument for this function is the list of paragraphs (NOT sentences)
# the exploration list is a way of extracting clauses on particular subjects (in this case based on 
# common 'concepts' in a lease, but can be extended to a set of terms for other 'types' of document)
def findClauses(myparastats,request):
    # TO DO: convert this to CSV, JSON?
    explorationlist = getSearchList()# now go and try and find these topic clauses, extract and save as markdown file
    items=["default","default"]
    print("exploration list: ", explorationlist)
    matches=0
    for i in explorationlist:
    	if (i[0].lower().find(request.lower())!=-1):  # lowercase test.  Any word in list gives True
    		review.matchtitle(myparastats,i) # this just prints to output
    		matches=matches+1
    # if no matches just use the searchterm
    if matches<1:
    	mylist=[request.lower(),request.lower()]
    	print(mylist)
    	review.matchtitle(myparastats,mylist)
    #review.exploredata(myparastats,explorationlist) # includes output to markdown files

def findallheadingsblock(plist):
	titlelist=[]
	for i in plist:
		rank=i[-1:][0]
		if (rank>0.8): # threshold for headings
			start=i[4] # this holds the generic paragraph number.  This may not be the doc 'start' if it's before 'definitions etc'
			title=i[0]
			blockj=review.getthisheadingblock(plist,start+1)
			mytitle=blockj[0][0]
			mypair=[mytitle,rank]
			titlelist.append(mypair)
			markdown=review.simpleLMD(blockj)
			print(markdown)  # print simple block text
	for t in titlelist:
		# threshold for a heading
		if t[1]>=0.8:
			print(t[0],t[1]) 

def checkStatus():
    dp=review.getDefParas()
    bp=review.getBodyParas() # These haven't been updated?
    print ("DefParas range:%d,%d" % (dp[0],dp[1])) 
    print ("BodyParas range:%d,%d" % (bp[0],bp[1])) # from exploredata

def getSearchList():
    datapair1=["definitions","definition","interpretation"] # This is a significant one (global/metadata)
    explorationlist=[["promotion levy","promotion","levy"],["GST","goods and services","GST"],datapair1,["outgoings","outgoings"],["rent","rent","rent reviews"],["grant","grant","grant of lease"],["turnover rent","turnover"],["permitted use","permitted use","use"],["insurance","insurance","insurances"],["default","default"],["indemnity","indemnity","warranty"],["guarantee","guarantee"],["termination", "termination"],["redevelopment", "redevelopment"],["holding over", "holding over"],["option","option"],["bank guarantee","bank guarantee"],["security deposit","security deposit","security"],["Trust","Trust"],["general","general","provisions"],["assignment","assignment"]]
    return explorationlist

# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
print(args)
# if this is run as the top-level stand-alone program with 1 parameter
if (args==3 and __name__ == '__main__'):
	nbname=sys.argv[1]
	request=sys.argv[2]
	if len(nbname)!=0:
		# remainder is optional for now:
		#
		nameonly,suffix=nbname.split('.')
		if (suffix=="docx"):
			print("Review file name is "+nbname)
			#openfile(nbname)
			#getheadings(nbname)
			#get sentencelist
			slist=review.getSentenceList(nbname)
			plist=review.getParaList(nbname)
			if (request.find("?")==-1):
				finder(plist,request)
			else:
				print("finding all...")
				findallheadingsblock(plist)
		else:
			print("This program requires .docx filename and search word i.e. python3 findphrase.py myfile.docx GST")
			print("Case sensitive.  Include phrases in quotes.  Use ? to findall")
	else:
		doError()