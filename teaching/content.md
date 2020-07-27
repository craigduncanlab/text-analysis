# Computational legal document content and data management

(c) 2020 Craig Duncan

This note explains why I think that management of the specific content in legal documents is going to pave the way for the next big shift in legal tools, for both lawyers and customers/clients. It requires acknowledging that Word Processors are ill-suited to anything more than basic data management of legal content and that a new paradigm is needed.

For enquiries about the use of this material or for presentations contact software@craigduncan.com.au.

# Traditional drafting

The process of drafting legal documents probably only matters to those who are in the business of making legal documents, and want to think about them intelligently. Some large firms have dedicated precedent lawyer roles. The senior lawyers who then want to prepare documents for clients will use these templates, but with the intention, in many cases, of delegating the drafting work to more junior lawyers. They want to use the templates so that they don’t have to explain everything in detail, and any variations will be minimal. Even with a degree of independence given to the junior lawyer, instructions might be simplified to something like this:

> Here’s a template, copy the structure and make what amendments you think you need. Check your clauses match the clause library, and make sure you’ve got all the definitions that are needed.

Templates might be written with preparation or use notes, but often not on the assumption that you want to take a higher-level, more generic approach to contractural drafting.

Most law schools do not spend a great deal of time on practical instructions like drafting contracts and they know that the precedent books and law office templates exist anyway. They focus on the meta-data that exists as contract law – the rules that tell you what a contract is – its essence, and whether it exists, and for how long. In so doing, they tend not to focus on the recipes (algorithms) needed to do any drafting.

Once we start to think about the contents of legal documents as data, we might want to know what algorithms the lawyers (experts in their domain) actually use to work with legal information. We can’t just ask them how they use Word Processors, because that just described how they fit the tools they are given. Lawyers adopted ‘desktop publishing’ tools when they moved from secretarial assistance to their own desktop computers and the use of the ‘word processors’. But that’s not how they work with the content in their minds.

# Contracts as template documents

Contract drafting is a bit like following a recipe. The basic approach to writing these documents (according to some unspecified recipe) is, however, quite different to how the results are stored. The results are the finished work, in a fairly rigid and static form. Lawyer’s templates come from an age where paper was used, and paper isn’t an interactive medium.

Templates are not just single examples of work, that do not connect to anything else. Templates, particularly the conventional electronic word processor files are:

 - high-frequency data containers that form the mainstay of both legal business and the contract management function in large organisations.
 - tools for answering questions about legal topics. They need to be read and used by reading in different ways
 - data containers that might need to add or subtract content. They may need to be customised depending on the purpose, and who is using them.
 - data containers that need to be updated when the law changes.
 - created using a recipe for the content, and using expert domain knowledge.
- data containers that have some content in common with other templates.
- intended to be read interactively and in a non-linear way by people.
- part of the knowledge base for firms that work with legal agreements.
- based on knowledge of the law, and decisions about drafting.
- captured knowledge which may itself reflect implicit knowledge that needs to be passed on to other drafters or users.

If these are electronic documents, there is no reason why they shouldn’t be able to store data in intelligent structures, and permit computation that assists with how they are to be used.

# Who cares about these templating concerns?

I believe customers and lawyers will care a lot when they see the advantages of moving on from Word Processors to store legal information, and start using computers intelligently to store, analyse and modify document content, including meta-data. For the first time, they will be working with data that is stored in a way designed for computation and manipulation, and not in passive templates.

The paradigm shift is to attempt to work with document contents as the primary data, in a way that separates data from code or markup(styling), and allows intelligent programs that can manipulate that data directly.

Styles can be applied to data for output purposes, but they should not define the data. The data should not be referenced indirectly, for example by where or in what format, heading level or style it appears in a Word Processing document file format. The mapping of styles to ‘heading levels’ still does not define individual units of data in an unambiguous way, where they can be referenced and manipulated independently.

# General disadvantages of Word processing software

The ‘Word Processing’ software is a legacy item of software, but it is still perceived as the foundation of legal software tools. This view will need to change.

Surprisingly, word processors in current software aren’t much different than paper, if you think about how non-interactive they are. It only seems there is a lot of interaction, but this tends to be about key-presses needed to get input and output done.

- They amount of typing (individual alpha-numeric key-strokes) that is needed for input/interaction when using a word processor is huge compared to the benefits of some other interactive computing function that acts as a time-saver, or manipulates data in some way. {To do: quantify this. Most likely there will be thousands of words, tens of thousands of keystrokes that surround a few menu selections} Even the ubiquitous search function is often used only as a means to facilitate further key-strokes or changes to individual parts of text.
- The Word Processors that are used to store templates in specific document files were never designed as diverse knowledge repositories. They were not designed in a way that different types of content could be classified and hidden easily (e.g notes, comments), or extracted as individual blocks, or used across different documents.
- It’s not the best approach to assume that external document management systems, that try and store individual documents in word-processor formats, with meta-data, can overcome the lack of attention to document contents. This approach fails to provide any real ability to work with document contents as the primary data.
- There is still a close connection between the physical disk file that stores a document and the document as a ‘record’.
- It’s not in the design assumptions for individual documents to all exist in some kind of in-memory database.
- It’s not part of the design assumptions to link information for use cases of one or more documents (like letters, and legal documents), that can be saved and retrieved.
- If the software allows in-text notes, or notes that were themselves capable of data analysis, they’d still be stuck inside a single document, that is loaded up on a case by case basis.
- Notes and comment ‘bubbles’ are still very much inserted into a document on the assumption that the document is a stand-alone creation.

We are going to need to understand how documents are put together in terms of content, not in terms of just some simply styles or templates. We are going to need to think about how the content of multiple documents can co-exist in an in-memory database, not just in separate files on a disk. We are going to need to know how to extract data from legacy formats (the current Word Processors), in order to efficiently work it into new databases and data file formats.

# Algorithms in legal drafting

The algorithms for drafting, if we are to speak about them intelligently, will also need words for the units of data or information that we are manipulating, whether it be contract clauses, or definitions, or quantitative information. We shouldn’t be writing custom code for a single document and its unique contents – we should be acquiring conceptual tools to help us write programs that separate data and code, and allow us to work across many similar documents, or identify why they are unique.

Legal drafting is easily amenable to a more theoretical abstract model, if you start with a different set of questions, like – how do I go from inputs to outputs, when I do the drafting? What instructions are needed? How is information transformed? Which information is capable of being treated as a ‘unit’ of information etc.

Those who are more interested in abstract models of the content of documents (software developers, especially for document creation), haven’t had the benefit of thinking about it in terms of the subject matter (law) and subject matter expertise. As a result, contract drafting and legal automation tools tend to focus on stylistic elements, rather than content.

# Workflow disadvantages when using Word processors

Word processors were always about single documents, not bulk data management and analysis. Documents are labelled and stored in document libraries, as if each is a unique book. There are databases that handle document management by providing ‘meta-data’, but because the data is held in Word Processor formats, it isn’t easily accessible for specific content data analysis. The meta data might have to be inserted manually too.

Even in this ‘desktop publishing’ environment, the labour-saving tools in Word Processors (e.g changing font, or style) are themselves manual tools. The tools do not provide a user with much ability to apply sophisticated data analysis tools to the content of the document, or its structure. Mental effort is always needed (and subject matter expertise is non-existent). The result is also something that is held in the same form for both input and output.

What if you want to work smarter with all your documents, and not craft each one as if it existed in its own box? It’s very easy for people to accept the only option (cut and paste) to move things around. But when you do that, you’ve given up on doing it a better way.

There is a gap here (probably one that the market hasn’t worried about too much). The topic of ‘data science’ as applied to the content of legal documents has never really existed. Word processors disguise this big ‘gap’ in the flow of information. They always rely on the human authors configuring the information content for each document as it should appear in the final output. We cannot achieve any kind of interaction with our text data, or space for computation or data analysis, without creating a gap between input and output. It’s the basic requirement for computation. In Word Processors, that gap does not exist.

If the Word Processor encourages your input to ‘look’ like your output, then you avoid computation because the input is the output, and you have to do all the work yourself. This is not really that much different when ‘templates’ that allow data inserts are used, because 99% of the content in the template is not involved in any computational process either. Templates are a way of avoiding the need to think about information, but often you have to, because of the nature of the work. So they appear helpful, but you soon run into new problems.

A very small gap between input and output exists for mail merge programs. Mail merge still uses a simple ‘merge’ in place of intelligent data storage and functions. It splits data into (a) the small pieces that may change and (b) everything else. It is not a particularly intelligent approach, and though it may improve the speed of generating relatively static documents for customers, it doesn’t improve the tools that might be needed by the professionals who craft documents every day. It doesn’t help manage the content data in the template.

# Data management improves customer service and value

Data management is linked to contract management, to document design, and customer needs

If we wanted to think about data analysis tools that would be in demand, what questions might lawyers or customers want to answer? e.g.

 - Is this document a lease or contract of sale? What topics does it cover? Can the customer load the document in, and have some basic ‘dashboard’ information get put up (whether it is in a legacy format or not). Can this be stored as new metadata?
 - Can you show me the topics in the order that I need to read them?
 - Which of the definitions is a concept I need to read first?
 - If I want to insert some extra information about topic X, can I easily do so?
 - Can I update this clause in all my documents?
 - Which are the most variable topics when I deal with my clients?
 - How can I get some statistics about the use of a particular clause in my business, or the use of very similar clauses that are on the same topic?
 - Can I attach the same cover letter to all the documents of a particular type, and insert the client information as needed?
 - Can I pull up the main data for all my client’s contracts, see what the specifications are, and also what should be the current status re financial payments, reviews, unexpired options etc?
 - How will I be able to check if I refer to a particular piece of legislation in my agreements?
 - In my suite of client documents, what are the similarities and differences?
 - Can I flick between a graphical representation of the document structure and the text?
 - How does my linear set-out of the document compare to the more tree-like structures that reflect the real relationships between the topics?
 - Can I present to the client the document in a summary form for presentation, then drill down and edit specific topics as they make suggestions?
 - Can the system make useful suggestions at this point, so that removing or adding components prompts for additional information (at a high level, content focussed), that need to be included?

Some of the answers to these will promote ideas about how to get better information out of current documents, which clients or lawyers can use, and also inspire ideas for how to store document data and meta-data in new formats.

# Usability/design considerations

Or what about these questions, where we might be able to gather hard data if the data was stored in a way we could attempt to analyse its use, instead of just looking at it:

 - How often is this particular clause used in documents in different subject areas?
 - How often do I ask whether my documents are using a particular clause, or trying to compare two clauses?
 - How often do I want to see the relationship between my clause/topic and its definition?
 - How often do I find myself reading back and forth between concepts because the way I have written my document requires me to revisit information in a very unhelpful way?
 - What is the most logical structure for setting out the concepts in my document?

# Machine learning pitfalls

What about machine learning? You might be asking, since everyone else is these days. The difficulty with assuming that some kind of ‘machine learning’ is useful, just because there is ‘learning’, is that it isn’t looking at the actual work practices of lawyers, or even what information is used to transform inputs to outputs, and what kind of instructions are needed. The algorithms of machine-learning are more heavily geared toward statistical analysis of information, and for the software to use correlations between different topics.

Machine learning often requires a very specific problem, and it produces a very specific solution. It can mean that you system is trained for a very specific purpose. If you have to train a machine to recognise correlations, it usually means you don’t have a lot of flexibility in that system. It favours ‘yes’/’no’ type results – is this a picture of a cat or not? That’s essentially the most basic model of computation – a boolean truth statement, about a single question.

Many people also get the idea that if we use ‘computers’, we have to try and shift the entire human role off to a computer (i.e. ‘AI will make lawyers redundant’). This is a fairly naive view of how algorithms can or should be used to help with existing workflows and behaviour. It’s a naive view of how we go about developing tools using computers at all. AI is also a broad term but it can encompass both expert-reasoning systems that process information automatically, and it can encompass reasoning systems that also achieve greater problem-solving by absorbing data and being able to apply statistical analysis to it (machine learning).

Machine learning uses algorithms, but it doesn’t necessarily help us understand what algorithms humans are using.

# Why not store documents as code?

Storing documents with the addition of code for ‘automation’ does not really achieve the gains that we should expect from treating the contents as data directly. Algorithms should apply to data that can be loaded up as data sets. However, some trends in document automation (particularly of contracts) make it harder, not easier, to apply an algorithmic, data-orientated approach.

The current approaches to using logic, or code, to influence the content of legal documents inside Word processors has included:

 - storing document templates, and then using code to influence a mail-merge operation.
 - inserting code inside the word processing content itself, so that it is processed ‘in-situ’, to influence what content is ultimately displayed in a word-processing file or not.

The code wrapping solution generally seems to work for individual documents (after a lot of setup), but it has limitations and is hard to scale. It doesn’t encourage a data management environment that is different to single-use word processing. In fact, it might encourage trying to insert more conditional data inside a single container (WP document) because there’s no other way to hold the data for similar, but not identical documents.

Code is not a particularly good data storage format, with the ability to apply data analysis to its contents. If documents have similar data, then having each separately coded makes it even more difficult to deal with that data (and encourages people to shove more code around the data, in a single code file).

Having that code inside a word processing application further increases the barriers to understanding what it does. It is a layer built on top of a raw format (like OOXML) that has nothing to do with the types of data in the document content.

Some of the problems with using the ‘computer programming’ metaphor by wrapping code around word-processing data are the ultimate cost, efficiency and limited data exploration options, i.e. :

 - It is like having an object-orientated approach where you assume you will only have one set of data for your code.
 - There is no clear separation of code and data, even for a single document.
 - You have word-processing formats used as both intermediate and final formats (this is not space efficient and it doesn’t really improve the ability to analyse the contents as data). This can easily confuse the users who want to describe their documents as ‘templates’. Which one is it?
 - The content data you have is still inside a single bloated container that assumes it is unique, and stored as a disk file.
 - There’s still no opportunity to hold lots of documents in memory at the same time, or easily link them to each other.
 - It forces code into the content environment, which has negative consequences for those updated templates. It creates a higher overhead in terms of needing an in-house coder or consultant to make changes. It tends to further separate the data from the professional users, without providing any direct advantage to them for single-use situations.
 - It is ultimately still a lot like a mail-merge algorithm, except that some of the content that appears in the final rendered output is conditional on what kind of data is coming in.
 - The design of the software may also be based on assumptions about the availability of staff in certain roles, like data input, content updating, or coding.

# Conclusion – data management of content is the way forward

The way forward? Lawyers need to be able to explain what they do (their data algorithms for content), and in terms sufficiently nuanced that they will lend themselves to computational analysis.

We are going to need people trained and experienced in both fields to lead the way. Once we have that, then we’ll be able to introduce a new paradigm, in which legal content is itself units of data, that is manipulated in software applications that treat it as units of data, and not merely some text laid out on a page.
