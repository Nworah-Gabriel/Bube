let researchWorks = [
    {
        id: 1,
        image: "https://via.placeholder.com/200x150",
        title: "AI Enhancing Healthcare",
        description: "A study on AI-powered diagnosis improvements.",
        date: "2024-01-01"
    }
];

const admResList = document.getElementById("admResList");

function loadResearch() {
    admResList.innerHTML = "";

    researchWorks.forEach(r => {
        admResList.innerHTML += `
            <div class="adm-res-item">
                <img src="${r.image}" class="adm-res-thumb">

                <div class="adm-res-info">
                    <h3>${r.title}</h3>
                    <p>${r.description}</p>
                    <small>${r.date}</small>
                </div>

                <div class="adm-res-actions">
                    <button onclick="editResearch(${r.id})">Edit</button>
                    <button onclick="deleteResearch(${r.id})">Delete</button>
                </div>
            </div>
        `;
    });
}

function deleteResearch(id) {
    researchWorks = researchWorks.filter(item => item.id !== id);
    loadResearch();
}

function editResearch(id) {
    alert("Edit feature (simulation)");
}

loadResearch();
