import api from "../../../api/client";


export interface LoginRequest {
  username: string;
  password: string;
}


export interface LoginResponse {
  access_token: string;
  token_type: string;
}


export async function login(
  data: LoginRequest,
): Promise<LoginResponse> {

  const formData = new URLSearchParams();

  formData.append(
    "username",
    data.username,
  );

  formData.append(
    "password",
    data.password,
  );


  const response = await api.post<LoginResponse>(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
    },
  );


  return response.data;
}



export async function logout() {

  const response = await api.post(
    "/auth/logout",
  );


  return response.data;
}