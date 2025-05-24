// ✅ Limpia el token al abrir el login manualmente
localStorage.removeItem("token");

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

// Variables para el QR modal
let currentUserId = null;
let currentDb = null;

document.getElementById("registerBtn").addEventListener("click", async () => {
  const username = document.getElementById("registerUser").value.trim();
  const password = document.getElementById("registerPassword").value.trim();
  const email = document.getElementById("registerEmail").value.trim();
  const dob = document.getElementById("registerDob").value;
  const gender = document.getElementById("registerGender").value;

  const selectedDbs = Array.from(document.querySelectorAll('input[name="dbSelect"]:checked')).map(cb => cb.value);

  if (!username || !password || !email || !dob || !gender || selectedDbs.length === 0) {
    return alert("Por favor, completa todos los campos y selecciona al menos una base de datos.");
  }

  const payload = {
    username,
    password_hash: password,
    date_of_birth: dob,
    gender,
    email
  };

  for (const db of selectedDbs) {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/${db}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const result = await res.json();

      if (!res.ok) {
        alert(`❌ Error al registrar en ${db}: ${result.detail}`);
        continue;
      }

      // Guardar para verificar OTP luego
      currentUserId = result.user.id;
      currentDb = db;

      // Mostrar QR en modal
      const qrImage = document.getElementById("qrImage");
      qrImage.src = `data:image/png;base64,${result.qr_code_base64}`;
      document.getElementById("qrContainer").classList.remove("hidden");

      return; // Solo procesamos uno a la vez
    } catch (err) {
      console.error(`Error en ${db}:`, err);
      alert(`Error en ${db}: ${err.message}`);
    }
  }

  alert("✅ Registro completado.");
});

// ✅ Verificación de OTP desde el modal
document.getElementById("verifyOtpBtn").addEventListener("click", async () => {
  const otp_code = document.getElementById("otpInput").value.trim();

  if (!otp_code || !currentUserId || !currentDb) {
    return alert("Completa el código correctamente.");
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/${currentDb}/verify-otp/${currentUserId}?otp_code=${otp_code}`, {
      method: "POST"
    });

    const data = await res.json();

    if (res.ok && data.success) {
      alert(`✅ Autenticación 2FA activada en ${currentDb}`);
    } else {
      alert(`❌ Código OTP incorrecto en ${currentDb}`);
    }
  } catch (err) {
    console.error("Error verificando OTP:", err);
    alert("Error al verificar OTP.");
  }

  // Cerrar y limpiar modal
  document.getElementById("qrContainer").classList.add("hidden");
  document.getElementById("otpInput").value = "";
  currentUserId = null;
  currentDb = null;
});

document.getElementById("closeQRBtn").addEventListener("click", () => {
  document.getElementById("qrContainer").classList.add("hidden");
  document.getElementById("otpInput").value = "";
  currentUserId = null;
  currentDb = null;
});

document.getElementById("loginBtn").addEventListener("click", async () => {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();
  const otp_code = document.getElementById("loginOtp").value.trim();

  if (!email || !password) {
    return alert("Por favor, completa tu email y contraseña");
  }

  const endpoints = ["users", "oracle-users", "sql-users"];
  let token = null;

  for (const db of endpoints) {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/${db}/validate-login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password, otp_code })
      });

      const result = await res.json();

      if (res.ok && result.success && result.access_token) {
        token = result.access_token;
        break;
      }
    } catch (err) {
      console.error(`Error en ${db}:`, err);
    }
  }

  if (token) {
    console.log("🔐 TOKEN GUARDADO:", token);
    localStorage.setItem("token", token);
    alert("✅ Inicio de sesión exitoso");
    window.location.href = "dashboard.html";
  } else {
    alert("❌ Usuario, contraseña o código OTP incorrecto");
  }
});
