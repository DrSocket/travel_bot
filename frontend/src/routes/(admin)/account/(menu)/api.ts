

export async function callFastAPIRoute({ locals: { supabase, getSession }, }) {
    try {
      console.log("Calling FastAPI route");
  
      // Get the Supabase session
      const session = await getSession();
  
      // Check if the session exists and contains an access token
      if (session && session.access_token) {
        const accessToken = session.access_token;
        const baseUrl = import.meta.env.VITE_BASE_URL || "http://127.0.0.1:8001"; // Default to localhost if BASE_URL is not defined
        const response = await fetch(`${baseUrl}/protected`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${accessToken}` // Include the access token in the Authorization header
          }
        });
  
        if (response.ok) {
          const data = await response.json();
          return data;
        } else {
          throw new Error("Failed to call FastAPI route");
        }
      } else {
        throw new Error("User is not logged in or session is invalid");
      }
    } catch (error) {
      console.error("Error calling FastAPI route:", error);
      throw error;
    }
  }
  