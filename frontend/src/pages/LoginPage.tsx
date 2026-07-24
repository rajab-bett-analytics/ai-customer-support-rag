import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login } from "../features/auth/services/authService";

function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
    try {
      const response = await login({
        username,
        password,
      });

      // Store the JWT access token
      localStorage.setItem(
        "access_token",
        response.access_token,
      );

      console.log("Login successful:", response);

      // Redirect to dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error(error);

      alert("Invalid email or password.");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-96 rounded-lg border p-6 shadow">
        <h1 className="mb-6 text-2xl font-bold">
          Login
        </h1>

        <input
          className="mb-4 w-full rounded border p-2"
          type="email"
          placeholder="Email"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          className="mb-4 w-full rounded border p-2"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button
          onClick={handleLogin}
          className="w-full rounded bg-blue-600 p-2 text-white hover:bg-blue-700"
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default LoginPage;