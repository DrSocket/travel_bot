<script lang="ts">
  import { onMount } from "svelte"
  import { getContext } from "svelte"
  import type { Writable } from "svelte/store"
  import { goto } from "$app/navigation"
  import { writable } from "svelte/store"

  let adminSection: Writable<string> = getContext("adminSection")
  adminSection.set("home")

  let userData: { id: any; email: any } | null = null
  export let data
  let { session } = data

  async function callFastAPI() {
    try {
      console.log("Session:", session?.access_token)
      const response = await fetch("http://127.0.0.1:8001/protected", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${session?.access_token}`,
        },
      })
      if (response.ok) {
        userData = await response.json()
      } else {
        console.error("Failed to fetch user data from FastAPI")
      }
    } catch (error) {
      console.error("Error calling FastAPI:", error)
    }
  }

  let searchQuery = ""
  let criteria = [
    { label: "Chief Data Officer", completionStatus: 80, coefficient: 1.5 },
    { label: "Data Analyst", completionStatus: 70, coefficient: 1.3 },
    { label: "Data Engineer", completionStatus: 90, coefficient: 1.7 },
    {
      label: "Machine Learning Engineer",
      completionStatus: 60,
      coefficient: 1.2,
    },
    { label: "Database Administrator", completionStatus: 85, coefficient: 1.6 },
    {
      label: "Business Intelligence Analyst",
      completionStatus: 75,
      coefficient: 1.4,
    },
    { label: "Statistician", completionStatus: 65, coefficient: 1.1 },
    {
      label: "Data Visualization Specialist",
      completionStatus: 95,
      coefficient: 1.8,
    },
    { label: "Data Scientist", completionStatus: 88, coefficient: 1.9 },
  ]

  let details = [
    {
      label: "Project Management",
      detail: "Oversees large datasets",
      importance: "High",
    },
    {
      label: "Statistical Analysis",
      detail: "Ability to perform complex calculations",
      importance: "Medium",
    },
    {
      label: "Data Cleaning",
      detail: "Ensures accuracy of data analysis",
      importance: "Critical",
    },
  ]

  let candidate_list = [
    {
      label: "Data Scientist",
      completionStatus: 88,
      coefficient: 1.9,
    },
    {
      label: "Data Analyst",
      completionStatus: 70,
      coefficient: 1.3,
    },
    {
      label: "Data Engineer",
      completionStatus: 90,
      coefficient: 1.7,
    },
    {
      label: "Machine Learning Engineer",
      completionStatus: 60,
      coefficient: 1.2,
    },
    {
      label: "Database Administrator",
      completionStatus: 85,
      coefficient: 1.6,
    },
    {
      label: "Business Intelligence Analyst",
      completionStatus: 75,
      coefficient: 1.4,
    },
    {
      label: "Statistician",
      completionStatus: 65,
      coefficient: 1.1,
    },
    {
      label: "Data Visualization Specialist",
      completionStatus: 95,
      coefficient: 1.8,
    },
    {
      label: "Chief Data Officer",
      completionStatus: 80,
      coefficient: 1.5,
    },
  ]

  let activeList = writable(criteria)
  let secondaryList = writable(details)
  let thirdList = writable(candidate_list)

  let activeTitle = writable("Criteria")
  let secondaryTitle = writable("Details")
  let thirdTitle = writable("Candidates")

  function handleListTransition() {
    ;[activeList, secondaryList] = [secondaryList, thirdList]
    ;[activeTitle, secondaryTitle] = [secondaryTitle, thirdTitle]
  }

  function addCriteria() {
    // Logic to add new criteria
  }

  onMount(() => {})
</script>

<svelte:head>
  <title>Account</title>
</svelte:head>

<main class="container mx-auto flex flex-col min-h-screen">
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-2">Dashboard</h1>
    <div class="flex justify-center mb-4">
      <input
        type="text"
        bind:value={searchQuery}
        placeholder="Search..."
        class="border border-gray-300 rounded px-4 py-2 max-w-md"
      />
    </div>

    <div class="flex flex-grow transition-all duration-500">
      <div class="w-1/2 mr-4">
        <h2 class="text-lg font-semibold mb-4">{$activeTitle}</h2>
        <div class="criteria-list overflow-y-auto max-h-96">
          {#each $activeList as item}
            <div class="border border-gray-300 rounded p-4 mb-4">
              <h3 class="text-base font-semibold mb-2">{item.label}</h3>
              <progress
                value={item.completionStatus || 100}
                max="100"
                class="w-full mb-2"
              ></progress>
              <p class="text-sm">
                {item.coefficient || item.detail || item.importance}
              </p>
            </div>
          {/each}
        </div>
      </div>

      <div class="w-1/2 cursor-pointer" on:click={handleListTransition}>
        <h2 class="text-lg font-semibold mb-4">{$secondaryTitle}</h2>
        <div class="candidate-list overflow-y-auto max-h-96">
          {#each $secondaryList as item}
            <div class="border border-gray-300 rounded p-4 mb-4">
              <h3 class="text-base font-semibold mb-2">{item.label}</h3>
              <progress
                value={item.completionStatus || 100}
                max="100"
                class="w-full mb-2"
              ></progress>
              <p class="text-sm">
                {item.coefficient || item.detail || item.importance}
              </p>
            </div>
          {/each}
        </div>
      </div>
    </div>

    <footer class="text-center mt-8 bg-gray-100 py-4">
      <div class="mb-4">
        <a href="#" class="mr-4 text-gray-600 hover:text-gray-800">Services</a>
        <a href="#" class="mr-4 text-gray-600 hover:text-gray-800">Company</a>
        <a href="#" class="mr-4 text-gray-600 hover:text-gray-800">Legal</a>
        <a href="#" class="text-gray-600 hover:text-gray-800">Social</a>
      </div>
      <p class="text-sm text-gray-500">
        &copy; 2023 Your Company Name. Providing reliable tech since 2023.
      </p>
    </footer>
  </div>
</main>

<style>
  .transition-all {
    transition: transform 0.5s ease-in-out;
  }
  .container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .list-container {
    display: flex;
    justify-content: space-between;
    overflow: hidden;
  }
  .list {
    width: 50%;
    padding: 1rem;
    overflow-y: auto;
    max-height: 400px;
    border: 1px solid lightgray;
  }
</style>
