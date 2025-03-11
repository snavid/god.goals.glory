document.addEventListener('DOMContentLoaded', function() {
    // Initialize HTMX
    htmx.process(document.body);

    // Progress bar functionality
    updateProgress();

    // Handle form submissions
    setupFormSubmission();

    // Setup delete confirmations
    setupDeleteConfirmations();
});

function updateProgress() {
    const progressFill = document.querySelector('.progress-fill');
    const currentStep = 3; // dependents is step 3
    const totalSteps = 6; // Total number of steps in the application
    const progress = (currentStep / totalSteps) * 100;
    progressFill.style.width = `${progress}%`;
}

function setupFormSubmission() {
    const submitAllBtn = document.getElementById('submit-all');
    if (submitAllBtn) {
        submitAllBtn.addEventListener('click', function() {
            const forms = document.querySelectorAll('.dependent-form form');
            forms.forEach(form => {
                const formData = new FormData(form);
                htmx.ajax('POST', form.action, {
                    target: '#dependent-list',
                    swap: 'beforeend',
                    values: formData
                });
            });
        });
    }
}

function setupDeleteConfirmations() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-action.delete')) {
            if (!confirm('Are you sure you want to delete this dependent?')) {
                e.preventDefault();
            }
        }
    });
}

// Animate progress steps on hover
document.querySelectorAll('.progress-step').forEach(step => {
    step.addEventListener('mouseenter', function() {
        if (!this.classList.contains('active')) {
            this.style.transform = 'scale(1.1)';
        }
    });

    step.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});
