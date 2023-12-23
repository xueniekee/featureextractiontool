from tkinter import *
import pandas
from tkinter import filedialog
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import csv
import os
import gensim.models
import pandastable as ps
from loghandler import add_log_event
import datetime
from filetypehandler import get_file_type

def convert_to_csv(text_file):
    csv_file = os.path.splitext(text_file)[0]+".csv"
    with open(text_file, 'r') as file:
        text_data = file.readlines()
        
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in text_data:
            row = line.strip().split('.')
            writer.writerow(row)
    return csv_file

def browseFile():
    global filename
    new_filetype = get_file_type()
    existing_filetype = [("All Files", "*.*")]
    filetype = existing_filetype + [(f"{ftype} files", f"*.{ftype}") for ftype in new_filetype] #type: ignore
    filename = filedialog.askopenfilename(
        initialdir="/*/Desktop/",
        title="Select a File",
        filetypes= filetype
    )
    label_file_explorer.configure(text="File Opened: "+filename, wraplength=300, justify="left")
    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": "Upload Done"}
    add_log_event(new_event)
    if filename and "txt" in filename.lower():
        filename = convert_to_csv(filename)
        return filename
    else:
        return filename

def remove_punctuation(text):
    punctuation = string.punctuation.replace('!', '')
    punctuationfree="".join([i for i in text if i not in punctuation])
    return punctuationfree

def tokenization (text):
    tokens = word_tokenize(text)
    return tokens

def remove_stopwords(text):
    output = [i for i in text if not i in stopwords.words('english')]
    return output

def preprocess():
    file = pandas.read_csv(filename, encoding="ISO-8859-1")
    text = file.iloc[:, 1].str.lower()
    text_list = []
    typename = ['.csv']
    for word in typename:
        global outputname
        outputname = filename.replace(word, "")
    
    global preprocessed
    preprocessed = outputname +'output.csv'
    if(os.path.exists(preprocessed) and os.path.isfile(preprocessed)):
        os.remove(preprocessed)
    
    with open (preprocessed, 'a', newline='') as f:  # type: ignore
        writer = csv.writer(f, delimiter=' ')
        for row in text:
            row = remove_punctuation(row)
            row = remove_stopwords(tokenization(row))
            writer.writerow(row)
            text_list.append(row)
    
    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": "Preprocess Done"}
    add_log_event(new_event)
    
    dataframe = pandas.read_csv(preprocessed)
    displaypreprocess(dataframe)
    
    global model        
    model = gensim.models.Word2Vec(sentences=text_list, min_count=1, vector_size=5, sg=1)
    
def main():
    global root 
    root = Tk()
    root.title('Feature Extraction')
    root.geometry("420x350")
    Label(root, text="Feature Extraction Tool", font="bold",bg="grey", height=3).grid(row=0, columnspan=4, sticky=E+W)
    Label(root, text="").grid(row=1, column=0)
    global label_file_explorer
    label_file_explorer = Label(root, text="Upload your File to Extract Features")
    label_file_explorer.grid(row=2, column=0, sticky="w")
    Button(root, text="Upload File",width=10, height=1, command=browseFile).grid(row=2, column=1)
    Label(root, text="Choose Features to Extract:").grid(row=3, column=0, sticky=W)
    global urgency_check
    urgency_check = BooleanVar()
    Checkbutton(root, text="Contains Urgency Words", variable=urgency_check).grid(row=4, column=0, sticky=W)
    global free_check
    free_check = BooleanVar()
    Checkbutton(root,text="Contains 'Free'", variable=free_check).grid(row=4, column=1,sticky=W)
    global exclamation_check
    exclamation_check = BooleanVar()
    Checkbutton(root, text="Contains '!'", variable=exclamation_check).grid(row=5, column=0, sticky=W)
    global url_check
    url_check = BooleanVar()
    Checkbutton(root, text="Contains URLs", variable=url_check).grid(row=5, column=1, sticky=W)    
    global count_check
    count_check = BooleanVar()
    Checkbutton(root, text="Word Count", variable=count_check).grid(row=6, column=0, sticky=W)
    global freq_check
    freq_check = BooleanVar()
    Checkbutton(root, text="Top 10 Most Frequent Words Found", variable=freq_check).grid(row=7, column=0, sticky=W)
    global similar_check
    similar_check = BooleanVar()
    Checkbutton(root, text="Top 3 Most Similar Words to 'Urgent' Fount", variable=similar_check).grid(row=8, column=0, sticky=W)
    Button(root, text="Preprocess & Extract", width=12,height=1, command=get_features).grid(row=9, columnspan=2)
    Button(root, text="Close",width=5, height=1, fg="red", command=close).grid(row=10, columnspan=2)

def get_features():
    preprocess()
    file = pandas.read_csv(preprocessed)
    feature_file = outputname +'_features.csv'
    text = file.iloc[:, 0]
    
    if(os.path.exists(feature_file) and os.path.isfile(feature_file)):
        os.remove(feature_file)

    global df
    df = pandas.DataFrame()
    
    if urgency_check.get() == True:
        contains_urgency(text)
    else:
        pass
    if free_check.get() == True:
        contains_free(text)
    else:
        pass
    if exclamation_check.get() == True:
        contains_exclamation(text)
    else:
        pass
    if url_check.get() == True:
        contains_url(text)
    else:
        pass
    if count_check.get() == True:
        word_count(text)
    else:
        pass
    if freq_check.get() == True:
        top_10_most_freq(text)
    else:
        pass
    if similar_check.get() == True:
        top_3_most_similar(text)
    else:
        pass
    
    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": "Extract Done"}
    add_log_event(new_event)

    df.to_csv(feature_file, index=False)
    display(df)

def contains_urgency(text):
    urgency = ['urgent', 'hurry', 'fast', 'verification required', 'important', 'action required', 'now']
    result = []
    for row in text:
        urgency_found = any(word in row for word in urgency)
        if urgency_found == True:
            result.append('1')
        else:
            result.append('0')
    df['Contains_Urgency'] = result
    
def contains_free(text):
    result = []
    for row in text:
        if "free" in row:
            result.append('1')
        else:
            result.append('0')
    df['Contains_Free'] = result
    
def contains_exclamation(text):
    result = []
    for row in text:
        if "!" in row:
            result.append('1')
        else:
            result.append('0')
    df['Contains_Exclamation_Mark'] = result

def contains_url(text):
    result = []
    for row in text:
        if "http" in row:
            result.append('1')
        else:
            result.append('0')
    df['Contains_Urls'] = result
    
def word_count(text):
    result5 = []
    for row in text:
        word_count = len(row)
        result5.append(word_count)
    df['Word_Count'] = result5

def top_3_most_similar(text):
    similar_words = model.wv.most_similar('urgent', topn=3)
    similar_words_list = []
    for word, vector in similar_words:
        similar_words_list.append(word)
        
    for i in range(3):
        result = []
        for row in text:
            if similar_words_list[i-1] in row:
                result.append('1')
            else:
                result.append('0')
        df['Contain_Most_Similar_Words_To_Urgent_' + similar_words_list[i-1]] = result

def top_10_most_freq(text):
    most_frequent_list = []
    for index, word in enumerate(model.wv.index_to_key):
        if index == 10:
            break
        most_frequent_list.append(word)    
    
    for i in range(10):
        result_most_freq = []
        for row in text:
            if most_frequent_list[i-1] in row:
                result_most_freq.append('1')
            else:
                result_most_freq.append('0')
        df['Contain_Most_Frequent_Word_' + most_frequent_list[i-1]] = result_most_freq

def displaypreprocess(dataframe):
    global root1
    root1 = Toplevel(root)
    root1.title('Preprocessed')
    root1.geometry("700x500")
    root1 = ps.Table(root1, dataframe=dataframe,showtoolbar=False, showstatusbar=False)
    root1.show()
    
def display(dataframe):
    global root2
    root2 = Toplevel(root)
    root2.title('Extracted Features')
    root2.geometry("700x500")
    root2 = ps.Table(root2, dataframe=dataframe, showtoolbar=False, showstatusbar=False)
    root2.show()

def close():
    root.destroy()

main()
root.mainloop() # type: ignore

