import os
import shutil

def update_app_py():
    with open('app.py', 'r') as file:
        content = file.read()
    
    # Change 'init' to 'create'
    content = content.replace('@app.route(\'/init\'', '@app.route(\'/create\'')
    content = content.replace('def init():', 'def create():')
    content = content.replace('Failed to initialize chatbot', 'Failed to create chatbot')
    
    with open('app.py', 'w') as file:
        file.write(content)

def update_test_bots_py():
    with open('test_bots.py', 'r') as file:
        content = file.read()
    
    # Change 'init' to 'create'
    content = content.replace('init_response = requests.post(f"{base_url}/init"',
                              'create_response = requests.post(f"{base_url}/create"')
    content = content.replace('if init_response.status_code != 200:',
                              'if create_response.status_code != 200:')
    content = content.replace('return f"Error initializing {bot_id}: {init_response.text}"',
                              'return f"Error creating {bot_id}: {create_response.text}"')
    content = content.replace('session_id = init_response.json()[\'session_id\']',
                              'session_id = create_response.json()[\'session_id\']')
    
    with open('test_bots.py', 'w') as file:
        file.write(content)

def update_bot_structure():
    bots = ['echo_bot', 'reverse_bot', 'uppercase_bot']
    
    for bot in bots:
        # Create bot directory
        os.makedirs(f'bots/{bot}', exist_ok=True)
        
        # Read existing bot file
        with open(f'bots/{bot}.py', 'r') as file:
            content = file.read()
        
        # Create new chatbot.py in bot directory
        with open(f'bots/{bot}/chatbot.py', 'w') as file:
            file.write(content)
        
        # Remove old bot file
        os.remove(f'bots/{bot}.py')

def main():
    update_app_py()
    update_test_bots_py()
    update_bot_structure()
    print("Project structure updated successfully.")
    print("New bot structure:")
    print("bots/")
    for bot in ['echo_bot', 'reverse_bot', 'uppercase_bot']:
        print(f"    ├── {bot}/")
        print(f"    │   └── chatbot.py")
    print("    └── ...")

if __name__ == "__main__":
    main()