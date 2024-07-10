from flask import Blueprint, request, jsonify, current_app
import json


bot_bp = Blueprint('bot', __name__)

@bot_bp.route('/create', methods=['POST'])
def create_bot():
    chatbot_type_id = request.json.get('chatbot_type_id')
    name = request.json.get('name')
    settings = request.json.get('settings', {})
    
    try:
        chatbot = current_app.storage.create_chatbot(chatbot_type_id, name, settings)
        return jsonify({'success': True, 'chatbot_id': chatbot.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bot_bp.route('/update_settings', methods=['POST'])
def update_bot_settings():
    chatbot_id = request.json.get('chatbot_id')
    new_settings = request.json.get('settings', {})
    new_name = request.json.get('name')
    
    try:
        chatbot = current_app.storage.get_chatbot(chatbot_id, format='object')
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        if new_name:
            new_settings['name'] = new_name
        
        current_app.storage.update_chatbot_settings(chatbot_id, new_settings)
        
        updated_chatbot = current_app.storage.get_chatbot(chatbot_id, format='object')
        return jsonify({'success': True, 'chatbot_id': chatbot_id, 'name': updated_chatbot.name})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bot_bp.route('/get_bots', methods=['GET'])
def get_bots():
    bots = current_app.storage.get_all_chatbots(format='dict')  # Always get as dict
    
    print(f"Type of bots: {type(bots)}")
    print(f"Bots data being sent: {bots}")
    
    # Ensure we're sending a list of dicts
    if isinstance(bots, list):
        json_data = json.dumps(bots)
    else:
        json_data = json.dumps(list(bots.values()) if isinstance(bots, dict) else [])
    
    print(f"JSON being sent: {json_data}")
    
    return json_data, 200, {'Content-Type': 'application/json'}
     
@bot_bp.route('/get_chatbot_types', methods=['GET'])
def get_chatbot_types():
    chatbot_types = current_app.storage.get_all_chatbot_types()
    return jsonify(chatbot_types)

@bot_bp.route('/delete/<bot_id>', methods=['DELETE'])
def delete_bot(bot_id):
    try:
        current_app.storage.delete_chatbot(bot_id)
        return jsonify({"success": True, "message": "Bot deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@bot_bp.route('/get_bot_settings/<bot_id>', methods=['GET'])
def get_bot_settings(bot_id):
    format = request.args.get('format', 'object')
    try:
        bot = current_app.storage.get_chatbot(bot_id, format=format)
        if bot:
            if format == 'object':
                return jsonify({**bot.settings, 'name': bot.name})
            else:
                return jsonify({**bot['settings'], 'name': bot['name']})
        else:
            return jsonify({"error": "Bot not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500