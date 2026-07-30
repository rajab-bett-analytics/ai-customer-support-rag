import api from "../../../api/client";
import type { Analytics } from "../types/Analytics";

export async function getAnalytics(): Promise<Analytics> {
  const response = await api.get<Analytics>(
    "/analytics",
  );

  return response.data;
}