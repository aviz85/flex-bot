// Global variables
let currentPage = 'bots-library';
let bots = [];
let threads = [];
let currentChatbotId = null;
let currentThreadId = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadChatbotTypes();
    showPage('bots-library');
    addEventListeners();
});

async function startChatWithBot(botId) {
    try {
        // Set the current chatbot ID
        currentChatbotId = botId;

        // Update the UI to reflect the selected chatbot
        document.getElementById('chatbot-select').value = botId;
        updateChatbotName(botId);
        await showPage('chat');

        // Clear the chat messages area
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';

        // Disable the chat input and send button while initializing
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-message');
        userInput.disabled = true;
        sendButton.disabled = true;

        // Show a loading message or spinner
        showToast('Initializing chat...', 'info');

        // Create a new thread for this chat session
        await createNewThread(botId);

        // Enable the chat input and send button
        userInput.disabled = false;
        sendButton.disabled = false;

        // Focus on the chat input
        userInput.focus();

        // Show a welcome message or instructions
        const welcomeMessage = `Chat started with ${getBotName(botId)}. Type your message and press Enter to send.`;
        addMessageToChat('system', welcomeMessage);

        // Optionally, you could fetch and display any initial messages or prompts from the server here

        showToast('Chat session initialized successfully!', 'success');
    } catch (error) {
        console.error('Error starting chat with bot:', error);
        showToast('Failed to start chat session. Please try again.', 'error');

        // Reset the UI in case of error
        currentChatbotId = null;
        document.getElementById('chatbot-select').value = '';
        updateChatbotName(null);
    }
}

// Helper function to get bot name (implement this based on your data structure)
function getBotName(botId) {
    const bot = bots.find(b => b.id === botId);
    return bot ? bot.name : 'Unknown Bot';
}

function addEventListeners() {
    document.getElementById('createBotBtn').addEventListener('click', createBot);
    document.getElementById('send-message').addEventListener('click', sendMessage);
    document.getElementById('user-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

function addStartChatListeners() {
    document.querySelectorAll('.start-chat').forEach(button => {
        button.addEventListener('click', (e) => {
            const botId = e.target.closest('.start-chat').getAttribute('data-bot-id');
            startChatWithBot(botId);
        });
    });
}

function addEditBotListeners() {
    document.querySelectorAll('.edit-bot').forEach(button => {
        button.addEventListener('click', (e) => {
            const botId = e.target.closest('.edit-bot').getAttribute('data-bot-id');
            showPage('settings');
            document.getElementById('botSelect').value = botId;
            loadBotSettings();
        });
    });
}

function addBotCardListeners() {
    addStartChatListeners();
    addEditBotListeners();
    addDeleteBotListeners();
}

function addStartChatListeners() {
    document.querySelectorAll('.start-chat').forEach(button => {
        button.addEventListener('click', (e) => {
            const botId = e.target.closest('.start-chat').getAttribute('data-bot-id');
            startChatWithBot(botId);
        });
    });
}

function addDeleteBotListeners() {
    document.querySelectorAll('.delete-bot').forEach(button => {
        button.addEventListener('click', async (e) => {
            const botId = e.target.closest('.delete-bot').getAttribute('data-bot-id');
            if (confirm('Are you sure you want to delete this bot?')) {
                try {
                    const response = await fetch(`/bot/delete/${botId}`, { method: 'DELETE' });
                    if (response.ok) {
                        showToast('Bot deleted successfully', 'success');
                        loadBots();
                    } else {
                        const data = await response.json();
                        showToast(`Failed to delete bot: ${data.message}`, 'error');
                    }
                } catch (error) {
                    console.error('Error deleting bot:', error);
                    showToast('Error deleting bot. Please try again.', 'error');
                }
            }
        });
    });
}


