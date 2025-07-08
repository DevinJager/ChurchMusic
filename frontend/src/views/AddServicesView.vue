<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Holds liturgy data
const liturgy = ref([])

// Form input
const newEntry = ref({ LiturgyDate: '', LitYearCode: '', LitYearCycle: '' })

// Add a new service entry
const addEntry = async () => {
  try {
    const response = await axios.post('http://localhost:5001/data/liturgy', newEntry.value)
    if (response.data) {
      liturgy.value.push(response.data)
      console.log('Data added successfully:', response.data)
    }
  } catch (error) {
    console.error('Error adding entry:', error)
  }
}

</script>


<template>
  <div>
    <h1>Add a Service</h1>

    <!-- Add a new service entry -->
    <form @submit.prevent="addEntry">
      <input v-model="newEntry.LiturgyDate" placeholder="Liturgy Date" required />
      <input v-model="newEntry.LitYearCode" placeholder="Lit Year Code" required />
      <input v-model="newEntry.LitYearCycle" placeholder="Lit Year Cycle" required />
      <button type="submit">Add</button>
    </form>
  </div>
</template>


<style scoped>
h1 {
  margin-top: 20px;
  text-align: left;
}

form {
  display: flex;
}
</style>
