from flask import Flask, render_template, request, jsonify
import os
import replicate
import importlib

app = Flask(__name__)

# Ensure the API token is set in the environment

# Get the API token from the environment variable
api_token = os.getenv("REPLICATE_API_TOKEN")
if not api_token:
    raise ValueError("API token is not set in the environment!")

os.environ["REPLICATE_API_TOKEN"] = api_token

# Reload the replicate module to access the updated environment variable
importlib.reload(replicate)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_oracle():
    user_question = request.json.get('question')

    # Using the replicate API to stream responses
    try:
        output = replicate.stream(
            "meta/meta-llama-3-70b-instruct",  # Model ID
            input={
                "top_k": 0,
                "top_p": 0.9,
                "prompt": f"Please reply only with the prophecy.{user_question}",
                "max_tokens": 512,
                "min_tokens": 0,
                "temperature": 0.6,
                "system_prompt": "You are a mystical oracle offering prophetic insights. You are an AI oracle with the voice of an ancient prophet. Offer guidance through crafted prophecies, using poetic, mysterious, and metaphorical language.",
                "length_penalty": 1,
                "stop_sequences": "<|end_of_text|>,<|eot_id|>",
                "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a mystical oracle offering prophetic insights.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                "presence_penalty": 1.15,
                "log_performance_metrics": False
            },
        )
        return jsonify({'response': output})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
