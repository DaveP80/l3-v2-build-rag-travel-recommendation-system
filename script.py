import psycopg2
from sentence_transformers import SentenceTransformer
import config

# This script updates the embeddings for all the data on the mountains vs beaches database.
# Initialize the Sentence Transformer model
model = SentenceTransformer('all-mpnet-base-v2')
# Connect to your database
conn = psycopg2.connect(
        user=config.Config.USER,
        password=config.Config.PASSWORD,
        host=config.Config.HOST,
        port=config.Config.PORT,
        dbname=config.Config.DBNAME
    )
cur = conn.cursor()
# Fetch data
# 13 cols
cur.execute("""SELECT id, "Age", "Gender", "Income", "Education_Level", "Travel_Frequency", "Preferred_Activities",
            "Vacation_Budget", "Location", "Proximity_to_Mountains", "Proximity_to_Beaches", "Favorite_Season",
            "Pets", "Environmental_Concerns" FROM mountains_vs_beaches where _vector is NULL;""")
rows = cur.fetchall()
for row in rows:
    record_id = row[0]
    row_item = [str(field) for field in row[1:]]
    for i,j in enumerate(row_item):
        if j == None:
            row_item[i] = ""
            continue
        if i == 0:
            row_item[i] = f"This person age is {j}"
        if i == 1:
            row_item[i] = f"Gender: {j}"
        if i == 2:
            row_item[i] = f"Income: {j}"
        if i == 3:
            row_item[i] = f"Education level: {j}"
        if i == 4:
            row_item[i] = f"travel frequency: {j}"
        if i == 5:
            row_item[i] = f"preferred activities is {j}"
        if i == 6:
            row_item[i] = f"vacation budget is {j}"
        if i == 7:
            row_item[i] = f"the location is {j}"
        if i == 8:
            row_item[i] = f"proximity to mountains is {j}"
        if i == 9:
            row_item[i] = f"proximity to beaches is {j}"
        if i == 10:
            row_item[i] = f"favorite season is {j}"
        if i == 11:
            ans = "yes"
            if j == 0 or j == "0":
                ans = "no"
            row_item[i] = f"pets is a {ans}"
        if i == 12:
            p_ans = "yes"
            if j == 0 or j == "0":
                p_ans = "no"
            row_item[i] = f"environmental concerns is a {p_ans}"
    # If row from the database has lots of information in it.
    if len(row_item) > 7:
        concatenated_text = ' '.join(row_item)  # Concatenate and convert to string
        print(concatenated_text)
        embedding = model.encode([concatenated_text], show_progress_bar=False)
        # Update the record with the embedding
        cur.execute("UPDATE mountains_vs_beaches SET _vector = %s WHERE id = %s", (embedding.tolist()[0], record_id))
        conn.commit()
# Close connections
cur.close()
conn.close()