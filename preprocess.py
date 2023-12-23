from tkinter import *
import pandas
from tkinter import filedialog
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import csv
import os
import gensim.models
from gensim.test.utils import datapath
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
            row = line.strip().split(',')
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
    root.title('Upload File')
    root.geometry("300x300")
    root.resizable(False,False)
    Label(root, text="Feature Extraction Tool", font="bold",bg="grey", height=3).pack(fill=X)
    Label(root, text="").pack()
    global label_file_explorer
    label_file_explorer = Label(root, text="Upload your File to Extract Features")
    label_file_explorer.pack()
    Button(root, text="Upload File", command=browseFile).pack()
    Button(root, text="Preprocess", command=preprocess).pack()

def displaypreprocess(dataframe):
    global root1
    root1 = Toplevel(root)
    root1.title('Preprocessed')
    root1.geometry("700x500")
    root1 = ps.Table(root1, dataframe=dataframe,showtoolbar=False, showstatusbar=False)
    root1.show()
    
main()
root.mainloop() # type: ignore

