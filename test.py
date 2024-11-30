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
    text = "I am the vector test"
    result = get_embedding(text)
    if result:
        #print("Embedding result:", result)
        print(f"Embedding 1 of {len(result['embeddings'])}: {result['embeddings'][0]}, dimensions: {len(result['embeddings'][0])}")
