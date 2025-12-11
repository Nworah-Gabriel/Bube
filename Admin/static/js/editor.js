// js/editor.js

const params = new URLSearchParams(window.location.search);
const projectId = params.get('id');

const titleInput = document.getElementById('title');
const ownersInput = document.getElementById('owners');
const dateInput = document.getElementById('date');
const livePreview = document.getElementById('live-preview');
const saveDraftBtn = document.getElementById('save-draft');
const publishBtn = document.getElementById('publish');

// Initialize Quill editor
const quill = new Quill('#editor', {
    modules: { toolbar: '#quill-toolbar' },
    theme: 'snow'
});

// Load project if editing
if(projectId){
    const p = getProjectById(projectId);
    if(p){
        titleInput.value = p.title;
        ownersInput.value = p.owners;
        dateInput.value = p.date;
        quill.root.innerHTML = p.content;
        updatePreview();
    }
}

// Live preview
function updatePreview(){
    livePreview.innerHTML = `
        <h2>${titleInput.value}</h2>
        <p><strong>Owners:</strong> ${ownersInput.value}</p>
        <p><strong>Date:</strong> ${dateInput.value}</p>
        <div>${quill.root.innerHTML}</div>
    `;
}

titleInput.addEventListener('input', updatePreview);
ownersInput.addEventListener('input', updatePreview);
dateInput.addEventListener('input', updatePreview);
quill.on('text-change', updatePreview);

// Save function
function saveProjectData(status){
    const project = {
    id: projectId || Date.now().toString(),
    title: titleInput.value,
    owners: ownersInput.value,
    date: dateInput.value,
    content: quill.root.innerHTML,
    featuredImage: featuredImageBase64, // <-- add this line
    status
};
saveProject(project);

    alert(`Project ${status === 'draft' ? 'saved as draft' : 'published'}!`);
    window.location.href='dashboard.html';
}

saveDraftBtn.addEventListener('click', ()=>saveProjectData('draft'));
publishBtn.addEventListener('click', ()=>saveProjectData('published'));

let featuredImageBase64 = '';


const featuredImageInput = document.getElementById('featured-image');

featuredImageInput.addEventListener('change', function(e){
    const file = e.target.files[0];
    if(file){
        const reader = new FileReader();
        reader.onload = function(ev){
            featuredImageBase64 = ev.target.result; // stores the image in Base64
        }
        reader.readAsDataURL(file);
    }
});

