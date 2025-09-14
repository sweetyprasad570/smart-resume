// Smart Resume - Main JavaScript functionality

// API Base URL - adjust based on current location
const API_BASE = window.location.origin;

// Demo mode flag
const DEMO_MODE = false; // Set to false to use real authentication

// Authentication helpers
function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function removeToken() {
  localStorage.removeItem("access_token");
}

function isAuthenticated() {
  return !!getToken();
}

// API request helper
async function apiRequest(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add token to headers if available
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
      credentials: "include", // Include cookies in requests
    });

    const data = await response.json();

    if (!response.ok) {
      // Handle JWT token expiration
      if (response.status === 401) {
        if (
          data.msg === "Token has expired" ||
          data.message === "Token has expired"
        ) {
          removeToken();
          updateAuthUI();
          showAlert("Session expired. Please login again.", "warning");
          setTimeout(() => {
            window.location.href = "/login";
          }, 2000);
          return;
        } else if (
          data.message === "Please login to view resumes" ||
          data.msg === "Authorization token required"
        ) {
          showAlert("Please login to access this feature.", "warning");
          setTimeout(() => {
            window.location.href = "/login";
          }, 2000);
          return;
        }
      }
      throw new Error(data.message || data.msg || "Request failed");
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Show/hide elements based on authentication
function updateAuthUI() {
  const isAuth = isAuthenticated();
  const authElements = document.querySelectorAll(".auth-required");
  const guestElements = document.querySelectorAll(".guest-only");

  console.log('UpdateAuthUI called, isAuth:', isAuth);
  console.log('Found auth elements:', authElements.length);
  console.log('Found guest elements:', guestElements.length);

  // Show/hide authenticated elements
  authElements.forEach((el) => {
    if (isAuth) {
      el.style.display = "";
      // Add smooth fade-in animation
      el.style.opacity = "0";
      el.style.transition = "opacity 0.3s ease-in-out";
      setTimeout(() => {
        el.style.opacity = "1";
      }, 100);
    } else {
      el.style.display = "none";
    }
  });

  // Show/hide guest elements
  guestElements.forEach((el) => {
    if (isAuth) {
      // Fade out guest elements
      el.style.opacity = "0";
      el.style.transition = "opacity 0.3s ease-in-out";
      setTimeout(() => {
        el.style.display = "none";
      }, 300);
    } else {
      el.style.display = "";
      el.style.opacity = "1";
    }
  });
  
  // Update user info if logged in
  if (isAuth) {
    const userData = localStorage.getItem('user_data');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        console.log('Updating user info for:', user.name || user.email);
        
        // Update user name elements
        const userNameElements = document.querySelectorAll('.user-name');
        userNameElements.forEach(el => {
          el.textContent = user.name || user.email || 'User';
        });
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
  } else {
    // Clear user name when logged out
    const userNameElements = document.querySelectorAll('.user-name');
    userNameElements.forEach(el => {
      el.textContent = 'User';
    });
  }
}

// Login functionality
async function login(email, password) {
  try {
    const data = await apiRequest("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    setToken(data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("user_data", JSON.stringify(data.user));
    updateAuthUI();
    showAlert("Login successful!", "success");
    // Redirect to dashboard after login
    window.location.href = "/dashboard";
    return true;
  } catch (error) {
    showAlert(error.message, "danger");
    return false;
  }
}

// Enhanced Logout functionality
async function logout() {
  console.log('Logout initiated...');
  
  try {
    // Show loading state on logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      const originalText = logoutBtn.innerHTML;
      logoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Logging out...';
      logoutBtn.disabled = true;
    }
    
    // Call backend logout endpoint
    await apiRequest("/api/auth/logout", { method: "POST" });
    console.log('Backend logout successful');
  } catch (error) {
    console.error("Logout API error:", error);
    // Continue with logout even if API call fails
  }

  // Clear all authentication data
  removeToken();
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_data");
  
  console.log('Authentication data cleared');

  // Update UI immediately
  updateAuthUI();
  
  // Show success message
  showAlert("Logged out successfully! Redirecting to home page...", "success");
  
  // Redirect to home page
  setTimeout(() => {
    window.location.href = "/";
  }, 1500);
}

// Registration functionality
async function register(name, email, password) {
  try {
    const data = await apiRequest("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password }),
    });

    showAlert("Registration successful! Redirecting to login...", "success");
    // Redirect to login page after registration
    setTimeout(() => {
      window.location.href = "/login";
    }, 2000);
    return true;
  } catch (error) {
    showAlert(error.message, "danger");
    return false;
  }
}

// Show alert messages
function showAlert(message, type = "info") {
  const alertContainer = document.getElementById("alert-container");
  if (!alertContainer) return;

  const alert = document.createElement("div");
  alert.className = `alert alert-${type} alert-dismissible fade show`;
  alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  alertContainer.appendChild(alert);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (alert.parentNode) {
      alert.remove();
    }
  }, 5000);
}

// Initialize Smart Resume App
document.addEventListener("DOMContentLoaded", function () {
  console.log('🚀 Smart Resume initialized - DOM loaded');
  console.log('Current path:', window.location.pathname);
  console.log('Is authenticated:', isAuthenticated());
  
  // Always update auth UI on all pages
  updateAuthUI();
  
  // Set up logout button handler
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", function(e) {
      e.preventDefault();
      console.log('Logout button clicked');
      logout();
    });
    console.log('✅ Logout button handler attached');
  } else {
    console.log('ℹ️ Logout button not found (user not logged in)');
  }
  
  // Add navbar scroll effect (optional enhancement)
  let lastScrollTop = 0;
  window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.smart-navbar');
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down - slightly transparent
      navbar.style.backgroundColor = 'rgba(37, 99, 235, 0.95)';
    } else {
      // Scrolling up - fully opaque
      navbar.style.backgroundColor = '';
    }
    lastScrollTop = scrollTop;
  });
  
  // Debug current authentication state
  const userData = localStorage.getItem('user_data');
  if (userData) {
    try {
      const user = JSON.parse(userData);
      console.log('✅ Logged in as:', user.name || user.email);
    } catch (e) {
      console.log('⚠️ Invalid user data, clearing...');
      localStorage.removeItem('user_data');
    }
  } else {
    console.log('ℹ️ No user data found (guest mode)');
  }
  
  console.log('🎉 Smart Resume initialization complete');
});
