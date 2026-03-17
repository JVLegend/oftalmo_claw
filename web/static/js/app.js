/**
 * OftalmoClaw - Main Application JS
 * Created by GeekVision
 */

// Mobile sidebar toggle
document.addEventListener('DOMContentLoaded', () => {
    // Animate bars on page load
    setTimeout(() => {
        document.querySelectorAll('.chart-bar').forEach(bar => {
            bar.style.transition = 'width 0.8s ease';
        });
        document.querySelectorAll('.progress-fill').forEach(bar => {
            bar.style.transition = 'width 0.8s ease';
        });
    }, 100);
});

// API helper
const api = {
    async get(url) {
        const res = await fetch(url);
        return res.json();
    },
    async post(url, data) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        return res.json();
    },
};

// Sidebar mobile toggle
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}
