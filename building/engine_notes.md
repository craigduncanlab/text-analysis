# Engine workflow:

1. Read OOXML in as paragraph objects (in an array structure), where each is returned as : text,style,wordcount,index
2. Compress OOXML paras to 'sentences'
3. Prepare rolling ave word density for those  sentences.
Different ave calcs are possible.  
Output array with item,style,index,density,words,chars outline level
4. Further downstream analyses can be done on this 'rollave' summary
5. Use these stats to differentiate different parts (divisions) of docx documents now...
This paves the way for analysis of information by 'type' (clause/definition/schedule)

# Notes on word density parameters

Why 'rolling' average used in the review.py?

Smooths out headings, short lines and enables an index value that signals the context of the paragraph
i.e. is it in a high word count region or not.

The statistic itself (with no other filters) is reasonably effective in distinguishing word count regions

We could try and pattern-match on regions, or filter the density index itself by threshold.
e.g. we may be able to detect in-document table of contents, forms and schedules (incomplete) because of low word densities

We graph it to see (see 'dots' functions).  

Learning methods: have a test region (e.g. paras with clauses) and have the threshold change until this is clearly in or out

Drop threshold down even lower (say 2 to 4) to see title page, execution clause sections etc

Latest update: 19 July 2020
