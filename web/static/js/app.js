/**
 * OftalmoClaw - Main Application JS
 * Created by GeekVision
 */

// ---- Global Error Boundary ----
window.onerror = function(msg, url, line, col, error) {
    console.error('Global error:', msg, url, line);
    showToast('Ocorreu um erro inesperado', 'error');
    return true; // Prevent white screen
};
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    // Don't toast for network errors (already handled by API helper)
});

// ---- Toast Notifications ----
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${icons[type] || ''}</span> ${message}`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4100);
}

// ---- API Helper (with error handling) ----
const api = {
    async get(url) {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`Erro ${res.status}`);
        return res.json();
    },
    async post(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || `Erro ${res.status}`);
        }
        return res.json();
    },
};

// ---- Modal Helpers ----
function openModal(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal on overlay click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Close modal on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal-overlay.active');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});

// ---- Sidebar Mobile Toggle ----
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    sidebar.classList.toggle('open');
    if (overlay) overlay.classList.toggle('active');
}

// ---- Intro Box Dismissal ----
function dismissIntro(id, storageKey) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
    if (storageKey) localStorage.setItem(storageKey, '1');
}

function checkIntroDismissed(id, storageKey) {
    if (localStorage.getItem(storageKey)) {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
    }
}

// ---- Collapsible Sections ----
function toggleSection(id) {
    const el = document.getElementById(id);
    const toggleEl = document.getElementById(id.replace('-section', '-toggle'));
    if (!el) return;
    if (el.style.display === 'none') {
        el.style.display = 'block';
        if (toggleEl) toggleEl.textContent = '▲ ocultar';
    } else {
        el.style.display = 'none';
        if (toggleEl) toggleEl.textContent = '▼ mostrar';
    }
}

// ---- Simple Markdown Renderer (for assistant messages) ----
function renderMarkdown(text) {
    // Escape HTML first
    let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Code blocks (```)
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g,
        '<pre style="background:var(--slate-100);padding:12px;border-radius:6px;overflow-x:auto;font-family:var(--font-mono);font-size:13px;margin:8px 0;"><code>$2</code></pre>');

    // Inline code
    html = html.replace(/`([^`]+)`/g,
        '<code style="background:var(--slate-100);padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:13px;">$1</code>');

    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Headers
    html = html.replace(/^### (.+)$/gm, '<h4 style="margin:12px 0 4px;font-size:14px;">$1</h4>');
    html = html.replace(/^## (.+)$/gm, '<h3 style="margin:12px 0 4px;font-size:15px;">$1</h3>');

    // List items
    html = html.replace(/^[-•] (.+)$/gm, '<li style="margin-left:16px;">$1</li>');

    // Paragraphs (double newline)
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n/g, '<br>');

    return html;
}

// ---- Notifications Panel ----
function toggleNotifications() {
    const panel = document.getElementById('notif-panel');
    const userMenu = document.getElementById('user-menu');
    if (userMenu) userMenu.classList.remove('active');
    if (panel) panel.classList.toggle('active');
}

// ---- User Menu ----
function toggleUserMenu() {
    const menu = document.getElementById('user-menu');
    const panel = document.getElementById('notif-panel');
    if (panel) panel.classList.remove('active');
    if (menu) menu.classList.toggle('active');
}

// Close dropdowns on outside click
document.addEventListener('click', (e) => {
    const userMenu = document.getElementById('user-menu');
    const notifPanel = document.getElementById('notif-panel');
    if (userMenu && !e.target.closest('.topbar-user') && !e.target.closest('.user-menu')) {
        userMenu.classList.remove('active');
    }
    if (notifPanel && !e.target.closest('#notif-btn') && !e.target.closest('.notif-panel')) {
        notifPanel.classList.remove('active');
    }
});

// ---- Global Search ----
let searchCache = [];

async function loadSearchData() {
    try {
        const data = await api.get('/api/v1/cases/');
        searchCache = (data.cases || []).map(c => ({
            id: c.id,
            number: c.case_number,
            patient: `${c.patient.gender === 'F' ? 'Feminino' : 'Masculino'}, ${c.patient.age} anos`,
            complaint: c.chief_complaint || '',
            doctor: c.requested_by.name,
            specialty: c.specialty_requested || '',
            badge: c.urgency === 'urgent' ? 'Urgente' : c.status === 'in_analysis' ? 'Em análise' : 'Pendente',
        }));
    } catch (e) {}
}

function handleSearch(query) {
    const results = document.getElementById('search-results');
    if (!query || query.length < 2) {
        results.classList.remove('active');
        return;
    }
    if (searchCache.length === 0) {
        loadSearchData().then(() => handleSearch(query));
        return;
    }
    const q = query.toLowerCase();
    const matches = searchCache.filter(c =>
        c.number.toLowerCase().includes(q) ||
        c.patient.toLowerCase().includes(q) ||
        c.complaint.toLowerCase().includes(q) ||
        c.doctor.toLowerCase().includes(q) ||
        c.specialty.toLowerCase().includes(q)
    ).slice(0, 5);

    if (matches.length === 0) {
        results.innerHTML = '<div class="search-no-results">Nenhum resultado para "' + query + '"</div>';
    } else {
        results.innerHTML = matches.map(c => `
            <a href="/second-opinion" class="search-result-item">
                <strong>${c.number}</strong>
                <span>${c.patient} — ${c.complaint.substring(0, 40)}${c.complaint.length > 40 ? '...' : ''}</span>
                <span class="badge badge-pending" style="font-size:10px;">${c.badge}</span>
            </a>
        `).join('');
    }
    results.classList.add('active');
}

// ---- Init on DOMContentLoaded ----
document.addEventListener('DOMContentLoaded', () => {
    // Animate chart bars
    setTimeout(() => {
        document.querySelectorAll('.chart-bar').forEach(bar => {
            bar.style.transition = 'width 0.8s ease';
        });
        document.querySelectorAll('.progress-fill').forEach(bar => {
            bar.style.transition = 'width 0.8s ease';
        });
    }, 100);

    // Pre-load search data
    loadSearchData();
});
