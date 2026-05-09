const SUPABASE_URL = "https://fjjbsilexhoorjuiywyq.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZqamJzaWxleGhvb3JqdWl5d3lxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5OTY2MTgsImV4cCI6MjA5MzU3MjYxOH0._2DSwLGg14Wx5rQmdA7xhpoRif79i-wBSZh4iAymfJQ";

document.addEventListener("DOMContentLoaded", () => {
    try {
        if (typeof supabase === "undefined") {
            console.error("Supabase failed:", new Error("Supabase library not loaded."));
            return;
        }
        if (!window.supabaseClient) {
            window.supabaseClient = supabase.createClient(
                "https://fjjbsilexhoorjuiywyq.supabase.co",
                SUPABASE_ANON_KEY
            );
        }
        console.log("Supabase URL:", "https://fjjbsilexhoorjuiywyq.supabase.co");
        console.log("Supabase initialized");
    } catch (e) {
        console.error("Supabase failed:", e);
    }
});

console.log("Supabase loaded version:", supabase);
console.log("Client:", window.supabaseClient);
