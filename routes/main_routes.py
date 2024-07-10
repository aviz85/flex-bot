from flask import Blueprint, render_template, send_from_directory
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@main_bp.route('/bot_settings_template/<chatbot_type_id>')
def bot_settings_template(chatbot_type_id):
    template_path = os.path.join('bots', chatbot_type_id, 'templates', 'settings.html')
    if os.path.exists(template_path):
        return send_from_directory(os.path.dirname(template_path), 'settings.html')
    else:
        return "Settings template not found", 404

@main_bp.route('/bot_thumbnail/<chatbot_type_id>')
def bot_thumbnail(chatbot_type_id):
    thumbnail_path = os.path.join('bots', chatbot_type_id, 'static', 'thumbnail.png')
    if os.path.exists(thumbnail_path):
        return send_from_directory(os.path.dirname(thumbnail_path), 'thumbnail.png')
    else:
        return send_from_directory('static', 'default_thumbnail.png')