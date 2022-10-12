import logging
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
import re
import warcio
import unicodedata
from warcio.archiveiterator import ArchiveIterator
from urllib.request import urlopen
from bs4 import BeautifulSoup

dir = './english_sample_100.warc'
#dir = ''
identifier = 'WARC/0.18'
remove_punctuation = 1
case_fold = 1
lemmatize = 1
remove_stopwords = 1
def extract_text(html):
    soup = BeautifulSoup(html_doc, features="html.parser")

    # Remove script, style
    # 把 JS, CSS 刪除
    for script in soup(["script", "style"]):
        # Extract (no storing)
        script.extract() 

    # Retrieve text
    text = soup.get_text(separator="\n", strip=True)

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # Drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)

    # Remove unicode
    text = unicodedata.normalize("NFKD", text).replace('\n', ' ')
 
    return text
docs = []
html_doc = ''
all_text = ''
doc_id = -1
is_html = 0
content_len_counter = 0


with open(dir, "rb") as fp:
    for i, line in enumerate(fp):
        
        # Remove leading & trailing spaces
        line = line.strip()      
        # Remove 'b' char (byte string)
        line = line.decode("unicode-escape", errors = 'ignore')

        # If line is blank, skip operations 
        if line != '':
            # New doc
            if line == identifier:
                if html_doc:
                    
                    # Extract doc from html
                    html_doc = extract_text(html_doc)
                    docs.append(html_doc)
                    all_text += html_doc + ' '
                    html_doc = ''
                    
                is_html = 0
                doc_id += 1
                content_len_counter = 0

            elif 'Content-Length:' in line:
                # End of 'header', next line is start of html
                if content_len_counter: 
                    is_html = 1
                content_len_counter = 1 
            # Currently in html doc
            elif is_html:
                html_doc += line

        #if i > 100:
        #    break
    # Read last doc as there is no identifier
    html_doc = extract_text(html_doc)
    docs.append(html_doc)
    all_text += html_doc + ' '

print("len(docs) = ",len(docs))
print("len(all_text) = ",len(all_text))
# Remove punctuation via regex
if remove_punctuation:
    all_text = re.sub(r'[^\w\s]', ' ', all_text)

# Lowercase
if case_fold:
    all_text = all_text.lower()
# Lemmatize
if lemmatize:
    temp = ''
    for i in all_text.split():
        temp += lemmatizer.lemmatize(i) + ' '
    all_text = temp
# Tokenize
text_tokens = word_tokenize(all_text)
text_tokens = sorted(list(set(text_tokens)))

len(text_tokens)  #teams
# Remove stopwords, if needed
# 55 seconds for 10k words
if remove_stopwords:
    text_tokens = [word for word in text_tokens if not word in stopwords.words()]
    len(text_tokens)
dict = {}  
prog_freq = 10
prog_docs = int(doc_id / prog_freq)

class dataset_process:
    def __init__(
        self,
    ):
        self.dateset = {}
    def scan_dataset(self, df):
        for doc_id_maber in range(doc_id):
            count_word = 0
            for team_ in docs[doc_id_maber].split():
                count_word += 1
                if team_ not in self.dateset:
                    self.dateset[team_] = {doc_id_maber: {}}
                    self.dateset[team_] = {'team_frequency': 1}
                    self.dateset[team_][doc_id_maber] = {'pos': [count_word], 'doc_frequency': 1}
                else:
                    self.dateset[team_]['team_frequency'] += 1
                    if doc_id_maber not in self.dateset[team_]:
                        self.dateset[team_][doc_id_maber] = {'pos': [count_word], 'doc_frequency': 1}
                    else:
                        self.dateset[team_][doc_id_maber]['doc_frequency'] += 1
                        self.dateset[team_][doc_id_maber]['pos'].append(count_word)
    def _get_config(self, args):
        try:
            idx = test.dateset[args]
            print("keyword = ", args)
            print(idx)
            return idx
        except KeyError:
            print('Keyword not in index')


test = dataset_process()
#df = pd.read_csv ('2.csv')
test.scan_dataset(docs)
keyword = 'your'
index_doc = test._get_config(keyword)
