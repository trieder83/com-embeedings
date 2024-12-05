import requests

def get_embedding(text):
    url = "http://127.0.0.1:8888/embedding"
    headers = {"Content-Type": "application/json"}
    data = {"text": text}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP error codes
        return response.json()  # Parse the response as JSON
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    text = "I am the vector test. Im am sentence 2."
    #text = "CNN “Our leader forever” was a slogan one often saw in Syria during the era of President Hafez al-Assad, father of today’s Syrian president.  The prospect that the dour, stern Syrian leader would live forever was a source of dark humor for many of my Syrian friends when I lived and worked in Aleppo in the late 1980s and early 1990s.  Hafez al-Assad died in June 2000. He wasn’t immortal after all.  His regime, however, lives on under the leadership of his son Bashar al-Assad.  There were moments when the Bashar regime’s survival looked in doubt. When the so-called Arab Spring rolled across the region in 2011, toppling autocrats in Tunisia, Egypt and Libya, and mass protests broke out in Yemen, Bahrain and Syria, some began to write epitaphs for the Assad dynasty.  But Syria’s allies – Iran, Lebanon’s Hezbollah and Russia – came to the rescue. For the past few years the struggle in Syria between a corrupt, brutal regime in Damascus and a divided, often extreme opposition seemed frozen in place.  Once shunned by his fellow Arab autocrats, Bashar al-Assad was gradually regaining the dubious respectability Arab regimes afford one another."
    result = get_embedding(text)
    if result:
        #print("Embedding result:", result)
        print(f"Embedding 1 of {len(result['embeddings'])}: {result['embeddings'][0][0:10]}, dimensions: {len(result['embeddings'][0])}")
