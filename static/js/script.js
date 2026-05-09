// Main Application Script
// Clean script without accidental console prompts

console.log('🚀 Loading main application script...');

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM loaded, initializing application...');
    
    // Initialize any global app functionality
    initializeApp();
});

function initializeApp() {
    // Application initialization logic
    console.log('🔧 Application initialized');
    
    // Setup any global event listeners
    setupGlobalEventListeners();
    
    // Initialize UI components
    initializeUIComponents();
}

function setupGlobalEventListeners() {
    // Setup global event listeners
    console.log('👂 Setting up global event listeners');
    
    // Example: Handle navigation clicks
    document.addEventListener('click', function(e) {
        // Handle any global click events
    });
}

function initializeUIComponents() {
    // Initialize UI components
    console.log('🎨 Initializing UI components');
    
    // Initialize tooltips, modals, etc.
    initializeTooltips();
    initializeModals();
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        console.log('✅ Tooltips initialized');
    }
}

function initializeModals() {
    // Initialize Bootstrap modals if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
        console.log('✅ Modals ready');
    }
}

// Global utility functions
window.AppUtils = {
    // Show notification — prefers Finovo toast stack when available
    showNotification: function(message, type) {
        type = type || "info";
        if (window.FinovoToast && typeof window.FinovoToast.show === "function") {
            window.FinovoToast.show(message, type === "danger" ? "error" : type, {
                title: type === "success" ? "Finovo" : type === "error" || type === "danger" ? "Something went wrong" : "Finovo",
                duration: type === "error" || type === "danger" ? 6500 : 4200
            });
            return;
        }
        const notification = document.createElement("div");
        notification.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
        notification.style.zIndex = "9999";
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    },
    
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

console.log('✅ Main application script loaded successfully');
