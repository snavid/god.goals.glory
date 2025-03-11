interface ThemeManager {
    isDarkMode: boolean;
    toggleTheme(): void;
}

class TanSAFThemeManager implements ThemeManager {
    private readonly DARK_MODE_KEY = 'tansaf-dark-mode';
    public isDarkMode: boolean;

    constructor() {
        this.isDarkMode = localStorage.getItem(this.DARK_MODE_KEY) === 'true';
        this.applyTheme();
    }

    public toggleTheme(): void {
        this.isDarkMode = !this.isDarkMode;
        localStorage.setItem(this.DARK_MODE_KEY, this.isDarkMode.toString());
        this.applyTheme();
    }

    private applyTheme(): void {
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

    private initializeFormFields(): void {
        const formFields = document.querySelectorAll('input, select, textarea');
        formFields.forEach(field => {
            field.addEventListener('focus', () => this.handleFieldFocus(field));
            field.addEventListener('blur', () => this.handleFieldBlur(field));
        });
    }

    private handleFieldFocus(field: Element): void {
        field.closest('.form-group')?.classList.add('field-focus');
    }

    private handleFieldBlur(field: Element): void {
        if ((field as HTMLInputElement).value === '') {
            field.closest('.form-group')?.classList.remove('field-focus');
        }
    }

    private initializeTooltips(): void {
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
    themeToggle?.addEventListener('click', () => themeManager.toggleTheme());
});
