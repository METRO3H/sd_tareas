
import os

CHECKPOINT_FILE = "/data/generator_data/checkpoint.txt"

def save_checkpoint(i):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(i))

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 0