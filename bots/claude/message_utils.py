# File: bots/claude/message_utils.py

from .config import MAX_CONVERSATION_MESSAGES

def filter_messages(messages):
    # First, ensure alternating user/assistant pattern
    filtered = ensure_alternating_roles(messages)
    
    # Then, limit the number of messages
    limited = limit_message_count(filtered)
    
    return limited

def ensure_alternating_roles(messages):
    filtered = []
    expected_role = 'user'

    for message in messages:
        if message['role'] not in ['user', 'assistant']:
            continue

        if message['role'] != expected_role:
            # Insert a dummy message to maintain the alternating pattern
            dummy_content = "Continuing the conversation..." if expected_role == 'assistant' else "Understood, please continue."
            filtered.append({'role': expected_role, 'content': dummy_content})

        filtered.append(message)
        expected_role = 'assistant' if expected_role == 'user' else 'user'

    # Ensure the conversation starts with a user message
    if filtered and filtered[0]['role'] != 'user':
        filtered.pop(0)

    # Ensure the conversation ends with a user message
    if filtered and filtered[-1]['role'] != 'user':
        filtered.append({'role': 'user', 'content': "Please continue."})

    return filtered

def limit_message_count(messages):
    if len(messages) <= MAX_CONVERSATION_MESSAGES:
        return messages

    # If we need to trim, ensure we keep an odd number of messages
    # This guarantees we always start with a user message
    trim_to = MAX_CONVERSATION_MESSAGES - 1 if MAX_CONVERSATION_MESSAGES % 2 == 0 else MAX_CONVERSATION_MESSAGES

    return messages[-trim_to:]