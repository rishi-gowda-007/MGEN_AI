from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise EnvironmentError("SECRET_KEY environment variable is not set!")

from langchain_huggingface import HuggingFaceEndpoint
repo_id= os.getenv('repo_id')
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
            # print(f"Output: {output}")  

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)