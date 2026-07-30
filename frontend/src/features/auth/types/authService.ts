import api from "../../../api/client";

import type { RegisterRequest } from "../types/RegisterRequest";
import type { UserResponse } from "../types/UserResponse";

export async function register(
  data: RegisterRequest,
) {
  const response =
    await api.post<UserResponse>(
      "/auth/register",
      data,
    );

  return response.data;
}