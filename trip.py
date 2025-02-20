import psycopg2
from sentence_transformers import SentenceTransformer
import config
import psycopg2.extras
import sys
import openai
import json
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

OPEN_AI_KEY = config.Config.OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY

def getTrip(args):
    prompt = args
    try:
        query_embedding = model.encode([prompt], show_progress_bar=False)
        cur.execute("""SELECT id, "Age", "Gender", "Income", "Education_Level", "Travel_Frequency", "Preferred_Activities",
            "Vacation_Budget", "Location", "Proximity_to_Mountains", "Proximity_to_Beaches", "Favorite_Season",
            "Pets", "Environmental_Concerns", _vector <-> %s AS distance FROM mountains_vs_beaches where _vector is not NULL ORDER BY distance ASC LIMIT 5""", (json.dumps(query_embedding.tolist()[0]),))
        results = cur.fetchall()
        combined_texts = []
        for row in results:
            row_item = [str(field) for field in row[1:-1]]
            for i,j in enumerate(row_item):
                if j == None:
                    row_item[i] = ""
                    continue
                if i == 0:
                    row_item[i] = f"This vacationer age is {j}"
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
                    if j == "0":
                        ans = "no"
                    row_item[i] = f"pets is a {ans}"
                if i == 12:
                    p_ans = "yes"
                    if j == "0":
                        p_ans = "no"
                    row_item[i] = f"environmental concerns is a {p_ans}"
            combined_texts.append(' '.join(row_item) + ".")
        context_paragraph = ' '.join(combined_texts)  # Concatenate and convert to string
        system_prompt = f"Use the provided context to make your response. {context_paragraph} What sort of trip would a {prompt}"
        response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct", 
        prompt=system_prompt, 
        max_tokens=450)
        return response.choices[0].text
    except Exception as e:
        return e
    finally:
        # Close connections
        cur.close()
        conn.close()

if __name__ == "__main__":
    response = getTrip(sys.argv[1])
    print(response)