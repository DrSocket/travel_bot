<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { slide } from 'svelte/transition';
  import Error from '../../../+error.svelte'

  let logoVisible = writable(true);
  let searchText = '';
  let searchResults = writable([]);

  export let data: { session: { access_token: string }; }
  let { session } = data

  // Function to call FastAPI
  async function callFastAPI() {
    try {
      console.log("Session:", session?.access_token)
      const response = await fetch("http://127.0.0.1:8000/protected", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${session?.access_token}`,
        },
      })
      if (response.ok) {
        const userData = await response.json()
        console.log(userData)
      } else {
        console.error("Failed to fetch user data from FastAPI")
      }
    } catch (error) {
      console.error("Error calling FastAPI:", error)
    }
  }

  async function fetchAgent(query: string) : Promise<string> {
    console.log("fetching agent for query:", query);
    if (!session || !session.access_token) return '';

    const url = `http://127.0.0.1:8000/api/agency?query=${encodeURIComponent(query)}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      return data;
      // jobs.set(data);
    } else {
      console.error("Failed to fetch jobs.");
    }
  }

  async function fetchResults(query: string) {
    searchResults.set([`Result for ${query}`]);
    logoVisible.set(false);
  }

  async function handleSearch(query: string) {
    const res = await fetchAgent(query)
    if (res.trim() !== '') {
      fetchResults(searchText);
      searchText = '';
    }
  }

  // Call the FastAPI function on page load
  onMount(() => {
    callFastAPI()
  })
</script>

<svelte:head>
  <title>Animated Search</title>
</svelte:head>

<main class="main-content">
  {#if $logoVisible}
    <img src="/logo.png" alt="Logo" class="my-4 mx-auto" />
  {/if}

  <div class="results-container">
    {#each $searchResults as result}
      <p class="result">{result}</p>
    {/each}
  </div>

  <input
    class="search-input"
    type="text"
    bind:value={searchText}
    placeholder="Search Here..."
    on:keydown={(e) => e.key === 'Enter' && handleSearch(searchText)}
  />

  <style>
    html, body {
      height: 100%;
      margin: 0;
      overflow: hidden;
    }
    .main-content {
      display: flex;
      flex-direction: column;
      height: 100vh;
      padding: 1rem;
      box-sizing: border-box;
      overflow: hidden;
    }
    .results-container {
      flex-grow: 1;
      overflow-y: auto; /* Allows internal scrolling of result items if needed */
    }
    .search-input {
      flex: none; /* Ensures the search bar does not grow and stays at the bottom */
      padding: 0.5rem;
      margin-top: auto; /* Keeps the search bar at the bottom */
    }
  </style>
</main>