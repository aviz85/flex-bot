let chatbotId = null;
let threadId = null;
const botTypes = ['echo_bot', 'reverse_bot', 'uppercase_bot'];

async function loadBotLibrary() {
    const response = await fetch('/get_bots');
    const bots = await response.json();
    const botsList = document.getElementById('botsList');
    botsList.innerHTML = '';

    bots.forEach(bot => {
        const botCard = createBotCard(bot);
        botsList.appendChild(botCard);
    });
}

function createBotCard(bot) {
    const card = document.createElement('div');
    card.className = 'bot-card';
    card.innerHTML = `
        <img src="/static/images/${bot.chatbot_type_id}/thumbnail.png" alt="${bot.chatbot_type_id} thumbnail" class="bot-thumbnail">
        <div class="bot-info">
            <div class="bot-name">${bot.name}</div>
            <div class="bot-type">${bot.chatbot_type_id}</div>
        </div>
        <div class="bot-actions">
            <button onclick="selectBot('${bot.id}')" class="bot-action-btn">Chat</button>
            <button onclick="editBot('${bot.id}')" class="bot-action-btn">Edit</button>
            <button onclick="deleteBot('${bot.id}')" class="bot-action-btn">Delete</button>
        </div>
    `;
    return card;
}

async function selectBot(botId) {
    chatbotId = botId;
    await createThread();
    document.getElementById('chat').classList.remove('hidden');
    document.getElementById('bots-library').classList.add('hidden');
    refreshThread();
}

async function createBot() {
    const botType = document.getElementById('botType').value;
    const botName = document.getElementById('botName').value;
    const response = await fetch('/create_bot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chatbot_type_id: botType, name: botName }),
    });
    const data = await response.json();
    await loadBotLibrary();
    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('createBotModal'));
    modal.hide();
}

async function editBot(botId) {
    // Implement edit bot functionality
    console.log('Edit bot:', botId);
}

async function deleteBot(botId) {
    if (confirm('Are you sure you want to delete this bot?')) {
        await fetch(`/delete_bot/${botId}`, { method: 'DELETE' });
        await loadBotLibrary();
    }
}

async function createThread() {
    const response = await fetch('/create_thread', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chatbot_id: chatbotId }),
    });
    const data = await response.json();
    threadId = data.thread_id;
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message) {
        addMessageToChat('user', message);
        userInput.value = '';
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: message, chatbot_id: chatbotId, thread_id: threadId }),
        });
        const data = await response.json();
        addMessageToChat('bot', data.content[0].text.value);
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

async function refreshThread() {
    const response = await fetch(`/get_thread?thread_id=${threadId}`);
    const data = await response.json();
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
    data.messages.forEach(message => {
        addMessageToChat(message.role === 'user' ? 'user' : 'bot', message.content[0].text.value);
    });
}

window.onload = async function() {
    await loadBotLibrary();
    document.getElementById('createBotBtn').addEventListener('click', createBot);
};

document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Add event listeners for navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const targetPage = this.getAttribute('data-page');
        document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
        document.getElementById(targetPage).classList.remove('hidden');
    });
});