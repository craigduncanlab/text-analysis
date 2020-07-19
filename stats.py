import sys
import review # this uses xmlutil as well

# a utility function that works with the review.py
# inputs: 
# runs review.py with the chosen docx (legal) document
# 
def main(nbname):
    print("Review file name is "+nbname)
    plist=review.getParaList(nbname)
    # dlist=review.getDefsList(plist)
    #review.doParaStats(getParaList)
    # This lease_analysis3 is specific to trying to find the parts of a lease that include certain keywords.
    # i.e. to match the parts of the file with clauses.  This is too technical, but it provides proof of concept.
    # a better way is just to grab the file data, and put it into containers of some sort.
    print("-----do lease_analysis3-----")
    lease_analysis3(plist)
    # analysis 2 is all about testing the styles applied in Word, and if that is significant
    print("----do stylestats2------")
    review.stylestats2(plist)
    print("Finished")

# the input argument for this function is the list of paragraphs (NOT sentences)
# the exploration list is a way of extracting clauses on particular subjects (in this case based on 
# common 'concepts' in a lease, but can be extended to a set of terms for other 'types' of document)
def lease_analysis3(myparastats):
    # TO DO: convert this to CSV, JSON?
    explorationlist = getLeaseExplorationList()# now go and try and find these topic clauses, extract and save as markdown file
    review.exploredata(myparastats,explorationlist) # includes output to markdown files
    dp=review.getDefParas()
    bp=review.getBodyParas() # These haven't been updated?
    print ("DefParas range:%d,%d" % (dp[0],dp[1])) 
    print ("BodyParas range:%d,%d" % (bp[0],bp[1])) # from exploredata

# ---Domain specific legal headings

# create exploration lists for agent to use: 
# effectively, this is the 'knowledge base' or 'structure' for a single document type
# TO DO: expand this to sets for other topics.
# JSON in future?
# first item in each list is topic label, rest are terms for identifying heading
# TO DO: check if guarantee and indemnity are same clause

def getLeaseExplorationList():
    datapair1=["definitions","definition","interpretation"] # This is a significant one (global/metadata)
    explorationlist=[["promotionlevy","promotion","levy"],["GST","goods and services","GST"],datapair1,["outgoings","outgoings"],["rent","rent","rent reviews"],["grant","grant","grant of lease"],["turnoverrent","turnover"],["permitteduse","permitted use","use"],["insurance","insurance","insurances"],["default","default"],["indemnity","indemnity","warranty"],["guarantee","guarantee"],["termination", "termination"],["redevelopment", "redevelopment"],["holdingover", "holding over"],["option","option"],["bankguarantee","bank guarantee"],["securitydeposit","security deposit","security"],["Trust","Trust"],["general","general","provisions"],["assignment","assignment"]]
    return explorationlist

# --- Legal figures of speech
# TO DO: use self-referencing language like "In this Deed" or "In this Lease" to help characterise the document


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
