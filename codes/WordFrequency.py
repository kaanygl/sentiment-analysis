import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import os

nltk.download('punkt')
nltk.download('stopwords')

# Directory containing the xlsx file(s)
directory = r"C:\*"

all_words = []

custom_stopwords = set([
    "excludedword1","excludedword2"
])

for filename in os.listdir(directory):
    if filename.endswith(".xlsx") :
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)
        comments = df['comment'].tolist() # Column that includes the entries to be analyzed.
        for comment in comments:
            if isinstance(comment, str):
                words = word_tokenize(comment)  # Tokenize the comment
                all_words.extend(words)        

all_words = [word.lower() for word in all_words]

stop_words = set(stopwords.words('turkish')).union(custom_stopwords)

filtered_words = [word for word in all_words if word not in stop_words and word.isalpha()]

word_freq = Counter(filtered_words)

print("Top 20 most common words:")
for word, freq in word_freq.most_common(20):
    print(word, ":", freq)
