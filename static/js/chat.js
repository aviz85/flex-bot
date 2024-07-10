
async function startChatWithBot(botId) {
    currentChatbotId = botId;
    await showPage('chat');
    document.getElementById('chatbot-select').value = botId;
    updateChatbotName(botId);
    await createNewThread(botId);
}

async function createNewThread(botId) {
    try {
        const response = await fetch('/chat/create_thread', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chatbot_id: botId }),
        });
        const data = await response.json();
        currentThreadId = data.thread_id;
        document.getElementById('chat-messages').innerHTML = '';
        showToast('New chat thread created!', 'success');
    } catch (error) {
        console.error('Error creating chat thread:', error);
        showToast('Error creating chat thread. Please try again.', 'error');
    }
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message && currentChatbotId && currentThreadId) {
        addMessageToChat('user', message);
        userInput.value = '';

        try {
            const response = await fetch('/chat/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chatbot_id: currentChatbotId,
                    thread_id: currentThreadId,
                    content: message
                }),
            });
            const data = await response.json();
            addMessageToChat('bot', data.content[0].text.value);
        } catch (error) {
            console.error('Error sending message:', error);
            showToast('Error sending message. Please try again.', 'error');
        }
    }
}

function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateChatbotName(botId) {
    const chatHeader = document.getElementById('chat-header');
    const chatBotNameSpan = document.getElementById('chat-bot-name');
    
    if (!chatHeader || !chatBotNameSpan) {
        console.warn('Chat header or bot name elements not found in the DOM');
        return;
    }
    
    if (botId) {
        const bot = bots.find(b => b.id === botId);
        if (bot) {
            chatBotNameSpan.textContent = bot.name;
            chatHeader.style.display = 'block';
        } else {
            chatBotNameSpan.textContent = 'Unknown Bot';
            chatHeader.style.display = 'block';
        }
    } else {
        chatBotNameSpan.textContent = 'Select a Chatbot';
        chatHeader.style.display = 'none';
    }
}

// Initialize markdown-it
const md = window.markdownit();

let sendingMessage = false;

function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    // Parse markdown and set innerHTML
    messageElement.innerHTML = md.render(message);
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showLoadingMessage() {
    const chatMessages = document.getElementById('chat-messages');
    const loadingElement = document.createElement('div');
    loadingElement.classList.add('loading');
    loadingElement.innerHTML = '<span>.</span><span>.</span><span>.</span>';
    chatMessages.appendChild(loadingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingElement;
}

async function sendMessage() {
    if (sendingMessage) return;

    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message === '') return;

    addMessageToChat('user', message);
    userInput.value = '';

    sendingMessage = true;
    const loadingElement = showLoadingMessage();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        loadingElement.remove();
        
        if (data && data.response) {
            addMessageToChat('bot', data.response);
        } else {
            addMessageToChat('bot', 'Sorry, something went wrong.');
        }
    } catch (error) {
        console.error('Error:', error);
        loadingElement.remove();
        addMessageToChat('bot', 'Sorry, something went wrong.');
    } finally {
        sendingMessage = false;
    }
}

function clearChat() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    
    // Clear chat history on the server
    fetch('/reset', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            console.log('Chat history cleared');
        } else {
            console.error('Failed to clear chat history');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('send-message').addEventListener('click', sendMessage);
    document.getElementById('clear-chat').addEventListener('click', clearChat);
    document.getElementById('user-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});