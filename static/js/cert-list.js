const admCertList = document.getElementById("admCertList");

let certifications = [
    { id: 1, image: "https://via.placeholder.com/300x200" },
    { id: 2, image: "https://via.placeholder.com/300x200" },
];

function loadCerts() {
    admCertList.innerHTML = "";

    certifications.forEach(cert => {
        admCertList.innerHTML += `
            <div class="adm-cert-card">
                <img src="${cert.image}" alt="Certification">
                <button class="adm-cert-delete" onclick="deleteCert(${cert.id})">Delete</button>
            </div>
        `;
    });
}

function deleteCert(id) {
    certifications = certifications.filter(c => c.id !== id);
    loadCerts();
}

loadCerts();
