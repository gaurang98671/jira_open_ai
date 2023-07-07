from langchain.embeddings import OpenAIEmbeddings
from jira_service import Jira_service
from langchain.vectorstores import Pinecone
import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from datetime import date
from dotenv import dotenv_values
from preprocess import Preprocessor

#Fetch env vars
env_vars = dotenv_values('.env')

token = env_vars["TOKEN"]
email = env_vars["JIRA_EMAIL"]
pinecone_api_key = env_vars["PINECONE_API_KEY"]
pinecone_region = env_vars["PINECONE_REGION"]
openai_key = env_vars["OPEN_AI_KEY"]

if __name__ == "__main__":

    jira = Jira_service(token, email)
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_region)
    index = pinecone.Index("jira")
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    vectorstore = Pinecone(index, embeddings.embed_query, "text")

    docsearch = Pinecone.from_existing_index(index_name="jira", embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0.8, max_tokens=200, openai_api_key=openai_key)
    qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)

    
    #Clear all vectors and re-ingest all data
    #vectorstore.delete(delete_all=True)
    #jira.add_by_project_id(vectorstore, "DV")
    #jira.add_by_project_id(vectorstore, "DEV")

    #Initialize query processor
    pprocessor = Preprocessor(
        name= "Gaurang Pawar"
    )

    query = input("enter query >> ")
    
    metadata = {
        "today" : date.today(),
        "my name" : "gaurang  pawar",
        "current day/today" : date.today().day,
        "current month" : date.today().month,
        "my department" : "DEVOPS",
        "my email" : 'pawargaurang1212@gmail.com'
    }
    
    while query != "kill":
        #Add some metadata with current query
        query = pprocessor.process_pronouns(query=query)
        query = pprocessor.process_time(query=query)
        query = query + "Extra context : {}".format(metadata)
        response = qa({"query" : query})
        print(response['result'] + "\n")
        query = input("enter query >> ")