**\*NOTE: this is just a rough outline, most of the contents are still work in progress**

# Sapling 
- current release: `v0.1`
- *Provide intelligent answers based on your given reading materials???*
- Intended for journal articles, but can also be used for any text files such as pdf of textbook chapters or e-book

## Features
- search keywords across multiple documents and return the 5 most relevant sentences

*Notes*
1. Returned sentences may not be full sentence. This will be fixed in future versions


## How To's:
1. **Installation and using Sapling for the first time**	
	- Download 'Sapling' for [Windows]() [Mac]()
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