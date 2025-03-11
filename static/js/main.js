"use strict";
class TanSAFThemeManager {
    constructor() {
        this.DARK_MODE_KEY = 'tansaf-dark-mode';
        this.isDarkMode = localStorage.getItem(this.DARK_MODE_KEY) === 'true';
        this.applyTheme();
    }
    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        localStorage.setItem(this.DARK_MODE_KEY, this.isDarkMode.toString());
        this.applyTheme();
    }
    applyTheme() {
        document.body.classList.toggle('dark-mode', this.isDarkMode);
        const themeIcon = document.getElementById('theme-toggle-icon');
        if (themeIcon) {
            themeIcon.className = this.isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
        }
        // Animate theme transition
        document.body.style.transition = 'background-color 0.5s, color 0.5s';
    }
}
// Form field animations and enhancements
class FormEnhancer {
    constructor() {
        this.initializeFormFields();
        this.initializeTooltips();
    }
    initializeFormFields() {
        const formFields = document.querySelectorAll('input, select, textarea');
        formFields.forEach(field => {
            field.addEventListener('focus', () => this.handleFieldFocus(field));
            field.addEventListener('blur', () => this.handleFieldBlur(field));
        });
    }
    handleFieldFocus(field) {
        var _a;
        (_a = field.closest('.form-group')) === null || _a === void 0 ? void 0 : _a.classList.add('field-focus');
    }
    handleFieldBlur(field) {
        var _a;
        if (field.value === '') {
            (_a = field.closest('.form-group')) === null || _a === void 0 ? void 0 : _a.classList.remove('field-focus');
        }
    }
    initializeTooltips() {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(element => {
            // @ts-ignore
            new bootstrap.Tooltip(element);
        });
    }
}
// Initialize on document load
document.addEventListener('DOMContentLoaded', () => {
    const themeManager = new TanSAFThemeManager();
    const formEnhancer = new FormEnhancer();
    // Theme toggle button event listener
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle === null || themeToggle === void 0 ? void 0 : themeToggle.addEventListener('click', () => themeManager.toggleTheme());
});
