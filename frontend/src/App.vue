<script setup>
import { ref, onMounted } from "vue";
import Header from "@/components/Header.vue"; // Import Header

const message = ref("");

onMounted(async () => {
  try {
    const response = await fetch("http://127.0.0.1:5001/data");
    const data = await response.json();
    message.value = data.message;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
});
</script>

<template>
  <div class="container">
    <Header />
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.content {
  width: 90%;
  max-width: 1200px;
  margin-top: 20px;
}
</style>
