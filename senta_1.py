import paddlehub as hub
import pandas as pd

skep = hub.Module(name="ernie_skep_sentiment_analysis")

df = pd.read_excel("data/db_2_full.xlsx")
context = df['context'].tolist()

attitude = skep.predict_sentiment(context, use_gpu=True)
attitude = [x['positive_probs'] for x in attitude]

df['attitude'] = attitude
df.to_excel("data/db_2_full.xlsx", index=False)
