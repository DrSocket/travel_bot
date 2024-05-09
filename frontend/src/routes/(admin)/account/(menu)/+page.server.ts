import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types"


export const load: PageServerLoad = async ({
  locals: { getSession, supabaseServiceRole },
}) => {
  const session = await getSession()
  if (!session) {
    throw redirect(303, "/login")
  }
}

export const actions = {
  signout: async ({ locals: { supabase, getSession } }) => {
    try {
      const session = await getSession();
      if (session) {
        await supabase.auth.signOut();
        throw redirect(303, "/");
      }
    } catch (error) {
      console.error("Error signing out:", error);
      throw error;
    }
  },

};
