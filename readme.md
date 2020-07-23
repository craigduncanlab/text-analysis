# Legal document review tools

(c) 2020 Craig Duncan

A set of software tools (work in progress) for data analysis (content) of legal docx contents.

The aim is to treat Word (docx) files as a legacy file format and prepare tools that can extract and then work with the content in a more intelligent, data-orientated way.

The front end scripts are used with engine apps review.py and xmlutil.py

# Instructions for front-end tools:

run as (separately):

python3 findphrase.py filename.docx "search phrase"

python3 definitions.py filename.docx

python3 stats.py filename.docx 

python3 findclause filename.docx clausename

python3 findclause filename.docx ?  <---- find all clauses
