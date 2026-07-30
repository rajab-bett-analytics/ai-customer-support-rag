import type { UserProfile } from "../types/UserProfile";

const API_URL = "http://127.0.0.1:8000";

export interface PasswordChangeRequest {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem("access_token");

  if (!token) {
    throw new Error("No authentication token found.");
  }

  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}

export async function getProfile(): Promise<UserProfile> {
  const response = await fetch(`${API_URL}/auth/me`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch profile.");
  }

  return response.json();
}

export async function changePassword(
  passwordData: PasswordChangeRequest,
): Promise<void> {
  const response = await fetch(
    `${API_URL}/auth/change-password`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify(passwordData),
    },
  );

  if (!response.ok) {
    const error = await response.json();

    throw new Error(
      error.detail ?? "Failed to change password.",
    );
  }
}