import sys
import itertools
import time
import shutil
import textwrap

BLUE = "\033[34m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Introduction ASCII Logo
def print_logo():
    logo = fr"""
{BLUE}
    ██████╗ ██╗███████╗ ██████╗       ██╗   ██╗
    ██╔══██╗██║██╔════╝██╔════╝       ██║   ██║
    ██████╔╝██║███████╗██║     █████╗ ██║   ██║
    ██╔══██╗██║╚════██║██║     ╚════╝ ╚██╗ ██╔╝
    ██║  ██║██║███████║╚██████╗        ╚████╔╝ 
    ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝         ╚═══╝  
{YELLOW}
     ██████╗ ██████╗ ████████╗          
    ██╔════╝ ██╔══██╗╚══██╔══╝          
    ██║  ███╗██████╔╝   ██║             
    ██║   ██║██╔═══╝    ██║             
    ╚██████╔╝██║        ██║             
     ╚═════╝ ╚═╝        ╚═╝             
{RESET}
"""
    print(logo)

# Draw LLM response in border box
def draw_box(text, margin=2, padding=1):
    term_width = shutil.get_terminal_size((80, 20)).columns
    max_width = term_width - 2 * margin - 2 * padding - 2  # borders + padding

    wrapped_lines = []
    for paragraph in text.splitlines():
        wrapped = textwrap.wrap(paragraph, width=max_width) or [""]
        wrapped_lines.extend(wrapped)

    width = max(len(line) for line in wrapped_lines)

    print(" " * margin + f"{BLUE}┌{RESET}" + f"{BLUE}─{RESET}" * (width + 2 * padding) + f"{BLUE}┐{RESET}")
    for line in wrapped_lines:
        print(" " * margin + f"{BLUE}│{RESET}" + " " * padding + line.ljust(width) + " " * padding + f"{BLUE}│{RESET}")
    print(" " * margin + f"{BLUE}└{RESET}" + f"{BLUE}─{RESET}" * (width + 2 * padding) + f"{BLUE}┘{RESET}")
    print()

# Simple Spinner Animation
def spinner(text="Generating", margin=4):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if spinner.stop_flag:
            break
        sys.stdout.write(f"{YELLOW}\033[1m{' ' * margin}{c} {text}...\033[0m\r{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(text) + margin + 5) + "\r")  # Clear line