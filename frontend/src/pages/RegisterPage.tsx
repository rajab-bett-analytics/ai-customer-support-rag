import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function RegisterPage() {
  const navigate = useNavigate();

  const [fullName, setFullName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [confirmPassword, setConfirmPassword] =
    useState("");

  async function handleRegister() {
    if (
      !fullName ||
      !email ||
      !password ||
      !confirmPassword
    ) {
      alert("Please complete all fields.");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    // TODO:
    // Connect your backend registration API here.

    alert(
      "Registration endpoint not connected yet.",
    );

    // After successful registration:
    // navigate("/login");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-100 via-blue-50 to-slate-200 px-6">
      <div className="w-full max-w-md rounded-3xl border border-white/50 bg-white/90 p-10 shadow-2xl backdrop-blur">

        {/* Logo */}
        <div className="mb-10 text-center">
          <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-2xl bg-blue-600 text-4xl text-white shadow-lg">
            👤
          </div>

          <h1 className="text-3xl font-bold text-slate-900">
            Create Account
          </h1>

          <p className="mt-3 text-gray-500">
            Register to start using your AI Customer Support platform.
          </p>
        </div>

        {/* Full Name */}
        <div className="mb-5">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Full Name
          </label>

          <input
            type="text"
            placeholder="John Doe"
            value={fullName}
            onChange={(e) =>
              setFullName(e.target.value)
            }
            className="w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 transition focus:border-blue-500 focus:bg-white focus:outline-none"
          />
        </div>

        {/* Email */}
        <div className="mb-5">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Email Address
          </label>

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 transition focus:border-blue-500 focus:bg-white focus:outline-none"
          />
        </div>

        {/* Password */}
        <div className="mb-5">
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
            className="w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 transition focus:border-blue-500 focus:bg-white focus:outline-none"
          />
        </div>

        {/* Confirm Password */}
        <div className="mb-6">
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Confirm Password
          </label>

          <input
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(
                e.target.value,
              )
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleRegister();
              }
            }}
            className="w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 transition focus:border-blue-500 focus:bg-white focus:outline-none"
          />
        </div>

        {/* Register Button */}
        <button
          onClick={handleRegister}
          className="w-full rounded-xl bg-blue-600 py-3 text-lg font-semibold text-white shadow-lg transition hover:bg-blue-700"
        >
          Create Account
        </button>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          Already have an account?{" "}
          <Link
            to="/login"
            className="font-semibold text-blue-600 hover:text-blue-700"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;