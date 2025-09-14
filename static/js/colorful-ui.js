// Colorful UI Enhancement Script
// Dynamically applies colorful 3D classes to generated content

document.addEventListener('DOMContentLoaded', function() {
    
    // Color classes for different card types
    const resumeColorClasses = ['resume-card-blue', 'resume-card-green', 'resume-card-orange', 'resume-card-purple', 'resume-card-cyan'];
    const jobColorClasses = ['job-card-blue', 'job-card-green', 'job-card-orange', 'job-card-purple', 'job-card-cyan'];
    
    // Function to apply colors to resume cards
    function applyResumeColors() {
        const resumeCards = document.querySelectorAll('#resumes-container .card');
        resumeCards.forEach((card, index) => {
            const colorClass = resumeColorClasses[index % resumeColorClasses.length];
            card.classList.add(colorClass);
            card.classList.add('feature-float-' + ((index % 3) + 1));
        });
    }
    
    // Function to apply colors to job cards
    function applyJobColors() {
        const jobCards = document.querySelectorAll('#jobs-container .job-card');
        jobCards.forEach((card, index) => {
            const colorClass = jobColorClasses[index % jobColorClasses.length];
            card.classList.add(colorClass);
            card.classList.add('feature-float-' + ((index % 3) + 1));
            
            // Also add job-listing class for CSS targeting
            card.closest('.col-md-6, .col-lg-4').classList.add('job-listing');
        });
    }
    
    // Function to enhance feature cards on home page
    function enhanceFeatureCards() {
        const featureCards = document.querySelectorAll('.col-md-4 .card');
        featureCards.forEach((card, index) => {
            card.classList.add('feature-float-' + ((index % 3) + 1));
            
            // Add gradient text to icons
            const icon = card.querySelector('.fa-3x');
            if (icon) {
                icon.style.background = `var(--gradient-${['blue', 'green', 'orange'][index]})`;
                icon.style.webkitBackgroundClip = 'text';
                icon.style.webkitTextFillColor = 'transparent';
                icon.style.backgroundClip = 'text';
            }
        });
    }
    
    // Function to enhance dashboard stats cards
    function enhanceDashboardCards() {
        const statsCards = document.querySelectorAll('.dashboard-stats .card');
        statsCards.forEach((card, index) => {
            card.classList.add(`dashboard-card-${index + 1}`);
        });
    }
    
    // Apply colors immediately if elements exist
    applyResumeColors();
    applyJobColors();
    enhanceFeatureCards();
    enhanceDashboardCards();
    
    // Set up MutationObserver to apply colors when content is dynamically loaded
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                // Check if resumes were loaded
                if (mutation.target.id === 'resumes-container') {
                    setTimeout(applyResumeColors, 100);
                }
                
                // Check if jobs were loaded
                if (mutation.target.id === 'jobs-container') {
                    setTimeout(applyJobColors, 100);
                }
            }
        });
    });
    
    // Observe changes to container elements
    const resumesContainer = document.getElementById('resumes-container');
    const jobsContainer = document.getElementById('jobs-container');
    
    if (resumesContainer) {
        observer.observe(resumesContainer, { childList: true, subtree: true });
    }
    
    if (jobsContainer) {
        observer.observe(jobsContainer, { childList: true, subtree: true });
    }
    
    // Enhanced loading animations
    function enhanceLoadingSpinners() {
        const spinners = document.querySelectorAll('.fa-spinner');
        spinners.forEach(spinner => {
            spinner.style.background = 'var(--gradient-blue)';
            spinner.style.webkitBackgroundClip = 'text';
            spinner.style.webkitTextFillColor = 'transparent';
            spinner.style.backgroundClip = 'text';
            spinner.style.filter = 'drop-shadow(0 0 8px rgba(102, 126, 234, 0.5))';
        });
    }
    
    // Apply enhanced spinners
    enhanceLoadingSpinners();
    
    // Apply colors to skill badges as they're created
    function enhanceSkillBadges() {
        const skillBadges = document.querySelectorAll('.skill-badge');
        skillBadges.forEach((badge, index) => {
            const colors = ['var(--gradient-blue)', 'var(--gradient-forest)', 'var(--gradient-orange)', 'var(--gradient-purple)', 'var(--gradient-cyan)'];
            const textColors = ['white', 'white', '#2d3436', 'white', '#2d3436'];
            
            badge.style.background = colors[index % colors.length];
            badge.style.color = textColors[index % textColors.length];
            badge.style.border = 'none';
            badge.style.fontWeight = '600';
        });
    }
    
    // Apply skill badge colors immediately and on updates
    enhanceSkillBadges();
    
    // Re-apply on any content updates
    const allObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                setTimeout(() => {
                    enhanceSkillBadges();
                    enhanceLoadingSpinners();
                }, 50);
            }
        });
    });
    
    // Observe the entire document for skill badge updates
    allObserver.observe(document.body, { childList: true, subtree: true });
    
    console.log('Colorful UI enhancements applied!');
});
