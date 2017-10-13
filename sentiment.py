import pandas as pd
import numpy as np
import time
import apis.aylienapi.aylienapiclient.textapi
import apis.alchemyapi.alchemyapi


def calculate_score(polarity, polarity_conf, r):
    if polarity == "neutral":
        return 3
    elif polarity == "negative":
        if polarity_conf > 0.5:
            return 1
        return 2
    else:
        if polarity_conf > 0.5:
            return 5
        return 4


df = pd.read_excel("data.xlsx")
text = df['reviewText'].tolist()
summary = df['summary'].tolist()
rating = df['overall'].tolist()

num_reviews = len(rating)

# # ALCHEMY
# alchemyapi = apis.alchemyapi.alchemyapi.AlchemyAPI()

# AYLIEN
# aylien = apis.aylienapi.aylienapiclient.textapi.Client("4df6473c", "f827888e31b6b52f85a6061eb3f18ad1")
# aylien = apis.aylienapi.aylienapiclient.textapi.Client("8f14979e", "4b1ff15f606a003e025a93070a822d54")
aylien = apis.aylienapi.aylienapiclient.textapi.Client("4969e38e", "f8de4ced275a6b449a677d3efeae6e5b")

# # Textalytics
# api = 'http://api.meaningcloud.com/sentiment-2.0'
# key = '6c46872fd5bded758034d0e5c6d1cf00'
# model = 'general_es' # general_es / general_es / general_fr


# AYLIEN
text_matrix = np.zeros([5,5])
sum_matrix = np.zeros([5,5])

text_fd = open('text_score.out', 'w')
sum_fd = open('sum_score.out', 'w')


i = 0
while(1):
    while(i < num_reviews):
        
        t = text[i]
        s = summary[i]
        r = int(rating[i])

        text_sentiment = aylien.Sentiment({'text': t})
    #     print(text_sentiment)
        text_polarity = text_sentiment['polarity']
        text_polarity_conf = text_sentiment['polarity_confidence']

        text_score = calculate_score(text_polarity, text_polarity_conf, r)
        text_matrix[r-1][text_score-1] += 1

        sum_sentiment = aylien.Sentiment({'text': s})
        sum_polarity = sum_sentiment['polarity']
        sum_polarity_conf = sum_sentiment['polarity_confidence']

        sum_score = calculate_score(sum_polarity, sum_polarity_conf, r)
        sum_matrix[r-1][sum_score-1] += 1
        
        print(str(text_score) + "," + str(sum_score) + "," + str(r))
        text_fd.write(str(text_score) + "," + str(r))
        sum_fd.write(str(sum_score) + "," + str(r))

        i += 1
        if i%25 == 0:
            break

    time.sleep(60)
    
text_fd.close()
sum_fd.close()



