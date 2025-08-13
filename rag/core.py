from langchain_ollama.llms import OllamaLLM
import threading
from utils.graphic import BLUE, YELLOW, RESET
from utils.graphic import print_logo, draw_box, spinner
from config.config import setup
from .prompt_builder import prompt, format_context_with_sources
from .vector import retriever

class ChatSession:
    def __init__(self):
        self.info_model = None
        self.model_name = None
        self.model = None
        self.chain = None
        self.exit_kw = ["/q", "/quit", "/exit"]
        self.init_model()

    def init_model(self, exist=False):
        self.info_model, self.model_name = setup(exist=exist)
        self.model = OllamaLLM(model=self.model_name, temperature=0.4)
        self.chain = prompt | self.model

    def chat(self):
        print_logo()
        print(self.info_model)
        print("    \033[38;5;250m↪ Type your question here (or type '/q', '/quit', '/exit' to quit)\033[0m")
        print("    \033[38;5;250m↪ Use '/model' to change your base model\n\033[0m")

        while True:
            question = input(f"{YELLOW}❯ {RESET}").strip()
            if question.lower() in self.exit_kw:
                print("\n    \033[38;5;250m↪ Goodbye! See you soon.\033[0m\n")
                break
            if question.lower() == "/model":
                self.info_model, self.model_name = setup(exist=True)
                self.model = OllamaLLM(model=self.model_name) # New model
                self.chain = prompt | self.model # New chain
                print("\n", self.info_model, "\n")
                continue
            if question.startswith("/"):
                print("\n    \033[38;5;250m↪ Type your question here (or type '/q', '/quit', '/exit' to quit)\033[0m")
                print("    \033[38;5;250m↪ Use '/model' to change your base model\n\033[0m")
                continue
            if not question:
                continue

            print()  # Formatting

            # Retrieve context (using RAG)
            context_docs = retriever.invoke(question) # Find relevant context using Vector DB
            metadata_source, formatted_context = format_context_with_sources(context_docs)
            
            #print(formatted_context, "\n") # Testing/Debugging RAG Results (can be removed)
            
            # Print Vector DB Search Result Metadata
            if len(metadata_source) != 0:
                print(f"  {BLUE}Using the following sources as reference:{RESET}")
                for source in metadata_source:
                    print(f"    \033[1m{BLUE}+ {source}{RESET}\033[0m")
                
            print("") # Formatting

            # LLM Inference
            # Start Spinner Thread (UI Animation)
            spinner.stop_flag = False
            t = threading.Thread(target=spinner)
            t.start()
            
            # Answer question (LLM inference using context from RAG)
            result = self.chain.invoke({"context": formatted_context, "question": question})

            # Finish Spinner Thread (UI Animation)
            spinner.stop_flag = True
            t.join()

            # Output LLM response (with UI Box)
            draw_box(result)