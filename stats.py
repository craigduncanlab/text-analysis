import sys
import review # this uses xmlutil as well

# a utility function that works with the review.py
# inputs: 
# runs review.py with the chosen docx (legal) document
# 
def main(nbname):
    filename=nbname+".docx"
    print("Review file name is "+filename)
    plist=review.getParaList(filename)
    # dlist=review.getDefsList(plist)
    #review.doParaStats(getParaList)
    print("-----convert docx to legal md-----")
    review.docxToMarkdown(nbname)
    #
    #print("-----do lease_analysis3-----")
    #lease_analysis3(plist)
    # analysis 2 is all about testing the styles applied in Word, and if that is significant
    print("----do stylestats2------")
    review.stylestats2(plist)
    print("Finished stats")
    review.navigationTest(plist)

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
            main(nameonly)
        else:
            print("This program requires .docx filename and search word i.e. python3 definitions.py myfile.docx")
    else:
        doError()
