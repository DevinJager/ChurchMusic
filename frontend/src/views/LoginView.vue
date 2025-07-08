<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();

// Check if already logged in
onMounted(() => {
  const token = localStorage.getItem("token");
  if (token) router.push("/musiclibrary");
});

// Handle login
const login = async () => {
  try {
    const response = await axios.post("http://localhost:5001/login", {
      email: email.value,
      password: password.value,
    });

    if (response.data.success) {
      console.log("Login successful:", response.data);
      localStorage.setItem("token", response.data.token); // Save token
      router.push("/musiclibrary"); // Redirect on success
    } else {
      error.value = response.data.error || "Login failed";
    }
  } catch (err) {
    console.error("Error logging in:", err.response?.data?.error || err.message);
    error.value = "Invalid email or password";
  }
};
</script>

<template>
  <div class="login-container">
    <h1>Login</h1>

    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  margin-top: 200px;
  text-align: center;
}

h1 {
  color: #3c8cb9;
  margin-bottom: 20px;
}

input {
  width: 80%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #3c8cb9;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #306a8a;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
