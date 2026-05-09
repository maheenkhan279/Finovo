// Session Timeout Manager
// Auto-logout users after 4 minutes of inactivity for security

console.log('🔒 Session timeout manager loading...');

class SessionTimeoutManager {
    constructor() {
        this.timeoutDuration = 4 * 60 * 1000; // 4 minutes in milliseconds
        this.warningDuration = 30 * 1000; // 30 seconds warning
        this.timeoutId = null;
        this.warningId = null;
        this.lastActivity = Date.now();
        this.isActive = false;
        
        this.init();
    }
    
    init() {
        // Only activate if user is logged in
        this.checkAuthentication();
    }
    
    async checkAuthentication() {
        try {
            // Wait for Supabase client to be available
            let retries = 0;
            while ((!window.supabaseClient || !window.supabaseClient.auth) && retries < 5) {
                console.log(`⏳ Session timeout: Waiting for Supabase client... (${retries + 1}/5)`);
                await new Promise(resolve => setTimeout(resolve, 200));
                retries++;
            }
            
            if (!window.supabaseClient || !window.supabaseClient.auth) {
                console.log('⚠️ Session timeout: Supabase not available after retries, disabling timeout');
                this.isActive = false;
                return;
            }
            
            console.log("✅ Session timeout: Supabase client available, checking session...");

            let uwrap = await window.supabaseClient.auth.getUser();
            let user = uwrap && uwrap.data ? uwrap.data.user : null;
            if (!user) {
                try {
                    await window.supabaseClient.auth.refreshSession();
                } catch (e) {
                    /* ignore */
                }
                uwrap = await window.supabaseClient.auth.getUser();
                user = uwrap && uwrap.data ? uwrap.data.user : null;
            }

            if (user) {
                console.log("✅ Session timeout: User authenticated, activating session timeout");
                console.log("👤 Session timeout: User:", user.email);
                this.startTimeout();
                this.setupActivityListeners();
                this.isActive = true;
            } else {
                console.log('ℹ️ Session timeout: No active session, timeout manager disabled');
                this.isActive = false;
            }
        } catch (error) {
            console.error('❌ Session timeout: Error checking authentication:', error);
            console.log('⚠️ Session timeout: Disabling timeout manager due to error');
            this.isActive = false;
        }
    }
    
    startTimeout() {
        this.resetTimeout();
        console.log('⏱️ Session timeout started (4 minutes)');
    }
    
    resetTimeout() {
        // Clear existing timeouts
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }
        if (this.warningId) {
            clearTimeout(this.warningId);
        }
        
        this.lastActivity = Date.now();
        
        // Set warning timeout (3.5 minutes)
        this.warningId = setTimeout(() => {
            this.showWarning();
        }, this.timeoutDuration - this.warningDuration);
        
        // Set logout timeout (4 minutes)
        this.timeoutId = setTimeout(() => {
            this.logout();
        }, this.timeoutDuration);
    }
    
    showWarning() {
        console.log('⚠️ Session expiring soon - showing warning');
        
        // Create warning modal
        const warningModal = document.createElement('div');
        warningModal.className = 'modal fade show';
        warningModal.style.display = 'block';
        warningModal.style.backgroundColor = 'rgba(0,0,0,0.5)';
        warningModal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle"></i> Session Expiring
                        </h5>
                    </div>
                    <div class="modal-body">
                        <p>Your session will expire in <strong>30 seconds</strong> due to inactivity.</p>
                        <p>Click "Stay Logged In" to continue your session.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" onclick="sessionTimeoutManager.stayLoggedIn()">
                            <i class="fas fa-check"></i> Stay Logged In
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(warningModal);
        
        // Auto-remove warning after 30 seconds
        setTimeout(() => {
            if (warningModal.parentNode) {
                warningModal.parentNode.removeChild(warningModal);
            }
        }, this.warningDuration);
    }
    
    stayLoggedIn() {
        console.log('✅ User chose to stay logged in');
        
        // Remove warning modal if exists
        const warningModal = document.querySelector('.modal.show');
        if (warningModal && warningModal.parentNode) {
            warningModal.parentNode.removeChild(warningModal);
        }
        
        this.resetTimeout();
    }
    
    setupActivityListeners() {
        // Track user activity
        const activityEvents = [
            'mousedown', 'mousemove', 'keypress', 
            'scroll', 'touchstart', 'click'
        ];
        
        activityEvents.forEach(event => {
            document.addEventListener(event, () => {
                if (this.isActive) {
                    this.resetTimeout();
                }
            }, true);
        });
        
        console.log('👂 Activity listeners setup complete');
    }
    
    async logout() {
        console.log('🔒 Session expired - logging out user');
        
        try {
            // Show session expired message
            this.showSessionExpiredMessage();
            
            // Logout from Supabase
            if (window.supabaseClient && window.supabaseClient.auth) {
                await window.supabaseClient.auth.signOut();
            }
            try {
                if (typeof window.finovoDestroyDashboardState === "function") {
                    window.finovoDestroyDashboardState();
                }
            } catch (e) {
                /* ignore */
            }
            try {
                sessionStorage.clear();
            } catch (e) {
                /* ignore */
            }
            try {
                localStorage.clear();
            } catch (e) {
                /* ignore */
            }
            try {
                await fetch("/logout", { method: "GET", credentials: "same-origin" });
            } catch (e) {
                /* non-fatal */
            }

            // Redirect to login page after 2 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
            
        } catch (error) {
            console.error('❌ Error during logout:', error);
            // Still redirect even if error
            window.location.href = '/login';
        }
    }
    
    showSessionExpiredMessage() {
        const expiredModal = document.createElement('div');
        expiredModal.className = 'modal fade show';
        expiredModal.style.display = 'block';
        expiredModal.style.backgroundColor = 'rgba(0,0,0,0.5)';
        expiredModal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-clock"></i> Session Expired
                        </h5>
                    </div>
                    <div class="modal-body">
                        <p>Your session has expired due to inactivity.</p>
                        <p>Please login again to continue.</p>
                    </div>
                    <div class="modal-footer">
                        <div class="text-muted">
                            <i class="fas fa-spinner fa-spin"></i> Redirecting to login...
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(expiredModal);
    }
    
    // Public method to manually reset timeout
    reset() {
        if (this.isActive) {
            this.resetTimeout();
            console.log('🔄 Session timeout manually reset');
        }
    }
    
    // Public method to disable timeout manager
    disable() {
        this.isActive = false;
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }
        if (this.warningId) {
            clearTimeout(this.warningId);
        }
        console.log('⏹️ Session timeout manager disabled');
    }
}

// Initialize session timeout manager
let sessionTimeoutManager;

document.addEventListener('DOMContentLoaded', function() {
    sessionTimeoutManager = new SessionTimeoutManager();
    
    // Make it globally available
    window.sessionTimeoutManager = sessionTimeoutManager;
    
    console.log('✅ Session timeout manager initialized');
});

// Listen for auth state changes to enable/disable timeout
document.addEventListener('DOMContentLoaded', function() {
    if (window.supabaseClient && window.supabaseClient.auth) {
        window.supabaseClient.auth.onAuthStateChange((event, session) => {
            if (session && session.user) {
                console.log('👤 User logged in, enabling session timeout');
                sessionTimeoutManager.checkAuthentication();
            } else {
                console.log('👤 User logged out, disabling session timeout');
                sessionTimeoutManager.disable();
            }
        });
    }
});
