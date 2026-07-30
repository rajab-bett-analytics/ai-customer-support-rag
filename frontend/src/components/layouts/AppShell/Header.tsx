import {
  useEffect,
  useState,
} from "react";

import {
  Bell,
  LogOut,
  ChevronDown,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import { logout } from "../../../features/auth/services/authService";
import { getProfile } from "../../../features/profile/services/profileService";
import type { UserProfile } from "../../../features/profile/types/UserProfile";

export default function Header() {
  const navigate = useNavigate();

  const [user, setUser] =
    useState<UserProfile | null>(
      null,
    );

  useEffect(() => {
    async function loadProfile() {
      try {
        const profile =
          await getProfile();

        setUser(profile);
      } catch (error) {
        console.error(
          "Failed to load profile:",
          error,
        );
      }
    }

    loadProfile();
  }, []);

  async function handleLogout() {
    try {
      await logout();

      localStorage.removeItem(
        "access_token",
      );

      navigate("/login");
    } catch (error) {
      console.error(
        "Logout failed:",
        error,
      );

      localStorage.removeItem(
        "access_token",
      );

      navigate("/login");
    }
  }

  const initials = user
    ? user.full_name
        .split(" ")
        .map((name) => name[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "U";

  return (
    <header
      className="
        sticky
        top-0
        z-40
        flex
        h-16
        items-center
        justify-between
        border-b
        border-slate-200
        bg-white/90
        px-6
        backdrop-blur
      "
    >
      {/* Brand */}

      <div className="flex items-center gap-3">
        <div
          className="
            flex
            h-10
            w-10
            items-center
            justify-center
            rounded-xl
            bg-blue-600
            font-bold
            text-white
            shadow-sm
          "
        >
          AI
        </div>

        <div>
          <h1 className="text-base font-semibold text-slate-900">
            AI Support
          </h1>

          <p className="text-xs text-slate-500">
            Customer Platform
          </p>
        </div>
      </div>

      {/* Actions */}

      <div className="flex items-center gap-3">
        {/* Notifications */}

        <button
          className="
            relative
            flex
            h-10
            w-10
            items-center
            justify-center
            rounded-xl
            border
            border-slate-200
            transition
            hover:bg-slate-100
          "
        >
          <Bell
            size={18}
            className="text-slate-600"
          />

          <span
            className="
              absolute
              right-2.5
              top-2.5
              h-2
              w-2
              rounded-full
              bg-red-500
            "
          />
        </button>

        {/* User */}

        <button
          className="
            flex
            items-center
            gap-3
            rounded-xl
            border
            border-slate-200
            bg-white
            px-3
            py-2
            transition
            hover:bg-slate-50
          "
        >
          <div
            className="
              flex
              h-9
              w-9
              items-center
              justify-center
              rounded-full
              bg-blue-600
              font-semibold
              text-white
            "
          >
            {initials}
          </div>

          <div className="hidden text-left md:block">
            <p className="text-sm font-medium text-slate-900">
              {user?.full_name ??
                "Loading..."}
            </p>

            <p className="text-xs text-slate-500">
              {user?.email ?? ""}
            </p>
          </div>

          <ChevronDown
            size={16}
            className="hidden text-slate-500 md:block"
          />
        </button>

        {/* Logout */}

        <button
          onClick={handleLogout}
          className="
            flex
            h-10
            w-10
            items-center
            justify-center
            rounded-xl
            border
            border-slate-200
            text-slate-600
            transition
            hover:border-red-200
            hover:bg-red-50
            hover:text-red-600
          "
          title="Sign out"
        >
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
}