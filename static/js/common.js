/**
 * Common JavaScript utilities and API functions
 */

// Configuration
const API_BASE = ""; // Since we're serving from the same domain

// Global variables
let currentResumeId = null;

/**
 * Make API request with proper error handling
 */
async function apiRequest(endpoint, options = {}) {
  try {
    const defaultOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const requestOptions = { ...defaultOptions, ...options };

    // Add token if available
    const token = localStorage.getItem("access_token");
    if (token) {
      requestOptions.headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(API_BASE + endpoint, {
      ...requestOptions,
      credentials: "include", // Include cookies in requests
    });

    if (!response.ok) {
      let errorMessage;
      try {
        const errorData = await response.json();
        errorMessage =
          errorData.error || errorData.message || `HTTP ${response.status}`;

        // Handle authentication errors
        if (response.status === 401) {
          if (
            errorData.msg === "Token has expired" ||
            errorData.message === "Token has expired"
          ) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("user_data");
            if (typeof updateAuthUI === "function") {
              updateAuthUI();
            }
            if (typeof showAlert === "function") {
              showAlert("Session expired. Please login again.", "warning");
            }
            setTimeout(() => {
              window.location.href = "/login";
            }, 2000);
            return;
          } else if (
            errorData.message === "Please login to view resumes" ||
            errorData.msg === "Authorization token required"
          ) {
            if (typeof showAlert === "function") {
              showAlert("Please login to access this feature.", "warning");
            }
            setTimeout(() => {
              window.location.href = "/login";
            }, 2000);
            return;
          }
        }
      } catch {
        errorMessage = `HTTP ${response.status} - ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    console.error("API Request failed:", error);
    throw error;
  }
}

/**
 * Show alert message to user
 */
function showAlert(message, type = "info") {
  // Remove existing alerts
  document.querySelectorAll(".alert").forEach((alert) => {
    if (!alert.classList.contains("permanent")) {
      alert.remove();
    }
  });

  // Create alert element
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.style.position = "fixed";
  alertDiv.style.top = "20px";
  alertDiv.style.right = "20px";
  alertDiv.style.zIndex = "9999";
  alertDiv.style.maxWidth = "400px";
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  // Add to page
  document.body.appendChild(alertDiv);

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove();
    }
  }, 5000);
}

/**
 * Validate form data
 */
function validateResumeForm(data) {
  const errors = [];

  if (!data.full_name || data.full_name.trim().length < 2) {
    errors.push("Full name is required (minimum 2 characters)");
  }

  if (!data.email || !isValidEmail(data.email)) {
    errors.push("Valid email address is required");
  }

  if (data.phone && !isValidPhone(data.phone)) {
    errors.push("Phone number format is invalid");
  }

  if (data.linkedin && !isValidURL(data.linkedin)) {
    errors.push("LinkedIn URL format is invalid");
  }

  return errors;
}

/**
 * Validate email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate phone format
 */
function isValidPhone(phone) {
  const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
  return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ""));
}

/**
 * Validate URL format
 */
function isValidURL(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * Format date for display
 */
function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/**
 * Debounce function for search/input handling
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Generate random ID
 */
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * Sanitize HTML to prevent XSS
 */
function sanitizeHTML(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Show loading state on button
 */
function showButtonLoading(button, loadingText = "Loading...") {
  if (!button.dataset.originalText) {
    button.dataset.originalText = button.innerHTML;
  }
  button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${loadingText}`;
  button.disabled = true;
}

/**
 * Hide loading state on button
 */
function hideButtonLoading(button) {
  if (button.dataset.originalText) {
    button.innerHTML = button.dataset.originalText;
    button.disabled = false;
  }
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showAlert("Copied to clipboard!", "success");
    return true;
  } catch (error) {
    console.error("Failed to copy to clipboard:", error);
    showAlert("Failed to copy to clipboard", "danger");
    return false;
  }
}

/**
 * Download file from blob
 */
function downloadFile(blob, filename) {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.style.display = "none";
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

// Initialize common functionality when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Initialize all tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize all popovers
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Add smooth scroll behavior to anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Handle form validation styling
  document.querySelectorAll(".needs-validation").forEach((form) => {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
          showAlert("Please fill in all required fields correctly", "warning");
        }
        form.classList.add("was-validated");
      },
      false
    );
  });

  console.log("Common JavaScript utilities loaded successfully");
});
