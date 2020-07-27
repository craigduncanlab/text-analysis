# Data science applied to OOXML (legal documents).
(c) Craig Duncan 2020
27 July 2020

# Introduction

Data science recipes allow data to be repurposed and made more amenable to analysis, logical deductions and inferences, and database functions.

## Present Goals:

Systematic workflows for increasing the computability of a raw text format (OOXML) designed for other purposes.

OOXML + legal agreements = a specific application for data science techniques.

i.e. instead of treating OOXML as the sequential representation of an object-orientated record of rendered document state, we treat it as the basis for extracting data into a form that can be interrogated using more traditional data science techniques (and als make it more amenable to being directly manipulated by computational reasoning).

What we want to do is store the true set of data within an OOXML representation of a legal document, and data structure to organise the information within each of those containers.   The OOXML format can only represent this implicitly, and because it is not concerned with performing further data science operations on the data, it requires transformation of the OOXML format, having regard to the kind of data that is held within that format, but not aligned to it.

Recognising that OOXML is a rendering/style annotation, we want to produce a form of data storage that reflects the true nature of the data, rather than how it might be displayed.   This requires throwing off some of the assumptions that documents we see are incapably of producing data that can be stored independently, by reference to the true set of data items and their features.  We need to recognise that written languages, grammar and sentences are ways in which units of information are captured (and to the extent that OOXML does not protect or preserve that fact, repair the data that has been damaged by OOXML partitions or tagging)

There are two ways of looking at the goal: either to extract the true data from the OOXML, so that it represents the 'original' and true form of the data, which was effectively put into OOXML for rendering purposes.  ALternatively, we view it as a supplementary form of data, that takes OOXML as the original data (including style information etc), and then tries to use that to make a new database that will be needed 'downstream' of the OOXML.  There is no doubt that the programs that produce OOXML still leave traces of data that could be helpful in working with the content data in another form.  Perhaps the distinction doesn't matter, because the new form of data will be independent of the OOXML, and capable of being analysed on its own.

If this exercise is successful, and we can reverse the output so that we systematically apply styles and then convert back to OOXML, we might render the original OOXML a legacy format, or something that is only needed *after* data manipulation and analysis has occurred.

Why would we want to work on documents using data science techniques at all?  

 - It provides a useful way of confirming that we are using the actual units of data that are needed for the legal work, and not just the arbitrary units and layout that is forced on us by word processing 'typing' interfaces and 'desktop publishing' assumptions.
 - If the ingestion is automated, consistency and successful, we can start to 'read' and answer questions using computational techniques, which in effect substitute as a 'reading' workflow.  We can speak to the contents of documents using more familiar query languages and data filtering techniques, without needing to immediately be concerned with natural language processing.
 - The search for ways to extract and store relevant information will highlight the way in which human interpretation of legacy OOXML (or rendered output of OOXML) can be understood in new, data-centric ways.
 - It may enable new data formats or conventions to be developed independent of specific formats like OOXML, and based on a more universal, generic representation of the data.

# Raw data, storing as observations

## OOXML data ingestion and cleanup

Paragraphs are the base OOXML unit

When an OOXML file is loaded, you can store each paragraph as an observation (text).  The list index provides a unique reference for each row.

In data science terms, this is like creating the row/column rectangle.

You can clean up this data by interpreting the tags in the OOXML and re-arranging into sentences, contiguous text etc.

{bioinformatics analogy: preparation of the FASTQ formats from sequencing data, before downstream processing begins}

## Raw data ingestion - grammatical consistency of data

Text data from OOXML might be split across paragraphs because the paragraph has punctuation that is designed to make it look like a list (i.e. semi-colons and colon). 

The result of this is that grammatical sentences are stored in different 'observations' (paragraphs) in OOXML, even though for our data storage we might want them to be single observations, and therefore held in the same 'row' entry.

If the OOXML text data for a single sentence is converted (compressed) back into a single sentence, it means that there are fewer line breaks, and we can agree that each 'observation' in our new database will exist as a single grammatical sentence, unbroken by the OOXML paragraphs.

This decision means that statistical analysis is more meaningful, and classification can operate with common assumptions about what the data represents ('know your data')

## Functions for navigating data(base)

The stored paragraphs (raw data) can be navigated directly by index value.  {One of the basic advantages of storage of data in computer}.

# Adding derived features to the data

## Data annotation/observations from analysis (extra columns in array)

Other stats can be associated (attached to each row).

These can be obtained by data analysis of the text (raw data).

Instead of performing an analysis, or functional transform as and when needed, the 'raw data' can be expanded by adding the additional data analysis as new columns (categories) for each row entry, knowing that they can be used later.

## Raw data/features

OOXML data's raw features, as ingested, might be limited to the text, the indent level, and the style applied.  This is not fixed but that is a useful start.

## Storing derived feature data as if raw data in the database

Calculations can be performed on the raw data which produces new data.  Storing these additional calculations as intermediate data (i.e. as if attached to the raw data, permanently) can be useful for simplying the other functions we want to write.  We can describe these as derived 'features' (derived quantities or observations).  They represent functions of the raw data, but it is convenient to store the results so that they can be used.   

Adding additional derived features as observation data with the raw data, is useful in that we can enrich the data used for later data analysis or functions.  This form of 'data-orientated' workflow enables higher-level reasoning about transformed raw data. 

If the additional observations are derived from the original data (i.e. statistical analysis etc) and other known data sets, then there are no other dependencies that require run-time calculations to expand the raw data.  The expansion of columns could be done at the same time as the data is loaded in/ingested.

For example, calculating ranking/probability scores (classifiers) for certain features of the raw data and storing them with each row enables that data to be used as a basis for navigation, filtering etc.

## Useful derived features for OOXML

Useful statistical analysis includes

 - word counts
 - word density etc. 
 - probability of the raw text being a heading or some other human-readable feature.

 This helps to reason about what the text 'looks like', or the nature of the sentences even if we don't have access to the actual rendering program (i.e. the word processor). 

# Database

## Indexing

The original OOXML indexing is important to allow contiguous data rows to be extracted/filtered as needed (data blocks = sets of rows and observations).  Having an index preserves sequence.

## Expanded database

The exanded observations (features) when stored in arrays in-memory are, in effect, the basis for an expanded row/column database.  This expanded database is now the base information that we can interact with and query for statistical and text analysis.

It is also now in a form that can be stored in a rectangular database, or even manipulated with the R program and R Studio.

# Queries

By ingesting the data in a way that ensures like data is stored with like data, and different features are associated with the text, we have a basis for querying the original document using traditional data science and database techniques.

Data navigation is performed on a consistent in-memory representation of the data, which preserves the original sequence of the data, but allows us to access it independently of that sequence.  In particular, having data indexed as observations frees us from the need to navigate through the sequential length of text in the file, or to try and navigate only with reference to human-readable landmarks.  We can jump ahead to data with particular features, or filter the data in order to list the data we want.

This frees us from crude dependencies on word 'search', and allows a far more quantitative and precise approach to 'learning' to find useful features of the text.   

We may also be able to utilise some more traditional database programs, or even SQL, having now converted a traditional text document into something with both an index for data containers

# Advanced queries

Having stored a single document this way, it is natural to ask if we can store multiple documents and then perform queries across the whole of the in-memory representation.

Writing sort functions, and re-arranging lists in order, with python and SQL, will be useful knowledge to have for other applications.


