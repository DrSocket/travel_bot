<script lang="ts">
  import { writable } from "svelte/store"
  import { onMount } from "svelte"
  import { getContext } from "svelte"

  // If adminSection expects a specific type, you must also specify this in your getContext call
  let adminSection = getContext<string>("adminSection")
  adminSection.set("jobs")

  export let data: { session: { access_token: string }; supabase: any }
  let { session, supabase } = data

  let jobs = writable([])
  let activeIndexes = writable([]) // Stores open states for each accordion item

  async function fetchJobs() {
    if (!session || !session.access_token) return
    const response = await fetch("http://127.0.0.1:8001/api/jobs", {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    })
    if (response.ok) {
      const data = await response.json()
      jobs.set(data.jobs)
      // Initialize all items to closed state
      activeIndexes.set(new Array(data.jobs.length).fill(false))
    } else {
      console.error("Failed to fetch jobs.")
    }
  }

  function toggleAccordion(index: number) {
    activeIndexes.update((current) => {
      let newArray = [...current]
      newArray[index] = !newArray[index] // Toggle the state of the specific accordion item
      return newArray
    })
  }

  onMount(() => {
    fetchJobs()
  })
</script>

<svelte:head>
  <title>Jobs</title>
</svelte:head>

<h1 class="text-2xl font-bold mb-6">Jobs</h1>

<div class="join join-vertical w-full">
  {#each $jobs as job, index}
    <div class="collapse collapse-arrow join-item border border-base-300">
      <input
        type="checkbox"
        id="job-{index}"
        bind:checked={$activeIndexes[index]}
      />
      <label
        for="job-{index}"
        class="collapse-title text-l font-medium flex justify-between items-center w-full"
      >
        <span class="flex-1 text-left ml-3">{job.agg_job_name}</span>
        <span class="flex-none inline-flex items-center justify-center flex-1">
          {#if job.agg_status === "CLOSED"}
            <span
              class="inline-flex items-center gap-x-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-800/30 dark:text-red-500"
              >Closed</span
            >
          {:else if job.agg_status === "OPEN"}
            <span
              class="inline-flex items-center gap-x-1.5 py-1.5 px-3 rounded-full text-xs font-medium bg-teal-100 text-teal-800 dark:bg-teal-800/30 dark:text-teal-500"
              >Open</span
            >
          {/if}
        </span>
        <span class="flex-1 text-xs mr-3 text-right"
          >{job.agg_remote_created}</span
        >
      </label>
      <div class="collapse-content text-sm">
        <div class="m-3">
          {@html job.agg_job_description}
        </div>
      </div>
    </div>
  {/each}
</div>
