# NM396_Alpha_Squad
Sentiment Analysis from text feedback - ISRO PS - SIH 2020.

## :star: Note
__Kindly refer ReadMe.md file inside actual root directory **'brain'**.__

* __Team Name :__ Alpha Squad
* __Organization name :__ Indian Space Research Organization (ISRO)
* __PS Number :__ NM396
* __Problem Statement :__ Sentiment Analysis from text feedback

## Idea   
In our software, we propose a hybrid approach to classify and analyze sentiments from user-feedbacks. This approach is a combination of ML-based and Lexicon-based techniques. It will be able to classify individual feedback at a scale of 1-5 (where, 1-> Highly Negative, 5-> Highly Positive), and subsequently it will provide overall rating. In addition, the software will be able to yield ‘Aspect based Analysis’, i.e., it will not only provide the user ratings for different entities but also will analyze the ratings for different aspects/attributes associated to those entities. Here, an entity means a topic/product/service on which feedback is given. The software will be able to automatically extract entities and aspects from the provided feedback-data.  

As an end-product, we intent to make a web-based application. For visualization, it will use various graphical representations like- Pie chart, Doughnut chart, Line and Bar graphs, etc. The software is open for different types of input formats. The input can be provided directly from feedback forums or feedback management systems. Besides, the software will provide Web-embedded feedback-form API for real-time feedback analysis. A feedback manager would generate feedback-form web API links and manage them.The organization has to just put the API link on its website where the feedback form is needed, and all the relevant analysis will be shown on our software. Results can be analyzed for any specific time-period using the provided filtration options. In order to provide domain-independence to the software, the feedback manager can update the training dataset used in algorithms. Additionally, the software will be able to depict the recent trends in user feedback, like- on what topic people are giving more feedback.

## Novelty of our idea:  
• Hybrid approach for sentiment analysis  
• Aspect based analysis  
• Web–embedded feedback form API  
• Extraction of trending topics  
• Different types of input variants  

## Technology Used    
* __Front-end__  
JavaScript, jQuery: For client-side scripting  
AJAX: For asynchronous data transfer between client and server  
Bootstrap: Framework for front-end development  
HTML/CSS: For web-page designing   

* __Back-end__  
Python: Language for server-side scripting and Algorithm design  
Machine Learning: For classification of user opinions/feedback  
Natural Language Processing: For lexicon and aspect based analysis  
Flask: Web framework for connectivity between back-end and front-end  
JSON: For transmitting data between server and client  

* __IDE’s__
Anaconda (Spyder): For ML Coding and Simulations  
Notepad++: Simple text editor  

## Use Case Diagram:
__Dependencies / Show Stopper:__  
• Domain-specific dataset for training purpose  
• Computational power  

<p align="center"><img src="" width="700" height="400"></p>

## Architecture Diagram  
<p align="center"><img src="" width="700" height="400"></p>
