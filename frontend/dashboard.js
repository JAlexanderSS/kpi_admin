let chart;
let lastUserData = {};

// Bases de datos y sus rutas (orden fijo)
const orderedDbs = [
  ["PostgreSQL", "users"],
  ["Oracle", "oracle-users"],
  ["SQL Server", "sql-users"]
];

function fetchAndUpdateChart() {
  const token = localStorage.getItem("token");
  if (!token) return redirectToLogin();

  fetch("http://127.0.0.1:8000/api/v1/kpis/users-distribution", {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
    .then(response => {
      if (!response.ok) throw new Error("Token inválido o expirado");
      return response.json();
    })
    .then(data => {
      const labels = Object.keys(data);
      const values = Object.values(data);

      if (!chart) {
        const ctx = document.getElementById('myChart').getContext('2d');
        chart = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: labels,
            datasets: [{
              data: values,
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            }]
          }
        });
      } else {
        chart.data.labels = labels;
        chart.data.datasets[0].data = values;
        chart.update();
      }

      const now = new Date();
      document.getElementById("updateTime").textContent = "Última actualización: " + now.toLocaleTimeString();

      // Actualizar tabla de usuarios solo cuando el gráfico lo haga
      fetchAndDisplayUsers();
    })
    .catch(err => {
      alert(err.message);
      redirectToLogin();
    });
}

async function fetchAndDisplayUsers() {
  const token = localStorage.getItem("token");
  const userTablesContainer = document.getElementById("userTables");
  const newUserData = {};

  for (const [label, endpoint] of orderedDbs) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/${endpoint}/`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      const users = await response.json();
      newUserData[label] = { users, endpoint };
    } catch (err) {
      console.error(`Error cargando usuarios de ${label}:`, err);
    }
  }

  // Solo actualizamos si los datos cambiaron
  if (JSON.stringify(newUserData) !== JSON.stringify(lastUserData)) {
    lastUserData = newUserData;
    userTablesContainer.innerHTML = "";

    for (const [label, data] of Object.entries(newUserData)) {
      const users = data.users;
      const endpoint = data.endpoint;

      const table = document.createElement("table");
      table.className = "w-full border text-sm mb-6";
      table.innerHTML = `
        <caption class="text-lg font-semibold mb-2">${label}</caption>
        <thead class="bg-gray-200">
          <tr>
            <th class="border px-2">ID</th>
            <th class="border px-2">Usuario</th>
            <th class="border px-2">Email</th>
            <th class="border px-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          ${users.map(u => `
            <tr class="border-b">
              <td class="border px-2">${u.id}</td>
              <td class="border px-2">${u.username}</td>
              <td class="border px-2">${u.email}</td>
              <td class="border px-2 text-center">
                <button onclick="editUser('${endpoint}', ${u.id})" class="text-blue-600 hover:underline">✏️</button>
                <button onclick="deleteUser('${endpoint}', ${u.id})" class="text-red-600 hover:underline ml-2">🗑️</button>
              </td>
            </tr>
          `).join("")}
        </tbody>
      `;

      userTablesContainer.appendChild(table);
    }
  } else {
    console.log("✅ Datos de usuarios sin cambios. No se actualiza la tabla.");
  }
}

function deleteUser(endpoint, id) {
  const token = localStorage.getItem("token");
  if (!confirm(`¿Estás seguro de eliminar el usuario con ID ${id}?`)) return;

  fetch(`http://127.0.0.1:8000/api/v1/${endpoint}/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  })
    .then(response => {
      if (response.ok) {
        alert("✅ Usuario eliminado correctamente");
        fetchAndUpdateChart(); // Esto también vuelve a llamar a fetchAndDisplayUsers()
      } else {
        alert("❌ No se pudo eliminar el usuario");
      }
    });
}

function editUser(endpoint, id) {
  alert(`Función para editar usuario con ID ${id} en ${endpoint} (en desarrollo)`);
}

function redirectToLogin() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

window.onload = function () {
  if (!localStorage.getItem("token")) return redirectToLogin();

  fetchAndUpdateChart();
  setInterval(fetchAndUpdateChart, 1000); // cada 10s para no sobrecargar
  document.getElementById("logoutBtn").addEventListener("click", redirectToLogin);
};
