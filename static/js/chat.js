// chat.js

let isSending = false;

// Initialize markdown-it
const md = window.markdownit();

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
    if (isSending) return;

    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-message');
    const message = userInput.value.trim();

    if (message && currentChatbotId && currentThreadId) {
        isSending = true;
        sendButton.disabled = true;
        userInput.disabled = true;

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
                    content: message,
                    role: 'user'
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.content && data.content[0] && data.content[0].text) {
                addMessageToChat('bot', data.content[0].text.value);
            } else {
                console.error('Unexpected response format:', data);
                showToast('Received an unexpected response format from the server.', 'error');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            showToast('Error sending message. Please try again.', 'error');
        } finally {
            isSending = false;
            sendButton.disabled = false;
            userInput.disabled = false;
            userInput.focus();
        }
    }
}

function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.innerHTML = md.render(message);
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

function clearChat() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    
    fetch('/chat/create_thread', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chatbot_id: currentChatbotId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.thread_id) {
            currentThreadId = data.thread_id;
            console.log('New chat thread created');
            showToast('Chat cleared and new thread created', 'success');
        } else {
            console.error('Failed to create new chat thread');
            showToast('Failed to clear chat. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error clearing chat. Please try again.', 'error');
    });
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.classList.add('toast', `toast-${type}`);
    toast.textContent = message;

    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    document.getElementById('toast-container').appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }, 100);
}

document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-message');
    const userInput = document.getElementById('user-input');
    const clearChatButton = document.getElementById('clear-chat');

    sendButton.addEventListener('click', sendMessage);
    clearChatButton.addEventListener('click', clearChat);
    
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey && !isSending) {
            event.preventDefault();
            sendMessage();
        }
    });

    userInput.addEventListener('input', function() {
        sendButton.disabled = this.value.trim() === '' || isSending;
    });

    // Initialize the toast container
    const toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    document.body.appendChild(toastContainer);
});