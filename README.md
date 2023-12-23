# Feature Extraction Tool for Phishing Dataset

Feature Extraction Tool for Phishing Dataset is a tool that extracts phishing related features from raw dataset. 

## Description

The feature extraction tool offers the flexibility to extract user-selected features or all phishing-related features from the raw text dataset, enhancing its applicability in diverse research scenarios. Features that are included are Contains_Urgency, Contains_Free, Contains_Exclamation_Marks, Contains_Urls, Word_Count, Contain_Most_Similar_Words_To_Urgent_Word, and Contain_Most_Frequent_Word_Word. Features such as Contain_Most_Similar_Words_To_Urgent_Word and Contain_Most_Frequent_Word_Word are extracted using the Word2vec model. Main modules that are included in the tool are the user register module, user login module, upload module, download module, and feature extraction module.

## Getting Started

### Dependencies

* Any PCs that can run Python file are good to run the tool.
* Python version: Python 3.10.5 or later

### Installing

* Python Libraries
```
pip3 install nltk
```
```
pip3 install tkinter
```
```
pip3 install hashlib
```
```
pip3 install gensim
```
```
pip3 install pandas
```
```
pip3 install pandastable
```
```
pip3 install csv
```

### Steps to Execute File
You may start to run the registerlogin file once all libraries mentioned above are installed.
* Open registerlogin.py in terminal
```
python3 registerlogin.py
```

* Register a new account if you are a new user.
    * Fill username and password
    * Password should have a minimum of 8 characters, with the combination of at least 1 numeric character, at least 1 alphabetic character, and at least 1 special character.
* Login to your account
* Choose 'Preprocess and Extract' if you want to preprocess the raw dataset and extract features.
    * Upload your file in csv file type.
    * Make sure that your text is in column B.
    * Choose the features that you want to extract.
    * Click the 'Preprocess and Extract' button to start the process.
    * The result will be downloaded back to the same file path as the uploaded file once the process is done and the previews are shown.

### Features provided
* Contains_Urgency: Urgency words, which are ‘urgent’, ‘hurry’, ‘fast’, ‘verification required’, ‘important’, ‘action required’, ‘now’. This feature will show if the data contains urgency words mentioned above. 
* Contains_Free: This feature shows if the word ‘free’ is found in the data.
* Contains_Exclamation_Marks: This feature shows if the ‘!’ is found in the data.
* Contains_Urls: This feature checks if ‘http’ found in the data.
* Word_Count: This feature counts the total of words in a text.
* Contain_Most_Similar_Words_To_Urgent_Word: This feature shows top 3 words found most similar to ‘urgent’ in Word2vec model. Then the occurrence in text is found.
* Contain_Most_Frequent_Word_Word: This feature shows top 10 most frequent words found in Word2vec model. Then their occurrences in text are found.

## Help

Email to anniekee0527@gmail.com for help and enquires.

## Authors

Kee Xue Nie, Isredza Rahmi A Hamid
Faculty of Computer Science and Information Technology
Universiti Tun Hussein Onn Malaysia
