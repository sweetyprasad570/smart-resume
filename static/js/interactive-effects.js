// Interactive Effects for Smart Resume - Enhances button and UI interactions
// This file adds interactive behaviors without modifying core functionality

// Track user interaction to prevent browser intervention errors
document.addEventListener('DOMContentLoaded', function() {
    // Set up user interaction tracking
    document.hasStoredUserInteraction = false;
    
    // Mark user interaction on first click or keypress
    const userInteractionEvents = ['click', 'keydown', 'touchstart'];
    userInteractionEvents.forEach(event => {
        document.addEventListener(event, function() {
            document.hasStoredUserInteraction = true;
        }, { once: true });
    });
    
    // Enhanced button hover effects with sound/vibration (where supported)
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        // Add ripple effect on click
        button.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
        
        // Add subtle hover feedback
        button.addEventListener('mouseenter', function() {
            // Haptic feedback for supported devices (only after user interaction)
            if (navigator.vibrate && document.hasStoredUserInteraction) {
                navigator.vibrate(10); // Very short vibration
            }
            
            // Add glow effect
            this.style.filter = 'drop-shadow(0 0 8px rgba(0, 123, 255, 0.3))';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.filter = 'none';
        });
    });
    
    // Ripple effect function
    function createRippleEffect(event, button) {
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
            pointer-events: none;
        `;
        
        button.appendChild(ripple);
        
        // Remove ripple after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.remove();
            }
        }, 600);
    }
    
    // Add CSS for ripple animation if not already present
    if (!document.querySelector('#ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Enhanced card interactions
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Subtle tilt effect on hover
            this.style.transform = 'translateY(-5px) rotateY(2deg) rotateX(2deg)';
            this.style.transformStyle = 'preserve-3d';
            
            // Animate icons within the card
            const icons = this.querySelectorAll('.fas, .far, .fab');
            icons.forEach(icon => {
                icon.style.transform = 'scale(1.1)';
            });
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            
            // Reset icon transforms
            const icons = this.querySelectorAll('.fas, .far, .fab');
            icons.forEach(icon => {
                icon.style.transform = '';
            });
        });
    });
    
    // Interactive skill badges
    const skillBadges = document.querySelectorAll('.skill-badge');
    
    skillBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            // Temporary highlight effect on click
            this.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
            this.style.transform = 'scale(1.1)';
            
            setTimeout(() => {
                this.style.background = '';
                this.style.transform = '';
            }, 200);
        });
    });
    
    // Navigation link active state enhancement
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = '600';
        }
        
        // Enhanced hover effect for nav links
        link.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        link.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = '';
            }
        });
    });
    
    // Parallax effect for hero section (if it exists)
    const heroSection = document.querySelector('.display-4');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            heroSection.style.transform = `translateY(${parallax}px)`;
        });
    }
    
    // Progressive loading animation for cards
    const cardElements = document.querySelectorAll('.card');
    
    // Intersection Observer for scroll-triggered animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                entry.target.style.opacity = '1';
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Apply initial state and observe cards
    cardElements.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Button loading state enhancement
    function enhanceButtonLoading() {
        const buttons = document.querySelectorAll('[data-loading]');
        
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                if (this.disabled) return;
                
                // Store original content
                this.setAttribute('data-original-html', this.innerHTML);
                
                // Set loading state
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                this.disabled = true;
                
                // Simulate loading (in real app, this would be tied to actual operations)
                setTimeout(() => {
                    this.innerHTML = this.getAttribute('data-original-html');
                    this.disabled = false;
                }, 2000);
            });
        });
    }
    
    // Form validation visual enhancement
    const formInputs = document.querySelectorAll('.form-control');
    
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = '';
        });
        
        // Real-time validation feedback
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = '#28a745';
                this.style.boxShadow = '0 0 0 0.2rem rgba(40, 167, 69, 0.25)';
            } else {
                this.style.borderColor = '';
                this.style.boxShadow = '';
            }
        });
    });
    
    // Navbar collapse animation enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const icon = this.querySelector('.navbar-toggler-icon');
            icon.style.transform = icon.style.transform === 'rotate(90deg)' ? '' : 'rotate(90deg)';
            icon.style.transition = 'transform 0.3s ease';
        });
    }
    
    // Page transition effects
    const links = document.querySelectorAll('a[href^="/"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Don't interfere with external links or hash links
            if (href.startsWith('http') || href.startsWith('#')) {
                return;
            }
            
            // Add subtle page transition
            document.body.style.opacity = '0.95';
            document.body.style.transition = 'opacity 0.2s ease';
        });
    });
    
    // Initialize all enhancements
    enhanceButtonLoading();
    
    console.log('Interactive effects loaded successfully!');
});
