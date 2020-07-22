# Review.py is a python utility to explore text in legal docx files
# This version started 5.12.2019, with a few minor tweaks 18-19 July 2020
# 
# Craig Duncan (c) 2019-2020
#

import xmlutil
import sys # for processing command line args
import codecs # to write in utf8
from collections import deque

# Global WayPoints
global defStartPara
global BodyParas
global DefParas

# Functions

def makeContiguous(thispara):
    # print ("Trying to make this contiguous:")
    # print(thispara)
    # make para contiguous text
    output="" 
    stop = len(thispara)
    # print("in makeC, length:"+str(stop))
    newstart=0
    starttag="<w:t"
    starttagend=">" # to allow for insertion of attributes (Word). 
    endtag="</w:t>"
    while newstart<=stop:
        sindex=thispara.find(starttag,newstart,stop) 
        test=thispara[sindex+len(starttag):sindex+len(starttag)+1]
        if test==starttagend or test==" ":
            sindexend=thispara.find(starttagend,sindex,stop) 
            gap=sindexend-sindex
            findex=thispara.find(endtag,newstart,stop)
            # whenever we find end tag we capture internal w:t tags text
            if (findex!=-1):
                thistext=thispara[sindex+gap+1:findex]
                output=output+thistext
                newstart=findex+len(endtag)
            else:
                newstart=newstart+1
        else:
            newstart=newstart+1
    #print("new contig output:"+output)
    return output

# input args: no help to algos on the style names
# If necessary, could use styleprefix="Heading" as default for a legal doc
# output: returns contiguos para text and useful attributes:
# [item,style,words,sentences,index] 
# index is count of paragraph from start of paralist
# index can be used for navigation later
def openfilestyles(filepath):
    #myoutput=xmlutil._getZipInfo(filepath)
    #print(myoutput)
    result=[]
    myfile=xmlutil.getDocxContent(filepath) #finds this in xmlutil
    # the OpenOffice XML contained in the docx document.xml
    print("OOXML opened")
    paralist=xmlutil.getParasInclusiveStyle(myfile) # may need getParasGeneral for .doc or converted .doc
    result = getParaWithAttributes(paralist) #includes make contiguous function call
    return result

# function to compress paragraphs into sentences where appropriate and use this in place of OOXML
# That is, a 'sentence' is the grammatical sentence, not the multi-line version that OOXML splits
# into paragraphs with each semi-colon or colon.
# TO DO: retain reference to original OOXML start/end paras and include the paras in the new list
# input: [newitem,style,words,sentences,index,mchars,molevel,pbreak,sbreak] 
def getSentenceObjects(myLines):
	startwindow=0
	stop = len(myLines)
	linecount=0
	sentence=""
	sbreakflag=0
	sentencelist=[]
	firstline=0
	lastline=0
	for x in myLines:
		text=x[0]
		style=x[1] #choose style of the first line.
		words=x[2]
		pbreak=x[7]
		sbreak=x[8]
		first=text[:1] 
		last=text[-1:]
		last2=text[-2:]
		last3=text[-3:]
		last4=text[-4:]
		last5=text[-5:]
		isnum=last.isnumeric()
		# setflag for this 'sentence'
		if (sbreak==1 and sbreakflag==0):
			sbreakflag=1
		# like a title line
		if (first.isupper()==True and last!="," and last!=":" and last2!=": " and last!="." and last !=";" and last2!="; " and last2!="or" and last3!="and"):
			firstline=linecount
			if (lastline==0):
				lastline=firstline
			mchars=len(text)
			if (mchars>0): # only if there are some characters, test if a split in words
				words = len(text.split(' '))
			sentences=len(text.split('.'))
			sentence=sentence+text
			record=[sentence,style,words,sentences,firstline,mchars,0,pbreak,sbreakflag,lastline]
			if (len(sentence)>0):
				sentencelist.append(record)
				sentence=""
				sbreakflag=0
				firstline=0
				lastline=0
		# Why not append x here?
		else:
			if (first.isupper() and last=="."):
				firstline=linecount
				lastline=linecount
				#
				mchars=len(text)
				if (mchars>0): # only if there are some characters, test if a split in words
					words = len(text.split(' '))
				sentences=len(text.split('.'))
				sentence=sentence+text
				record=[sentence,style,words,sentences,firstline,mchars,0,pbreak,sbreakflag,lastline]
				if (len(sentence)>0):
					sentencelist.append(record)
					sentence=""
					sbreakflag=0
					firstline=0
					lastline=0
			else:
				if (first.isupper() and last==":" or last2==": "):
					if (last==":"):
						text=text.replace(":",": ")
					firstline=linecount
					lastline=linecount
					sentence=sentence+text # doesn't remove end chars yet
				else:
					if (len(sentence)==0 and len(text)>0):
						firstline=linecount
						lastline=linecount
					if (last=="."):
						sentence=sentence+text
						lastline=linecount
						#
						mchars=len(sentence)
						if (mchars>0): # only if there are some characters, test if a split in words
							words = len(sentence.split(' '))
						sentences=len(sentence.split('.'))
						record=[sentence,style,words,sentences,firstline,mchars,0,pbreak,sbreakflag,lastline]
						if (len(sentence)>0):
							sentencelist.append(record)
							sentence=""
							sbreakflag=0
							firstline=0
							lastline=0
					else:
						if (last==";"):
							text=text.replace(";","; ")
						if (last5=="; and"):
							#print(sentence)
							#print(text)
							#print(last5)
							#exit()
							text=text.replace("; and","; and ")
						if (last4=="; or"):
							text=text.replace("; or","; or ")
						if (len(text)>0):
							sentence=sentence+text
							lastline=linecount
		
		#sentence=sentence.replace("; and"," and ")
		#sentence=sentence.replace("; or"," or ")
		#sentence=sentence.replace(";",",")
		#sentence=sentence.replace(":"," - ")
		linecount=linecount+1
	#output results to console
	for s in sentencelist:
		print(s[0])
	return sentencelist




# Input: Takes para info (XML text,style,index,olevel,pbreak)
# makes the para text contiguous
# adds word, sentence information
# moves index data to end of each record
# Output: returns array with these lists: [newitem,style,words,sentences,index,mchars] 
def getParaWithAttributes(paralist):
	result=[]
	for item in paralist:
		#print(item[0])
		newitem = makeContiguous(item[0])
		style=item[1]
		index=item[2]
		mchars=len(newitem)
		molevel=item[3]
		pbreak=item[4]
		sbreak=item[5]
		words=0
		if (mchars>0): # only if there are some characters, test if a split in words
			words = len(newitem.split(' '))
		sentences=len(newitem.split('.')) # doesn't care about other punctuation for now
		stats=[newitem,style,words,sentences,index,mchars,molevel,pbreak,sbreak] 
		result.append(stats)
		# print(newitem)
	#print(result)
	return result

# open file, obtain OOXML paragraphs, convert to sentences
def getSentenceList(filepath):
	myparastats=openfilestyles(filepath) # myparastats = text,style,wordcount,index
	sentencelist=getSentenceObjects(myparastats)
	doSentenceAnalysis(sentencelist)
	return sentencelist

# myparastats = text,style,wordcount,index
def getParaList(filepath): 
	myparastats=openfilestyles(filepath) 
	return myparastats

def getRollAve(sentencelist):
	rollave=[]
	rollave=getRollingWordDensity(sentencelist)
	return rollave

def doSentenceAnalysis(sentencelist):
	rollave=getRollAve(sentencelist)
	# test analsis for the 'rlease.docx'

	#---- these are all analysis where we also use rollave
	print("---====DIVISION ANALYSES===---")
	print("---Analyse the main divisions in the document---")
	coverpage_analysis(rollave)
	body_analysis(rollave,10)
	title_analysis(rollave)
	print("----roll those density dots-------")
	rolldensitydots(rollave)
	

def printsentence(myList,index):
	stop=len(myList)
	if (index<stop):
		print("%d:%s" % (index,myList[index]))

def printpara(myList,index):
	stop=len(myList)
	if (index<stop):
		print("%d:%s" % (index,myList[index]))

# inputs: for measuring paras: about 7
# for measuring sentences: about 
def body_analysis(rollave, threshold):
	print("---BODY ANALYSIS---")
	print("----Filter doc for high word density---")
	filterlist=[]
	for item in rollave:
		density=item[3]
		if (density>threshold):
			filterlist.append(item)
	divisionanalysis(filterlist)

def title_analysis(rollave):
	print("---TITLE ANALYSIS---")
	print("----Filter doc for high word density---")
	filterlist=[]
	for item in rollave:
		density=item[3]
		if (density<10):
			filterlist.append(item)
	print(filterlist) #text,style,index,density
	#exit()
	divisionanalysis(filterlist)

# input rollave with # item,style,index,density,words,chars, outline level
# low density region, with normal style, words less than 8.  capture it for now
# NB structural analysis is a good filter:
# this will retrieve isolated, low density sections that we can further subdivide
def coverpage_analysis(rollave):
	print("---COVERPAGE ANALYSIS---")
	print("----Filter doc for high word density---")
	filterlist=[]
	for item in rollave:
		tester=item[0][0:4]
		#if (tester=="COMM" and item[1]!="TOC1"):
			#print(item)
			#exit()
		#text=item[0]
		style=item[1]
		prefix=style[0:3]
		#index=item[2]
		density=item[3]
		words=item[4]
		#if(style=="TOC1"):
		#	print(prefix)
		#	exit()
		if (density<8 and words<8):
			# can we rely on title names? or just word count?
			#if (style=="Normal" or style=="Title" and words<8):
			if (prefix!="TOC"):
				filterlist.append(item)
	print(filterlist) #text,style,index,density
	#exit()
	divisionanalysis(filterlist)

def TOC_analysis(rollave):
	print("---TOC ANALYSIS---")
	print("----Filter doc for low word density---")
	filterlist=[]
	for item in rollave:
		density=item[3]
		words=item[4]
		style=item[1]
		prefix=style[0:2]
		if (density<5 and words<12):
			# can we rely on title names? or just word count?
			#if (style=="Normal" or style=="Title" and words<8):
			if (prefix=="TOC"):
				filterlist.append(item)
	print(filterlist) #text,style,index,density
	#exit()
	divisionanalysis(filterlist)


# inputs: rollave is a list of word density, text, paragraph index
# inputs: filtered
# [mtext,mstyle,mindex,density,mwords,mchars,molevel,pbreak,sbreak]
def divisionanalysis(filterlist):
	divisions=[]
	gap=10 # I used 5 when checking paragraphs not sentences
	print("---Checking divisions---")
	count=0
	min=0
	prev=0
	for p in filterlist:
		index=p[2]
		pbreak=p[7]
		sbreak=p[8]
		print(index)
		if (min==0):
			min=index
		if (index>0):
			if (index-prev>gap or sbreak==1): #break on every 'section break'
				divisions.append(index) # record any breaks in para flow (jumps)
				prev=index
			else:
				prev=index
	print("---Reporting index numbers of divisions---")
	print("Number of divisions: %d" % len(divisions))
	for div in divisions:
		print (div)
	divcount=0
	masterlist=[]
	currentdiv=[]
	stopindex=0
	if len(filterlist)>0:
		stopindex=filterlist[len(filterlist)-1][2]
	marker=0
	#make division lists ready for markup
	for p in filterlist:
		index=p[2]
		if (marker!=stopindex):
			marker=divisions[divcount]
		if (index<marker):
			text=p[0] #[mtext,mstyle,mindex,density]
			style=p[1]
			index=p[2]
			store=[text,style,index] # loses density?
			currentdiv.append(store)
			print(store)
		#print(currentdiv)
		if (index==marker):
			print("---division break %d at %d ----" % (divcount,marker))
			print()
			print()
			print(index)
			if(len(currentdiv)>0):
				masterlist.append(currentdiv)
				currentdiv=[]
			if (divcount<(len(divisions)-1)):
				divcount=divcount+1 
			else:
				marker=stopindex
		#print(p)
		#currentdiv.append(p)
	dc=1
	for y in masterlist:
		print("-------div---------")
		fname="masterlist_div"+str(dc)
		print(fname)
		#print(y)
		convertToMarkdown(y,fname) # each y is a currendiv list of paragraphs.  Performs save?
		dc=dc+1

# A second set of tests and navigation functions
# 1. styleanalysis() provides statistics about the use of styles in the document
# 2. Paragraph navigation test is based on jumping between headings, which in turn is based
# on a 'heading test' function called testheading() that uses some indications of what a heading looks like
# i.e. lack of punction, short line length etc.
# it tests if it can define the range of each 'paragraph' block
def stylestats2(myparastats):
	print("! Style analysis:")
	styleanalysis(myparastats)
	
def navigationTest(myparastats):
	print("Testing paragraph navigation:")
	start=0
	# better than range because range uses an immutable list
	#iterative
	while(start<len(myparastats)):
		start=nh(myparastats,start)
		#print("n: %d x: %d" % (n,x))
	#
	start=len(myparastats)
	while(start>0):
		start=ph(myparastats,start)
	start=18 #why?  This must be an integer, not float
	for i in range(0,4):
		start=np(myparastats,start)
		printPara(start,myparastats)
	for i in range(0,2):
		start=pp(myparastats,start)
		printPara(start,myparastats)
	start=nh(myparastats,start)
	printPara(start,myparastats)

	#
	# NB: if DefParas[0]>BodyParas[0] it's because first recognised 'definition' is after clause title
	#ScheduleSearch(myparastats,DefParas,BodyParas)
	# TO DO: confine to outside the body paras etc
	#getSentenceDensity(myparastats) 

def headingsToMarkdown(myparastats):
	result = getheadingsstyle(myparastats) # subset of all paras that pass the heading test
	# convertToMarkdown will write data to file as well as convert to Markdown.
	convertToMarkdown(result,"demo3") # Only writes headings to docx at this stage

def docxToMarkdown(filename):
	filepath=filename+".docx"
	myparastats=openfilestyles(filepath)
	parasToMarkdown(myparastats,filename)

# convert paras to markdown
def parasToMarkdown(myparastats,filename):
	convertToMarkdown(myparastats,filename) #the whole document as markdown

# A rolling word density index (biased forward) with a threshold density
# output: array with # item,style, index,density,words,chars outline level
def getRollingWordDensity(myparastats):
	
	startwindow=0 #-3,9
	endwindow=6
	stop=len(myparastats)-(endwindow-startwindow)
	rollave=[]
	#for u in range(0,4):  
	#	pairme=("Not found","Indent1",u,0) #text,style,index,density
	#	rollave.append(pairme) # first few entries no average
	count=0
	for line in myparastats:  # these will be sentences if that is the supplied list
		mtext=line[0]
		mstyle=line[1]
		mwords=line[2]
		msent=line[3]
		mindex=line[4] # this is merely the start line in OOXML file, not whole 'sentence' index
		mchars=line[5]
		molevel=line[6]
		pbreak=line[7]
		sbreak=line[8]
		if (count<stop):
			density=worddensity(count,myparastats)
			pair=[mtext,mstyle,mindex,density,mwords,mchars,molevel,pbreak,sbreak] # item,style, index,density,words,chars outline level
			rollave.append(pair) # avewords
			count=count+1
	rolldensitydots(rollave)
	return rollave

# sentence counts average over several lines to give rolling ave sentence 'rolling' density
def worddensity(index,myparastats):
	#print("SENTENCE WORDDENSITY CHECK")
	EOLC="\r\n"
	startwindow=0 #-3,9
	endwindow=6 # less means sharper drop off at end
	stop=len(myparastats)-(endwindow-startwindow)
	if (index+endwindow<stop):
		stop=index+endwindow
	wc=0
	for sentenceindex in range(index,stop):
		line=[]
		line=myparastats[sentenceindex]
		#linetext=line[0]
		words=line[2]
		wc=wc+words
	density=wc/(stop-index) 
	return density

def getSentenceRollAve(myparastats):
	print("SENTENCE DENSITYCHECK")
	EOLC="\r\n"
	start=4
	stop=len(myparastats)-12
	rollave=[]
	for u in range(0,3):
		pairme=(0,"")
		rollave.append(pairme) # first few entries no average
	for line in myparastats:
		linetext=line[0]
		#words=line[2]
		#print(line)
		index=line[4]
		sentcount=0
		block=""
		if (index<stop):
			# limit the lookback range,but take a few more in front
			for x in range(-3,9): # tried average 5 behind, 5 in front.  Test for accuracy
				line2=myparastats[index+x]
				text=line2[0]
				sentences=line2[3]
				# print(sentences)
				sentcount=sentcount+sentences
				block=block+EOLC+text
			#density=sentcount/12
			density=sentcount/6 #(this is only half the number of samples)
			pair=[density,linetext]
			rollave.append(pair) # avewords
	return rollave

# Alternative rolling average
# sentence counts average over several lines to give rolling ave sentence density
# the range (-3,9) is the effective 'window' over which average is taken for this value
def getSentenceDensity(myparastats):
	rollAve=getSentenceRollAve(myparastats)
	rolldensitydots(rollave)
	
# input: list structure is [mtext,mstyle,mindex,density,wordcount]
# output: the output is a series of stats, for each line:
# [list item count/index,(density index) dots to indicate density | [style], [outline level], [pagebreak],[sectionbreak],[textt],[wordcount],[mchars]))
def rolldensitydots(myList):
	print("---Rolling word/sentence density---")
	count=0
	for p in myList:
		#print(p)
		#exit()
		#print(p)
		t2=p[0]
		textt=t2[0:15]
		style=p[1]
		index=p[2]
		d2=p[3]
		di=int(d2)
		wc=p[4]
		mchars=p[5]
		olevel=p[6]
		pbreak=p[7]
		sbreak=p[8]
		dots=""
		for i in range (0,di):
			dots=dots+"."
		#if (di>100):
		print("%d/p:%d(%d):%s | [%s][ol:%s][pb:%d][sb:%d] %s (%s)(%s)" % (count,index,di,dots,style,olevel,pbreak,sbreak,textt,wc,mchars))
		count=count+1

# Value for paragraph is 'on' when rolling density meets a threshold ave word count (e.g. 8)
# This is pretty effective as a filter for which paras are part of the main clause 'body' or regions like "RULES" or "GUIDES" that are incorporated into document.
# If title page is present before main body of document, forms a convenient 'division' marker
#
# Takes rolling densitycheck with average over (-3,9) backward or forward of present position
# Then filters that so that if ave density index is <8, shows 0, otherwise shows an 'on' value (e.g. 4)
# Probably >98% accurate in defining the 'clauses' section just on word count alone.
def rolldensitydotsbinary(rollave):
	print("---Rolling word/sentence density binary---")
	#print(rollave)
	count=0
	for p in rollave:
		d2=p[0]
		di=int(d2)
		t2=p[1]
		dots=""
		tt=t2[0:15]
		if (di<8):
			dots="."  # off value
		else:
			dots="...." # on value
		print("%d:%s | %s" % (count,dots,tt))
		count=count+1


def wordcountdots(myparastats):
	print("---Word counts---")
	#print(rollave)
	count=0
	for p in myparastats:
		txt=p[0][0:15] # text,style,words
		index=p[2]
		wc=int(p[4]/5)
		dots=""
		for i in range (0,wc):
			dots=dots+"."
		print("%d/%d:%s | %s" % (count,index,dots,txt))
		count=count+1

def wordcountbinary(myparastats):
	print("---Word counts binary---")
	#print(rollave)
	count=0
	for p in myparastats:
		txt=p[0][0:15] # text,style,words
		wc=int(p[2])
		dots=""
		if (wc<3):
			dots="."
		else:
			dots="....."
		print("%d:%s | %s" % (count,dots,txt))
		count=count+1


def lowrolldensitydots(rollave):
	print("---Low Rolling word density---")
	#print(rollave)
	count=0
	for p in rollave:
		d2=p[0]
		di=int(d2)
		t2=p[1]
		dots=""
		for i in range (0,di):
			dots=dots+"."
		if (d2<11): # i.e. low density index.  Need to pick a threshold that discriminates (ML)
			print("%d:%s" % (count,dots))
		count=count+1

def lowdensitytext(rollave):
	print("---Rolling word density text---")
	#print(rollave)
	count=0
	for p in rollave:
		d2=p[0]
		t2=p[1]
		shorttext=t2[0:15]
		if (d2<11): # i.e. low density index.  Need to pick a threshold that discriminates (ML)
			print("%d:%d (%s)" % (count,d2,shorttext))
		count=count+1
		#if (avewords>1 and avewords<8):
			#print("idx: %d this para has ave word density: %d" % (index,rollave[p]))
			#print(block)

def densitytext(rollave):
	print("---Rolling word density text---")
	#print(rollave)
	count=0
	for p in rollave:
		d2=p[0]
		t2=p[1]
		shorttext=t2[0:15]
		print("%d:%d (%s)" % (count,d2,shorttext))
		count=count+1
		#if (avewords>1 and avewords<8):
			#print("idx: %d this para has ave word density: %d" % (index,rollave[p]))
			#print(block)


# other tests to combine with density check
# read in the definitions section
# find those sections of document where the ratio of defined words to sentence length or ave density is high.

def ScheduleSearch(myparas,defp,bodyp):
	print("Paragraphs up to start of definitions:")
	for x in range (0,defp[0]):
		print(myparas[x])
	print("Paragraphs after end of clauses:")
	for x in range (bodyp[1],len(myparas)):
		print(myparas[x])

# return basic document divisions data, if required
def getDefParas():
	return DefParas

def getBodyParas():
	return BodyParas

# --- DEFINITIONS EXPLORATION (WALK THROUGH)
# Function to list all definitions found in block after the definitions heading
# Requires: Find Definition/Interpretation heading and then the blockstart,end (para indexes) to next heading
# Each paragraph is checked to see if it satisfies basic test as to whether it is a 'definition'

def getDefsList(myparastats):
	global DefParas
	defslist=[] # this will be term, text, parastart, parend,style (for now)
	stylelist=[]
	start=getDefsPara(myparastats) # Get the first paragraph for definitions or return -1 if no results
	dmin=0
	dmax=0
	if (start!=-1):
		# work with all paragraphs from definitions through to next 'heading'
		paralist= getthisheadingblock(myparastats,start)
		print("List all definitions in def heading block")
		print("------------------------------------------")
		defslist=makeDefsIndex(paralist)
		for item in defslist:
			index=item[4] #
			# some output
			printdefarray(item)
			style=item[4]
			stylelist.append(style)
		print("Unique defs: %d" % len(defslist))
		defstylemax=max(stylelist,key=stylelist.count)
		print("Max style in use: %s" % defstylemax)
		return defslist
	else:
		print("No Definitions paras found")

# helper function to print the array with the processed definitions
def printdefarray(item):
	startdefpara=item[0]
	enddefpara=item[1]
	term=item[2]
	deftext=item[3]
	style=item[4]
	print("%s : %s [%d %d] : %s" % (deftext,term,startdefpara,enddefpara,style))

# makes a list of definitions and paragraphs in main docx
# input: paralist has list of lists, with (text, style, pararef) in each item.
# output: should be a list with (start,end para refs, then the defined term, text, and style)
# TO DO: use these para refs for definitions navigation forward and back, and capturing def blocks
def makeDefsIndex(paralist):
	print("Making defs index...")
	global DefParas
	defslist=[]
	dmin=0
	dmax=0
	for item in paralist:
		text=item[0]
		style=item[1]
		pararef=item[2]
		#print("Def Paragraph %d: %s %s" % (pararef,text,style)) #pararef,text,style

		if (isDefinitionLine(text)==True):
			# print(text)
			defterm=findDefTerm(text) # break out some more of the info in this line (or following?)
			# above function will not capture subsequent paras of def yet... just first line
			startdefpara = pararef
			enddefpara = pararef # for now, end line is same as first for def para.  can use next parastart
			term=defterm[0]
			deftext=defterm[1]
			defmeta=[startdefpara,enddefpara,term,deftext,style]
			defslist.append(defmeta)
			if (dmin==0):
				dmin=startdefpara
			if (enddefpara>dmax):
				dmax=enddefpara
	DefParas=[dmin,dmax] # stores state w.r.t original document
	return defslist

# These are tests of line contents, in context of a block of text we already know is a definition block
# tests for presence of word 'means' only, not quotes
def isDefinitionLine(defpara):
	result=False
	quote="\""
	#print(defpara[0])
	text=defpara
	numquot=text.count(quote)
	meansquot=text.count("means")
	meansquot2=text.count("includes")
	# print("numquot: %d meansquote: %d" % (numquot,meansquot))
	#if (numquot>=2 and meansquot>0):
	if(meansquot<=0):
		if(meansquot2>0):
			result=True #still return true if it only has 'includes'
	else:
		result=True	
	#print("Definition line: %s Result:%s" % (defpara[0],result))
	return result

# find the definitions terms, whether it includes 'means' or 'includes'
# means has priority
def findDefTerm(defpara):
	quote="\""
	quote2="”"
	quote3="“"
	delimit="means"
	delimit2="includes"
	text=defpara
	max=len(text)
	starttext=text.find(delimit,0,max)
	starttext2=text.find(delimit2,0,max)
	endtext=max;
	if (starttext==-1):
		if starttext2==-1:
			return "Not found"
		else:
			starttext=starttext2 # use the 'includes' splitter, not 'means'
			delimit=delimit2 # use includes
		# TO DO: test for 'includes' as well
	delimsize=len(delimit)
	endtext=text.find(delimit,starttext+delimsize,max)
	term = text[starttext+delimsize:max] #slice at 'means'.  
	mydef = text[0:starttext]
	cleandef=mydef.replace(quote,"")
	cleandef=cleandef.replace(quote2,"") #other quote type
	cleandef=cleandef.replace(quote3,"") #other quote type
	cleandef=cleandef.strip() # clean whitespace both sides
	term=term.strip()
	term=delimit+" "+term
	pair = [term,cleandef]
	return pair

# In one definition scheme, a definition line should have two quotes and a 'means' or 'includes' close together
# The first step is to establish that this scheme is being used, at least once.
# Once you have done that, you can proceed
# having established that, you can capture the defined team as that between the quotes

# --- Docx exploration

# use the definitions section to help define where the clauses start
# TO DO: explore document so we can define the main content divisions intelligently
# as well as confirming type of document
def findLegalDocStart(myparastats):
	start=getDefsPara(myparastats) # for now
	if (start>0):
		start=start-1 # To ensure the definitions item itself can be found
	return start 

def getDefsStartPara(myparastats,index):
	print("Getting Defs Start Para...")
	datapair1=["definitions","definition","interpretation"]
	topic=datapair1[0] # topic name and file name
	terms=datapair1[1:]
	# junp to next heading with keywords definition or interpretation in it
	start=jumpGenericHeading(myparastats,index,terms) # will index always be zero here?
	checkstart=checkDefsList(myparastats,start)
	if (checkstart==-1):
		checkstart=checkDefsList(myparastats,start+1)
	return checkstart

def checkDefsList(myparastats,start):
	global defStartPara
	paralist= getthisheadingblock(myparastats,start)
	# print(paralist)
	defslist=makeDefsIndex(paralist)
	# print(defslist)
	if (len(defslist)>0):
		print("Found a definitions list...")
		defStartPara = start
		return start 
	else:
		return -1

# The goal is to return the para index reference within the paragraph list
# that corresponds to the definitions list
# Searching for a generic heading for definitions will return a first hypothesis
# For greater accuracy, do not accept first answer unconditionally but
# Test hypothesis (e.g. walk through definitions and count them - provided you have that function)
def getDefsPara(myparastats):
	start=getDefsStartPara(myparastats,0) 
	# Apply some rudimentary tests
	if (start>0):
		return start
	else:
		print("No definitions list found...")
		return -1 # is this okay?  Or use error code

# Explore data and output in markdown  
# input : an exploration list with a 'topic' and then the search term(s)
# the topic is itself included too?
# if the topic is found, then the text for the relevant paragraph is added to the title list.
# each found heading paragraph is supplemented by the block of text, then saved in a markdown file.
# finally, the division of the document containing these headings is defined by the start,end paras.

def exploredata(myparastats,explorationlist):
	titlelist=[]
	initstart=findLegalDocStart(myparastats)
	if (initstart<0 or initstart>len(myparastats)):
		initstart=0
	for goal in explorationlist:
		topic=goal[0] # topic name and is used for file name
		terms=goal[1:] # the list of search terms to find in the heading
		# this goes directly to the relevant heading text list, not in a sequence
		start=jumpGenericHeading(myparastats,initstart,terms)
		print(terms,start)
		# only do if match - save a file with the paragraphs that follow this heading.
		if (start>0):
			titlelist.append(myparastats[start-1][1]) #add this paragraph text to titlelist  Index value is one less
			blockj=getthisheadingblock(myparastats,start)
			convertToMarkdown(blockj,topic)
	
	expandbodytitles(myparastats,titlelist)

# takes as an input, a paragraph list and a list of heading styles (probably H1)?
# identifies the most common word heading style in use, then 
# finds all similar style paragraphs that look like headings
# it returns the full Word paragraphs, in which each heading is contained, as a list of the array items.
# also, updates the minimum and maximum 'Body Paras' for this document.
	
def expandbodytitles(myparastats,titlelist):
	print ("Explore Heading Data")
	for item in titlelist:
		style=item
		print("Style: %s" % style)
	stylemax=max(titlelist,key=titlelist.count)
	print("H1 style in use: %s" % stylemax)
	printTitleList(myparastats,stylemax)

def printTitleList(myparastats,stylemax):
	# myparastats = text,style,wordcount
	fulltitles=[]
	clmin=0
	clmax=0
	for nav in myparastats:
		style=nav[1]
		text=nav[0]
		#words=nav[2]
		index=nav[4]
		if (style==stylemax):
			if(testheading(text)==True):  #passes basic grammatical tests too
				# print(nav)
				if (clmin==0):
					clmin=index
				if (index>clmax):
					clmax=index
				fulltitles.append(nav) # to do - add index to initial data?
	print("These are the headings found:")
	print(fulltitles)
	setBodyParas(clmin,clmax)
	return fulltitles
	
# set State in case it needs to be queried
def setBodyParas(clmin,clmax):
	global BodyParas
	BodyParas=[clmin,clmax]

# --- AGENT KNOWLEDGE OF DOCUMENT

# simple AI to detect headings in a docx (legal) document
def getheadings(filepath):
	myparas=openfile(filepath)
	print(myparas)
	paralist=[]
	for item in myparas:
		check=testheading()
		if (check==True):
			count=0
			for word in words:
				if(len(word)>0 and word[0].isupper()):  
					count=count+1
					print(item)
					paralist.append(item)
	return paralist

# simple AI to detect headings in a docx (legal) document
# returns the style in use, but at this stage doesn't use that in the analysis
# TO DO (optional): after this has been done, see if the name of Style etc influences decision
# Alternatively, use main heading style as default marker of where text divisions occur.
# myparas input = text,style,wordcount,index
def getheadingsstyle(myparas):
	
	paralist=[]
	for itempair in myparas:
		item=itempair[0] # just the text not the style
		result=testheading(item)
		if(result==True):
			#pair=(itempair[0],itempair[1],itempair[2]) # no wordcount here
			#paralist.append(pair)	
			paralist.append(itempair) # append everything		
	return paralist

# --- AGENT KNOWLEDGE - Landmark clauses (e.g. those headings in a 'Lease')
# TO DO: make use of data to specify document components, avoid repetition in function.

# uses the list supplied as argument to test if definition topics and associated words are present
def isGenericTitle(myText,myList):
	# mylist=["goods and services","GST"]
	for x in myList:
		if (myText.lower().find(x.lower())!=-1):  # lowercase test.  Any word in list gives True
			return True
	return False

# simple iteration of a dictionary item returns the key, not value
def getDictList(myDict):
	mylist=[]
	for p in myDict:
		mylist.append(p)
	#print(mylist)
	return mylist

# -- AGENT KNOWLEDGE ACQUISITION

# A function to grab all paragraphs between two paragraphs identified as 'headings' (no keywords required)
# returns text, style, para number
def getthisheadingblock(myparastats,n):
	outputdata=[]
	nextheading=nh(myparastats,n)
	x=n-1
	print("Getting heading block:")
	while(x<nextheading-1):
		x=np(myparastats,x)
		text=myparastats[x-1][0]
		style=myparastats[x-1][1]
		words=myparastats[x-1][2] # words
		pararef = x
		pair = (text,style,pararef) # text and style
		outputdata.append(pair)
		#print("Paragraph %d: %s" % (x,myparastats[x-1][0]))
	return outputdata

def printPara(x,myparastats):
	print("Paragraph %d: %s" % (x,myparastats[x-1][0]))

# --- DOCX PARA NAVIGATION ----

def jumpnextdefheading(myparastats,n):
	max = len(myparastats)
	for x in range (n+1,max):
		text = myparastats[x-1][0]
		if (isDefinitionTitle(text)==True and (testheading(text)==True)): # re-processes text.  TO DO. Store heading category
			#print("Paragraph %d: %s" % (x,myparastats[x-1][0]))
			return x
	return max

def jumpnextjurisheading(myparastats,n):
	max = len(myparastats)
	for x in range (n+1,max):
		text = myparastats[x-1][0]
		if (isJurisdictionTitle(text)==True and (testheading(text)==True)): # re-processes text.  TO DO. Store heading category
			# print("Paragraph %d: %s" % (x,myparastats[x-1][0]))
			return x
	return max

def jumpnextGSTheading(myparastats,n):
	print("Getting next GST heading:")
	max = len(myparastats)
	for x in range (n+1,max):
		text = myparastats[x-1][0]
		if (isGSTTitle(text)==True and (testheading(text)==True)): # re-processes text.  TO DO. Store heading category
			# print("Paragraph %d: %s" % (x,text))
			return x
	return 0

# This function tries to find the next matching 'heading' up to the maximum paras in myparastats
# Inputs:
# list of paragraphs from OOXML
# 'n' term is the starting paragraph index of the heading term.
# the List is a list of key words (e.g. 'interpretation', 'GST' etc .  
# The first term of the list is the 'topic', but the remainder are keywords/synonyms
# Any hit for the search terms will produce a 'true result' for a Word paragraph (in any style)
# Even if keywords are found, the 'testheading' criteria must also be satisfied.
#
# The output returned is the paragraph index in the paragraph list.
def jumpGenericHeading(myparastats,n,myList):
	print("Getting next Generic heading: %s" % myList[0])
	max = len(myparastats)
	for x in range (n+1,max):
		text = myparastats[x-1][0]
		if (isGenericTitle(text,myList)==True and (testheading(text)==True)): # re-processes text.  TO DO. Store heading category
			# print("Paragraph %d: %s" % (x,text))
			return x
	return 0

# one of functions to navigate around docx by heading (after adopting a 'heading' category etc)
# jump to the next paragraph that matches a 'heading' test, or no change
# Similar to jump to generic heading, but this doesn't care to look for keywords
def nh(myparastats,n):
	#print("A jump to next heading (could be temp)")
	max = len(myparastats)
	for x in range (n+1,max):
		text = myparastats[x-1][0]
		if (testheading(text)==True): # re-processes text.  TO DO. Store heading category
			#print("Paragraph %d: %s" % (x,myparastats[x-1][0]))
			return x
	return max

def np(myparastats,n):
	max = len(myparastats)
	if n<max:
		x=n+1
		# print("Paragraph %d: %s (%s)" % (x,myparastats[x-1][0],myparastats[x-1][1]))
		return x

def pp(myparastats,n):
	max = len(myparastats)
	if n>0:
		x=n-1
		# print("Paragraph %d: %s" % (x,myparastats[x-1][0]))
		return x

def ph(myparastats,n):
	max = len(myparastats)
	for x in range(n-1,0,-1): # third parameter needed to reverse
		text = myparastats[x-1][0]
		if (testheading(text)==True): # re-processes text.  TO DO. Store heading category
			# print("Paragraph %d: %s" % (x,myparastats[x-1][0]))
			return x
	return 0

# --- GENERAL DOCUMENT ANALYSIS

def styleanalysis(myparas):
	stylesused = [] # empty list
	counts = dict()
	for item in myparas:
		txt=item[0]
		i = item[1]
		# For a full output of what text is being classified by style type uncomment this:
		#print("Style: %s. Text: %s" % (i,txt))
		#item = myparas[1] # styles info
		counts[i] = counts.get(i, 0) + 1
		if i not in stylesused:
			stylesused.append(i)
	print("Styles used:")
	print(stylesused)
	for i in counts:
		print(i,counts.get(i,0))
	#print(counts.str())
	#python 3.7+
	sortoutput=sorted(counts.items(), key=lambda x:x[1])
	print("\n\nSorted by count value:")
	for citem in sortoutput:
		print(citem[0],citem[1])
	#sorted by key
	print("\n\nSorted by key:")
	sorted_dict = sorted(counts.items(), key=lambda x:x[0])
	for sk in sorted_dict:
		print(sk[0],sk[1])
	# tell me the headings at level 1 and 2?
	# we want to construct a graph/tree that tells us which headings follow which...
	# i.e. can the machine always tell that heading 2 is lower level than heading 1?
	# i.e. does it need to check neighbours?
	# other clues - text headings have short contents.
	# the 'heading test' - rank by shortness, then by occurrence...
	print("\n\nHeading tests:")
	print("---------------")
	hcounts = performHeadingTests(myparas)
	maxheading = getFollowerMax(hcounts)

	# iterative testing of highest style successors
	mystack=deque()
	outstack=[]
	seen=[]
	mystack.append(maxheading) # do not put root heading on stack (implemented as list)
	while (len(mystack)>0):
		#fcounts=getFollowerStats(myparas,maxheading)
		node=mystack.popleft() # FIFO not LIFO like a stack
		outstack.append(node)
		fcounts=getFollowerStats(myparas,node)
		fheading = getFollowerMax(fcounts)
		for i in fcounts:
			if i not in outstack and i not in mystack:
				mystack.append(i) #put all on?
				if (outstack.count(i)>0):
					print("%s . Outstack count error:" % (i,outstack.count(i)))
		# nb the order of items on outstack tells us the sequence?
	print(outstack)

	#isRootHeadingInStats(fcounts,maxheading)
	#ffcounts=getFollowerStats(myparas,fheading)
	#ffheading = getFollowerMax(ffcounts)
	#isRootHeadingInStats(ffcounts,maxheading)
	#fffcounts=getFollowerStats(myparas,ffheading)
	#fffheading = getFollowerMax(fffcounts)
	#isRootHeadingInStats(fffcounts,maxheading)
	
def isRootHeadingInStats(myDict,rootHeading):
	mylist = getDictList(myDict)
	if (rootHeading in mylist):
		print("Reached end of clause tree")
		return True
	else:
		print("Still exploring")
		return False

def performHeadingTests(myparas):
	hcounts = dict()
	for p in myparas:
		if (len(p)>=3):
			result=testheading(p[0])
			if (result==True): # first letter capitals only
				hcounts[p[1]]=hcounts.get(p[1], 0) + 1
				print("para: %s, style: %s, wordcount: %s" % (p[0],p[1],p[2]))
	return hcounts

	
def getFollowerMax(fcounts):
	maxcount=0
	print("Follower style stats:")
	maxfollower="Not found"
	for i in fcounts:
		thiscount=fcounts.get(i,0)
		print(i,thiscount)
		if (thiscount>maxcount):
			maxfollower=i
			maxcount=thiscount

	print("Highest follower rank: %s count: %d" % (maxfollower,maxcount))
	return maxfollower

def getFollowerStats(myparas,styleheading):
	print("\n\n"+styleheading)
	print("---------------")
	fcounts=dict()
	maxparas=len(myparas)
	pcount=0
	lastmatch=0
	#for p in myparas:
	for pcount in range(0,maxparas-1):
		index2=pcount
		style=myparas[pcount][1]
		#print("maxhead: %s style for this %d is : %s" % (maxheading,pcount,style))
		if (style==styleheading):
			index2=pcount+1;  #immediately following
			stylenext=myparas[index2][1]
			#print("next style for this %d is : %s" % (pcount,stylenext))
			fcounts[stylenext]=fcounts.get(stylenext, 0) + 1
	return fcounts
	

# checks for criteria of headings - line length, grammatical ending, excluded words
# in general, we look for short lines, without punctuation
# TO DO: first find the parts of document that should contain headings (clause section)
def testheading(item):
	result=False
	words=item.split(' ')
	last=item[-5:] #last 5 chars
	nextlast=item[:-2]
	# eliminate short lines that end with these punctuation marks
	check1=":"
	check2=")"
	check3=";"
	check4="."
	check5=","
	if(len(words)>0 and words[0].isupper() and len(words)<10 and len(last)!=0):
		firstletter=words[0][0]
		if (firstletter.isnumeric()==False):
			if(check1 not in last and check2 not in last and check3 not in last and check4 not in last and check5 not in last): 
				check6 = "EXECUTED" #case sensitive checks
				check7="IP" #WP inclusions
				if (check6 not in item and check7 not in item[0]):
					result=True
	return result

def getwordcount(onepara):	
 	words=len(onepara.split(' '))
 	return words

# Currently only workds with docx paragraphs that have explicit "Heading1" style scheme
# Most suited to legal docs that use structured heading levels
# To do: the map between H1 and heading names should be flexible for each docx

def convertToMarkdown(myparas,filename):
	EOLC="\r\n"
	output=""
	style=""
	#if not already a 'new' document we can add a filename
	if (myparas[0][:3]!="-n-"):
		pair="-n-"+filename+EOLC
		output=output+pair+EOLC
	for item in myparas:
		style="#Indent1" # default
		i=item[1]
		if (i=="Heading1"):  # number one ranked heading style
			style="#H1"
		if (i=="Heading2"):
			style="#H2"
		if (i=="Heading3"):
			style="#H3"
		if (i=="Heading4"):
			style="#H4"
		if (i=="Heading5"):
			style="#H5"
		if (i=="Heading6"):
			style="#H6"
		if (i=="Heading7"):
			style="#Indent1"
		text=item[0]
		print(text)
		print(style)
		pair = text+style
		output=output+pair+EOLC
		#print(output)
	filename=filename+".lmd"
	textfile=codecs.open(filename,"w","utf-8") # utf8 needed for python2 only?
	textfile.write(output)
	textfile.close()

# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
# if this is run as the top-level stand-alone program with 1 parameter
if (args==2 and __name__ == '__main__'):
    nbname=sys.argv[1]
    if len(nbname)!=0:
        # remainder is optional for now:
        #
        nameonly,suffix=nbname.split('.')
        if (suffix=="docx"):
            print("Review file name is "+nbname)
            #openfile(nbname)
            #getheadings(nbname)
            getSentenceList(nbname)
        else:
            print("This program requires .docx filename i.e. textview myfile.docx")
    else:
        doError()