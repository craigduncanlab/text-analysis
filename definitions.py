import sys
import review # this uses xmlutil as well

# a utility function that works with the review.py
# inputs: 
# runs review.py with the chosen docx (legal) document
# 
def main(nbname):
	print("Review file name is "+nbname)
	plist=review.getParaList(nbname)
	dlist=review.getDefsList(plist)
	print("Finished")

# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
# if this is run as the top-level stand-alone program with 1 parameter
if (args==2 and __name__ == '__main__'):
    nbname=sys.argv[1]
    #request=sys.argv[2]
    if len(nbname)!=0:
        # remainder is optional for now:
        #
        nameonly,suffix=nbname.split('.')
        if (suffix=="docx"):
            main(nbname)
        else:
            print("This program requires .docx filename and search word i.e. python3 definitions.py myfile.docx")
    else:
        doError()

# request="The Lessee must"
# findphrase(sentencelist,request)
# # lower case is in middle of sentence
# request="the Lessee must"
# findphrase(sentencelist,request)
# printsentence(sentencelist,531)
