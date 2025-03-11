class ContactInfoForm {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.form = document.querySelector('form');
        this.inputs = document.querySelectorAll('.form-control');
        this.prevBtn = document.querySelector('.btn-secondary');
        this.nextBtn = document.querySelector('.btn-primary');
        this.progressFill = document.querySelector('.progress-fill');
    }

    setupEventListeners() {
        // Form input animations
        this.inputs.forEach(input => {
            input.addEventListener('focus', () => this.handleInputFocus(input));
            input.addEventListener('blur', () => this.handleInputBlur(input));
            // Add validation on input change
            input.addEventListener('input', () => this.validateInput(input));
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

        // Update progress bar
        if (this.progressFill) {
            this.progressFill.style.width = '66%';
        }
    }

    handleInputFocus(input) {
        const formGroup = input.closest('.form-group');
        if (formGroup) {
            formGroup.classList.add('focused');
        }
    }

    handleInputBlur(input) {
        const formGroup = input.closest('.form-group');
        if (formGroup && !input.value) {
            formGroup.classList.remove('focused');
        }
    }

    validateInput(input) {
        const isValid = input.checkValidity();
        const formGroup = input.closest('.form-group');
        
        if (formGroup) {
            if (!isValid && input.value) {
                this.showError(input, this.getValidationMessage(input));
            } else {
                this.clearError(input);
            }
        }
    }

    getValidationMessage(input) {
        if (input.validity.valueMissing) {
            return 'This field is required';
        }
        if (input.validity.typeMismatch) {
            return 'Please enter a valid format';
        }
        if (input.validity.patternMismatch) {
            return 'Please match the requested format';
        }
        return input.validationMessage;
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
                this.showError(field, 'This field is required');
            } else {
                this.clearError(field);
            }
        });

        if (!isValid) {
            e.preventDefault();
            // Scroll to first error
            const firstError = this.form.querySelector('.error-text');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }

    showError(field, message) {
        const formGroup = field.closest('.form-group');
        if (formGroup) {
            let errorDiv = formGroup.querySelector('.error-text');
            if (!errorDiv) {
                errorDiv = document.createElement('small');
                errorDiv.className = 'error-text';
                formGroup.appendChild(errorDiv);
            }
            errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
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
    new ContactInfoForm();
});
