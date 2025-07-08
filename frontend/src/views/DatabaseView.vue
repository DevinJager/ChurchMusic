<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Holds music library data
const musicLibrary = ref([])

// Form input with the column names needed
const newEntry = ref({
  Title: '',
  Composer_Fname: '',
  Composer_Lname: '',
  Publisher: '',
  Collection: '',
  Voice_Part: '',
  Location: '',
  HymnalNum: '',
  CatalogNum: '',
  Instrumentation: '',
  Advent: '',
  Christmas: '',
  Ordinary_Time: '',
  Lent: '',
  Palm_Sunday: '',
  Good_Friday: '',
  Easter: '',
  Pentecost: '',
  Communion: '',
  Marian: '',
  All_Saints: '',
  Count: '',
  Marked: '',
  Notes: '',
  HighFrequency: '',
  Favorite: '',


})

// Fetches existing music library data
const fetchMusicLibrary = async () => {
  try {
    const response = await axios.get('http://localhost:5001/data/music_library')
    console.log('Data fetched:', response.data) // Add this line for debugging
    musicLibrary.value = response.data
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

// Add a new entry from form to database
const addEntry = async () => {
  try {
    const response = await axios.post('http://localhost:5001/data/music_library', newEntry.value)

    if (response.data) {
      musicLibrary.value.push(response.data) // Use the backend response with correct ID
    }

    newEntry.value = {
      Title: '',
      Composer_Fname: '',
      Composer_Lname: '',
      Publisher: '',
      Collection: '',
      Voice_Part: '',
      Location: '',
      HymnalNum: '',
      CatalogNum: '',
      Instrumentation: '',
      Advent: '',
      Christmas: '',
      Ordinary_Time: '',
      Lent: '',
      Palm_Sunday: '',
      Good_Friday: '',
      Easter: '',
      Pentecost: '',
      Communion: '',
      Marian: '',
      All_Saints: '',
      Count: '',
      Marked: '',
      Notes: '',
      HighFrequency: '',
      Favorite: '',
    } // Reset form
  } catch (error) {
    console.error('Error adding entry:', error)
  }
}

// Confirms if user wants to delete entry
const confirmDelete = (library_key) => {
  if (confirm("Are you sure you want to delete this entry?")) {
    deleteEntry(library_key);
  }
}

// Deletes an entry
const deleteEntry = async (library_key) => {
  try {
    // Send DELETE request to the backend using the correct 'id' parameter
    const response = await axios.delete(`http://localhost:5001/data/music_library/${library_key}`)

    if (response.status === 200) {
      musicLibrary.value = musicLibrary.value.filter((entry) => entry.id !== library_key)
    } else {
      console.error('Failed to delete entry:', response.data.error || response.data.message)
    }
  } catch (error) {
    console.error('Error deleting entry:', error.response?.data?.error || error.message)
  }
}



onMounted(fetchMusicLibrary)
</script>

<template>
  <div>
    <h1>Music Library</h1>

    <!-- Add new music entry -->
    <form @submit.prevent="addEntry">
      <input v-model="newEntry.Title" placeholder="Title" required />
      <input v-model="newEntry.Composer_Fname" placeholder="Composer_Fname" required />
      <input v-model="newEntry.Composer_Lname" placeholder="Composer_Lname" required />
      <input v-model="newEntry.Publisher" placeholder="Publisher" />
      <input v-model="newEntry.Collection" placeholder="Collection" required />
      <input v-model="newEntry.Voice_Part" placeholder="Voice_Part" />
      <input v-model="newEntry.Location" placeholder="Location" />
      <input v-model="newEntry.HymnalNum" placeholder="HymnalNum" />
      <input v-model="newEntry.CatalogNum" placeholder="CatalogNum" />
      <input v-model="newEntry.Instrumentation" placeholder="Instrumentation" />
      <input v-model="newEntry.Advent" placeholder="Advent" />
      <input v-model="newEntry.Christmas" placeholder="Christmas" />
      <input v-model="newEntry.Ordinary_Time" placeholder="Ordinary_Time" />
      <input v-model="newEntry.Lent" placeholder="Lent" />
      <input v-model="newEntry.Palm_Sunday" placeholder="Palm_Sunday" />
      <input v-model="newEntry.Good_Friday" placeholder="Good_Friday" />
      <input v-model="newEntry.Easter" placeholder="Easter" />
      <input v-model="newEntry.Pentecost" placeholder="Pentecost" />
      <input v-model="newEntry.Communion" placeholder="Communion" />
      <input v-model="newEntry.Marian" placeholder="Marian" />
      <input v-model="newEntry.All_Saints" placeholder="All_Saints" />
      <input v-model="newEntry.Count" placeholder="Count" />
      <input v-model="newEntry.Marked" placeholder="Marked" />
      <input v-model="newEntry.Notes" placeholder="Notes" />
      <input v-model="newEntry.HighFrequency" placeholder="HighFrequency" />
      <input v-model="newEntry.Favorite" placeholder="Favorite" />
      <button type="submit">Add</button>
    </form>

    <!-- Music library table -->
    <table>
      <thead>
        <tr>
          <th>library_key</th>
          <th>Title</th>
          <th>Composer_Fname</th>
          <th>Composer_Lname</th>
          <th>Publisher</th>
          <th>Collection</th>
          <th>Voice_Part</th>
          <th>Location</th>
          <th>HymnalNum</th>
          <th>CatalogNum</th>
          <th>Instrumentation</th>
          <th>Advent</th>
          <th>Christmas</th>
          <th>Ordinary_Time</th>
          <th>Lent</th>
          <th>Palm_Sunday</th>
          <th>Good_Friday</th>
          <th>Easter</th>
          <th>Pentecost</th>
          <th>Communion</th>
          <th>Marian</th>
          <th>All_Saints</th>
          <th>Count</th>
          <th>Marked</th>
          <th>Notes</th>
          <th>HighFrequency</th>
          <th>Favorite</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in musicLibrary" :key="entry.library_key">
          <td>{{ entry.library_key }}</td>
          <td>{{ entry.Title }}</td>
          <td>{{ entry.Composer_Fname }}</td>
          <td>{{ entry.Composer_Lname }}</td>
          <td>{{ entry.Publisher }}</td>
          <td>{{ entry.Collection }}</td>
          <td>{{ entry.Voice_Part }}</td>
          <td>{{ entry.Location }}</td>
          <td>{{ entry.HymnalNum }}</td>
          <td>{{ entry.CatalogNum }}</td>
          <td>{{ entry.Instrumentation }}</td>
          <td>{{ entry.Advent }}</td>
          <td>{{ entry.Christmas }}</td>
          <td>{{ entry.Ordinary_Time }}</td>
          <td>{{ entry.Lent }}</td>
          <td>{{ entry.Palm_Sunday }}</td>
          <td>{{ entry.Good_Friday }}</td>
          <td>{{ entry.Easter }}</td>
          <td>{{ entry.Pentecost }}</td>
          <td>{{ entry.Communion }}</td>
          <td>{{ entry.Marian }}</td>
          <td>{{ entry.All_Saints }}</td>
          <td>{{ entry.Count }}</td>
          <td>{{ entry.Marked }}</td>
          <td>{{ entry.Notes }}</td>
          <td>{{ entry.HighFrequency }}</td>
          <td>{{ entry.Favorite }}</td>
          <td>
            <button @click="confirmDelete(entry.library_key)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

h1 {
  margin-top: 200px;
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

button {
  margin: 10px;
  padding: 5px 10px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
