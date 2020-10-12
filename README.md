**\*NOTE: this is just a rough outline, most of the contents are still work in progress**

# Sapling 
- current release: `v0.1` [released for beta testing]
- Aims to help students pin-point answers from a large corpus of journal articles. It could also work for other formats of texts, suchs as textbook chapters or e-books.
- In doing so, the creation of Sapling hopes 
	1. to reduce the time needed by students' to learn about a (usually new) topic 
	2. to provides answers on the fly, such as during lectures and in workgroup sessions, or when refreshing knowledge on topics that was learnt months or years ago
	3. to help reduce anxiety, due to information overload, while preparing for exams or essay writing
	4. to ultimately reduce the knowledge acquisition barrier to help every one succeed in their education journey
- Inspired by advancements in AI on Natural Language Processing (NLP) such as IBM's Watson and FB's DrQA.


## Features
- *search keywords across multiple documents and return the 5 most relevant sentences*
- works by harnessing modern computers' ability to **quickly compare content diversity among texts**. So, for Sapling to work for you with higher accuracy, the more texts files you feed it the better (*note2*). You could for example feed it with all the articles and book chapters required for a course!
- Currently **supports most PDFs and `.txt` files**. Support for docx will be added in an upcoming version.
- *Uses artificial neural networks to perform machine comprehension of your texts, result in better matches for given queries*

*Notes*
1. Returned sentences may not be full sentence. This will be fixed in the upcoming versions.
2. Sapling has not yet been tested to its limit, but is imagined to suffer in performance when given hundreds of files. Performance is also machine dependant: processor speed, memory size and availability of GPUs/TPUs.


## How To's:
1. **Setup Sapling for the first time**	
	- Download 'Sapling' for [Windows (100MB)]() [Mac (400MB)]()
		- [ ] post links once program is completed and compiled

	- latest Java runtime installed 
		- Download for [any platform (recommended)](https://java.com/en/download/) OR [specific platform (advanced)](https://java.com/en/download/manual.jsp)

2. (*MacOS*) **Copy the path of the directory that you want to load**
	- ***Option 1:***
		- [ ] to add descriptions and screenshots

	- ***Option 2:***

3. **Run python script in your local environment**
	- install required libraries using following command
	```
	pip install -r requirements.txt
	```
	- run the main `.py` file

## FAQ
1. What it means by texts are not parsable?
2. Why am I getting `failed to see startup message` error?

### version history
- v0.1 [end-Sep-2020] - alpha testing + initial release
	- *features available*
		1. Extract texts from PDFs
		2. Return 5 top matching sentences to your query


### To-do for this readme
- [ ] installation instructions & requirements
- [ ] compatible file types
- [ ] features demonstration
- [ ] create link to form for feedback or issue reporting 
- [x] changelog
- [ ] disclaimer

### Further improvements:
- *Features*
	- [ ] ability to change the number of results returned
	- [ ] test accuracy of the tf-idf algorithm (possibly compare with alternative such as: SpaCy library, topic modelling, or POS tagging to identify contexts)
	- [ ] tidier preprocessing with XML and regex - the current hurdle is to be able to segment paragraphs (and therefore sentences) accurately
	- [ ] text based UI??
	- [ ] OCR capability for unreadable PDFs
	- [ ] extract text from docx files
	- [ ] save output to pdf
	- [ ] POS parsing
	- [ ] handles different types of questions differently. eg. how/why/what questions
	- [ ] host the scirpt in the cloud for web based deployment

- *Bug fixes*
	- [ ] handle error when query has no matches