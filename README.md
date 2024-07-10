# Flex-Bot: A Flexible Chatbot Framework

Flex-Bot is a versatile chatbot framework that allows you to create, manage, and interact with multiple types of chatbots through a single web interface. It's built with Flask and provides a Single Page Application (SPA) for easy interaction.

## Project Structure

```
flex-bot/
├── app.py
├── models.py
├── storage.py
├── extensions.py
├── routes/
│   ├── __init__.py
│   ├── main_routes.py
│   ├── bot_routes.py
│   └── chat_routes.py
├── bots/
│   ├── echo_bot/
│   │   ├── chatbot.py
│   │   └── templates/
│   │       └── settings.html
│   ├── reverse_bot/
│   │   ├── chatbot.py
│   │   └── templates/
│   │       └── settings.html
│   └── uppercase_bot/
│       ├── chatbot.py
│       └── templates/
│           └── settings.html
├── static/
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
└── README.md
```

## Key Components

1. `app.py`: The main Flask application file that initializes the app and registers blueprints.
2. `models.py`: Defines data models for Chatbot, Thread, and Message.
3. `storage.py`: Implements an in-memory storage system for managing chatbots, threads, and messages.
4. `extensions.py`: Initializes shared resources like the storage instance.
5. `routes/`: Contains route handlers for different parts of the application.
6. `bots/`: Houses individual chatbot implementations.
7. `static/js/app.js`: Client-side JavaScript for the SPA.
8. `templates/index.html`: The main HTML template for the SPA.

## How It Works

1. **Chatbot Creation**: Users can create new chatbots by selecting a bot type (e.g., echo_bot, reverse_bot) and providing a name. The system dynamically loads available bot types from the `bots/` directory.

2. **Chat Interface**: Users can select a chatbot and start a new chat thread. Messages are sent to the server, processed by the appropriate chatbot implementation, and responses are returned to the client.

3. **Storage**: The `Storage` class in `storage.py` manages the in-memory storage of chatbots, threads, and messages. This can be easily replaced with a database-backed solution in the future.

4. **Routing**: The application uses Flask blueprints to organize routes:
   - `main_routes.py`: Handles general routes like serving the main page.
   - `bot_routes.py`: Manages chatbot-related operations (create, update, list).
   - `chat_routes.py`: Handles chat operations (create thread, send message).

5. **Frontend**: The SPA is built using vanilla JavaScript and Bootstrap for styling. It communicates with the backend via AJAX requests.

6. **Bot Implementation**: Each bot type has its own directory in `bots/` with a `chatbot.py` file containing the bot's logic and a `settings.html` template for bot-specific settings.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flex-bot.git
   cd flex-bot
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open a web browser and navigate to `http://localhost:5000` to use the application.

## How to Use the App

### Navigating the Interface

1. **Bots Library**: View all created chatbot instances.
2. **Chat Logs**: Review past conversations with different chatbots.
3. **Settings**: Configure global settings for the application.
4. **Chat**: Interact with a selected chatbot in real-time.

### Creating and Using Chatbots

#### Understanding Chatbot Types vs. Chatbot Instances

- **Chatbot Type**: A blueprint or template for a specific kind of chatbot behavior (e.g., Echo Bot, Reverse Bot). These are defined by the folders in the `bots/` directory.
- **Chatbot Instance**: An individual chatbot created from a chatbot type. You can have multiple instances of the same chatbot type, each with its own settings and conversation history.

#### Creating a New Chatbot Instance

1. Navigate to the "Bots Library" page.
2. Click the "Create New Bot" button.
3. In the modal that appears:
   - Select a Chatbot Type from the dropdown (e.g., echo_bot, reverse_bot).
   - Give your chatbot instance a unique name.
   - Click "Create Bot".
4. Your new chatbot instance will appear in the Bots Library.

#### Chatting with a Chatbot

1. Go to the "Chat" page.
2. Select a chatbot instance from the dropdown.
3. Type your message in the input field and press Enter or click "Send".
4. View the chatbot's response in the chat window.

#### Viewing Chat History

1. Navigate to the "Chat Logs" page.
2. Select a specific chatbot instance to view its conversation history.
3. Browse through past messages and interactions.

### Creating a New Chatbot Type

To create a new type of chatbot with custom behavior:

1. Create a new directory in the `bots/` folder (e.g., `bots/my_custom_bot/`).
2. Inside this directory, create a `chatbot.py` file with the following structure:

   ```python
   from models import BaseChatBot, Message, Thread

   class ChatBot(BaseChatBot):
       def get_chat_response(self, message: Message, thread: Thread) -> Message:
           # Implement your custom chat logic here
           response_content = f"Your custom response to: {message.content[0].text.value}"
           return Message(
               role="assistant",
               content=[{"type": "text", "text": {"value": response_content}}],
               thread_id=thread.id
           )
   ```

3. (Optional) Add a `templates/settings.html` file in your bot directory if your bot requires custom settings.

4. Restart the Flask application to detect the new chatbot type.

5. Your new chatbot type will now appear in the "Create New Bot" dropdown, allowing you to create instances of this new type.

### Customizing Chatbot Behavior

- Each chatbot type can have its own unique behavior defined in its `get_chat_response` method.
- You can add custom properties and methods to your `ChatBot` class to implement more complex behaviors.
- Utilize the `self.settings` dictionary in your `ChatBot` class to access instance-specific settings.

### Tips for Effective Use

- Create multiple instances of the same chatbot type to compare different configurations.
- Use descriptive names for your chatbot instances to easily identify their purpose or behavior.
- Regularly review chat logs to understand user interactions and improve your chatbot designs.
- Experiment with different chatbot types to find the best fit for your specific use case.

By following these instructions, you can fully utilize the Flex-Bot framework to create, manage, and interact with a variety of chatbot types and instances.

## Future Enhancements

- Implement persistent storage using a database.
- Add user authentication and per-user chatbot instances.
- Improve error handling and input validation.
- Enhance the frontend with a more sophisticated UI/UX.
- Implement real-time chat using WebSockets.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.