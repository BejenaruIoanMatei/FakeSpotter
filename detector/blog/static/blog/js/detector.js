class ImageDetectorUI {
    constructor() {
        this.fileInput = null;
        this.fileLabel = null;
        this.form = null;
        this.submitBtn = null;
        this.container = null;
        
        this.init();
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
    }


    setupEventListeners() {
        this.fileInput = document.getElementById('imageInput');
        this.fileLabel = document.querySelector('.file-input-label');
        this.form = document.querySelector('form');
        this.submitBtn = document.querySelector('.submit-btn');
        this.container = document.querySelector('.container');

        this.setupFileInputListener();
        this.setupFormSubmitListener();
        this.setupHoverAnimations();
        this.setupDragAndDrop();
        this.setupResultsScroll();
    }

    setupFileInputListener() {
        if (!this.fileInput || !this.fileLabel) return;

        this.fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            
            if (file) {
                this.updateFileLabel(file.name, true);
                this.validateFile(file);
            } else {
                this.resetFileLabel();
            }
        });
    }

    updateFileLabel(fileName, hasFile = false) {
        if (!this.fileLabel) return;

        if (hasFile) {
            const displayName = fileName.length > 20 
                ? fileName.substring(0, 20) + '...' 
                : fileName;
            
            this.fileLabel.innerHTML = `${displayName}`;
            this.fileLabel.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
        } else {
            this.resetFileLabel();
        }
    }

    resetFileLabel() {
        if (!this.fileLabel) return;
        
        this.fileLabel.innerHTML = 'Choose Image';
        this.fileLabel.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
    }

    validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10mb
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];

        if (file.size > maxSize) {
            this.showTemporaryMessage('File too large! Please select an image under 10MB.', 'warning');
            return false;
        }

        if (!allowedTypes.includes(file.type)) {
            this.showTemporaryMessage('Invalid file type! Please select a valid image.', 'warning');
            return false;
        }

        return true;
    }


    setupFormSubmitListener() {
        if (!this.form || !this.submitBtn) return;

        this.form.addEventListener('submit', (e) => {
            const file = this.fileInput?.files[0];
            if (!file || !this.validateFile(file)) {
                e.preventDefault();
                return;
            }

            this.setLoadingState(true);
        });
    }

    setLoadingState(isLoading) {
        if (!this.submitBtn || !this.container) return;

        if (isLoading) {
            this.submitBtn.innerHTML = 'Analyzing...wait a sec';
            this.submitBtn.classList.add('loading');
            this.submitBtn.disabled = true;
            this.container.style.opacity = '0.8';
        } else {
            this.submitBtn.innerHTML = 'Analyze Image';
            this.submitBtn.classList.remove('loading');
            this.submitBtn.disabled = false;
            this.container.style.opacity = '1';
        }
    }
    setupHoverAnimations() {
        const animatedElements = document.querySelectorAll('.result, .error');
        
        animatedElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.transform = 'translateY(-2px)';
                element.style.transition = 'transform 0.3s ease';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translateY(0)';
            });
        });
    }
    setupDragAndDrop() {
        if (!this.container) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.container.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            this.container.addEventListener(eventName, () => this.highlightDropZone(true), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.container.addEventListener(eventName, () => this.highlightDropZone(false), false);
        });

        this.container.addEventListener('drop', (e) => this.handleDrop(e), false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    highlightDropZone(highlight) {
        if (!this.container) return;

        if (highlight) {
            this.container.style.background = 'rgba(255, 255, 255, 1)';
            this.container.style.borderColor = '#667eea';
            this.container.style.border = '2px dashed #667eea';
        } else {
            this.container.style.background = 'rgba(255, 255, 255, 0.95)';
            this.container.style.borderColor = 'transparent';
            this.container.style.border = 'none';
        }
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            const file = files[0];
            
            if (this.validateFile(file)) {
                this.fileInput.files = files;
                this.updateFileLabel(file.name, true);
                
                this.showTemporaryMessage('File ready for analysis!', 'success');
            }
        }
    }

    showTemporaryMessage(message, type = 'info') {
        const messageEl = document.createElement('div');
        messageEl.className = `temp-message temp-message-${type}`;
        messageEl.textContent = message;
        Object.assign(messageEl.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '1000',
            animation: 'slideIn 0.3s ease',
            maxWidth: '300px'
        });
        const colors = {
            success: 'linear-gradient(135deg, #48bb78, #38a169)',
            warning: 'linear-gradient(135deg, #ed8936, #dd6b20)',
            error: 'linear-gradient(135deg, #fc8181, #f56565)',
            info: 'linear-gradient(135deg, #667eea, #764ba2)'
        };
        messageEl.style.background = colors[type] || colors.info;

        document.body.appendChild(messageEl);

        setTimeout(() => {
            messageEl.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, 3000);
    }

    setupResultsScroll() {
        const resultElement = document.querySelector('.result');
        
        if (resultElement) {
            setTimeout(() => {
                resultElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }, 300);
        }
    }

    resetForm() {
        if (this.fileInput) {
            this.fileInput.value = '';
        }
        this.resetFileLabel();
        this.setLoadingState(false);
    }

    getCurrentFile() {
        return this.fileInput?.files[0] || null;
    }
}

const DetectorUtils = {
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    debounce(func, wait) {
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
};

const imageDetector = new ImageDetectorUI();

const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ImageDetectorUI, DetectorUtils };
}