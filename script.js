// ============================================
// D'XZUS NEWS - INTERACTIVE FEATURES
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initHamburgerMenu();
    initSearch();
    initSmoothScroll();
    initReadMoreButtons();
    initNewsletter();
    initPoll();
    initScrollToTop();
});

// ============================================
// HAMBURGER MENU
// ============================================

function initHamburgerMenu() {
    const hamburger = document.getElementById('hamburgerMenu');
    const nav = document.getElementById('mainNav');

    if (!hamburger) return;

    hamburger.addEventListener('click', function() {
        nav.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Close menu when a link is clicked
    const navLinks = nav.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            nav.classList.remove('active');
            hamburger.classList.remove('active');
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
}

// ============================================
// SEARCH FUNCTIONALITY
// ============================================

function initSearch() {
    const searchBox = document.getElementById('searchBox');
    const searchBtn = document.querySelector('.search-btn');

    if (!searchBox) return;

    searchBtn.addEventListener('click', function() {
        const query = searchBox.value.trim();
        if (query) {
            performSearch(query);
        }
    });

    searchBox.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = searchBox.value.trim();
            if (query) {
                performSearch(query);
            }
        }
    });
}

function performSearch(query) {
    console.log('Searching for:', query);
    // Highlight matching articles
    const articles = document.querySelectorAll('.article-card, .article-title, .opinion-card');
    
    articles.forEach(article => {
        const text = article.textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
            article.style.opacity = '1';
            article.style.order = '-1'; // Move to top
        } else {
            article.style.opacity = '0.5';
        }
    });

    showNotification(`Searching for: "${query}"`);
}

// ============================================
// SMOOTH SCROLL
// ============================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ============================================
// READ MORE BUTTONS
// ============================================

function initReadMoreButtons() {
    const readMoreBtns = document.querySelectorAll('.read-more-btn, .read-opinion, .analysis-link');

    readMoreBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const article = this.closest('.article-card, .opinion-card, .hero-story');
            if (article) {
                const title = article.querySelector('.article-title, .opinion-title, .hero-title')?.textContent;
                openArticle(title || 'Article');
            }
        });
    });
}

function openArticle(title) {
    // Create a modal for article view
    const modal = document.createElement('div');
    modal.className = 'article-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${title}</h2>
                <button class="close-modal">&times;</button>
            </div>
            <div class="modal-body">
                <p>Full article content would load here...</p>
                <p>This is a demo. In production, this would fetch the full article from your database.</p>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Style the modal
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    `;

    modal.querySelector('.modal-content').style.cssText = `
        background: #262626;
        color: #ffffff;
        padding: 40px;
        border-radius: 8px;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        border: 1px solid #333333;
    `;

    modal.querySelector('.modal-header').style.cssText = `
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 2px solid #dc143c;
        padding-bottom: 15px;
    `;

    const closeBtn = modal.querySelector('.close-modal');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        font-size: 32px;
        color: #dc143c;
        cursor: pointer;
    `;

    closeBtn.addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.remove();
    });
}

// ============================================
// NEWSLETTER SUBSCRIPTION
// ============================================

function initNewsletter() {
    const forms = document.querySelectorAll('.newsletter-form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            if (email) {
                subscribeNewsletter(email);
                this.reset();
            }
        });
    });
}

function subscribeNewsletter(email) {
    console.log('Subscribing email:', email);
    showNotification(`✓ Successfully subscribed ${email} to Daily Briefing!`, 'success');
    
    // Simulate API call
    setTimeout(() => {
        console.log('Newsletter subscription confirmed');
    }, 1000);
}

// ============================================
// POLL VOTING
// ============================================

function initPoll() {
    const voteBtn = document.querySelector('.vote-btn');
    const pollOptions = document.querySelectorAll('.poll-option input[type="radio"]');

    if (!voteBtn) return;

    voteBtn.addEventListener('click', function() {
        const selected = Array.from(pollOptions).find(option => option.checked);
        
        if (!selected) {
            showNotification('Please select an option first', 'error');
            return;
        }

        const label = selected.nextElementSibling?.textContent || 'Your option';
        castVote(label);
        voteBtn.disabled = true;
        voteBtn.textContent = '✓ Vote Recorded';
    });
}

function castVote(option) {
    console.log('Vote cast for:', option);
    showNotification(`✓ Your vote has been recorded!`, 'success');
}

// ============================================
// NOTIFICATIONS
// ============================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#dc143c'};
        color: white;
        border-radius: 8px;
        font-weight: 600;
        z-index: 3000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// ============================================
// ADD ANIMATIONS
// ============================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// CATEGORY FILTERING
// ============================================

function filterByCategory(category) {
    const articles = document.querySelectorAll('.article-card');
    
    articles.forEach(article => {
        const tag = article.querySelector('.category-tag');
        if (tag && tag.textContent === category) {
            article.style.display = 'block';
        } else {
            article.style.display = 'none';
        }
    });

    showNotification(`Showing ${category} articles`);
}

// ============================================
// SCROLL TO TOP BUTTON
// ============================================

function initScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.textContent = '↑';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: #dc143c;
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        display: none;
        z-index: 999;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.4);
    `;

    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollBtn.style.display = 'flex';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

document.addEventListener('keydown', function(e) {
    // Cmd/Ctrl + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchBox')?.focus();
        showNotification('Search focused (Cmd/Ctrl + K)');
    }

    // Esc to close any open modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.article-modal').forEach(modal => modal.remove());
    }
});

// ============================================
// TRACK PAGE VIEWS (ANALYTICS READY)
// ============================================

function trackPageView() {
    const url = window.location.pathname;
    console.log('Page view tracked:', url);
    // In production, send this to analytics service
}

trackPageView();

console.log('D\'XZUS News - Interactive features loaded successfully!');