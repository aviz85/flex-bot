from flask import Blueprint, request, jsonify, current_app
import importlib

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/create_thread', methods=['POST'])
def create_thread():
    chatbot_id = request.json.get('chatbot_id')
    
    if not chatbot_id:
        return jsonify({'error': 'chatbot_id is required'}), 400
    
    try:
        thread = current_app.storage.create_thread(chatbot_id)
        return jsonify({'success': True, 'thread_id': thread.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
   
@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    chatbot_id = request.json.get('chatbot_id')
    thread_id = request.json.get('thread_id')
    content = request.json.get('content')
    
    try:
        
        chatbot = current_app.storage.get_chatbot(chatbot_id, format='object')
        
        if not chatbot:
            return jsonify({'error': 'Invalid chatbot ID'}), 400
        thread = current_app.storage.get_thread(thread_id, format='object')
        if not thread:
            return jsonify({'error': 'Invalid thread ID'}), 400
        user_message = current_app.storage.create_message(
            thread_id=thread_id,
            role="user",
            content=content
        )
        module = importlib.import_module(f"bots.{chatbot.chatbot_type_id}.chatbot")
        ChatBotClass = getattr(module, 'ChatBot')
        bot_instance = ChatBotClass(chatbot.id)
        
        response_message = bot_instance.get_chat_response(user_message, thread)
        return jsonify(response_message.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@chat_bp.route('/chat', methods=['POST'])
def chat():
    chatbot_id = request.json.get('chatbot_id')
    thread_id = request.json.get('thread_id')
    content = request.json.get('content')
    
    try:
        chatbot = current_app.storage.get_chatbot(chatbot_id, format='object')
        if not chatbot:
            return jsonify({'error': 'Invalid chatbot ID'}), 400
        thread = current_app.storage.get_thread(thread_id, format='object')
        if not thread:
            return jsonify({'error': 'Invalid thread ID'}), 400
        user_message = current_app.storage.create_message(
            thread_id=thread_id,
            role="user",
            content=content
        )
        
        module = importlib.import_module(f"bots.{chatbot.chatbot_type_id}.chatbot")
        ChatBotClass = getattr(module, 'ChatBot')
        bot_instance = ChatBotClass(chatbot.id)
        
        response_message = bot_instance.get_chat_response(user_message, thread)
        
        return jsonify(response_message.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@chat_bp.route('/get_thread', methods=['GET'])
def get_thread():
    thread_id = request.args.get('thread_id')
    
    if not thread_id:
        return jsonify({'error': 'thread_id is required'}), 400
    
    try:
        # Get the thread
        thread = current_app.storage.get_thread(thread_id, format='dict')
        if not thread:
            return jsonify({'error': 'Thread not found'}), 404
        
        # Get the messages for this thread
        messages = current_app.storage.get_thread_messages(thread_id, format='dict')
        
        # Combine thread and messages
        response_data = {
            'thread': thread,
            'messages': messages
        }
        
        return jsonify(response_data)
    except Exception as e:
        current_app.logger.error(f"Error in get_thread: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
@chat_bp.route('/get_threads', methods=['GET'])
def get_threads():
    current_app.logger.info("get_threads route called")
    try:
        threads = current_app.storage.get_all_threads(format='dict')
        current_app.logger.info(f"Retrieved {len(threads)} threads")
        return jsonify(threads)
    except Exception as e:
        current_app.logger.error(f"Error in get_threads: {str(e)}")
        return jsonify({'error': str(e)}), 400