document.getElementById("showRegister").addEventListener("click", (e) => {
  e.preventDefault();
  document.getElementById("loginForm").classList.add("hidden");
  document.getElementById("registerForm").classList.remove("hidden");
});

document.getElementById("showLogin").addEventListener("click", (e) => {
  e.preventDefault();
  document.getElementById("registerForm").classList.add("hidden");
  document.getElementById("loginForm").classList.remove("hidden");
});

document.getElementById("registerBtn").addEventListener("click", async () => {
  const username = document.getElementById("registerUser").value.trim();
  const password = document.getElementById("registerPassword").value.trim();
  const email = document.getElementById("registerEmail").value.trim();
  const dob = document.getElementById("registerDob").value;
  const gender = document.getElementById("registerGender").value;

  const selectedDbs = Array.from(document.querySelectorAll('input[name="dbSelect"]:checked')).map(cb => cb.value);

  if (!username || !password || !email || !dob || !gender) {
    return alert("Por favor, completa todos los campos");
  }

  if (selectedDbs.length === 0) {
    return alert("Selecciona al menos una base de datos");
  }

  const payload = {
    username,
    password_hash: password,
    date_of_birth: dob,
    gender,
    otp_secret: "STATIC_OTP",
    is_2fa_enabled: false,
    email
  };

  console.log("Payload a enviar:", payload);

  for (const db of selectedDbs) {
    console.log(`Enviando a /api/v1/${db}/`);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/${db}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const error = await res.json();
        console.error(`Error en ${db}:`, error);
        alert(`Error al registrar en ${db}: ${error.detail || 'Error desconocido'}`);
      } else {
        console.log(`Usuario registrado correctamente en ${db}`);
      }
    } catch (err) {
      console.error(`Fallo la conexión con ${db}:`, err);
      alert(`Error de conexión con ${db}: ${err.message}`);
    }
  }

  alert("Registro completado.");
});



document.getElementById("loginBtn").addEventListener("click", async () => {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  if (!email || !password) {
    return alert("Por favor, completa tu email y contraseña");
  }

  const endpoints = ["users", "oracle-users", "sql-users"];
  let loginCorrecto = false;

  for (const db of endpoints) {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/${db}/validate-login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password
        })
      });

      if (res.ok) {
        const result = await res.json();
        if (result.success === true) {
          loginCorrecto = true;
          break;
        }
      }
    } catch (err) {
      console.error(`Error en ${db}:`, err);
    }
  }

  if (loginCorrecto) {
    alert("✅ Inicio de sesión exitoso");
  } else {
    alert("❌ Usuario o contraseña incorrectos");
  }
});
