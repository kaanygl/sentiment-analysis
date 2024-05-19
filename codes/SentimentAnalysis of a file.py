import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

file_path = r"C:\*"
df = pd.read_excel(file_path)

sentences = df["Column_name"].tolist()

analyzer = SentimentIntensityAnalyzer()

all_scores = []

for sentence in sentences:
    try:
        if isinstance(sentence, str):
            print("Analyzing:", sentence)

            vs = analyzer.polarity_scores(sentence)

            print("Sentiment Score:", vs)

            all_scores.append(vs)
        else:
            print("Warning: Sentence is not a string")
    except Exception as e:
        print("Error occurred:", e)


if all_scores:
    average_score = {
        "compound": sum(score["compound"] for score in all_scores) / len(all_scores)
    }

    print("\nGeneral Result:", average_score)
else:
    print("No sentiment scores calculated. Check your input data.")
