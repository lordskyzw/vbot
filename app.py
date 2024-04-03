from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.tools import get_history, get_ai_response, create_history
from utils.helpers import query_and_retrieve_texts
import logging
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app = Flask(__name__)
CORS(app)

@auth.verify_password
def verify_password(username: str, password: str):
    if username == 'admin' and password == 'secret':
        return True
    return False



@app.route('/chat', methods=['POST'])
@auth.login_required
def chat():

    data = request.get_json()

    conversation_id = data.conversation_id

    query = data.query

    logging.info(f'received the following data from client:\nDATA:{data}')

    logging.info(f'CONVERSATION ID: {conversation_id}\n QUERY:{query}')

    try:
        history = get_history(conversation_id=conversation_id)
        logging.info(f"====succesfully retrieved conversation history=====")
    except Exception as e:
        logging.error(f"Error in trying to retrieve history: {e}")
        return 'Error: {e}', 500
    
    try:
        semantic_docs = query_and_retrieve_texts(user_query=query)
        logging.info(f"======successfully ran query_and_retrieve_texts()=====")
    except Exception as e:
        logging.error(f"Error in trying to get semantic docs: {e}")
        return 'Error: {e}', 500

    try:
        vbot_response =  get_ai_response(history=history, query=query, semantic_docs=semantic_docs)
        create_history(conversation_id=conversation_id,query=query, vbot_response=vbot_response)
        logging.info(f"created chat history")
    except Exception as e:
        logging.error(f'ERROR! : {e}')
        return 'Error: {e}', 500

    response_object = {
        'conversation_id': conversation_id,
        'vbot_response': vbot_response,
    }

    return jsonify(response_object), 200



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5500, debug = True)
