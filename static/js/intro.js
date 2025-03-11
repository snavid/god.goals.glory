class IntroPage {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.form = document.querySelector('form');
        this.submitBtn = document.querySelector('.submit-btn');
        this.checkboxInput = document.querySelector('.checkbox-input');
        
        // Disable submit button initially if checkbox is unchecked
        this.submitBtn.disabled = !this.checkboxInput.checked;
    }

    setupEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Checkbox validation
        this.checkboxInput.addEventListener('change', () => this.validateForm());
    }

    handleSubmit(e) {
        if (!this.validateForm()) {
            e.preventDefault();
        } else {
            this.animateButton();
        }
    }

    validateForm() {
        const isChecked = this.checkboxInput.checked;
        this.submitBtn.disabled = !isChecked;
        return isChecked;
    }

    animateButton() {
        this.submitBtn.classList.add('loading');
        this.submitBtn.disabled = true;
        this.submitBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new IntroPage();
});
