import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  User,
  Mail,
  Lock,
  Bot,
} from "lucide-react";

import { register } from "../features/auth/types/authService";

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
    !fullName.trim() ||
    !email.trim() ||
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

  try {
    await register({
      full_name: fullName.trim(),
      email: email.trim(),
      password,
    });

    alert("Account created successfully.");

    navigate("/login");
  } catch (error: unknown) {
    let message = "Registration failed.";

    if (
      typeof error === "object" &&
      error !== null &&
      "response" in error
    ) {
      const apiError = error as {
        response?: {
          data?: {
            detail?: string;
          };
        };
      };

      message =
        apiError.response?.data?.detail ??
        message;
    }

    alert(message);
  }
}

  return (
    <div
      className="
        flex
        min-h-screen
        items-center
        justify-center
        bg-gradient-to-br
        from-slate-100
        via-blue-50
        to-slate-200
        p-6
      "
    >
      <div
        className="
          w-full
          max-w-2xl
          rounded-3xl
          border
          border-slate-200
          bg-white
          p-10
          shadow-2xl
        "
      >
        {/* Logo */}

        <div className="mb-10 text-center">
          <div
            className="
              mx-auto
              mb-5
              flex
              h-20
              w-20
              items-center
              justify-center
              rounded-3xl
              bg-blue-600
              text-white
              shadow-lg
            "
          >
            <Bot size={38} />
          </div>

          <h1 className="text-3xl font-bold text-slate-900">
            Create your account
          </h1>

          <p className="mt-2 text-slate-500">
            Join AI Support Platform and
            start building your AI knowledge
            base.
          </p>
        </div>

        {/* Form */}

        <div className="grid gap-5 md:grid-cols-2">

          {/* Full Name */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Full Name
            </label>

            <div className="relative">
              <User
                size={18}
                className="absolute left-4 top-3.5 text-slate-400"
              />

              <input
                type="text"
                placeholder="John Doe"
                value={fullName}
                onChange={(e) =>
                  setFullName(e.target.value)
                }
                className="
                  w-full
                  rounded-xl
                  border
                  border-slate-300
                  bg-slate-50
                  py-3
                  pl-11
                  pr-4
                  transition
                  focus:border-blue-600
                  focus:bg-white
                  focus:outline-none
                "
              />
            </div>
          </div>

          {/* Email */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Email Address
            </label>

            <div className="relative">
              <Mail
                size={18}
                className="absolute left-4 top-3.5 text-slate-400"
              />

              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
                className="
                  w-full
                  rounded-xl
                  border
                  border-slate-300
                  bg-slate-50
                  py-3
                  pl-11
                  pr-4
                  transition
                  focus:border-blue-600
                  focus:bg-white
                  focus:outline-none
                "
              />
            </div>
          </div>

          {/* Password */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Password
            </label>

            <div className="relative">
              <Lock
                size={18}
                className="absolute left-4 top-3.5 text-slate-400"
              />

              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                className="
                  w-full
                  rounded-xl
                  border
                  border-slate-300
                  bg-slate-50
                  py-3
                  pl-11
                  pr-4
                  transition
                  focus:border-blue-600
                  focus:bg-white
                  focus:outline-none
                "
              />
            </div>
          </div>

          {/* Confirm Password */}

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Confirm Password
            </label>

            <div className="relative">
              <Lock
                size={18}
                className="absolute left-4 top-3.5 text-slate-400"
              />

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
                className="
                  w-full
                  rounded-xl
                  border
                  border-slate-300
                  bg-slate-50
                  py-3
                  pl-11
                  pr-4
                  transition
                  focus:border-blue-600
                  focus:bg-white
                  focus:outline-none
                "
              />
            </div>
          </div>
        </div>

        {/* Register Button */}

        <button
          onClick={handleRegister}
          className="
            mt-8
            flex
            w-full
            items-center
            justify-center
            rounded-xl
            bg-blue-600
            py-3.5
            text-base
            font-semibold
            text-white
            shadow-lg
            transition
            hover:bg-blue-700
          "
        >
          Create Account
        </button>

        {/* Footer */}

        <div className="mt-8 text-center text-sm text-slate-500">
          Already have an account?{" "}
          <Link
            to="/login"
            className="
              font-semibold
              text-blue-600
              hover:text-blue-700
            "
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;