#storage_module.py

import os
import uuid
import json
import logging
from typing import List, Dict, Optional, Union
from models import Chatbot, Thread, Message, ContentItem, TextContent

# Import logging configuration
import config

logger = logging.getLogger(__name__)

def to_json_serializable(obj):
    """Convert an object to a JSON serializable format."""
    if isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_serializable(v) for v in obj]
    elif hasattr(obj, 'to_dict'):
        return obj.to_dict()
    else:
        return obj

class Storage:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.project_root, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.collections = {
            'chatbots': os.path.join(self.data_dir, 'chatbots.json'),
            'threads': os.path.join(self.data_dir, 'threads.json'),
            'messages': os.path.join(self.data_dir, 'messages.json')
        }

        self.data = {
            'chatbots': self.read('chatbots'),
            'threads': self.read('threads'),
            'messages': self.read('messages')
        }

    def read(self, collection: str) -> dict:
        """Read data from a JSON file."""
        filepath = self.collections[collection]
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON from {filepath}. Initializing empty data.")
                return {}
        else:
            return {}

    def save(self, collection: str):
        """Save data to a JSON file."""
        filepath = self.collections[collection]
        data = self.data[collection]

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def create_chatbot(self, chatbot_type_id: str, name: str, settings: dict) -> Chatbot:
        chatbot_id = f"chatbot_{uuid.uuid4().hex[:6]}"
        chatbot = Chatbot(id=chatbot_id, chatbot_type_id=chatbot_type_id, name=name, settings=settings)
        self.data['chatbots'][chatbot_id] = chatbot.to_dict()
        self.save('chatbots')
        logger.debug(f"Created chatbot: {chatbot}")
        return chatbot

    def get_chatbot(self, chatbot_id: str, format: str = 'object') -> Optional[Union[Chatbot, Dict, str]]:
        chatbot_data = self.data['chatbots'].get(chatbot_id)
        if chatbot_data:
            if format == 'object':
                return Chatbot(**chatbot_data)
            elif format == 'dict':
                return chatbot_data
            elif format == 'json':
                return json.dumps(chatbot_data)
            else:
                raise ValueError("Invalid format. Use 'object', 'dict', or 'json'.")
        return None

    def update_chatbot_settings(self, chatbot_id: str, new_settings: dict):
        chatbot = self.get_chatbot(chatbot_id, format='object')
        if chatbot:
            chatbot.settings.update(new_settings)
            if 'name' in new_settings:
                chatbot.name = new_settings['name']
            self.data['chatbots'][chatbot_id] = chatbot.to_dict()
            self.save('chatbots')
            logger.debug(f"Updated settings for chatbot {chatbot_id}: {new_settings}")
        else:
            raise ValueError(f"Chatbot with id {chatbot_id} not found")

    def get_all_chatbot_types(self) -> List[str]:
        bots_dir = os.path.join(self.project_root, 'bots')
        if not os.path.exists(bots_dir):
            raise FileNotFoundError(f"Bots directory not found at {bots_dir}")
        return [d for d in os.listdir(bots_dir) if os.path.isdir(os.path.join(bots_dir, d))]
 
    def get_all_chatbots(self, format: str = 'object') -> List[Union[Chatbot, Dict, str]]:
        chatbots = [Chatbot(**chatbot_data) for chatbot_data in self.data['chatbots'].values()]
        if format == 'object':
            return chatbots
        elif format == 'dict':
            return [chatbot.to_dict() for chatbot in chatbots]
        elif format == 'json':
            return json.dumps([chatbot.to_dict() for chatbot in chatbots])
        else:
            raise ValueError("Invalid format. Use 'object', 'dict', or 'json'.")
  
    def create_thread(self, chatbot_id: str, metadata: dict = None) -> Thread:
        thread = Thread(chatbot_id, metadata=metadata or {})
        thread_dict = thread.to_dict()
        thread_dict['chatbot_id'] = chatbot_id  # Add chatbot_id to the thread data
        self.data['threads'][thread.id] = thread_dict
        self.save('threads')
        logger.debug(f"Created thread: {thread}")
        return thread

    def get_thread(self, thread_id: str, format: str = 'object') -> Optional[Union[Thread, Dict, str]]:
        thread_data = self.data['threads'].get(thread_id)
        if thread_data:
            if format == 'object':
                return Thread(**thread_data)
            elif format == 'dict':
                return thread_data
            elif format == 'json':
                return json.dumps(thread_data)
            else:
                raise ValueError("Invalid format. Use 'object', 'dict', or 'json'.")
        return None

    def get_all_threads(self, format: str = 'object') -> List[Union[Thread, Dict, str]]:
        logger.info(f"get_all_threads called with format: {format}")
        if format == 'object':
            return [Thread(**thread_data) for thread_data in self.data['threads'].values()]
        elif format == 'dict':
            return list(self.data['threads'].values())  # Return the dictionary values directly
        elif format == 'json':
            return json.dumps(list(self.data['threads'].values()))
        else:
            raise ValueError("Invalid format. Use 'object', 'dict', or 'json'.")
        
    def create_message(self, thread_id: str, role: str, content: str, metadata: dict = None) -> Message:
        message = Message(
            role=role,
            content=[ContentItem(text=TextContent(content))],
            thread_id=thread_id,
            metadata=metadata or {}
        )
        self.data['messages'][message.id] = message.to_dict()

        thread_data = self.data['threads'].get(thread_id)
        if thread_data:
            thread = Thread.from_dict(thread_data)
            thread.add_message(message)
            self.data['threads'][thread_id] = thread.to_dict()
        else:
            # If the thread doesn't exist, create a new one
            thread = Thread(
                id=thread_id,
                created_at=int(time.time()),
                metadata={},
                messages=[message],
                chatbot_id=thread_id  # Assuming chatbot_id is the same as thread_id
            )
            self.data['threads'][thread_id] = thread.to_dict()

        self.save('threads')
        self.save('messages')
        logger.debug(f"Created message: {message}")
        return message
    
    def get_message(self, message_id: str, format: str = 'object') -> Optional[Union[Message, Dict, str]]:
        message_data = self.data['messages'].get(message_id)
        if message_data:
            if format == 'object':
                return Message(**message_data)
            elif format == 'dict':
                return message_data
            elif format == 'json':
                return json.dumps(message_data)
            else:
                raise ValueError("Invalid format. Use 'object', 'dict', or 'json'.")
        return None

    def get_thread_messages(self, thread_id: str, format: str = 'dict') -> List[Dict]:
        messages = [msg for msg in self.data['messages'].values() if msg['thread_id'] == thread_id]
    
        if format == 'dict':
            return messages
        elif format == 'json':
            return json.dumps(messages)
        else:
            raise ValueError("Invalid format. Use 'dict' or 'json'.")
  
    def delete_chatbot(self, chatbot_id: str):
        if chatbot_id in self.data['chatbots']:
            del self.data['chatbots'][chatbot_id]
            self.save('chatbots')
            logger.debug(f"Deleted chatbot: {chatbot_id}")
            # Optionally, delete associated threads and messages
            threads_to_delete = [thread_id for thread_id, thread in self.data['threads'].items() if thread['chatbot_id'] == chatbot_id]
            for thread_id in threads_to_delete:
                self.delete_thread(thread_id)

    def delete_thread(self, thread_id: str):
        if thread_id in self.data['threads']:
            del self.data['threads'][thread_id]
            self.save('threads')
            logger.debug(f"Deleted thread: {thread_id}")
            # Delete associated messages
            self.data['messages'] = {msg_id: msg for msg_id, msg in self.data['messages'].items() if msg['thread_id'] != thread_id}
            self.save('messages')

    def delete_message(self, message_id: str):
        if message_id in self.data['messages']:
            message = self.data['messages'][message_id]
            thread_id = message['thread_id']
            thread = self.get_thread(thread_id)
            if thread:
                thread.messages = [msg for msg in thread.messages if msg.id != message_id]
                self.data['threads'][thread_id] = thread.to_dict()
                self.save('threads')
            del self.data['messages'][message_id]
            self.save('messages')
            logger.debug(f"Deleted message: {message_id}")

    def get_messages_by_role(self, thread_id: str, role: str, format: str = 'object') -> List[Union[Message, Dict, str]]:
        thread_messages = self.get_thread_messages(thread_id, format='object')
        filtered_messages = [msg for msg in thread_messages if msg.role == role]
        if format == 'object':
            return filtered_messages
        elif format == 'dict':
            return [message.to_dict() for message in filtered_messages]
        elif format == 'json':
            return json.dumps([message.to_dict() for message in filtered_messages])
        else:
            raise ValueError("Invalid format. Use 'object', 'dict', or 'json'.")

    def archive_data(self, archive_dir: str):
        """Archive current data into a specified directory."""
        os.makedirs(archive_dir, exist_ok=True)
        for collection, filepath in self.collections.items():
            archive_filepath = os.path.join(archive_dir, os.path.basename(filepath))
            with open(filepath, 'r') as fsrc, open(archive_filepath, 'w') as fdst:
                fdst.write(fsrc.read())
        logger.debug(f"Archived data to {archive_dir}")