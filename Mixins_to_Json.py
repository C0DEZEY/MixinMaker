import os
import json
import pickle
from colorama import init, Fore, Style

# Init
init()

# Load last save
CONFIG_FILE = 'mixin_config.pkl'

def load_previous_directory():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'rb') as f:
            return pickle.load(f)
    return None

def save_directory(directory):
    with open(CONFIG_FILE, 'wb') as f:
        pickle.dump(directory, f)

# Prompt for dir
previous_directory = load_previous_directory()
if previous_directory:
    print(f"{Fore.CYAN}Previously used mixins directory: {previous_directory}{Style.RESET_ALL}")

MIXINS_DIR = input(f"{Fore.YELLOW}Enter the directory where your mixin classes are located [{previous_directory}]: {Style.RESET_ALL}") or previous_directory
MOD_ID = input(f"{Fore.CYAN} Please Enter the MODID of your project:  {Style.RESET_ALL}")
AUTHOR = input(f"{Fore.YELLOW} Please Enter the auther:  {Style.RESET_ALL}")

if not MIXINS_DIR:
    print(f"{Fore.RED}No directory provided. Exiting.{Style.RESET_ALL}")
    exit(1)
else:
    save_directory(MIXINS_DIR)

# Output File 
OUTPUT_FILE = f'src/main/resources/mixins.{MOD_ID}.json'

def get_mixin_classes(mixins_dir):
    mixin_classes = []
    client_mixins = []
    for root, _, files in os.walk(mixins_dir):
        print(f"{Fore.CYAN}🔍 Searching folder: {root}{Style.RESET_ALL}")
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                print(f"{Fore.BLUE}📄 Processing file: {file_path}{Style.RESET_ALL}")
                with open(file_path, 'r') as f:
                    content = f.read()
                    if '@Mixin' in content:
                        mixin_class = file_path.replace(mixins_dir + os.sep, '')
                        mixin_class = mixin_class.replace('.java', '')
                        mixin_class = mixin_class.replace(os.sep, '.')
                        if '@Client' in content or 'client' in mixin_class.lower():
                            client_mixins.append(mixin_class)
                            print(f"{Fore.GREEN}✔️ Found client mixin: {mixin_class}{Style.RESET_ALL}")
                        else:
                            mixin_classes.append(mixin_class)
                            print(f"{Fore.GREEN}✔️ Found mixin: {mixin_class}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}❌ No @Mixin annotation found in {file_path}{Style.RESET_ALL}")
    return mixin_classes, client_mixins

def generate_mixins_json(mixins_classes, client_mixins, output_file):
    mixins_json = {
        "required": True,
        "package": f"{AUTHOR}.{MOD_ID}.mixin",
        "compatibilityLevel": "JAVA_8",
        "mixins": mixins_classes,
        "client": client_mixins,
        "injectors": {
            "defaultRequire": 1
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(mixins_json, f, indent=4)

if __name__ == "__main__":
    mixin_classes, client_mixins = get_mixin_classes(MIXINS_DIR)
    generate_mixins_json(mixin_classes, client_mixins, OUTPUT_FILE)
    print(f"{Fore.MAGENTA}Generated {OUTPUT_FILE} with {len(mixin_classes)} mixins and {len(client_mixins)} client mixins.{Style.RESET_ALL}")
