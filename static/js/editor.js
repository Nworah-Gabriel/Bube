// js/editor.js

// Get project ID from URL
const params = new URLSearchParams(window.location.search);
const projectId = params.get('id');

// DOM Elements
const titleInput = document.getElementById('title');
const categoryInput = document.getElementById('project_category');
const ownersInput = document.getElementById('owners');
const dateInput = document.getElementById('date');
const livePreview = document.getElementById('live-preview');
const saveDraftBtn = document.getElementById('save-draft');
const publishBtn = document.getElementById('publish');
const featuredImageInput = document.getElementById('featured-image');
const galleryImagesInput = document.getElementById('gallery-images');

// Initialize Quill editor
const quill = new Quill('#editor', {
    modules: { 
        toolbar: '#quill-toolbar' 
    },
    theme: 'snow'
});

// Store images as Base64
let featuredImageBase64 = '';
let galleryImagesBase64 = [];


// Custom Preloader Functions
function showPreloader(message = 'Uploading...') {
    // Create preloader element if it doesn't exist
    if (!document.querySelector('.mil-upload-preloader')) {
        const preloaderHTML = `
            <div class="mil-upload-preloader" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100vh;
                background-color: rgba(0, 0, 0, 0.95);
                z-index: 9999;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            ">
                <div class="mil-preloader-animation" style="
                    position: relative;
                    height: 100vh;
                    color: rgb(255, 255, 255);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                ">
                    <div class="mil-pos-abs" style="
                        position: absolute;
                        height: 100vh;
                        width: 100%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-direction: column;
                    ">
                        <p class="mil-h3 mil-muted mil-thin" style="
                            opacity: 1;
                            margin-bottom: 10px;
                            font-size: 2.5rem;
                        ">${message}</p>
                        <p class="mil-h3 mil-muted" style="
                            opacity: 1;
                            margin-bottom: 10px;
                            font-size: 2rem;
                        ">Please wait</p>
                    </div>
                    <div class="mil-pos-abs" style="
                        position: absolute;
                        height: 100vh;
                        width: 100%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin-top: 100px;
                    ">
                        <div class="mil-reveal-frame" style="
                            position: relative;
                            padding: 0 30px;
                        ">
                            <p class="mil-reveal-box" style="
                                z-index: 4;
                                position: absolute;
                                opacity: 1;
                                height: 100%;
                                background-color: rgb(255, 152, 0);
                                animation: revealAnimation 2s ease-in-out infinite;
                                width: 100px;
                            "></p>
                            <p class="mil-h3 mil-muted mil-thin" style="
                                opacity: 1;
                                color: rgb(255, 255, 255);
                                font-size: 1.5rem;
                            ">Processing your project...</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', preloaderHTML);
        
        // Add animation keyframes
        const style = document.createElement('style');
        style.textContent = `
            @keyframes revealAnimation {
                0% {
                    width: 0;
                    left: 0;
                }
                50% {
                    width: 100%;
                    left: 0;
                }
                100% {
                    width: 0;
                    left: 100%;
                }
            }
        `;
        document.head.appendChild(style);
    } else {
        // Update existing preloader message
        const messageElement = document.querySelector('.mil-upload-preloader .mil-h3.mil-thin');
        if (messageElement) {
            messageElement.textContent = message;
        }
        document.querySelector('.mil-upload-preloader').style.display = 'flex';
    }
}

function hidePreloader() {
    const preloader = document.querySelector('.mil-upload-preloader');
    if (preloader) {
        preloader.style.display = 'none';
    }
}

// Custom Success Notification
function showSuccessNotification(message, status) {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.mil-success-notification');
    existingNotifications.forEach(notification => notification.remove());
    
    const notificationHTML = `
        <div class="mil-success-notification" style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(0, 0, 0, 0.9);
            border: 2px solid rgb(255, 152, 0);
            border-radius: 10px;
            padding: 40px;
            z-index: 10000;
            text-align: center;
            min-width: 400px;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        ">
            <div class="mil-notification-content" style="color: rgb(255, 255, 255);">
                <div class="mil-success-icon" style="
                    font-size: 48px;
                    color: rgb(255, 152, 0);
                    margin-bottom: 20px;
                ">
                    ✓
                </div>
                <h3 class="mil-h3" style="
                    color: rgb(255, 255, 255);
                    margin-bottom: 15px;
                    font-size: 28px;
                ">
                    Project ${status === 'draft' ? 'Saved' : 'Published'}!
                </h3>
                <p class="mil-text-lg" style="
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 30px;
                    font-size: 18px;
                    line-height: 1.5;
                ">
                    ${message}
                </p>
                <div class="mil-notification-buttons" style="
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                ">
                    <button class="mil-button mil-arrow-place" id="notification-continue" style="
                        background-color: rgb(255, 152, 0);
                        color: rgb(0, 0, 0);
                        border: none;
                        padding: 15px 30px;
                        border-radius: 70px;
                        font-size: 12px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 2px;
                        cursor: pointer;
                        transition: 0.4s cubic-bezier(0, 0, 0.3642, 1);
                        display: flex;
                        align-items: center;
                    ">
                        <span>Continue to Dashboard</span>
                        <svg style="
                            margin-left: 15px;
                            border-radius: 50%;
                            width: 40px;
                            height: 40px;
                            padding: 10px;
                            background-color: rgb(0, 0, 0);
                            transition: inherit;
                        " viewBox="0 0 128 128">
                            <path fill="rgb(255, 152, 0)" d="M106.1,41.9c-1.2-1.2-3.1-1.2-4.2,0c-1.2,1.2-1.2,3.1,0,4.2L116.8,61H11.2l14.9-14.9c1.2-1.2,1.2-3.1,0-4.2	c-1.2-1.2-3.1-1.2-4.2,0l-20,20c-1.2,1.2-1.2,3.1,0,4.2l20,20c0.6,0.6,1.4,0.9,2.1,0.9s1.5-0.3,2.1-0.9c1.2-1.2,1.2-3.1,0-4.2	L11.2,67h105.5l-14.9,14.9c-1.2,1.2-1.2,3.1,0,4.2c0.6,0.6,1.4,0.9,2.1,0.9s1.5-0.3,2.1-0.9l20-20c1.2-1.2,1.2-3.1,0-4.2L106.1,41.9	z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', notificationHTML);
    
    // Add event listener to continue button
    document.getElementById('notification-continue').addEventListener('click', function() {
        hideNotification();
        window.location.href = '/';
    });
    
    // Auto-hide after 5 seconds and redirect
    setTimeout(() => {
        hideNotification();
        window.location.href = '/';
    }, 5000);
}

function hideNotification() {
    const notification = document.querySelector('.mil-success-notification');
    if (notification) {
        notification.style.opacity = '0';
        notification.style.transform = 'translate(-50%, -50%) scale(0.9)';
        notification.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }
}

// Load project data from Django template context
function loadProjectData() {
    // Check if project data is passed via Django template
    if (typeof window.projectData !== 'undefined') {
        const p = window.projectData;
        titleInput.value = p.title || '';
        ownersInput.value = p.owners || '';
        if (categoryInput) categoryInput.value = p.category || '';
        dateInput.value = p.date || '';
        if (p.content) {
            quill.root.innerHTML = p.content;
        }
        updatePreview();
    }
}

// Live preview update
function updatePreview() {
    livePreview.innerHTML = `
        <h2 style="overflow-x: auto;overflow-wrap: break-word">${titleInput.value || 'Untitled Project'}</h2>
        <p style="overflow-x: auto;overflow-wrap: break-word"><strong>Client:</strong> ${ownersInput.value || 'Not specified'}</p>
        <p style="overflow-x: auto;overflow-wrap: break-word"><strong>Date:</strong> ${dateInput.value || 'Not specified'}</p>
        ${featuredImageBase64 ? `<img src="${featuredImageBase64}" style="max-width: 100%; height: auto; margin-bottom: 20px;" alt="Featured Image">` : ''}
        <div style="overflow-x: auto;overflow-wrap: break-word">${quill.root.innerHTML || '<p>No content yet...</p>'}</div>
    `;
}

// Event listeners for live preview
titleInput.addEventListener('input', updatePreview);
ownersInput.addEventListener('input', updatePreview);
dateInput.addEventListener('input', updatePreview);
quill.on('text-change', updatePreview);

// Handle featured image upload
featuredImageInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(ev) {
            featuredImageBase64 = ev.target.result;
            updatePreview();
        };
        reader.readAsDataURL(file);
    }
});

// Handle gallery images upload
galleryImagesInput.addEventListener('change', function(e) {
    galleryImagesBase64 = [];
    const files = Array.from(e.target.files);
    
    files.forEach(file => {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(ev) {
                galleryImagesBase64.push(ev.target.result);
            };
            reader.readAsDataURL(file);
        }
    });
});

// Save project function
async function saveProjectData(status) {
    try {
        // Show preloader
        showPreloader(status === 'draft' ? 'Saving Draft...' : 'Publishing Project...');
        
        // Prepare project data
        const projectData = {
            id: projectId || null,
            title: titleInput.value,
            owners: ownersInput.value,
            date: dateInput.value,
            content: quill.root.innerHTML,
            featuredImage: featuredImageBase64,
            galleryImage: galleryImagesBase64.length > 0 ? galleryImagesBase64[0] : '', // Send first image for now
            status: status,
            projectCategory: categoryInput ? categoryInput.value : ''
        };

        // Send to Django API
        const response = await fetch('https://bube-7hpy.onrender.com/admin/api/projects/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(projectData)
        });

        const result = await response.json();

        // Hide preloader
        hidePreloader();

        if (result.success) {
            // Show custom success notification instead of alert
            showSuccessNotification(
                `Your project "${titleInput.value}" has been successfully ${status === 'draft' ? 'saved as draft' : 'published and is now live!'}`,
                status
            );
        } else {
            // Show error notification
            const errorNotificationHTML = `
                <div class="mil-error-notification" style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: rgba(0, 0, 0, 0.9);
                    border: 2px solid #ff4444;
                    border-radius: 10px;
                    padding: 40px;
                    z-index: 10000;
                    text-align: center;
                    min-width: 400px;
                    max-width: 600px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                ">
                    <div class="mil-notification-content" style="color: rgb(255, 255, 255);">
                        <div class="mil-error-icon" style="
                            font-size: 48px;
                            color: #ff4444;
                            margin-bottom: 20px;
                        ">
                            ✗
                        </div>
                        <h3 class="mil-h3" style="
                            color: rgb(255, 255, 255);
                            margin-bottom: 15px;
                            font-size: 28px;
                        ">
                            Upload Failed
                        </h3>
                        <p class="mil-text-lg" style="
                            color: rgba(255, 255, 255, 0.8);
                            margin-bottom: 30px;
                            font-size: 18px;
                            line-height: 1.5;
                        ">
                            ${result.message || 'An error occurred while saving the project.'}
                        </p>
                        <button class="mil-button" id="error-close" style="
                            background-color: #ff4444;
                            color: rgb(255, 255, 255);
                            border: none;
                            padding: 15px 30px;
                            border-radius: 70px;
                            font-size: 12px;
                            font-weight: 500;
                            text-transform: uppercase;
                            letter-spacing: 2px;
                            cursor: pointer;
                            transition: 0.4s cubic-bezier(0, 0, 0.3642, 1);
                        ">
                            <span>Close</span>
                        </button>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', errorNotificationHTML);
            
            document.getElementById('error-close').addEventListener('click', function() {
                const errorNotif = document.querySelector('.mil-error-notification');
                if (errorNotif) errorNotif.remove();
            });
            
            console.log('Error details:', result);
        }

    } catch (error) {
        console.error('Error saving project:', error);
        
        // Hide preloader
        hidePreloader();
        
        // Show error notification for network errors
        const networkErrorHTML = `
            <div class="mil-error-notification" style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: rgba(0, 0, 0, 0.9);
                border: 2px solid #ff4444;
                border-radius: 10px;
                padding: 40px;
                z-index: 10000;
                text-align: center;
                min-width: 400px;
                max-width: 600px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            ">
                <div class="mil-notification-content" style="color: rgb(255, 255, 255);">
                    <div class="mil-error-icon" style="
                        font-size: 48px;
                        color: #ff4444;
                        margin-bottom: 20px;
                    ">
                        ✗
                    </div>
                    <h3 class="mil-h3" style="
                        color: rgb(255, 255, 255);
                        margin-bottom: 15px;
                        font-size: 28px;
                    ">
                        Network Error
                    </h3>
                    <p class="mil-text-lg" style="
                        color: rgba(255, 255, 255, 0.8);
                        margin-bottom: 30px;
                        font-size: 18px;
                        line-height: 1.5;
                    ">
                        Unable to connect to the server. Please check your internet connection and try again.
                    </p>
                    <button class="mil-button" id="network-error-close" style="
                        background-color: #ff4444;
                        color: rgb(255, 255, 255);
                        border: none;
                        padding: 15px 30px;
                        border-radius: 70px;
                        font-size: 12px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 2px;
                        cursor: pointer;
                        transition: 0.4s cubic-bezier(0, 0, 0.3642, 1);
                    ">
                        <span>Close</span>
                    </button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', networkErrorHTML);
        
        document.getElementById('network-error-close').addEventListener('click', function() {
            const errorNotif = document.querySelector('.mil-error-notification');
            if (errorNotif) errorNotif.remove();
        });
    }
}

// Button event listeners
saveDraftBtn.addEventListener('click', () => saveProjectData('draft'));
publishBtn.addEventListener('click', () => saveProjectData('published'));

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProjectData();
    updatePreview();
});