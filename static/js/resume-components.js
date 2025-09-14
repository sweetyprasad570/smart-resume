/**
 * Enhanced Resume Components
 * Provides advanced functionality for resume creation including:
 * - Skills with rating system
 * - Template selection
 * - Real-time preview
 * - Form validation
 */

class ResumeComponentsManager {
    constructor() {
        this.templates = {
            modern: {
                name: 'Modern Professional',
                description: 'Clean, contemporary design perfect for tech and creative industries',
                colors: ['#3498db', '#2c3e50'],
                icon: 'fa-laptop-code'
            },
            classic: {
                name: 'Classic Business',
                description: 'Traditional, professional layout ideal for corporate positions',
                colors: ['#2c3e50', '#34495e'],
                icon: 'fa-briefcase'
            },
            creative: {
                name: 'Creative Designer',
                description: 'Bold, innovative design for creative professionals',
                colors: ['#e74c3c', '#c0392b'],
                icon: 'fa-palette'
            },
            minimal: {
                name: 'Minimal Clean',
                description: 'Simple, elegant design that focuses on content',
                colors: ['#27ae60', '#2ecc71'],
                icon: 'fa-leaf'
            }
        };
        this.skillsData = [];
        this.selectedTemplate = 'modern';
    }

    /**
     * Initialize all resume components
     */
    init() {
        this.initTemplateSelector();
        this.initSkillsManager();
        this.initFormValidation();
        this.initRealTimePreview();
    }

    /**
     * Initialize template selection functionality
     */
    initTemplateSelector() {
        const container = document.getElementById('templateSelector');
        if (!container) return;

        let html = '<div class="row template-grid">';
        Object.keys(this.templates).forEach(key => {
            const template = this.templates[key];
            const isSelected = key === this.selectedTemplate ? 'selected' : '';
            
            html += `
                <div class="col-md-6 col-lg-3 mb-3">
                    <div class="template-card ${isSelected}" data-template="${key}">
                        <div class="template-preview" style="background: linear-gradient(135deg, ${template.colors[0]}, ${template.colors[1]});">
                            <i class="fas ${template.icon} fa-2x text-white"></i>
                        </div>
                        <div class="template-info">
                            <h6 class="template-name">${template.name}</h6>
                            <p class="template-description">${template.description}</p>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';

        container.innerHTML = html;

        // Add click handlers
        container.querySelectorAll('.template-card').forEach(card => {
            card.addEventListener('click', (e) => {
                // Remove previous selection
                container.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
                // Add selection to clicked card
                card.classList.add('selected');
                this.selectedTemplate = card.dataset.template;
                this.updatePreview();
            });
        });
    }

    /**
     * Initialize skills manager with rating system
     */
    initSkillsManager() {
        const container = document.getElementById('skillsManager');
        if (!container) return;

        container.innerHTML = `
            <div class="skills-input-section mb-3">
                <div class="input-group">
                    <input type="text" id="skillInput" class="form-control" placeholder="Enter a skill (e.g., JavaScript, Project Management)">
                    <select id="skillLevel" class="form-select" style="max-width: 120px;">
                        <option value="1">Beginner</option>
                        <option value="2">Basic</option>
                        <option value="3" selected>Intermediate</option>
                        <option value="4">Advanced</option>
                        <option value="5">Expert</option>
                    </select>
                    <button type="button" id="addSkillBtn" class="btn btn-primary">
                        <i class="fas fa-plus me-1"></i>Add
                    </button>
                </div>
            </div>
            <div id="skillsList" class="skills-list-container"></div>
        `;

        // Add event listeners
        document.getElementById('addSkillBtn').addEventListener('click', () => this.addSkill());
        document.getElementById('skillInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.addSkill();
            }
        });

        this.renderSkillsList();
    }

    /**
     * Add a new skill with rating
     */
    addSkill() {
        const skillInput = document.getElementById('skillInput');
        const levelSelect = document.getElementById('skillLevel');
        
        const skillName = skillInput.value.trim();
        const skillLevel = parseInt(levelSelect.value);

        if (!skillName) {
            this.showAlert('Please enter a skill name', 'warning');
            return;
        }

        // Check for duplicates
        if (this.skillsData.find(s => s.name.toLowerCase() === skillName.toLowerCase())) {
            this.showAlert('This skill already exists', 'warning');
            return;
        }

        // Add skill
        this.skillsData.push({
            id: Date.now(),
            name: skillName,
            level: skillLevel,
            levelText: this.getLevelText(skillLevel)
        });

        // Clear input
        skillInput.value = '';
        levelSelect.value = '3';

        this.renderSkillsList();
        this.updatePreview();
    }

    /**
     * Remove a skill
     */
    removeSkill(skillId) {
        this.skillsData = this.skillsData.filter(skill => skill.id !== skillId);
        this.renderSkillsList();
        this.updatePreview();
    }

    /**
     * Get level text from number
     */
    getLevelText(level) {
        const levels = {
            1: 'Beginner',
            2: 'Basic', 
            3: 'Intermediate',
            4: 'Advanced',
            5: 'Expert'
        };
        return levels[level] || 'Intermediate';
    }

    /**
     * Render skills list
     */
    renderSkillsList() {
        const container = document.getElementById('skillsList');
        if (!container) return;

        if (this.skillsData.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No skills added yet. Add your first skill above!</p>';
            return;
        }

        let html = '<div class="skills-grid">';
        this.skillsData.forEach(skill => {
            const stars = this.generateStars(skill.level);
            html += `
                <div class="skill-item-card" data-skill-id="${skill.id}">
                    <div class="skill-content">
                        <div class="skill-name">${skill.name}</div>
                        <div class="skill-rating">
                            ${stars}
                            <span class="skill-level-text">${skill.levelText}</span>
                        </div>
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-danger skill-remove" onclick="resumeComponents.removeSkill(${skill.id})">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
        });
        html += '</div>';

        container.innerHTML = html;
    }

    /**
     * Generate star rating HTML
     */
    generateStars(level) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            const starClass = i <= level ? 'fas fa-star text-warning' : 'far fa-star text-muted';
            stars += `<i class="${starClass}"></i>`;
        }
        return stars;
    }

    /**
     * Initialize form validation
     */
    initFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });

        // Add real-time validation
        document.querySelectorAll('input[required], textarea[required]').forEach(field => {
            field.addEventListener('blur', this.validateField);
            field.addEventListener('input', this.clearFieldError);
        });
    }

    /**
     * Validate individual field
     */
    validateField(e) {
        const field = e.target;
        const isValid = field.checkValidity();
        
        field.classList.toggle('is-valid', isValid);
        field.classList.toggle('is-invalid', !isValid);
    }

    /**
     * Clear field error state
     */
    clearFieldError(e) {
        const field = e.target;
        field.classList.remove('is-invalid', 'is-valid');
    }

    /**
     * Initialize real-time preview
     */
    initRealTimePreview() {
        const previewContainer = document.getElementById('resumePreview');
        if (!previewContainer) return;

        // Watch all form fields for changes
        document.querySelectorAll('input, textarea, select').forEach(field => {
            field.addEventListener('input', () => this.updatePreview());
            field.addEventListener('change', () => this.updatePreview());
        });

        this.updatePreview();
    }

    /**
     * Update resume preview
     */
    updatePreview() {
        const previewContainer = document.getElementById('resumePreview');
        if (!previewContainer) return;

        const formData = this.getFormData();
        const template = this.templates[this.selectedTemplate];

        const html = `
            <div class="resume-preview-content" style="border-left: 4px solid ${template.colors[0]};">
                <div class="preview-header" style="background: linear-gradient(135deg, ${template.colors[0]}, ${template.colors[1]}); color: white; padding: 20px; margin-bottom: 20px;">
                    <h3 class="preview-name">${formData.fullName || 'Your Name'}</h3>
                    <div class="preview-contact">
                        ${formData.email ? `📧 ${formData.email}` : ''}
                        ${formData.phone ? ` | 📞 ${formData.phone}` : ''}
                        ${formData.address ? ` | 🏠 ${formData.address}` : ''}
                    </div>
                </div>

                ${formData.summary ? `
                    <div class="preview-section">
                        <h5 style="color: ${template.colors[0]}; border-bottom: 2px solid ${template.colors[0]}; padding-bottom: 5px;">🎯 Professional Summary</h5>
                        <p>${formData.summary}</p>
                    </div>
                ` : ''}

                ${formData.education ? `
                    <div class="preview-section">
                        <h5 style="color: ${template.colors[0]}; border-bottom: 2px solid ${template.colors[0]}; padding-bottom: 5px;">🎓 Education</h5>
                        <p>${formData.education}</p>
                    </div>
                ` : ''}

                ${formData.experience ? `
                    <div class="preview-section">
                        <h5 style="color: ${template.colors[0]}; border-bottom: 2px solid ${template.colors[0]}; padding-bottom: 5px;">💼 Experience</h5>
                        <p>${formData.experience}</p>
                    </div>
                ` : ''}

                ${formData.projects ? `
                    <div class="preview-section">
                        <h5 style="color: ${template.colors[0]}; border-bottom: 2px solid ${template.colors[0]}; padding-bottom: 5px;">🚀 Projects</h5>
                        <p>${formData.projects}</p>
                    </div>
                ` : ''}

                ${this.skillsData.length > 0 ? `
                    <div class="preview-section">
                        <h5 style="color: ${template.colors[0]}; border-bottom: 2px solid ${template.colors[0]}; padding-bottom: 5px;">🛠️ Skills</h5>
                        <div class="preview-skills">
                            ${this.skillsData.map(skill => 
                                `<span class="preview-skill-tag" style="background-color: ${template.colors[0]}; color: white; padding: 4px 12px; border-radius: 15px; margin: 2px; display: inline-block; font-size: 0.85em;">
                                    ${skill.name} (${skill.levelText})
                                </span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        previewContainer.innerHTML = html;
    }

    /**
     * Get form data
     */
    getFormData() {
        return {
            fullName: document.getElementById('fullName')?.value || '',
            email: document.getElementById('email')?.value || '',
            phone: document.getElementById('phone')?.value || '',
            linkedin: document.getElementById('linkedin')?.value || '',
            address: document.getElementById('address')?.value || '',
            summary: document.getElementById('summary')?.value || '',
            education: document.getElementById('education')?.value || '',
            experience: document.getElementById('experience')?.value || '',
            projects: document.getElementById('projects')?.value || ''
        };
    }

    /**
     * Get skills as comma-separated string for API
     */
    getSkillsString() {
        return this.skillsData.map(skill => skill.name).join(', ');
    }

    /**
     * Get skills ratings as object for API
     */
    getSkillsRatings() {
        const ratings = {};
        this.skillsData.forEach(skill => {
            ratings[skill.name] = skill.level;
        });
        return ratings;
    }

    /**
     * Load skills from data (for editing)
     */
    loadSkills(skillsString, ratingsObject = {}) {
        this.skillsData = [];
        
        if (skillsString) {
            const skills = skillsString.split(',').map(s => s.trim()).filter(s => s);
            skills.forEach(skillName => {
                this.skillsData.push({
                    id: Date.now() + Math.random(),
                    name: skillName,
                    level: ratingsObject[skillName] || 3,
                    levelText: this.getLevelText(ratingsObject[skillName] || 3)
                });
            });
        }
        
        this.renderSkillsList();
        this.updatePreview();
    }

    /**
     * Show alert message
     */
    showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of page
        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    /**
     * Duplicate resume functionality
     */
    duplicateResume(resumeId) {
        if (confirm('Create a copy of this resume?')) {
            // Implementation would load the resume data and create a new one
            this.showAlert('Resume duplication feature will be implemented', 'info');
        }
    }

    /**
     * Export resume in different formats
     */
    exportResume(format, resumeId) {
        switch(format) {
            case 'pdf':
                downloadResumePDF(resumeId);
                break;
            case 'json':
                this.exportAsJSON(resumeId);
                break;
            default:
                this.showAlert('Export format not supported yet', 'warning');
        }
    }

    /**
     * Export resume as JSON
     */
    async exportAsJSON(resumeId) {
        try {
            const data = await apiRequest(`/api/resumes/${resumeId}`);
            const jsonData = JSON.stringify(data.resume, null, 2);
            
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `resume_${resumeId}.json`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            this.showAlert('Resume exported as JSON successfully!', 'success');
        } catch (error) {
            this.showAlert('Failed to export resume: ' + error.message, 'danger');
        }
    }
}

// Initialize the components manager
const resumeComponents = new ResumeComponentsManager();

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    resumeComponents.init();
});
