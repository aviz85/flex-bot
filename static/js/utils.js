function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function updateBotSelects() {
    const selects = ['botFilter', 'botSelect', 'chatbot-select'];
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">All Bots</option>';
        bots.forEach(bot => {
            const option = document.createElement('option');
            option.value = bot.id;
            option.textContent = bot.name;
            select.appendChild(option);
        });
    });
}

async function loadChatbots() {
    try {
        const response = await fetch('/bot/get_bots?format=json');
        const chatbots = await response.json();
        const select = document.getElementById('chatbot-select');
        select.innerHTML = '<option value="">Select a chatbot</option>';
        chatbots.forEach(bot => {
            const option = document.createElement('option');
            option.value = bot.id;
            option.textContent = bot.name;
            select.appendChild(option);
        });
} catch (error) {
        console.error('Error loading chatbots:', error);
        showToast('Error loading chatbots. Please try again.', 'error');
    }
}