import api from "../../../api/client";
import type { Settings } from "../types/Settings";

export async function getSettings() {
  const response = await api.get<Settings>(
    "/settings",
  );

  return response.data;
}

export async function updateSettings(
  settings: Settings,
) {
  const response = await api.put<Settings>(
    "/settings",
    settings,
  );

  return response.data;
}