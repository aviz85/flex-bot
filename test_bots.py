import requests
import concurrent.futures
import json
import logging
import time
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5000"

# Planned conversations
CONVERSATIONS = {
    "echo_bot": [
        {"message": "Hello, Echo!", "delay": 2},
        {"message": "How are you today?", "delay": 3},
        {"message": "What's the weather like?", "delay": 2}
    ],
    "reverse_bot": [
        {"message": "Reverse me!", "delay": 2},
        {"message": "Python is awesome", "delay": 3},
        {"message": "Can you flip this?", "delay": 2}
    ],
    "uppercase_bot": [
        {"message": "make me shouty!", "delay": 2},
        {"message": "whisper this", "delay": 3},
        {"message": "KEEP THIS LOUD", "delay": 2}
    ]
}

async def create_bot(bot_id):
    logger.info(f"Creating bot: {bot_id}")
    response = requests.post(f"{BASE_URL}/create", json={"bot_id": bot_id})
    if response.status_code != 200:
        logger.error(f"Error creating bot {bot_id}: {response.text}")
        raise Exception(f"Error creating bot {bot_id}: {response.text}")
    session_id = response.json()['session_id']
    logger.info(f"Bot created with session_id: {session_id}")
    return session_id

async def chat_with_bot(session_id, message):
    logger.debug(f"Sending message to bot: {message}")
    response = requests.post(f"{BASE_URL}/chat", 
                             json={"role": "user", "content": message, "session_id": session_id})
    logger.debug(f"Received response: {response.text}")
    if response.status_code != 200:
        logger.error(f"Error response from server: {response.text}")
        raise Exception(f"Error chatting with bot: {response.text}")
    return response.json()

async def get_thread(session_id):
    logger.debug(f"Retrieving thread for session_id: {session_id}")
    response = requests.get(f"{BASE_URL}/thread", params={"session_id": session_id})
    if response.status_code != 200:
        logger.error(f"Error retrieving thread: {response.text}")
        raise Exception(f"Error retrieving thread: {response.text}")
    return response.json()

async def run_conversation(bot_id, conversation):
    try:
        logger.info(f"Starting conversation with {bot_id}...")
        session_id = await create_bot(bot_id)
        
        for item in conversation:
            message = item['message']
            delay = item['delay']
            
            logger.debug(f"Sending message to {bot_id}: {message}")
            response = await chat_with_bot(session_id, message)
            logger.debug(f"Received response from {bot_id}: {response['content'][0]['text']['value']}")
            
            await asyncio.sleep(delay)
        
        thread = await get_thread(session_id)
        logger.info(f"Conversation with {bot_id} completed. Thread history:")
        logger.info(json.dumps(thread.to_dict(), indent=2))
        
        return f"{bot_id} conversation completed successfully"
    except Exception as e:
        logger.exception(f"Error in conversation with {bot_id}: {str(e)}")
        return f"Error in conversation with {bot_id}: {str(e)}"

async def run_all_conversations():
    tasks = [run_conversation(bot_id, conversation) for bot_id, conversation in CONVERSATIONS.items()]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(run_all_conversations())