// Make loadChatLogs function global
async function loadChatLogs() {
    console.log("loadChatLogs called");
    await loadBotLibrary();  // Load bots using the existing function
    console.log("Bots loaded, fetching threads...");
    await fetchThreads();
    console.log("Threads fetched, populating bot filter...");
    populateBotFilter();
    console.log("Bot filter populated, displaying threads...");
    displayThreads();
    console.log("Threads displayed");
}

async function fetchThreads() {
    try {
        console.log("Fetching threads...");
        const response = await fetch('/chat/get_threads');
        console.log("Fetch response:", response);
        if (!response.ok) {
            throw new Error('Failed to fetch threads');
        }
        allThreads = await response.json();
        console.log("Fetched threads:", allThreads);
    } catch (error) {
        console.error('Error fetching threads:', error);
        showToast('Error fetching chat logs. Please try again.', 'error');
    }
}

async function loadBotLibrary() {
    try {
        const response = await fetch('/bot/get_bots');
        if (!response.ok) {
            throw new Error('Failed to fetch bots');
        }
        bots = await response.json();
        console.log("Fetched bots:", bots);
    } catch (error) {
        console.error('Error fetching bots:', error);
        showToast('Error fetching bot library. Please try again.', 'error');
    }
}

function populateBotFilter() {
    const botFilter = document.getElementById('botFilter');
    botFilter.innerHTML = '<option value="">All Bots</option>';
    Object.values(bots).forEach(bot => {
        const option = document.createElement('option');
        option.value = bot.id;
        option.textContent = bot.name;
        botFilter.appendChild(option);
    });
    botFilter.addEventListener('change', displayThreads);
}

function displayThreads() {
    const threadsList = document.getElementById('threadsList');
    const selectedBotId = document.getElementById('botFilter').value;
    
    threadsList.innerHTML = '';  // Clear existing threads

    const filteredThreads = selectedBotId 
        ? Object.fromEntries(Object.entries(allThreads).filter(([_, thread]) => thread.chatbot_id === selectedBotId))
        : allThreads;

    // Group threads by chatbot
    const threadsByBot = {};
    Object.values(filteredThreads).forEach(thread => {
        if (!threadsByBot[thread.chatbot_id]) {
            threadsByBot[thread.chatbot_id] = [];
        }
        threadsByBot[thread.chatbot_id].push(thread);
    });

    // Display threads grouped by bot
    Object.entries(threadsByBot).forEach(([botId, botThreads]) => {
        const bot = bots[botId];
        const botName = bot ? bot.name : 'Unknown Bot';

        const botSection = document.createElement('div');
        botSection.className = 'bot-section mb-4';
        botSection.innerHTML = `<h3>${botName}</h3>`;

        botThreads.forEach(thread => {
            const threadElement = createThreadElement(thread);
            botSection.appendChild(threadElement);
        });

        threadsList.appendChild(botSection);
    });

    if (Object.keys(threadsByBot).length === 0) {
        threadsList.innerHTML = '<p>No chat logs found.</p>';
    }
}

function createThreadElement(thread) {
    const threadElement = document.createElement('div');
    threadElement.className = 'card mb-3';
    
    const bot = bots[thread.chatbot_id];
    const botName = bot ? bot.name : 'Unknown Bot';

    threadElement.innerHTML = `
        <div class="card-header">
            <h5 class="mb-0">
                <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#thread-${thread.id}">
                    Thread ${thread.id} - ${new Date(thread.created_at * 1000).toLocaleString()}
                </button>
            </h5>
        </div>
        <div id="thread-${thread.id}" class="collapse">
            <div class="card-body">
                <div class="thread-messages"></div>
            </div>
        </div>
    `;

    const messagesContainer = threadElement.querySelector('.thread-messages');
    threadElement.querySelector('button').addEventListener('click', () => loadThreadMessages(thread.id, messagesContainer));

    return threadElement;
}

async function loadThreadMessages(threadId, container) {
    if (container.dataset.loaded) return;  // Avoid reloading if already loaded

    try {
        const response = await fetch(`/chat/get_thread?thread_id=${threadId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch thread messages');
        }
        const data = await response.json();
        displayThreadMessages(data.messages, container);
        container.dataset.loaded = 'true';
    } catch (error) {
        console.error('Error fetching thread messages:', error);
        container.innerHTML = '<p>Error loading messages. Please try again.</p>';
    }
}

function displayThreadMessages(messages, container) {
    container.innerHTML = '';
    messages.forEach(message => {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.role}-message`;
        messageElement.textContent = message.content[0].text.value;
        container.appendChild(messageElement);
    });
}

// Event listeners and initialization
document.addEventListener('DOMContentLoaded', () => {
    const chatLogsPage = document.getElementById('chat-logs');
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                if (!chatLogsPage.classList.contains('hidden')) {
                    window.loadChatLogs();
                }
            }
        });
    });

    observer.observe(chatLogsPage, {
        attributes: true
    });
});