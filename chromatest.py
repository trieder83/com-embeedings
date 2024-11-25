import asyncio
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # beerere multilantuage
#model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

# Initialize default embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

# Initialize a sentence transformer embedding function
#embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
#    model_name="all-MiniLM-L6-v2"
#)

# Async main function
async def main():
    # Setup client to connect to your Chroma server
    client = await chromadb.AsyncHttpClient(host='localhost', port=8000)

    # Get or create a collection
    #collection = await client.get_or_create_collection(name="docs", embedding_function=embedding_function)
    collection = await client.get_or_create_collection(name="docs")
    #collection = await client.get_or_create_collection(name="docs2", embedding_function=embedding_function)

    # Add some documents to the collection
    documents = [
        "type: sms, text: my mother eats weed.",
        "type: sms, text: my mother is sick.",
        "type: sms, text: wanna buy weed?",
        "type: sms, text: do you smoke",
        "type: sms, text: how much is it",
        "type: sms, text: rauchst du gras",
        "type: sms, text: คุณสูบบุหรี่หรือเปล่า ",
        "type: sms, text: ตาย เอพเฟล คอมเมน มอร์เกน",
        "type: sms, text: هل تدخن الحشيش" ,
        "type: email, text: was macht deine mutter? ",
        "type: email, text: wenn treffen wir uns?",
        "type: email, text: mittags um 10 uhr, bring grass mit",
        "type: email, text: tu fumes de l'herbe ?",
        "type: email, on peut se retrouver derrière la gare pour vendre notre herbe et fumer un joint.",
        "type: radio, die polizei kommt, rennt weg und werft das grass weg!",
        "type: sms, text: die äpfel kommen morgen",
        "type: sms, text: die äpfel kommen morgen",
    ]
    #ids = ["1", "2", "3","4"]
    ids = [str(i + 1) for i in range(len(documents))]
    await collection.delete(ids)
    #metadatas = [{"topic": "nature"}, {"topic": "technology"}, {"topic": "education"}]
    #metadatas = [{"type": "nature"}, {"topic": "technology"}, {"topic": "education"}]
    embeddings = model.encode(documents)

    #await collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)
    await collection.add(documents=documents, ids=ids, embeddings=embeddings)
    print("Documents added to the collection.")

    # Query the collection
    #query_text = "sms wer raucht grass?"
    #query_text = "email wer raucht grass?"
    #query_text = "rauchst du marihuana?"
    query_text = "apfel lieferung"
    print(f"Query: {query_text}")
    query_embedding = model.encode([query_text])
    #results = await collection.query(query_texts=[query_text], n_results=2)
    results = await collection.query(query_embeddings=query_embedding, n_results=3)

    # Display results
    print("Query results:")
    for document, metadata in zip(results["documents"], results["metadatas"]):
        print(f"Document: {document}, Metadata: {metadata}")

    print("test raw embeddings")
    # Compute embeddings explicitly using the embedding function
    #embeddings = embedding_function.generate_embeddings(documents)
    # Print vector representation of each document
    print("Vector representations of the documents:")
    #for doc, vector in zip(documents, embeddings):
    #    print(f"Text: {doc}\nVector: {vector}\n")
    #print(f"Query: {query_embedding}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
