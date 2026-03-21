/**
 * OftalmoClaw - Main Application JS
 * Created by GeekVision
 */

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
});
