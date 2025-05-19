/**
 * MRI Insight - Main JavaScript
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality
    const fileInput = document.getElementById('formFile');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            previewImage(this);
        });
    }
    
    // Function to preview uploaded image
    function previewImage(input) {
        if (!previewContainer || !imagePreview) return;
        
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.style.display = 'block';
                
                // Add animation class
                imagePreview.classList.add('fade-in');
                
                // Remove animation class after animation completes
                setTimeout(() => {
                    imagePreview.classList.remove('fade-in');
                }, 500);
            }
            
            reader.readAsDataURL(input.files[0]);
        } else {
            imagePreview.src = '';
            previewContainer.style.display = 'none';
        }
    }
    
    // Form validation
    const uploadForm = document.querySelector('form[action="/upload"]');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            if (!fileInput.files || fileInput.files.length === 0) {
                event.preventDefault();
                alert('Please select an MRI image file to upload.');
                return false;
            }
            
            // Show loading state
            const uploadBtn = document.getElementById('upload-btn');
            if (uploadBtn) {
                uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
                uploadBtn.disabled = true;
            }
            
            return true;
        });
    }
    
    // Results page - Print functionality
    const printBtn = document.querySelector('.btn-download');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Add smooth scrolling for all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add fade-in animation to elements when they come into view
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card, .result-card').forEach(el => {
        el.classList.add('fade-in-element');
        observer.observe(el);
    });
});

// Add CSS class for fade-in animation
document.head.insertAdjacentHTML('beforeend', `
<style>
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .fade-in-element {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }
    
    .fade-in-element.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @media print {
        .btn-back, .btn-download, .header, .footer {
            display: none !important;
        }
        
        body {
            padding: 0;
            margin: 0;
        }
        
        .result-container {
            box-shadow: none;
            border: none;
        }
    }
</style>
`);