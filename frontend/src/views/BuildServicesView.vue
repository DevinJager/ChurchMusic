
<script setup>
import { ref } from 'vue'
import axios from 'axios'

// Initialize the table with 9 rows and placeholders 1 to 9
const entries = ref(Array.from({ length: 9 }, (_, index) => ({
  LiturgicalEventOrder: index + 1, // Pre-fill with 1-9
  LiturgicalEvent: '',
  library_key: ''
})))

const liturgyKey = ref('')

// Add row
const addRow = () => {
  // The new row will automatically have the correct LiturgicalEventOrder
  const newOrder = entries.value.length + 1
  entries.value.push({ LiturgicalEventOrder: newOrder, LiturgicalEvent: '', library_key: '' })
}

// Placeholder for LiturgicalEventOrder can be used or changed
const getLiturgicalEventOrder = (index) => {
  // This will return the order value 1 to 9 by default or the value it is changed to
  return entries.value[index].LiturgicalEventOrder
}

// Submit form
const submitForm = async () => {
  if (!liturgyKey.value) {
    alert("Please enter a Liturgy Key.")
    return
  }

  // Add liturgy_key to each entry
  const data = entries.value.map(entry => ({
    ...entry,
    liturgy_key: liturgyKey.value
  }))

  // Add data to backend
  for (const entry of data) {
    try {
      const response = await axios.post('http://localhost:5001/data/music_list', entry)
      console.log('Data added successfully:', response.data)
    } catch (error) {
      console.error('Error adding entries:', error)
      alert('An error occurred while adding entries.')
      break
    }
  }

  alert('Entries added successfully!')
}
</script>

<template>
  <div>
    <h1>Build a Service</h1>
    <h3>Enter Liturgy Key:</h3>

    <!-- Input for liturgy key -->
    <input v-model="liturgyKey" placeholder="Enter Liturgy Key" required />


    <!-- Table for entries -->
    <table>
      <thead>
        <tr>
          <th>LiturgicalEventOrder</th>
          <th>LiturgicalEvent</th>
          <th>Library Key</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in entries" :key="index">
          <td>
            <input
              v-model="entry.LiturgicalEventOrder"
              :placeholder="getLiturgicalEventOrder(index)"
              required
            />
          </td>
          <td>
            <input v-model="entry.LiturgicalEvent" placeholder="LiturgicalEvent" required />
          </td>
          <td>
            <input v-model="entry.library_key" placeholder="library_key" required />
          </td>
        </tr>
      </tbody>
    </table>

    <!-- New row button -->
    <button @click="addRow">Add Row</button>

    <!-- Submit button -->
    <button @click="submitForm">Submit</button>
  </div>
</template>


<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

h1 {
  margin-top: 150px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #3c8cb9;
  color: white;
}
</style>
