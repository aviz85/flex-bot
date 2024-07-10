async function loadBots() {
    try {
        const response = await fetch('/bot/get_bots?format=json');
        const responseText = await response.text();
        console.log('Raw response:', responseText);

        let data;
        try {
            data = JSON.parse(responseText);
        } catch (parseError) {
            console.error('Error parsing JSON:', parseError);
            data = [];
        }

        console.log('Parsed bot data:', data);
        
        bots = Array.isArray(data) ? data : (typeof data === 'object' ? Object.values(data) : []);
        
        const botsList = document.getElementById('botsList');
        botsList.innerHTML = '';
        
        if (bots.length === 0) {
            botsList.innerHTML = '<p>No bots available.</p>';
            return;
        }

        bots.forEach(bot => {
            console.log('Processing bot:', bot);
            if (typeof bot !== 'object') {
                console.error('Invalid bot data:', bot);
                return;
            }
            const botElement = document.createElement('div');
            botElement.className = 'col';
            botElement.innerHTML = `
                <div class="card h-100">
                    <img src="/bot_thumbnail/${bot.chatbot_type_id || 'default'}" class="card-img-top" alt="${bot.name || 'Unnamed Bot'} thumbnail">
                    <div class="card-body">
                        <h5 class="card-title">${bot.name || 'Unnamed Bot'}</h5>
                        <p class="card-text">Type: ${bot.chatbot_type_id || 'Unknown'}</p>
                        <div class="d-flex justify-content-between">
                            <button class="btn btn-primary start-chat" data-bot-id="${bot.id || ''}"><i class="fas fa-comments"></i> Start Chat</button>
                            <button class="btn btn-secondary edit-bot" data-bot-id="${bot.id || ''}"><i class="fas fa-edit"></i> Edit</button>
                            <button class="btn btn-danger delete-bot" data-bot-id="${bot.id || ''}"><i class="fas fa-trash"></i> Delete</button>
                        </div>
                    </div>
                </div>
            `;
            botsList.appendChild(botElement);
        });
        updateBotSelects();
        addBotCardListeners();
    } catch (error) {
        console.error('Error loading bots:', error);
        showToast('Error loading bots. Please try again.', 'error');
    }
}

function createBotCard(bot) {
    const card = document.createElement('div');
    card.className = 'bot-card';
    card.innerHTML = `
                <div class="card h-100">
                    <img src="/bot_thumbnail/${bot.chatbot_type_id || 'default'}" class="card-img-top" alt="${bot.name || 'Unnamed Bot'} thumbnail">
                    <div class="card-body">
                        <h5 class="card-title">${bot.name || 'Unnamed Bot'}</h5>
                        <p class="card-text">Type: ${bot.chatbot_type_id || 'Unknown'}</p>
                        <div class="d-flex justify-content-between">
                            <button class="btn btn-primary start-chat" data-bot-id="${bot.id || ''}"><i class="fas fa-comments"></i> Start Chat</button>
                            <button class="btn btn-secondary edit-bot" data-bot-id="${bot.id || ''}"><i class="fas fa-edit"></i> Edit</button>
                            <button class="btn btn-danger delete-bot" data-bot-id="${bot.id || ''}"><i class="fas fa-trash"></i> Delete</button>
                        </div>
                    </div>
                </div>
    `;    
    return card;
}

async function loadBotLibrary() {
    const response = await fetch('bot/get_bots?format=json');
    const bots = await response.json();
    const botsList = document.getElementById('botsList');
    botsList.innerHTML = '';

    bots.forEach(bot => {
        const botCard = createBotCard(bot);
        botsList.appendChild(botCard);
        addBotCardListeners();
    });
}

async function createBot() {
    const botType = document.getElementById('botType').value;
    const botName = document.getElementById('botName').value;
    const response = await fetch('bot/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chatbot_type_id: botType, name: botName }),
    });
    const data = await response.json();
    await loadBotLibrary();
    
    // Debugging: Check if the modal element is correctly selected
    const modalElement = document.getElementById('createBotModal');
    console.log(modalElement); // Check if this logs the correct modal element

    if (modalElement) {
        // Ensure the modal is correctly initialized
        const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
        console.log(modal); // Check if this logs the correct modal instance
        modal.hide();
    }
}

async function deleteBot(botId) {
    if (confirm('Are you sure you want to delete this bot?')) {
        await fetch(`bot/delete_bot/${botId}`, { method: 'DELETE' });
        await loadBotLibrary();
    }
}

async function loadChatbotTypes() {
    try {
        const response = await fetch('/bot/get_chatbot_types');
        const chatbotTypes = await response.json();
        const select = document.getElementById('botType');
        select.innerHTML = '<option value="">Select a bot type</option>';
        chatbotTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading chatbot types:', error);
        showToast('Error loading chatbot types. Please try again.', 'error');
    }
}