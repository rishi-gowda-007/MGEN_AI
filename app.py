from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

app = Flask(__name__)

SECRET_KEY = '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'

from langchain_huggingface import HuggingFaceEndpoint
os.environ["HF_API_TOKEN"]=SECRET_KEY
repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=SECRET_KEY)

@app.route("/", methods=["POST", "GET"])
def home():
    output = None
    if request.method == "POST":
        input_text = request.form.get("input")
        if input_text:
            response = llm.invoke(input_text)
            response = response.replace('\n', '<br/>')
            response = response.lstrip('?')
            output=response
            print(f"Output: {output}")  

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)