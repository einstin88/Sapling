![Sapling Logo](/img/original.jpeg)

# Sapling 🌱 <a name="top"></a>
- current release: `v0.1` 
- Aims to help students pin-point answers *([1](#note1))* from a large corpus of journal articles. It could also work for other formats of texts, suchs as textbook chapters or e-books.

#### Acknowledgement
This release is possible due to encouragements and contributions by the campus community and a few friends. Special thanks to ...


## Contents 
1. [What it does?](#first)
2. [Why Sapling?](#second)
3. [Features](#third)
	- [Example](#examples)
4. [Getting started](#forth)
5. [FAQ](#fifth)
6. [Technical description](#sixth)
7. [Known issues](#bugs)


## What it does? <a name="first"></a>
**In short**: 
1. It reads in the passages of the documents in your folder and determine their relevancy to your questions. The top 5 passages will then be shown!
2. Imagine a custom Google-like search engine for specific ideas or concepts in your readings! You can then tell Sapling to open the correct document for you and dive right in~~
3. You may also use Sapling to do a **negative query**, that is searching the documents to be certain that they don't have the information you are looking for. Useful for filtering! 
	- For example, if the retrieved answers turn out to have low confidence scores, it is likely that the information you need is not in those given documents (even after you tried rephrasing the question)
- It **does NOT assess** your texts qualitatively, i.e., strengths & weaknesses or arguments, fallacies, robustness of results or the underlying research methodologies unless they are explicitly mentioned! These tasks will remain the responsibility of the reader fortunately/unfortunately 😪


## Why Sapling? <a name="second"></a>
The creation of Sapling hopes :-
1. to reduce the time ⏲ needed by students to learn about any text-based (usually new) topic 
2. to provides answers on the fly, such as during lectures 🙋‍♀️🙋‍♂️ and in workgroup sessions
3. to help when you want to refresh on old knowledge such as topics that was learnt months or years ago
4. to help reduce anxiety (due to information overload) while preparing for exams 👨‍💻👩‍💻 or essay writing
5. to ultimately reduce the knowledge acquisition barrier to help every one succeed in their education journey

(Inspired by advancements in AI 🤖 on Natural Language Processing (NLP) such as IBM's Watson, FB's DrQA, and Google Research's BERT & ALBERT)


## Features <a name="third"></a>
1. Uses *nearly* state-of-the-art human language comprehension and question answering architechture (produced in end-2019 to early-2020) that does not rely on memorizing words or questions to find answers. (The method is too technical to explain here, look at the article "Attention is all you need" by Google if you are interested )
2. Sapling **reads your texts to find the 5 most relevant sentences across multiple PDF articles within minutes** based on your question about its topic. 😎 Confidence scores of each result are displayed! 
3. Locate the files and paragraphs where the answers are. You can open the file from the results if you want to.
4. Leverages modern computing capability and speed to **quickly 'read' contents among texts**. Sapling works best when more texts files are being fed *([2](#note2))*. You could for example feed it with all the articles and book chapters required for a course!
5. Currently **supports most `PDFs` files**. Support for `.txt` and `docx` will be added in an upcoming version. 
6. Works on Windows 10 🍊 and MacOS 13 🍎 or newer.


## Getting Started: <a name="forth"></a>
<ins>Download, Unzip, Run!</ins>
1. **Setting up**	
	1. Download 'Sapling':
		- [For Windows](https://drive.google.com/file/d/1jNh1BU15eKFKZtZvSNWfRTLj5t7Qx7lz/view?usp=sharing)
		- [For macOS 10.13.6 or newer](https://drive.google.com/drive/folders/1-D2qTUL0S43HrnTgIvMqcLLpi6w0mNN9?usp=sharing)

	2. Download and install **Java** runtime
		- [For Windows](https://java.com/en/download/) 
		- [For macOS](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html) ➡ choose 'macOS installer'
		- Java is required to run the parser that converts PDFs to a text format that is understandable by the computer. The same parser can also convert images or other document formats to plain texts which will come in future releases.

2. **Extract and run**
	- <ins>Windows</ins> : Run `autorun.bat` after extracting the zip file
	- <ins>Mac</ins>: 
		1. Follow instructions in the zipped file to run `autorun.command`.
		2. When you get a prompt about security, goto 'Setting' > 'Security & Privacy' > select 'open anyway'

3. **Provide path to the folder with your PDFs**
	- This is the knowledge base which Sapling draw her answers from.

	- Example: 
	
	<ins>This is the folder with the PDFs</ins>

	![directory](/img/mac_folder_1.png)

	<ins>The full path to the folder provided like this</ins>

	![then path to the folder](/img/provide_path.png)

	- <ins>For macOS</ins>: **2 easy ways to copy the folder path**
		1. ***Option 1:***
			- Drag and drop into the console window
		2. ***Option 2:***
			- Right click on the folder, then **hold** the 'option' key. You should see `'Copy xxx as pathname'` option
	
	![copy path on mac](/img/mac_folder_3.JPG)

	- You can easily drag and drop into the console on Windows

4. **Question away!**
	- Ask anything or something you vaguely remember from reading the texts
	- And repeat!


### Example query & results: <a name="examples"></a>
<ins>Key in a question</ins>

![Example query](/img/query.png)

***Voila!***

![Results](/img/result_disp.png)


## FAQ <a name="fifth"></a>
1. What it means by `texts are not parsable`?
	- It means that the PDF is a scanned image, or the internal character mapping is corrupt. Usually occur with very old PDFs.

2. Why isn't there a normal graphical interface? Why does it only have a text-based console?
	- The text-based console is what's actually running behind the scenes in all of the programs/games that you use (i.e. the program's logics and functionalities), but is hidden under the layers of graphics. It will take a bit more time to familiarize, design and implement a graphical interface that most people are familiar with. It is definitely a feature that will be rolled out in the near future. This is also the reason why it is not on the AppStore of any platform yet. It is in the to-do list for Sapling at the bottom of this page.

3. Why am I getting segmentation fault : 11?
	- This should be fixed now. If you're using MacOS, it is due to the way Python and Mac handles memory. You may have fed it with a large file, increasing RAM and cache usage by the program.

4. Why does it take a couple of minutes every time I enter a question?
	- It is still in the preliminary development phase of the program. So the focus is on accuracy of the results. Speed will be improved in the future for sure! Please let us know if you find the program useful or what needs to be improved, so it can be added as a future feature!

5. Why am I getting `failed to see startup message` error?
	- It takes a couple of seconds to load the PDF parser. Sometimes the process monitor times out before it is loaded. If it continues, then don't worry about the message. Otherwise, you may be running with MacOS 10.14 or older, which has old Java setup and will cause strange behaviour.


### Feedback & issues reporting
1. If you have a Github account, issues can be reported directly on the page
2. Public feedback through Google form is coming soon


### Technical description <a name="sixth"></a>
1. Preprocessing
	1. Retrieves compatible files from given directory
	2. Parse and clean texts of headers/footers/annotations/references
2. Query processing
	1. Naive search for relevant docs with TF-IDF
	2. Fit query and passages using model pre-trained on Wiki texts and fine-tuned on Squad tasks, with span classification head
	3. Retrieve cross entropy losses to score passage fit and embedding vectors to compute argmax'es for answer spans
3. Current model specifications
	1. Name: ALBERT base
	2. Vocabulary amount: 30,000
	3. Training data: English wikipedia, Squad v2


### Version Releases
- v0.1 [13-Oct-20]: debut for alpha testing
	- *features available*
		1. Extract & clean texts from PDFs
		2. Return 5 top matching answers to your query
- v0.2 [26-Oct-20]: beta testing
	1. addressed reliability issues on macOS
	2. streamlined user interaction process
	3. added option to include subdirectories


#### *Notes*
1. *Sapling's internal model was trained to understand public domain language and has not been trained on domain specific language, such as Political Science or Arts. That may reduce accuracy of answers slightly, but this limitation will be improved in future releases when it is used more often.* <a name="note1"></a>
2. *Sapling has not yet been tested to its limit, but will perform slower when given hundreds of files. Performance is also machine dependant: processor speed, memory size and availability of Cuda-GPUs.* <a name="note2"></a> 
[*(back)*](#third)

[<ins>return to top</ins>](#top)


#### Ideas for the future:
- **Improvements**
	- [ ] simplify explanations for users with less technical background

- *Features*
	- [ ] implement updates without fresh download
	- [ ] ability to change the number of results returned
	- [ ] improve search speed with multi-thread processing
	- [ ] tidier preprocessing of PDF headers, footers and citations
	- [ ] web-based UI
	- [ ] option to save previously accessed directory
	- [ ] OCR capability for unparsable PDFs
	- [ ] extract text from docx files
	- [ ] save outputs
	- [ ] combine multiple directories as a common knowledge base

- *Bug fixes* <a name="bugs"></a> 
	- [ ] Segmentation fault 11 - seems to be due to sentencepiece, fix to be tested
	- [ ] splitting paragraphs sometimes does not work - fix to be tested
