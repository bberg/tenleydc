/**
 * Tenley DC - Local History & Community Publication
 * Main JavaScript functionality
 */

(function() {
    'use strict';

    // DOM Elements
    const sidebar = document.getElementById('sidebar');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileOverlay = document.getElementById('mobileOverlay');

    // ==========================================
    // Sidebar Toggle Functionality
    // ==========================================
    function toggleSidebar() {
        sidebar.classList.toggle('open');
        mobileOverlay.classList.toggle('open');
        document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        mobileOverlay.classList.remove('open');
        document.body.style.overflow = '';
    }

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleSidebar);
    }

    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeSidebar);
    }

    // Close sidebar on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebar();
        }
    });

    // Close sidebar when clicking a link (mobile)
    if (sidebar) {
        const sidebarLinks = sidebar.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 900) {
                    closeSidebar();
                }
            });
        });
    }

    // ==========================================
    // Collapsible Navigation Groups
    // ==========================================
    function initNavGroups() {
        const STORAGE_KEY = 'tenley-ledger-nav-collapsed';
        const DEFAULT_EXPANDED = ['Community']; // Groups to keep expanded by default

        // Get collapsed state from localStorage
        function getCollapsedGroups() {
            try {
                const saved = localStorage.getItem(STORAGE_KEY);
                if (saved === null) {
                    // First visit: collapse all except DEFAULT_EXPANDED
                    return null; // Signal to use defaults
                }
                return JSON.parse(saved) || [];
            } catch {
                return null;
            }
        }

        // Save collapsed state to localStorage
        function saveCollapsedGroups(groups) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(groups));
        }

        const groupHeaders = document.querySelectorAll('.nav-group-header');
        const savedCollapsed = getCollapsedGroups();

        groupHeaders.forEach(header => {
            const groupName = header.dataset.group;
            const groupItems = header.nextElementSibling;

            // Apply state: if no saved state, collapse all except DEFAULT_EXPANDED
            const shouldCollapse = savedCollapsed === null
                ? !DEFAULT_EXPANDED.includes(groupName)
                : savedCollapsed.includes(groupName);

            if (shouldCollapse) {
                header.classList.add('collapsed');
                if (groupItems) groupItems.classList.add('collapsed');
            }

            // Toggle on click
            header.addEventListener('click', () => {
                const isCollapsed = header.classList.toggle('collapsed');
                if (groupItems) groupItems.classList.toggle('collapsed');

                // Update localStorage
                let currentCollapsed = getCollapsedGroups();
                // If first interaction, initialize with current visible state
                if (currentCollapsed === null) {
                    currentCollapsed = [];
                    groupHeaders.forEach(h => {
                        if (h.classList.contains('collapsed') && h !== header) {
                            currentCollapsed.push(h.dataset.group);
                        }
                    });
                }
                if (isCollapsed) {
                    if (!currentCollapsed.includes(groupName)) {
                        currentCollapsed.push(groupName);
                    }
                } else {
                    const index = currentCollapsed.indexOf(groupName);
                    if (index > -1) {
                        currentCollapsed.splice(index, 1);
                    }
                }
                saveCollapsedGroups(currentCollapsed);
            });
        });
    }

    initNavGroups();

    // ==========================================
    // Smooth Scrolling for Anchor Links
    // ==========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Update URL without jumping
                history.pushState(null, null, href);
            }
        });
    });

    // ==========================================
    // Search Highlighting
    // ==========================================
    function highlightSearchTerms() {
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');

        if (!query) return;

        const snippets = document.querySelectorAll('.result-snippet, .snippet');
        snippets.forEach(snippet => {
            const text = snippet.textContent;
            const regex = new RegExp(`(${query})`, 'gi');
            snippet.innerHTML = text.replace(regex, '<mark>$1</mark>');
        });
    }

    highlightSearchTerms();

    // ==========================================
    // Interactive Map Site Cards
    // ==========================================
    function initMapSiteCards() {
        const siteCards = document.querySelectorAll('.site-card');
        siteCards.forEach(card => {
            card.addEventListener('click', function() {
                const lat = this.dataset.lat;
                const lng = this.dataset.lng;
                const title = this.querySelector('h4')?.textContent || 'Location';

                console.log(`Selected: ${title} at ${lat}, ${lng}`);

                // Highlight the selected card
                siteCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    }

    initMapSiteCards();

    // ==========================================
    // Reading Progress Indicator
    // ==========================================
    function initReadingProgress() {
        const article = document.querySelector('.article-content');
        if (!article) return;

        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, #b54a32, #c4a35a);
            z-index: 1000;
            width: 0%;
            transition: width 0.1s ease;
        `;
        document.body.appendChild(progressBar);

        function updateProgress() {
            const articleRect = article.getBoundingClientRect();
            const articleTop = articleRect.top + window.scrollY;
            const articleHeight = article.offsetHeight;
            const windowHeight = window.innerHeight;
            const scrollY = window.scrollY;

            const startReading = articleTop;
            const endReading = articleTop + articleHeight - windowHeight;
            const currentProgress = ((scrollY - startReading) / (endReading - startReading)) * 100;

            progressBar.style.width = `${Math.min(100, Math.max(0, currentProgress))}%`;
        }

        window.addEventListener('scroll', updateProgress);
        updateProgress();
    }

    initReadingProgress();

    // ==========================================
    // Image Lazy Loading
    // ==========================================
    function initLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        if (images.length === 0) return;

        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '100px'
        });

        images.forEach(img => imageObserver.observe(img));
    }

    initLazyLoading();

    // ==========================================
    // Back to Top Button
    // ==========================================
    function initBackToTop() {
        const button = document.createElement('button');
        button.className = 'back-to-top';
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.setAttribute('aria-label', 'Back to top');
        button.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #b54a32;
            color: white;
            border: none;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s, transform 0.3s;
            z-index: 90;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            box-shadow: 0 4px 12px rgba(44, 24, 16, 0.2);
        `;
        document.body.appendChild(button);

        function toggleButton() {
            if (window.scrollY > 500) {
                button.style.opacity = '1';
                button.style.visibility = 'visible';
            } else {
                button.style.opacity = '0';
                button.style.visibility = 'hidden';
            }
        }

        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.1)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
        });

        window.addEventListener('scroll', toggleButton);
    }

    initBackToTop();

    // ==========================================
    // External Link Handler
    // ==========================================
    function initExternalLinks() {
        const articleLinks = document.querySelectorAll('.article-content a');
        articleLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && (href.startsWith('http://') || href.startsWith('https://')) && !href.includes(window.location.hostname)) {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');

                // Add external link indicator
                if (!link.querySelector('.fa-external-link-alt')) {
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-external-link-alt';
                    icon.style.cssText = 'font-size: 0.7em; margin-left: 0.25em; opacity: 0.6;';
                    link.appendChild(icon);
                }
            }
        });
    }

    initExternalLinks();

    // ==========================================
    // Copy Link Functionality for Headings
    // ==========================================
    function initHeadingLinks() {
        const headings = document.querySelectorAll('.article-content h2[id], .article-content h3[id]');
        headings.forEach(heading => {
            const link = document.createElement('a');
            link.className = 'heading-link';
            link.href = `#${heading.id}`;
            link.innerHTML = '<i class="fas fa-link"></i>';
            link.style.cssText = `
                opacity: 0;
                margin-left: 0.5rem;
                font-size: 0.8em;
                color: #4a3728;
                text-decoration: none;
                transition: opacity 0.2s;
            `;

            heading.style.position = 'relative';
            heading.appendChild(link);

            heading.addEventListener('mouseenter', () => {
                link.style.opacity = '1';
            });

            heading.addEventListener('mouseleave', () => {
                link.style.opacity = '0';
            });

            link.addEventListener('click', (e) => {
                e.preventDefault();
                const url = new URL(window.location);
                url.hash = heading.id;
                navigator.clipboard.writeText(url.toString()).then(() => {
                    link.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        link.innerHTML = '<i class="fas fa-link"></i>';
                    }, 2000);
                });
            });
        });
    }

    initHeadingLinks();

    // ==========================================
    // Keyboard Navigation
    // ==========================================
    document.addEventListener('keydown', (e) => {
        // Press '/' to focus search
        if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
            const searchInput = document.querySelector('.search-form input, .search-form-large input');
            if (searchInput && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        }

        // Press 'h' to go home
        if (e.key === 'h' && !e.ctrlKey && !e.metaKey && document.activeElement.tagName !== 'INPUT') {
            window.location.href = '/';
        }
    });

    // ==========================================
    // Print Functionality
    // ==========================================
    window.printArticle = function() {
        window.print();
    };

    // Log initialization
    console.log("Tenley DC initialized");

})();
