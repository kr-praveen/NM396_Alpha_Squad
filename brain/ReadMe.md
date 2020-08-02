 <h1 align="center">User Manual</h1> 

## :key: Prerequisites  

## 1. Environment   

 * __Hardware Requirements__

Following hardware requirements are needed for smooth deployment of the software –
1. __Hosted Server with the following configurations:__
  32 GB+ RAM, 1 TB+ HDD, 250 GB+ SSD, 16 GB+ Graphics Card.  

2. __Local System with the following configurations:__
  8 GB+ RAM, 500 GB+ HDD, 4 GB+ Graphics Card, Network Interface Card.  
 
3. Printer  

  * __Software Requirements__  
  
  Following software requirements are needed to set-up a favourable environment for the software –  
  
1. __Hosted Server should have the following software:__  
  Python 3.7 or above  
  MySQL 5.6 or above  
  Anaconda (Spyder)  
  
2. __Local System should have the following software:__
   Any Browser (Chrome, Firefox, Safari, Opera, IE, Microsoft Edge, etc.)
   MS-Excel or Google Docs
   Adobe PDF Viewer  
   
The computational power is the most important dependency of the software. If the computation power of the environment provided for the software is high, the performance of the software will abruptly increase in a similar proportion.

## 2. Packages And Libraries  
  Anaconda (Python) Libraries and Packages  
      - [Flask](https://flask.palletsprojects.com/en/1.1.x/)  
      - [Keras](https://keras.io/)  
      - [TensorFlow](https://www.tensorflow.org/) 
      - [Scikit Learn](https://scikit-learn.org/stable/user_guide.html)  
      - [Numpy](https://numpy.org/)
      - [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)  
      - [Matplotlib](https://matplotlib.org/)  
      - [Wordnet](https://wordnet.princeton.edu/documentation)  
      - [Pickle](https://docs.python.org/3/library/pickle.html)   
      - [NLTK](https://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html)  
      - [Pymysql](https://pymysql.readthedocs.io/en/latest/)  

## 🚀&nbsp; Installation Guide
1. Clone the repository in your system.
```
$ git clone https://github.com/kr-praveen/NM396_Alpha_Squad.git
```
2. Unzip the folder and extract the files.   

3. Open the spyder or any python web framework IDE. Now, Set the working directory path as the root folder of the cloned repo.  

4. Now open app.py file and run it.

5. Now, on your browser, run http://127.0.0.1:5000/.  

6. The software will start working.


## :hourglass: Project Demo
:movie_camera: [YouTube Demo Link](https://www.youtube.com/watch?v=53ePTxXjwTg)

## :bulb: Basic User Functionalities  
Mainly there are 4 functionalities:  
  1. Training  
  2. Testing    
  3. Web API  
  4. Single Comment  
  
## Training

__1. Login__
* Login by entering username and password and click login button.  

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/login.png" width="700" height="400"></p>  

__2. Default Dataset__
* After login, click on Training Dataset then all the available dataset will be available. One default dataset will be available for which the model will be already trained. You can not Remove that Dataset you can only modify it.   

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/dataset.png" width="700" height="400"></p>  

__3. New Training Dataset__
* For Training model on new training Dataset, first you have to click on Upload new training dataset button. After that one form will be open in which some fields will be there, Training Data name, Upload image, upload dataset, Description of dataset. The image and description you upload will reflect when the data will be uploaded and model will have trained.  

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/new%20dataset.png" width="700" height="400"></p>  

__4. Sample Dataset__  
* Sample training dataset can be downloaded from the link given below the input file field, so that you convert your training data into same format as given so that model can easily get the required attributes.

__5. Model Training__
* When successfully data will be uploaded then the model will start training in background. The above screen can be seen. Please do not press back or refresh button.
After the model will be trained the new training data will be added into training data and you can use it for further testing model.
You can also remove or modify that training dataset from training dataset section. When you put arrow on the newly added training data click on more info and you can modify it or remove it.  

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/model%20training.png" width="700" height="400"></p>  

## Testing  
__1. Log In__
* For Testing Data or feedback data first, you have to log In. After that go to feedback data section. There will be testing dataset if uploaded previously otherwise you have to upload training data.  

__2. Using existing Testing Data__  
* If training data is already uploaded then you can test on that data. We can view or modify by putting arrow on that dataset and also can view result by click on result button. 

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/sample%20dataset.png" width="700" height="400"></p>   

__3. Sample testing Dataset__  
* When you upload testing dataset then in the form there will be sample testing data. You can download it and make your testing data into same format so that it can be accepted .

__4. Uploading new Testing Data__
* For uploading new training dataset click on upload new testing dataset. After that new form will be open in which you have to fill testing data name, image (will be shown after the data will be uploaded in feedback dataset section), training dataset and description of data. There is dropdown in which you can choose on which training data you want to test your data. And want to store that testing data on local storage or on cloud.

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/upload%20feedback%20data.png" width="700" height="400"></p> 

__5. Result Analysis__  
* When you click on result button it will redirected to new webpage in which model is testing on that data meanwhile do not press back or refresh button. When model will test data result will be shown as mentioned below.   

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/result%20page.png" width="700" height="400"></p>   

## Web API  
__1. Get web API Link__
* After login when you click on web API you will see Get API click on that circle, you will get Web API link you can use it by just putting that link. When you put that link a webform will be opened and user can give their feedback in that form.  

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/web%20api.png" width="700" height="400"></p>
 
__2. Get web API feedback__
* When user will submit feedback, it will store on Cloud. If you want to get the feedback of user you can click on Get Web API Dataset circle, you can download the feedback of user given by user from web API.  

__3. Analyze Result__
* By clicking on Analyze result, the model will test all the feedback in background meanwhile do not press back or refresh button. When testing will be done, result page will be shown as mentioned in testing dataset result analysis.  

## Single Comment  
* For the introduction of our software single comment is available before login. You can just try without even login to our software. Just put any comment, our software will analyze it and will give result in the form of doughnut chart at the scale of 1-5. You can easily see that whether that comment is positive or negative. Same is also available after login so you can use it after login too.   

<p align="center"><img src="https://github.com/kr-praveen/NM396_Alpha_Squad/blob/development1/brain/Readme_images/single%20comment.png" width="700" height="400"></p>
