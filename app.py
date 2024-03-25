# Module with methods for interacting with the operating system, like creating files and directories, management of files and directories, 
# input, output, environment variables, process management, etc.
import os

# render_template() - workhorse for creating dynamic web pages. 
# It takes a template file and combines it with data from your Python code to generate the final HTML response sent to the user's browser.
# request - central piece for handling incoming data from the client (web browser) to your server-side Python code.
# Provides access to various aspects of the HTTP request, including: POST, GET, etc.
from flask import Flask, render_template, request


from openai import OpenAI
import base64

# Initializes a client object to interact with OpenAI's API. 
client = OpenAI(api_key="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")

# Creates an instance of the Flask class and assigns it to the variable app. __name___ holds the name of the current module.
app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------------------------------

# Defines root route of Flask application. Renders contents of html file called "index.html"
@app.route("/")
def index():
  return render_template("index.html")

#-----------------------------------------------------------------------------------------------------------------------------------------
# methods=["POST"] specifies that this route (/chat) only handles post requests.
@app.route("/chat", methods=["POST"])
def chat():
  # Retrieves message from an HTML form, assuming form field name is "user_input"
  user_input = request.form["user_input"]
  file_input = request.form["file_input"]

  # Creates a completion. The OpenAI model use for generating response is gpt-3.5-turbo. The role is set to user, and the content is 
  # user input. Provided text is from the user.
  response = client.chat.completions.create(messages= [{
      "role": "user",
      "content": [f"{user_input}",f"{file_input}"]
    }], model="gpt-4-vision-preview",max_tokens=300)
  
  # Processes response from OpenAI's API. Selects first choice (liekly best) and removes white space from the text.
  ai_response = response.choices[0].message.content.strip()

  # Return rendered template with the user input and AI response.
  return render_template("index.html", user_input=user_input, ai_response=ai_response)

# ---------------------------------------------------------------------------------------------------------------------------------------
# Executes when the Flask server is started. First line checks if Flask module is being run directly.
if __name__ == "__main__":
  #Runs Flask app.
  app.run(debug=True)


