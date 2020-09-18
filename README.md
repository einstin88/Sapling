** this is just a rough outline, most of the contents are still work in progress**

# Sapling 
- current release: `v0.1`
- *Provide intelligent answers based on your given reading materials*
- Intended for journal articles, but can also be used for any text files such as pdf of textbook chapters or e-book

## Features
- search keywords across multiple documents and return the 5 most relevant sentences

*Notes*
1. Returned sentences may not be full sentence. This will be fixed in future versions


## How To's:
1. **Installation and using Sapling for the first time**
	
	***Required***:
	- Download 'Sapling' for [Windows]() [Mac]()
		- [ ] post links once program is completed and compiled

	- latest Java runtime installed 
		- Download for [any platform (recommended)](https://java.com/en/download/) OR [specific platform (advanced)](https://java.com/en/download/manual.jsp)

2. (*MacOS*) **Copy the path of the directory that you want to load**
	- ***Option 1:***
		- [ ] to add descriptions and screenshots

	- ***Option 2:***

3. **Run python script in your local environment**
	- 

## FAQ
1. What it means by texts are not parsable?
2. Why am I getting `server response error`?

### version history
- v0.1 alpha testing, initial release
	- *features available*
		1. Extract texts from PDFs
		2. Return 5 top matching sentences to your query


### Todo for readme
- [ ] installation instructions & requirements
- [ ] compatible file types
- [ ] features demonstration
- [ ] create link to form for feedback or issue reporting 
- [x] changelog
- [ ] disclaimer

### Future improvements:
- *Features*
	- [ ] ability to change the number of results returned
	- [ ] handles situation when query has no result
	- [ ] tidier preprocessing
	- [ ] UI
	- [ ] OCR capability for unreadable PDFs
	- [ ] extract text from docx files
	- [ ] save output to pdf
	- [ ] POS parsing
	- [ ] handles different types of questions differently. eg. how/why/what questions
	- [ ] host the scirpt in the cloud for web based deployment
- *Bug fixes*
	- [ ] handle error when query does not produce any matches