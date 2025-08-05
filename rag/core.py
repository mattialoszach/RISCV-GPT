from langchain_ollama.llms import OllamaLLM
import threading
from .prompt_builder import prompt
from utils.graphic import BLUE, YELLOW, RESET
from utils.graphic import print_logo, draw_box, spinner
from config.config import setup
#from vector import retriever

info_model, model_name = setup()
model = OllamaLLM(model=model_name) # Base Model from Ollama

chain = prompt | model # Pipeline using Langchain

exit_kw = ["/q", "/quit", "/exit"]

def chat():
    print_logo()
    print(info_model)
    print("    \033[38;5;250m↪ Type your question here (or type '/q', '/quit', '/exit' to quit):\n\033[0m")

    while True:
        question = input(f"{YELLOW}❯ {RESET}").strip()
        if question.lower() in exit_kw:
            print("\n    \033[38;5;250m↪ Goodbye! See you soon.\033[0m\n")
            break
        if question.startswith("/"):
            print("\n    \033[38;5;250m↪ Type your question here (or type '/q', '/quit', '/exit' to quit):\n\033[0m")
            continue
        if not question:
            continue

        print()  # Formatting

        # Start Spinner Thread
        spinner.stop_flag = False
        t = threading.Thread(target=spinner)
        t.start()

        result = chain.invoke({"context": "Hello world!", "question": question})

        # Finish Spinner Thread
        spinner.stop_flag = True
        t.join()

        # Output LLM response
        draw_box(result)