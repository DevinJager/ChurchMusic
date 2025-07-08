<script setup>
import { ref } from "vue";
import axios from "axios";

const searchKey = ref(""); // Define searchKey (value user inputs for liturgy_key)
const singleEntry = ref(null); // Define singleEntry (gets row in liturgy table)
const music_list = ref([]); // Define music_list (gets the rows in music list & the music_library)
const music_lib = ref([]);

// Fetch liturgy data based on the entered liturgy_key
const fetchSingleEntry = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/data/liturgy`, {
      params: {
        filter_column: "liturgy_key",
        filter_value: searchKey.value
      }
    });

    if (response.data.length > 0) {
      singleEntry.value = response.data[0];
      fetchMusicList(); // Once liturgy data is found, fetch music list
    } else {
      singleEntry.value = null; // Reset if no liturgy data found
      music_list.value = []; // Reset music list if no liturgy data
    }
  } catch (error) {
    console.error("Error fetching liturgy entry:", error);
    singleEntry.value = null;
    music_list.value = [];
  }
};

// Fetch music list based on the entered liturgy_key
const fetchMusicList = async () => {
  try {
    const response = await axios.get(`http://localhost:5001/data/music_list`, {
      params: {
        filter_column: "Liturgy_Key",
        filter_value: searchKey.value
      }
    });

    if (response.data.length > 0) {
      music_list.value = response.data;
      fetchMusicLib(); // Once liturgy data is found, fetch music library data
    } else {
      music_list.value = []; // Reset if no music data found
    }
  } catch (error) {
    console.error("Error fetching music list:", error);
    music_list.value = [];
  }
};

const fetchMusicLib = async () => {
  try {
    // Take library keys from the music_list
    const libraryKeys = music_list.value.map(item => item.library_key);

    if (libraryKeys.length > 0) {
      const response = await axios.get(`http://localhost:5001/data/music_library`, {
        params: {
          filter_column: "library_key",
          filter_values: libraryKeys // Send multiple keys as an array
        }
      });

      if (response.data.length > 0) {
        // Now merge the music_lib data into music_list based on the library_key
        music_list.value.forEach(item => {
          // Find the corresponding music_lib entry for each music_list entry based on the library_key
          const musicLibItem = response.data.find(lib => lib.library_key === item.library_key);
          if (musicLibItem) {
            // Merge the fields from music_lib into the item from music_list
            item.Title = musicLibItem.Title;
            item.Composer_Fname = musicLibItem.Composer_Fname;
            item.Composer_Lname = musicLibItem.Composer_Lname;
            item.HymnalNum = musicLibItem.HymnalNum;
          }
        });
        music_list.value.sort((a, b) => a.LiturgicalEventOrder - b.LiturgicalEventOrder);
      } else {
        console.warn("No music library data found");
      }
    } else {
      console.warn("No library keys found in music_list");
    }
  } catch (error) {
    console.error("Error fetching music library:", error);
  }
};
</script>


<template>
  <div>
    <h1>Generate a Report</h1>

    <!-- Search for liturgy key -->
    <div>
      <input v-model="searchKey" placeholder="Enter liturgy_key" />
      <button @click="fetchSingleEntry">Search</button>
    </div>

    <!-- Display the liturgy details after the search -->
    <h2>St. Paul United Church of Christ Service Music</h2>
    <h3>Liturgy:</h3>
    <div v-if="singleEntry">
      <p>Date: {{ singleEntry.LiturgyDate }}</p>
      <p>Code: {{ singleEntry.LitYearCode }}</p>
      <p>Cycle: {{ singleEntry.LitYearCycle }}</p>
    </div>

    <!-- Music List Table -->
    <table v-if="music_list.length > 0">
      <thead>
        <tr>
          <th>LiturgicalEvent</th>
          <th>Title</th>
          <th>Composer/Hymn Tune</th>
          <th> </th>
          <th>Hymn</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in music_list" :key="entry.library_key">
          <td>{{ entry.LiturgicalEvent }}</td>
          <td>{{ entry.Title }}</td>
          <td>{{ entry.Composer_Fname }}</td>
          <td>{{ entry.Composer_Lname }}</td>
          <td>{{ entry.HymnalNum }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Message if no music entries found -->
    <p v-else>No music entries found for the entered liturgy key.</p>
  </div>
</template>

<style scoped>
.page {
  text-align: center;
  margin-top: 50px;
}

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
</style>
