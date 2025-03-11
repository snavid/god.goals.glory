class LoginForm {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.setupBlobAnimation();
    }

    initializeElements() {
        this.form = document.querySelector('.login-form');
        this.usernameInput = document.querySelector('#username');
        this.passwordInput = document.querySelector('#password');
        this.submitButton = document.querySelector('.submit-btn');
        this.blobs = document.querySelectorAll('.blob');
        this.container = document.querySelector('.login-container');
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        this.navLinks = document.querySelector('.nav-links');
        this.mousePosition = { x: 0, y: 0 };

        if (!this.form || !this.usernameInput || !this.passwordInput || !this.submitButton || !this.container) {
            throw new Error('Required elements not found in the DOM');
        }
    }

    setupEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Input animations
        [this.usernameInput, this.passwordInput].forEach(input => {
            input.addEventListener('focus', () => this.handleInputFocus(input));
            input.addEventListener('blur', () => this.handleInputBlur(input));
        });

        // Mouse move effect for blobs
        this.container.addEventListener('mousemove', (e) => this.handleMouseMove(e));

        // Mobile menu
        if (this.mobileMenuBtn && this.navLinks) {
            this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            const target = e.target;
            if (!target.closest('.nav-links') && !target.closest('.mobile-menu-btn')) {
                this.navLinks.classList.remove('active');
            }
        });
    }

    toggleMobileMenu() {
        this.navLinks.classList.toggle('active');
        const icon = this.mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.className = this.navLinks.classList.contains('active') 
                ? 'fas fa-times' 
                : 'fas fa-bars';
        }
    }

    setupBlobAnimation() {
        // Initial blob positions
        this.updateBlobPositions();

        // Animate blobs periodically
        setInterval(() => this.updateBlobPositions(), 3000);
    }

    handleSubmit(e) {
        if (!this.validateForm()) {
            e.preventDefault();
        } else {
            this.animateButton();
        }
    }

    validateForm() {
        let isValid = true;
        const inputs = [this.usernameInput, this.passwordInput];

        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showError(input, 'This field is required');
                isValid = false;
            } else {
                this.clearError(input);
            }
        });

        return isValid;
    }

    showError(input, message) {
        const formGroup = input.closest('.form-group');
        const errorElement = formGroup.querySelector('.error-message') || document.createElement('div');
        
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        
        if (!formGroup.querySelector('.error-message')) {
            formGroup.appendChild(errorElement);
        }

        input.classList.add('error');
        
        // Shake animation
        input.style.animation = 'shake 0.5s';
        setTimeout(() => input.style.animation = '', 500);
    }

    clearError(input) {
        const formGroup = input.closest('.form-group');
        const errorElement = formGroup.querySelector('.error-message');
        
        if (errorElement) {
            errorElement.remove();
        }
        
        input.classList.remove('error');
    }

    handleInputFocus(input) {
        const formGroup = input.closest('.form-group');
        formGroup.classList.add('focused');
    }

    handleInputBlur(input) {
        const formGroup = input.closest('.form-group');
        if (!input.value) {
            formGroup.classList.remove('focused');
        }
    }

    handleMouseMove(e) {
        const rect = this.container.getBoundingClientRect();
        this.mousePosition = {
            x: (e.clientX - rect.left) / this.container.offsetWidth,
            y: (e.clientY - rect.top) / this.container.offsetHeight
        };

        this.updateBlobPositions();
    }

    updateBlobPositions() {
        this.blobs.forEach((blob, index) => {
            const offsetX = (index === 0 ? -1 : 1) * (this.mousePosition.x * 100 - 50);
            const offsetY = (index === 0 ? -1 : 1) * (this.mousePosition.y * 100 - 50);

            blob.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
        });
    }

    animateButton() {
        this.submitButton.classList.add('loading');
        this.submitButton.disabled = true;
        this.submitButton.textContent = 'Logging in...';
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new LoginForm();
});
