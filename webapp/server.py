from flask import Flask, request,  render_template
import os
import sqlite3
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai.chat_models import ChatOpenAI

#environment setup
os.environ['OPENAI_API_KEY'] = "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"  ## thiw is wrong key : use a new one

# database connections setup and llm setup
db = SQLDatabase.from_uri("sqlite:///./Chinook.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm=llm, db=db, agent_type="openai-tools", verbose=True)

# Create a Flask application instance
app = Flask(__name__)

# Define a route (endpoint) using the `@app.route` decorator
@app.route('/db-chatbot')
def index():
    return render_template("index.html")

@app.route('/api/db-chatbot', methods=['POST'])
def db_chatbot_rest():
    data = request.json
    prompt = data['prompt']
    result = agent_executor.invoke(prompt)
    return {'result': result['output']}

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
