interface Coordinates {
    x: number;
    y: number;
}

class LoginForm {
    private form!: HTMLFormElement;
    private usernameInput!: HTMLInputElement;
    private passwordInput!: HTMLInputElement;
    private submitButton!: HTMLButtonElement;
    private blobs!: NodeListOf<HTMLElement>;
    private container!: HTMLElement;
    private mobileMenuBtn!: HTMLButtonElement;
    private navLinks!: HTMLElement;
    private mousePosition: Coordinates = { x: 0, y: 0 };

    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.setupBlobAnimation();
    }

    private initializeElements(): void {
        this.form = document.querySelector('.login-form') as HTMLFormElement;
        this.usernameInput = document.querySelector('#username') as HTMLInputElement;
        this.passwordInput = document.querySelector('#password') as HTMLInputElement;
        this.submitButton = document.querySelector('.submit-btn') as HTMLButtonElement;
        this.blobs = document.querySelectorAll('.blob') as NodeListOf<HTMLElement>;
        this.container = document.querySelector('.login-container') as HTMLElement;
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn') as HTMLButtonElement;
        this.navLinks = document.querySelector('.nav-links') as HTMLElement;

        if (!this.form || !this.usernameInput || !this.passwordInput || !this.submitButton || !this.container) {
            throw new Error('Required elements not found in the DOM');
        }
    }

    private setupEventListeners(): void {
        // Form submission
        this.form.addEventListener('submit', (e: Event) => this.handleSubmit(e));

        // Input animations
        [this.usernameInput, this.passwordInput].forEach(input => {
            input.addEventListener('focus', () => this.handleInputFocus(input));
            input.addEventListener('blur', () => this.handleInputBlur(input));
        });

        // Mouse move effect for blobs
        this.container.addEventListener('mousemove', (e: MouseEvent) => this.handleMouseMove(e));

        // Mobile menu
        if (this.mobileMenuBtn && this.navLinks) {
            this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e: MouseEvent) => {
            const target = e.target as HTMLElement;
            if (!target.closest('.nav-links') && !target.closest('.mobile-menu-btn')) {
                this.navLinks.classList.remove('active');
            }
        });
    }

    private toggleMobileMenu(): void {
        this.navLinks.classList.toggle('active');
        const icon = this.mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.className = this.navLinks.classList.contains('active') 
                ? 'fas fa-times' 
                : 'fas fa-bars';
        }
    }

    private setupBlobAnimation(): void {
        // Initial blob positions
        this.updateBlobPositions();

        // Animate blobs periodically
        setInterval(() => this.updateBlobPositions(), 3000);
    }

    private handleSubmit(e: Event): void {
        if (!this.validateForm()) {
            e.preventDefault();
        } else {
            this.animateButton();
        }
    }

    private validateForm(): boolean {
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

    private showError(input: HTMLInputElement, message: string): void {
        const formGroup = input.closest('.form-group') as HTMLElement;
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

    private clearError(input: HTMLInputElement): void {
        const formGroup = input.closest('.form-group') as HTMLElement;
        const errorElement = formGroup.querySelector('.error-message');
        
        if (errorElement) {
            errorElement.remove();
        }
        
        input.classList.remove('error');
    }

    private handleInputFocus(input: HTMLInputElement): void {
        const formGroup = input.closest('.form-group') as HTMLElement;
        formGroup.classList.add('focused');
    }

    private handleInputBlur(input: HTMLInputElement): void {
        const formGroup = input.closest('.form-group') as HTMLElement;
        if (!input.value) {
            formGroup.classList.remove('focused');
        }
    }

    private handleMouseMove(e: MouseEvent): void {
        const rect = this.container.getBoundingClientRect();
        this.mousePosition = {
            x: (e.clientX - rect.left) / this.container.offsetWidth,
            y: (e.clientY - rect.top) / this.container.offsetHeight
        };

        this.updateBlobPositions();
    }

    private updateBlobPositions(): void {
        this.blobs.forEach((blob, index) => {
            const offsetX = (index === 0 ? -1 : 1) * (this.mousePosition.x * 100 - 50);
            const offsetY = (index === 0 ? -1 : 1) * (this.mousePosition.y * 100 - 50);

            blob.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
        });
    }

    private animateButton(): void {
        this.submitButton.classList.add('loading');
        this.submitButton.disabled = true;
        
        const originalText = this.submitButton.textContent;
        this.submitButton.textContent = 'Logging in...';
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new LoginForm();
});
