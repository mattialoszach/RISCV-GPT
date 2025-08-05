import os
import json
from .ollama_model import choose_model
from utils.graphic import BLUE, YELLOW, RESET

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "preferences")
CONFIG_FILE = os.path.join(CONFIG_DIR, "user_config.json")

def update_config(exist):
    """Function for update/creation of config file"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR) # Create config directory, if non existing yet
    
    if exist == False:
        print(
            f"\n  {BLUE}\033[1mSetup with Ollama\033[0m{RESET}\n\n"
            "When using \033[1mRISCV-GPT\033[0m, your agent relies on a base model that must be selected. "
            "Your model runs locally via the Ollama service. Make sure Ollama is installed correctly "
            "(for more information visit 'https://ollama.com')\n\n"
            "Once you've selected a base model, it will be saved in a configuration file located at "
            "\033[1m'RISCV-GPT/preferences/config.json'\033[0m\n\n"
            "If you want to change the model later, just update the value of the 'model_name' key in that file.\n"
            "It is generally recommended to use models like 'llama3:latest'."
        )
    model_name = choose_model()
    config_data = {"model_name": model_name}

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    
    if exist == False:
        print(f"    \n↪ Config file created at {CONFIG_FILE}")

def load_config():
    """Loads existing configurations"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        return config_data.get("model_name")
    else:
        return None

# Setup model preference if non-existing or existing (/model command by demand)
def setup(exist=False):
    model_name = load_config()

    if model_name == None or exist == True: # Config file not found
        update_config(exist)
        model_name = load_config() # Config data can now be accessed
    info_model = f"    {YELLOW}\033[1m↪ Using model: \033[1m{model_name}\033[0m{RESET}"
    return info_model, model_name

if __name__ == "__main__":
    setup()