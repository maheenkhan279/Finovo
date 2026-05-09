console.log("JS FILE LOADED");
// Loading Screen
window.addEventListener('load', () => {
    const loadingScreen = document.querySelector('.loading-screen');
    loadingScreen.style.opacity = '0';
    setTimeout(() => {
        loadingScreen.style.display = 'none';
    }, 500);
});

// Navigation
document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileMenuToggle = document.createElement('button');
    mobileMenuToggle.className = 'mobile-menu-toggle';
    mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    document.querySelector('nav').appendChild(mobileMenuToggle);

    const navLinks = document.querySelector('.nav-links');
    
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('nav') && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.classList.add('fa-bars');
            icon.classList.remove('fa-times');
        }
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
                // Close mobile menu after clicking
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    const icon = mobileMenuToggle.querySelector('i');
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-times');
                }
            }
        });
    });

    // Search functionality
    const searchInput = document.querySelector('.search-bar input');
    const searchButton = document.querySelector('.search-bar button');
    
    searchButton.addEventListener('click', () => {
        performSearch(searchInput.value);
    });

    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch(searchInput.value);
        }
    });

    function performSearch(query) {
        if (query.trim()) {
            showNotification(`Searching for: ${query}`);
            // Close mobile menu after search
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                const icon = mobileMenuToggle.querySelector('i');
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-times');
            }
        }
    }

    // Chat Widget
    const chatToggle = document.querySelector('.chat-toggle');
    const chatContainer = document.querySelector('.chat-container');
    const closeChat = document.querySelector('.close-chat');
    const chatInput = document.querySelector('.chat-input input');
    const chatMessages = document.querySelector('.chat-messages');

    chatToggle.addEventListener('click', () => {
        chatContainer.classList.toggle('active');
    });

    closeChat.addEventListener('click', () => {
        chatContainer.classList.remove('active');
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && chatInput.value.trim()) {
            sendMessage(chatInput.value);
            chatInput.value = '';
        }
    });

    function sendMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Simulate bot response
        setTimeout(() => {
            const botResponse = document.createElement('div');
            botResponse.className = 'message bot-message';
            botResponse.textContent = 'Thank you for your message. Our support team will get back to you shortly.';
            chatMessages.appendChild(botResponse);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all items
            faqItems.forEach(i => i.classList.remove('active'));
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Newsletter Form
    const newsletterForm = document.querySelector('.newsletter-form');
    
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input').value;
        
        if (validateEmail(email)) {
            showNotification('Thank you for subscribing to our newsletter!', 'success');
            newsletterForm.reset();
        } else {
            showNotification('Please enter a valid email address.', 'error');
        }
    });

    // Notification System
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.querySelector('.notification-container').appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Email validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Progress bars animation
    const progressBars = document.querySelectorAll('.progress');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progress = entry.target;
                const width = progress.style.width;
                progress.style.width = '0';
                setTimeout(() => {
                    progress.style.width = width;
                }, 100);
            }
        });
    });

    progressBars.forEach(bar => observer.observe(bar));

    // Testimonials slider
    const testimonialsSlider = document.querySelector('.testimonials-slider');
    let isDown = false;
    let startX;
    let scrollLeft;

    testimonialsSlider.addEventListener('mousedown', (e) => {
        isDown = true;
        testimonialsSlider.classList.add('active');
        startX = e.pageX - testimonialsSlider.offsetLeft;
        scrollLeft = testimonialsSlider.scrollLeft;
    });

    testimonialsSlider.addEventListener('mouseleave', () => {
        isDown = false;
        testimonialsSlider.classList.remove('active');
    });

    testimonialsSlider.addEventListener('mouseup', () => {
        isDown = false;
        testimonialsSlider.classList.remove('active');
    });

    testimonialsSlider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - testimonialsSlider.offsetLeft;
        const walk = (x - startX) * 2;
        testimonialsSlider.scrollLeft = scrollLeft - walk;
    });

    // Touch events for testimonials slider
    testimonialsSlider.addEventListener('touchstart', (e) => {
        isDown = true;
        testimonialsSlider.classList.add('active');
        startX = e.touches[0].pageX - testimonialsSlider.offsetLeft;
        scrollLeft = testimonialsSlider.scrollLeft;
    });

    testimonialsSlider.addEventListener('touchend', () => {
        isDown = false;
        testimonialsSlider.classList.remove('active');
    });

    testimonialsSlider.addEventListener('touchmove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.touches[0].pageX - testimonialsSlider.offsetLeft;
        const walk = (x - startX) * 2;
        testimonialsSlider.scrollLeft = scrollLeft - walk;
    });
});

// Add animation to feature cards when they come into view
const featureCards = document.querySelectorAll('.feature-card');
const moduleCards = document.querySelectorAll('.module-card');

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Set initial styles for animation
featureCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
});

moduleCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
});

// Add click handlers for module buttons (only if buttons exist and not already linked)
document.querySelectorAll('.module-btn').forEach(button => {
    if (!button.href && !button.onclick) {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            if (window.showNotification) {
                showNotification('Module coming soon! Stay tuned for updates.', 'info');
            }
        });
    }
});

// Add click handlers for auth buttons (only if they're not links)
document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.querySelector('.login-btn');
    const signupBtn = document.querySelector('.signup-btn');
    
    if (loginBtn && !loginBtn.href && loginBtn.tagName !== 'A') {
        loginBtn.addEventListener('click', () => {
            if (window.showNotification) {
                showNotification('Please use the Login link in the navigation menu.', 'info');
            }
        });
    }
    
    if (signupBtn && !signupBtn.href && signupBtn.tagName !== 'A') {
        signupBtn.addEventListener('click', () => {
            if (window.showNotification) {
                showNotification('Please use the Sign Up link in the navigation menu.', 'info');
            }
        });
    }
    
    // Add click handler for CTA button (only if not already linked)
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton && !ctaButton.href && ctaButton.tagName !== 'A') {
        ctaButton.addEventListener('click', () => {
            if (window.showNotification) {
                showNotification('Start your financial journey with Finovo!', 'success');
            }
        });
    }
}); 