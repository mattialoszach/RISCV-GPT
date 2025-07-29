from langchain_ollama.llms import OllamaLLM
from .prompt_builder import prompt
from utils.graphic import print_logo
#from vector import retriever

model = OllamaLLM(model="llama3") # Base Model from Ollama

chain = prompt | model # Pipeline using Langchain

exit_kw = ["/q", "/quit", "/exit"]

def chat():
    print_logo()
    print("    \033[38;5;250m↳ Type your question here (or type '/q', '/quit', '/exit' to quit):\n\033[0m")
    while True:
        question = input(">>> ")
        if question.lower() in exit_kw:
            break
        if question.lower()[0] == '/':
            print("\033[90mType your question here (or type '/q', '/quit', '/exit' to quit):\033[0m")
            continue
        
        #profiles = retriever.invoke(question) # Find relevant Vector DB entries
        #result = chain.invoke({"profiles": profiles, "question": question}) # Run Pipeline
        #print(result)
        print("\n")