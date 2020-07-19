import sys
import review # this uses xmlutil as well

# a utility function that works with the review.py
# inputs: 
# it requires generation of 'sentence list' from the docx document using review.py
# 'request' is the search phrase
def findphrase(myList,request):
	count=0
	notcount=0
	print("============================")
	print("%s:" % request)
	print("============================")
	for item in myList:
		sentence=item[0]
		mstyle=item[1]
		mwords=item[2]
		msent=item[3]
		mindex=item[4] # this is merely the start item in OOXML file, not whole 'sentence' index
		mchars=item[5]
		molevel=item[6]
		pbreak=item[7]
		sbreak=item[8]
		output = sentence[0:len(request)] # longer output, not used
		if (request in sentence):
			findex=sentence.find(request,0,len(sentence))
			balance = sentence[findex+len(request):]
			pretext=sentence[0:findex]
			#print(balance)
			if (mindex==0):
				print("%d: %s" % (mindex,balance))
			else:
				print("%d: %s[*%s*]%s" % (mindex,pretext,request,balance))
			count=count+1
	print("Matches: %d" % count)

# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
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
            findphrase(slist,request)
        else:
            print("This program requires .docx filename and search word i.e. python3 findphrase.py myfile.docx lease")
            print("Case sensitive.  Include phrases in quotes")
    else:
        doError()

# request="The Lessee must"
# findphrase(sentencelist,request)
# # lower case is in middle of sentence
# request="the Lessee must"
# findphrase(sentencelist,request)
# printsentence(sentencelist,531)
