from pinecone import Pinecone
from openai import OpenAI
import os
from pymongo import MongoClient



client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index(name="thematrix")
openai_api_key =  os.environ.get("OPENAI_API_KEY")
mongo_uri = os.environ.get("MONGO_URI")
mongoclient = MongoClient(host=mongo_uri)
db = mongoclient.vbot
chunks_collection = db.chunks


def create_embeddings(text, model="text-embedding-3-small"):
   
   '''Returns a list of vectors of 1536 dimensions'''

   text = text.replace("\n", " ")

   return client.embeddings.create(input = [text], model=model).data[0].embedding




def query_and_retrieve_texts(user_query, top_k=5):

    '''takes a user query
    creates vector embeddings for it, 
    queries the pinecone index with those vectors
    retrieves similar vector_ids and matches those ids with the documents in the mongodb


    Returns: list of similar texts'''

    user_query_embeddings = create_embeddings(user_query)

    query_results = index.query(vector=user_query_embeddings, top_k=top_k, include_values=False)

    similar_ids = [match["id"] for match in query_results["matches"]]

    similar_texts = []
    for _id in similar_ids:
        document = chunks_collection.find_one({'_id': _id})
        if document:
            similar_texts.append(document['text_content'])
        else:
            similar_texts.append(f"Text not found for ID {_id}")

    return similar_texts


