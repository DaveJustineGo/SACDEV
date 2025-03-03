

    // INITIALIZER
document.addEventListener("DOMContentLoaded", function() {
    fetchOrganizations();
});

    // TABLE FUNCTIONS 
function fetchOrganizations() {
    fetch("/organizations")
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("organizationsTable");
            table.innerHTML = "";
            data.forEach(org => {
                let row = table.insertRow();
                row.innerHTML = `
                    <td>${org.id}</td>
                    <td>${org.name}</td>
                    <td>${org.president}</td>
                    <td>${org.officers}</td>
                    <td>${org.constitution}</td>
                    <td>
                        <button onclick="updateOrganization(${org.id}, '${org.name}', '${org.president}', '${org.officers}', '${org.constitution}')">Update</button>
                        <button onclick="deleteOrganization(${org.id})">Delete</button>
                    </td>
                `;
            });
        });
}

    // Add organization
function addOrganization() {
    const name = document.getElementById("name").value;
    const president = document.getElementById("president").value;
    const officers = document.getElementById("officers").value;
    const constitution = document.getElementById("constitution").value;

    fetch("/organizations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, president, officers, constitution })
    }).then(response => response.json())
        .then(() => fetchOrganizations());
}

    // Delete organization
function deleteOrganization(id) {
    fetch(`/organizations/${id}`, { method: "DELETE" })
        .then(() => fetchOrganizations());
}

    // Start update process
function updateOrganization(id, name, president, officers, constitution) {
    openPopup();
    document.getElementById("cID").innerText = id;
    document.getElementById("cName").value = name;
    document.getElementById("cPresident").value = president;
    document.getElementById("cOfficers").value = officers;
    document.getElementById("cConstitution").value = constitution;
    const newName = document.getElementById("cName").value;
    const newPresident =  document.getElementById("cPresident").value;
    const newOfficers = document.getElementById("cOfficers").value;
    const newConstitution = document.getElementById("cConstitution").value;

}

    // Submit Update
function submitUpdate() {
    const id = document.getElementById("cID").innerText;
    const newName = document.getElementById("cName").value;
    const newPresident = document.getElementById("cPresident").value;
    const newOfficers = document.getElementById("cOfficers").value;
    const newConstitution = document.getElementById("cConstitution").value;

    fetch(`/organizations/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: newName,
            president: newPresident,
            officers: newOfficers,
            constitution: newConstitution
        })
    }).then(response => response.json())
    .then(() => {
        fetchOrganizations(); // Refresh table
        closePopup(); // Close popup after update
    });
}

// Table Sorting
function sortTable(columnIndex) {
    let table = document.getElementById("organizationsTable");
    let rows = Array.from(table.rows).slice(0); // Exclude the header row
    let isNumeric = !isNaN(rows[0].cells[columnIndex].innerText);
    
    let sortedRows = rows.sort((a, b) => {
        let aVal = a.cells[columnIndex].innerText;
        let bVal = b.cells[columnIndex].innerText;
        
        return isNumeric ? aVal - bVal : aVal.localeCompare(bVal);
    });

    // Re-append sorted rows
    for (let row of sortedRows) {
        table.appendChild(row);
    }
}

// WEBSITE FUNCTIONS

document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const toggleButton = document.getElementById("toggleSidebar");

    toggleButton.addEventListener("click", function() {
        sidebar.classList.toggle("extended");
    });
});

function toggleSidebar() {

    var sidebar = document.querySelector('.sidebar');
    if (sidebar.style.width === '10rem') {
    sidebar.style.width = '3rem';
    } else {
    sidebar.style.width = '10rem';
    }
}
function openPopup() {
    document.getElementById("popup").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}
    
    