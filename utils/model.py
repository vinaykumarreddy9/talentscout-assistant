from langchain_groq import ChatGroq
from dotenv import load_dotenv
def model():
    load_dotenv()
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    return llm

llm = model()