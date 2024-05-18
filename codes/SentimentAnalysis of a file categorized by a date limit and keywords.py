import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Path of the xlsx file
file_path = "C:\*"

df = pd.read_excel(file_path)

df["datecolumn"] = pd.to_datetime(df['datecolumn'])

start_date = pd.Timestamp('2024-04-01 00:00:00')

start_date = start_date.tz_localize('UTC')

df_filtered = df.loc[df["datecolumn"] >= start_date]

keywords = ["keyword1","keyword2"]

analyzer = SentimentIntensityAnalyzer()

all_scores = []

sentence_number = 0

for index, row in df_filtered.iterrows():

  try:
    sentence = row['comment']
    if isinstance(sentence, str):
      if any(keyword in sentence for keyword in keywords):
        sentence_number += 1
        print("Sentence Number:", sentence_number)
        print("Analyzing:", sentence)
        vs = analyzer.polarity_scores(sentence)
        print("Sentiment Score:", vs)
        all_scores.append(vs)
      else:
        print("No keyword found in the sentence.")
    else:
      print("Warning: Sentence is not a string")
  except Exception as e:
    print("Error occurred:", e)

if all_scores:
  average_score = {'compound': sum(score['compound'] for score in all_scores) / len(all_scores)}
  print("\nGeneral Result:", average_score)

else:
  print("No sentiment scores calculated. Check your input data.")
  