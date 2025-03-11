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

class GeneralInfoForm {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.form = document.querySelector('form');
        this.inputs = document.querySelectorAll('.form-control');
        this.prevBtn = document.querySelector('.btn-secondary');
        this.nextBtn = document.querySelector('.btn-primary');
    }

    setupEventListeners() {
        // Form input animations
        this.inputs.forEach(input => {
            input.addEventListener('focus', () => this.handleInputFocus(input));
            input.addEventListener('blur', () => this.handleInputBlur(input));
        });

        // Button hover effects
        if (this.prevBtn) {
            this.prevBtn.addEventListener('mouseover', () => this.handlePrevButtonHover(true));
            this.prevBtn.addEventListener('mouseout', () => this.handlePrevButtonHover(false));
        }

        if (this.nextBtn) {
            this.nextBtn.addEventListener('mouseover', () => this.handleNextButtonHover(true));
            this.nextBtn.addEventListener('mouseout', () => this.handleNextButtonHover(false));
        }

        // Form validation
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }

    handleInputFocus(input) {
        input.parentElement.classList.add('focused');
    }

    handleInputBlur(input) {
        if (!input.value) {
            input.parentElement.classList.remove('focused');
        }
    }

    handlePrevButtonHover(isHovering) {
        const icon = this.prevBtn.querySelector('i');
        if (icon) {
            icon.style.transform = isHovering ? 'translateX(-4px)' : 'translateX(0)';
        }
    }

    handleNextButtonHover(isHovering) {
        const icon = this.nextBtn.querySelector('i');
        if (icon) {
            icon.style.transform = isHovering ? 'translateX(4px)' : 'translateX(0)';
        }
    }

    handleSubmit(e) {
        const requiredFields = this.form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                this.showError(field);
            } else {
                this.clearError(field);
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
    }

    showError(field) {
        const formGroup = field.closest('.form-group');
        if (formGroup) {
            let errorDiv = formGroup.querySelector('.error-text');
            if (!errorDiv) {
                errorDiv = document.createElement('small');
                errorDiv.className = 'error-text';
                formGroup.appendChild(errorDiv);
            }
            errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> This field is required`;
        }
    }

    clearError(field) {
        const formGroup = field.closest('.form-group');
        if (formGroup) {
            const errorDiv = formGroup.querySelector('.error-text');
            if (errorDiv) {
                errorDiv.remove();
            }
        }
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new GeneralInfoForm();
});
