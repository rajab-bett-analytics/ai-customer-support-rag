import type { UserProfile } from "../UserProfile";

const API_URL = "http://127.0.0.1:8000";


export async function getProfile(): Promise<UserProfile> {
  const token = localStorage.getItem(
    "access_token",
  );

  if (!token) {
    throw new Error("No authentication token found.");
  }


  const response = await fetch(
    `${API_URL}/auth/me`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  );


  if (!response.ok) {
    throw new Error(
      "Failed to fetch profile.",
    );
  }


  return response.json();
}