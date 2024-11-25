import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Step 0: Download the VADER lexicon
nltk.download('vader_lexicon')

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Step 1: Connect to the SQLite database and load data
db_path = r'C:\Users\sauln\OneDrive\Documents\CSC Practice\feedback.db'  # Replace with the path to your .db file

# Connect to the database
conn = sqlite3.connect(db_path)

# Load the feedback table into a Pandas DataFrame
query = "SELECT * FROM feedback;"  # Adjust table name if necessary
feedback_df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Step 2: Define the categorization function
def categorize_feedback_combined(comment):
    comment = comment.lower()
    if any(keyword in comment for keyword in ['battery', 'charge', 'power', 'drain', 'capacity', 'lasts', 'hours']):
        return 'Battery Life'
    elif any(keyword in comment for keyword in ['price', 'cost', 'expensive', 'affordable', 'value', 'worth', 'cheap']):
        return 'Pricing and Value'
    elif any(keyword in comment for keyword in [
        'comfort', 'weight', 'wear', 'cumbersome', 'tiring',
        'setup', 'calibration', 'manual', 'instructions', 'easy to set',
        'ar', 'vr', 'modes', 'gestures', 'productivity',
        'compatibility', 'compatible', 'optimize', 'apps', 'devices'
    ]):
        return 'Product Experience'
    elif any(keyword in comment for keyword in [
        'lag', 'performance', 'slow', 'freeze', 'crash', 'buggy', 'speed', 'efficient',
        'display', 'resolution', 'visuals', 'sharp', 'color accuracy',
        'audio', 'sound', 'immersive', 'spatial', 'quality'
    ]):
        return 'Performance and Quality'
    elif any(keyword in comment for keyword in [
        'support', 'customer service', 'help', 'guidance', 'resolve',
        'app', 'software', 'ecosystem', 'library', 'developers'
    ]):
        return 'Support and Ecosystem'
    else:
        return 'Other'

# Step 3: Define a sentiment analysis function
def analyze_sentiment(comment):
    score = sia.polarity_scores(comment)['compound']
    if score > 0.05:
        return 'Positive'
    elif score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Step 4: Apply categorization and sentiment analysis
feedback_df['Category'] = feedback_df['comment'].apply(categorize_feedback_combined)
feedback_df['Sentiment'] = feedback_df['comment'].apply(analyze_sentiment)

# Step 5: Check the distribution of categories and sentiments
print(feedback_df['Category'].value_counts())
print(feedback_df['Sentiment'].value_counts())

# Save the categorized and sentiment-analyzed data
feedback_df.to_csv('categorized_sentiment_feedback.csv', index=False)

# Step 6: Visualize the results
# Category distribution
feedback_df['Category'].value_counts().plot(kind='bar', color='skyblue', title='Feedback Categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('feedback_categories.png')
plt.show()

# Sentiment distribution
feedback_df['Sentiment'].value_counts().plot(kind='bar', color='salmon', title='Feedback Sentiment')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('feedback_sentiments.png')
plt.show()
