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


