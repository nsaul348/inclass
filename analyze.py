import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to the SQLite database and load data
db_path = r'c:\Users\nesaul42\Downloads\feedback.db'  # Replace with the path to your .db file

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




# Step 3: Apply categorization to the comments
# Apply the combined categorization function
feedback_df['Category'] = feedback_df['comment'].apply(categorize_feedback_combined)

# Check the distribution of combined categories
print(feedback_df['Category'].value_counts())

# Save the categorized data
feedback_df.to_csv('combined_categorized_feedback.csv', index=False)

# Visualize the results
feedback_df['Category'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Combined Feedback Categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('combined_feedback_categories.png')
plt.show()


