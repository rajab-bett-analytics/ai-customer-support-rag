import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { login } from "../features/auth/services/authService";

function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    if (!username || !password) {
      alert("Please enter your email and password.");
      return;
    }

    setLoading(true);

    try {
      const response = await login({
        username,
        password,
      });

      localStorage.setItem(
        "access_token",
        response.access_token,
      );

      navigate("/dashboard");
    } catch (error) {
      console.error(error);
      alert("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-100 via-blue-50 to-slate-200 px-6">
      <div className="w-full max-w-md rounded-3xl border border-white/50 bg-white/90 p-10 shadow-2xl backdrop-blur">

        {/* Logo */}
        <div className="mb-10 text-center">
          <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-2xl bg-blue-600 text-4xl text-white shadow-lg">
            🤖
          </div>

          <h1 className="text-3xl font-bold text-slate-900">
            AI Customer Support
          </h1>

          <p className="mt-3 text-gray-500">
            Sign in to access your AI-powered knowledge base.
          </p>
        </div>

        {/* Email */}
        <div className="mb-5">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Email Address
          </label>

          <input
            type="email"
            placeholder="you@example.com"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
            className="w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 transition focus:border-blue-500 focus:bg-white focus:outline-none"
          />
        </div>

        {/* Password */}
        <div className="mb-6">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Password
          </label>

          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleLogin();
              }
            }}
            className="w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 transition focus:border-blue-500 focus:bg-white focus:outline-none"
          />
        </div>

        {/* Login Button */}
        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full rounded-xl bg-blue-600 py-3 text-lg font-semibold text-white shadow-lg transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          {loading
            ? "Signing In..."
            : "Sign In"}
        </button>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          Don't have an account?{" "}
          <Link
            to="/register"
            className="font-semibold text-blue-600 hover:text-blue-700"
          >
            Create one
          </Link>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;