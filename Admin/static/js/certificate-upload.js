// js/certificate-upload.js

// DOM Elements
const certTitleInput = document.getElementById('certTitle');
const certIssuerInput = document.getElementById('certIssuer');
const certDateInput = document.getElementById('certDate');
const certDescriptionInput = document.getElementById('certDescription');
const certImageInput = document.getElementById('admCertInput');
const certUploadBtn = document.getElementById('admCertUploadBtn');

// Store certificate image as Base64
let certificateBase64 = '';

// Django CSRF Token function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Custom Preloader Functions (similar to project editor)
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
                z-index: 9000;
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
                            ">...</p>
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
function showSuccessNotification(message) {
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
                    Certificate Uploaded!
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
                        <span>Upload More</span>
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
        // Optionally reset form or redirect
        resetForm();
    });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideNotification();
        resetForm();
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

// Handle certificate image upload
certImageInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file && (file.type.startsWith('image/') || file.type === 'application/pdf')) {
        const reader = new FileReader();
        reader.onload = function(ev) {
            certificateBase64 = ev.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please select an image or PDF file.');
        certImageInput.value = '';
    }
});

// Upload certificate function
async function uploadCertificate() {
    try {
        const title = certTitleInput.value.trim();
        const issuer = certIssuerInput.value.trim();
        const date = certDateInput.value;
        const description = certDescriptionInput.value.trim();
        
        // Validation
        if (!certificateBase64) {
            alert('Please select a certificate image to upload.');
            return;
        }
        
        if (!title) {
            alert('Please enter a certificate title.');
            certTitleInput.focus();
            return;
        }
        
        if (!issuer) {
            alert('Please enter the issuing organization.');
            certIssuerInput.focus();
            return;
        }
        
        // Show preloader
        showPreloader('Uploading Certificate...');
        
        // Prepare certificate data
        const certificateData = {
            title: title,
            issuer: issuer,
            issue_date: date || null,
            description: description,
            certificate_image: certificateBase64
        };

        console.log("Sending certificate data:", { 
            title, 
            issuer, 
            date,
            hasImage: !!certificateBase64 
        });
        
        // Send to Django API
        const response = await fetch('/admin/api/certificates/upload/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(certificateData)
        });

        const result = await response.json();
        
        // Hide preloader
        hidePreloader();

        console.log("API Response:", result);

        if (result.success) {
            // Show success notification
            showSuccessNotification(
                `Your certificate "${title}" has been uploaded successfully!`
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
                            ${result.message || 'An error occurred while uploading the certificate.'}
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
        console.error('Error uploading certificate:', error);
        
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

function resetForm() {
    certTitleInput.value = '';
    certIssuerInput.value = '';
    certDateInput.value = '';
    certDescriptionInput.value = '';
    certImageInput.value = '';
    certificateBase64 = '';
}

// Button event listener
certUploadBtn.addEventListener('click', uploadCertificate);

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Certificate upload script loaded');
});