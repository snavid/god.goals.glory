class BaseNavigation {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        this.navLinks = document.querySelector('.nav-links');
    }

    setupEventListeners() {
        // Mobile menu toggle
        this.mobileMenuBtn?.addEventListener('click', () => this.toggleMobileMenu());

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.nav-links') && !e.target.closest('.mobile-menu-btn')) {
                this.navLinks?.classList.remove('active');
                this.updateMenuIcon(false);
            }
        });
    }

    toggleMobileMenu() {
        const isActive = this.navLinks?.classList.toggle('active');
        this.updateMenuIcon(isActive);
    }

    updateMenuIcon(isActive) {
        const icon = this.mobileMenuBtn?.querySelector('i');
        if (icon) {
            icon.className = isActive ? 'fas fa-times' : 'fas fa-bars';
        }
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new BaseNavigation();
});















document.addEventListener('DOMContentLoaded', () => {
    const formInputs = document.querySelectorAll('.form-control');

    formInputs.forEach(input => {
        input.addEventListener('focus', () => input.classList.add('focused'));
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.classList.remove('focused');
            }
        });
    });
});
