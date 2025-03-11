"use strict";
const toggleDarkMode = () => {
    document.documentElement.classList.toggle("dark");
    localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
};
const initializeDarkMode = () => {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    }
    else {
        document.documentElement.classList.remove('dark');
    }
};
const initializeToasts = () => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach((toast) => {
        const progressBar = toast.querySelector('.progress-bar');
        if (progressBar) {
            // Start progress bar animation
            progressBar.style.transition = 'width 5s linear';
            progressBar.style.width = '100%';

            // Auto dismiss after 5 seconds
            setTimeout(() => {
                toast.classList.add('animate-fade-out');
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 5000);
        }

        // Add click handler for close button
        const closeBtn = toast.querySelector('button');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                toast.classList.add('animate-fade-out');
                setTimeout(() => {
                    toast.remove();
                }, 300);
            });
        }
    });
};
document.addEventListener("DOMContentLoaded", () => {
    initializeDarkMode();
    const darkModeButton = document.getElementById("dark-mode-toggle");
    if (darkModeButton) {
        darkModeButton.addEventListener("click", toggleDarkMode);
    }
    initializeToasts();
});
