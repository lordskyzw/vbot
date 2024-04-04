# VBOT 🧟‍♂️

This Flask chat application provides an API for a chat interface that integrates with an AI model to assist users with inquiries about the Velocity Payments Infrastructure documentation and API. The application supports user authentication and maintains a history of interactions for each conversation.

## Features

- **AI Integration**: Leverages an AI model to generate responses based on the user's queries and context provided by the documentation.
- **Authentication**: Secures endpoints using HTTP Basic Authentication to ensure that only authorized users can access the chat service.
- **Conversation History**: Maintains a record of past interactions to provide context for AI responses and improve the user experience.

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- Flask
- Flask-CORS
- Flask-HTTPAuth
- MongoDB
- OpenAI API Key
- Pinecone API Key

### Installation

1. **Clone the repository**

   
   `git clone https://github.com/lordskyzw/vbot.git`

   `cd vbot`
  

2. **Set up a virtual environment** (optional but recommended)

  
   `python -m venv vbot`
   
   `source vbot/bin/activate` 
    #### On Windows use: 
    `vbot\\Scripts\\activate\`
   

3. **Install required packages**

  
   `pip install -r requirements.txt`
  

4. **Set environment variables**

   Create a \`.env\` file in the project root and add the following variables:

  
   `OPENAI_API_KEY='your_openai_api_key'`

   `PINECONE_API_KEY='your_pinecone_api_key'`
  

5. **Frontend Implementation**

    find how to interact with the api in:

   
    `docs/frontendexample.js`
    