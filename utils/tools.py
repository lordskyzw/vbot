import os
from pymongo import MongoClient
from openai import OpenAI
from pinecone import Pinecone


mongo_uri = os.environ.get("MONGO_URI")
mongoclient = MongoClient(host=mongo_uri)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index(name="thematrix")



def create_history(conversation_id, query, vbot_response):

    '''creates a chat interaction of the user and the llm and stores it in mongodb in the following format
    user: query
    vbot: response
    
    if a history already exists, the function just appends the new interaction to the existing one and returns success or failed'''

    db = mongoclient.vbot
    conversations = db.conversations

    # Attempt to find the conversation document by its ID
    conversation = conversations.find_one({"_id": conversation_id})

    if conversation:
        # If the conversation exists, append the new interaction
        result = conversations.update_one(
            {"_id": conversation_id},
            {"$push": {"interactions": {"user": query, "vbot": vbot_response}}}
        )
        return "Success" if result.modified_count > 0 else "Failed"
    else:
        # If the conversation does not exist, create a new document
        result = conversations.insert_one(
            {"_id": conversation_id, "interactions": [{"user": query, "vbot": vbot_response}]}
        )
        return "Success" if result.acknowledged else "Failed"



   

def get_history(conversation_id):
    '''retrieves the last 5 interactions between the ai and the user from the mongodb'''
    db = mongoclient.vbot
    conversations = db.conversations

    # Retrieve the conversation document by its ID
    conversation = conversations.find_one({"_id": conversation_id})

    if conversation and "interactions" in conversation:
        # Return the last 5 interactions
        return conversation["interactions"][-5:]
    else:
        return []

def get_ai_response(history, query, semantic_docs):
    '''Args: chat_history, semantic_docs, user question
    
    Returns: string response from the llm'''
    system_prompt = 'You are a chatbot built to help users of Velocity Payments Infrastructure understand the documentation and API more. Do not answer questions outside anything to do with help with the documentation or API. You are provided with the chat history, semantic docs and the lateset user query which you must help to the best of your abilities. Be helpful and clear with your explanation as much as possible'
    prompt = f'system_prompt: {system_prompt}\nchat_history: {history}\n semantic_documents: {semantic_docs}\nuser_query: {query}'
    response = client.chat.completions.create(
        model='gpt-4-turbo-preview',
        prompt = prompt
    )
    return response['choices'][0]['text']

