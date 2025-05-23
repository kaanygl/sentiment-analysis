﻿import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

directory = r"C:\*"

all_comments = []

for filename in os.listdir(directory):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)
        comments = df["comment"].tolist()
        all_comments.extend(comments)

all_comments_text = " ".join(all_comments)

custom_stopwords = set(STOPWORDS)
custom_stopwords.update(["excluded word1", "excludedword2"])

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    stopwords=custom_stopwords,
    min_font_size=10,
).generate(all_comments_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
