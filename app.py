from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
# prevent blocking from cors policy
from flask_cors import CORS

load_dotenv()
API_KEY = os.getenv('API_KEY')
PORT = int(os.getenv('PORT'))

app = Flask(__name__)
CORS(app)

openai.api_key = API_KEY

# create a post function tjat take in an array of messages
@app.route('/infer_response', methods=['POST'])
def example():
    if request.method == 'POST':
        # Retrieve the data from the request body
        # create a try catch below
        try:
            chatSlice = request.get_json()
            # transform the chatSlice roles to upper case and then from "YOU"  to "user" and any other role to "assistant"
            for i in range(len(chatSlice)):
                chatSlice[i]['role'] = chatSlice[i]['role'].upper()
                if chatSlice[i]['role'] == "YOU":
                    chatSlice[i]['role'] = "user"
                else:
                    chatSlice[i]['role'] = "assistant"

            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chatSlice
            )
            generatedText = res.choices[0].message.content

            # Return a JSON response
            return jsonify({'response': generatedText})
        except:
            # return 401
            return jsonify({'error': 'Invalid input'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)