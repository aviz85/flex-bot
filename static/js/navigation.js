document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const page = e.target.closest('.nav-link').getAttribute('data-page');
            await showPage(page);
        });
    });
});

async function showPage(page) {
    return new Promise((resolve) => {
        document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
        const pageElement = document.getElementById(page);
        if (pageElement) {
            pageElement.classList.remove('hidden');
        }
        currentPage = page;
        if (page === 'bots-library') loadBots();
        if (page === 'chat-logs'){
             console.log("Loading chat logs...");
             loadChatLogs();
        }
        if (page === 'settings') loadBotSettings();
        if (page === 'chat') loadChatbots();
        
        updateActiveNavLink(page);
        setTimeout(resolve, 0);
    });
}

function updateActiveNavLink(page) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === page) {
            link.classList.add('active');
        }
    });
}