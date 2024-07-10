async function loadBotSettings() {
    const botSelect = document.getElementById('botSelect');
    const botId = botSelect.value;
    if (!botId) return;

    try {
        const response = await fetch(`/bot/get_bot_settings/${botId}?format=json`);
        const settings = await response.json();
        const botSettings = document.getElementById('botSettings');
        botSettings.innerHTML = '';

        // Add bot name input field
        botSettings.innerHTML = `
            <div class="mb-3">
                <label for="botName" class="form-label">Bot Name</label>
                <input type="text" class="form-control" id="botName" value="${settings.name || ''}">
            </div>
        `;

        // Load bot-specific settings template
        const templateResponse = await fetch(`/bot/bot_settings_template/${settings.chatbot_type_id}`);
        const template = await templateResponse.text();
        botSettings.innerHTML += template;

        // Populate form with current settings
        Object.keys(settings).forEach(key => {
            const input = document.getElementById(key);
            if (input && key !== 'name') input.value = settings[key];
        });

        // Add save button
        botSettings.innerHTML += `
            <button id="saveBotSettings" class="btn btn-primary mt-3">Save Settings</button>
        `;

        // Add event listener for save button
        document.getElementById('saveBotSettings').addEventListener('click', saveBotSettings);
    } catch (error) {
        console.error('Error loading bot settings:', error);
        showToast('Error loading bot settings. Please try again.', 'error');
    }
}

async function saveBotSettings() {
    const botId = document.getElementById('botSelect').value;
    const botName = document.getElementById('botName').value;
    const settingsInputs = document.querySelectorAll('#botSettings input:not(#botName), #botSettings select, #botSettings textarea');
    const settings = {};

    settingsInputs.forEach(input => {
        settings[input.id] = input.value;
    });

    try {
        const response = await fetch('/bot/update_settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chatbot_id: botId,
                name: botName,
                settings: settings
            }),
        });

        const result = await response.json();
        if (result.success) {
            showToast('Bot settings updated successfully', 'success');
            loadBots();
        } else {
            showToast('Failed to update bot settings: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error saving bot settings:', error);
        showToast('Error saving bot settings. Please try again.', 'error');
    }
}
