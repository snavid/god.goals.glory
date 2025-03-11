class HomepageInteractions {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
        this.setupAnimations();
    }

    initializeElements() {
        this.navLinks = document.querySelector('.nav-links');
        this.mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        this.achievementCards = document.querySelectorAll('.achievement-card');
        this.universityCards = document.querySelectorAll('.university-card');
    }

    setupEventListeners() {
        // Mobile Menu Toggle
        if (this.mobileMenuBtn && this.navLinks) {
            this.mobileMenuBtn.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            const target = e.target;
            if (!target.closest('.nav-links') && !target.closest('.mobile-menu-btn')) {
                this.navLinks.classList.remove('active');
                this.updateMobileMenuIcon();
            }
        });
    }

    toggleMobileMenu() {
        this.navLinks.classList.toggle('active');
        this.updateMobileMenuIcon();
    }

    updateMobileMenuIcon() {
        const icon = this.mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.className = this.navLinks.classList.contains('active') 
                ? 'fas fa-times' 
                : 'fas fa-bars';
        }
    }

    setupAnimations() {
        // Card hover animations
        this.achievementCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-15px)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });

        this.universityCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.05)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1)';
            });
        });

        // Scroll-triggered animations
        this.setupScrollAnimations();
    }

    setupScrollAnimations() {
        const sections = document.querySelectorAll('.achievements-section, .universities-section, .application-section');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, { threshold: 0.1 });

        sections.forEach(section => {
            observer.observe(section);
        });
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    new HomepageInteractions();
});