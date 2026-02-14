import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent


# Load API Key

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
server = os.getenv("server")
database= os.getenv("database")

#Connect to SQL server


conn = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(conn)
db = SQLDatabase(engine)

print("✅ Connected to SQL Server!")


##Load LLM

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

#create SQL Agent

agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=False,
    handle_parsing_errors=True
)

print("🚀 SQL Automation Ready!")

#Ask Question

while True:
    question = input("\nAsk your sales question (type exit to stop): ")


    if question.lower() == "exit":
            break
    
    try:
        response = agent.invoke({"input":question})

        print("\n📊 Answer:")
        print(response["output"])
        
    except Exception as e:
         print("Error", e)
