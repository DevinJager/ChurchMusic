<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const msg = ref('')
const servicesDropdownVisible = ref(false)
const reportsDropdownVisible = ref(false)

const getMessage = async () => {
  try {
    const response = await axios.get('http://localhost:5001/header')
    msg.value = response.data.message // Ensure the correct data structure
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

onMounted(getMessage)
</script>

<template>
  <header>
    <div class="header-content">
      <img alt="ordologo" class="logo" src="@/assets/OrdoSplash.jpg" width="125" height="125" />
      <h1>{{ msg || 'Church Music Repository' }}</h1>
    </div>
    <nav>
      <RouterLink to="/musiclibrary">Music Library</RouterLink>

      <!-- Services dropdown -->
      <div
        class="dropdown"
        @mouseenter="servicesDropdownVisible = true"
        @mouseleave="servicesDropdownVisible = false"
      >
        <span class="dropdown-title">Services</span>
        <div v-if="servicesDropdownVisible" class="dropdown-menu">
          <RouterLink to="/addservice">Add a Service</RouterLink>
          <RouterLink to="/buildservice">Build a Service</RouterLink>
        </div>
      </div>

      <!-- Reports dropdown -->
      <div
        class="dropdown"
        @mouseenter="reportsDropdownVisible = true"
        @mouseleave="reportsDropdownVisible = false"
      >
        <span class="dropdown-title">Reports</span>
        <div v-if="reportsDropdownVisible" class="dropdown-menu">
          <RouterLink to="/generatereport">Generate a Report</RouterLink>
          <RouterLink to="/reporthistory">Report History</RouterLink>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
header {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  background-color: white;
  z-index: 1000;
  padding: 30px 0;
  text-align: center;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  margin-right: 15px;
}

h1 {
  font-size: 24px;
  margin: 0;
}

nav {
  margin-top: 10px;
}

nav a,
.dropdown-title {
  margin: 0 15px;
  text-decoration: none;
  color: #3c8cb9;
  font-weight: bold;
  cursor: pointer;
}

nav a:hover,
.dropdown-title:hover {
  text-decoration: underline;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.dropdown-menu a {
  padding: 10px;
  display: block;
  color: #3c8cb9;
  text-align: left;
}

.dropdown-menu a:hover {
  background-color: #f1f1f1;
}
</style>
