# readme2 (review.py)

Has ability to read in docx, perform analysis on headings and styles
Future goals: captioning system for parts of legal documents
Captioning system for contents of operative clauses, definitions etc. (integration of outside resources)

Capable of producing identified 'blocks' of related topics for legal clauses:
see 'exploredata()'
Will be able to use this to intelligently import docx into a database

# 9 December 2019

As at 9.12.2019 Adding agent-based exploration of document contents, using expert legal knowledge rules
## Aims: 

1. Ability for agent to 'read' a legal document much as lawyer would.

NB: An initial functional goal is ability to define the main divisions: defs, clauses, schedule etc
Objective co-ordinate/referencing system is needed for text terrains e.g. (e.g. using a master index of paragraphs) 

The advantage of this is that we know our data structures and their purposes (making explicit what was implicit)
2. To work within these divisions/data structures and act on knowledge of terms, cross-references to schedules etc.

## Classification and knowledge acquisition:

Two way processes e.g. from defs to clauses, or clauses to defs.
See 'Legal Data Book' for explanation of scientific approaches used

Use: For text-based searches/replacements that require plain, readable text.

```nb do not rely on <w:t> tag: use <w:t for opening as there are variations in those tags.  nb this is one of them: <w:t xml:space="preserve">```


# 14.12.2019

Performs series of analysis e.g. word density checks which gather more information
starts with structure and works toward detail

## USE:
Sample a docx file in this way : python3 review.py rlease.docx
It will also write the analysed file as new markdown to demo4.lmd (based on mapping to template styles)

The basic idea is that a standard markdown for style H1 etc is inserted in place of original style names

Then run shortcut.py (to be renamed md2wd) to convert that into a docx again (this time with new formatting, based on just the contig text in the md file)
python3 shortcut.py demo3.lmd

## GetFollowerMax function notes

Legal styles are generally hierarchical (i.e. in a tree structure, from H1 at root to lower levels)
Each paragraph may be followed by one or more paragraphs lower in the hierarchy.
Sometimes, change in styles are not new sentences, but are still broken into what OOXML calls a paragraph.

We can explore the 'followers' of our identified root (H1) style to see what styles are in use
and how they relate to each other.  This enables mapping them to pro-forma hierarchical styles

A Legal document can be defined as a collection of blocks that implement style 'trees'.
Within each block, the first paragraph has the root (H1) style and all subsequent paragraphs that exist as
lower levels in the style hierarchy without repetition of the root style.

There are paragraph styles (like indent) that can follow any number/style and so operate outside the hierarchy
We can detect these by looking for the fact they appear after several other heading styles.

We can 'learn' the styles in these trees by exploring the adjacent paragraphs in the document.
This is a form of machine learning, in which we use statistics to identify the most likely candidates 
for styles (without inspecting the style XML directly)
If there is a 'cycle' in any of the followers for paragraphs it means we have reached the end 
of the block.

Here's some stats (H4) showing most often followed by itself, then the higher level, then the lower
Heading4 82, Heading3 25, Heading5 7
Bare stats show proximity.  The numbers with same prefix help with ordering.

Heading/style follower style tests (node tree).  i.e. check chain, frequency of child nodes 
This assumes text para flow will be a tree starting with the first identified heading
It may also be possible to confirm by looking for 'follower' styles in docx metadata

## Deprecated density function

density check trying to assimilate sentences from paragraphs (OOXML)
deprecated in favour of working off sentence list
the density calculation is reasonably simple.  It is preferred over
word-specific divisions or content.  However, we can still acknowledge it is a Word WP environment.

To make it even more accurate we want to recognise that sentences are macro-structures
that are collections of Word 'paragraphs'.
There is no object/data structure in the .NET or Word environment that recognises this?
So we want to identify, as one object, the 'broken' paragraphs (plain english sub-paragraph breaks)
and combine them so the word density is maintained as if they were a single sentence.

One approach is just to reduce the denominator used for the average
by the number of colons or semi-colons we detect
(rather than just a sentence with colon count for numerator)
we should really have the density shared across all adjacent paragraphs in the sentence group (forward and backwards).

TO DO: fine tune the density calculation to cater for broken lines, but don't alter it too much.

def complexdensity(mindex,myparastats):
	# limit the lookback range,but take a few more in front
	print("DENSITYCHECK")
	EOLC="\r\n"
	start=5
	startwindow=0 #-3,9
	endwindow=6 # less means sharper drop off at end
	denominator=6
	wordcount=0
	ticker=0
	block=""
	for x in range(startwindow,endwindow): # tried average 5 behind, 5 in front.  Test for accuracy
		line2=myparastats[mindex+x]
		text=line2[0]
		style=line2[1]
		words=line2[2]
		pbreak=line2[7]
		sbreak=line2[8]
		# stop  - do not continue calculation across a section break/ or page break
		if (ticker>0 and (sbreak==1 )): # and ticker>0
			density=wordcount/ticker # may be less than denominator if we cut it short
			return density
		wordcount=wordcount+words
		block=block+EOLC+text
		breakflag=0
		if (text[-1:]==";" or text[-1:]==":" or text[-1:]=="." or text[-4:]==";and" or text[-3:]==";or" or text[-5:]=="; and" or text[-4:]=="; or"):
			# do not add anything to demonimator
			if (ticker<1):
				ticker=1
		else:
			if (ticker<(endwindow-startwindow)):
				ticker=ticker+1
	density=wordcount/ticker
	return density


# 19 July 2019

Checked the definition 'walk through code'

TO DO: 
Split this file into separate apps with specific functions, and use it as an OOXML processor (intermediate workflow)