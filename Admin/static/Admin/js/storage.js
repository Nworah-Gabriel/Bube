// js/storage.js

function getProjects() {
    return JSON.parse(localStorage.getItem('projects')) || [];
}

function saveProject(project) {
    const projects = getProjects();
    const index = projects.findIndex(p => p.id === project.id);
    if(index > -1){
        projects[index] = project;
    } else {
        projects.push(project);
    }
    localStorage.setItem('projects', JSON.stringify(projects));
}

function deleteProject(id) {
    const projects = getProjects().filter(p => p.id !== id);
    localStorage.setItem('projects', JSON.stringify(projects));
}

function getProjectById(id){
    return getProjects().find(p => p.id === id);
}





