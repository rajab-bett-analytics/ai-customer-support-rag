import { useEffect, useState } from "react";
import {
  Mail,
  User,
  Calendar,
  Shield,
  Edit,
  Key,
  CheckCircle2,
} from "lucide-react";

import { getProfile } from "../features/profile/services/profileService";
import type { UserProfile } from "../features/profile/types/UserProfile";

export default function ProfilePage() {
  const [profile, setProfile] =
    useState<UserProfile | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getProfile();
        setProfile(data);
      } catch {
        setError("Unable to load profile.");
      } finally {
        setLoading(false);
      }
    }

    void loadProfile();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-slate-500">
        Loading profile...
      </div>
    );
  }

  if (!profile || error) {
    return (
      <div className="flex h-full items-center justify-center text-red-600">
        {error}
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-6xl space-y-5">
      {/* Hero */}

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-blue-100">
              <User
                size={30}
                className="text-blue-600"
              />
            </div>

            <div className="min-w-0">
              <h1 className="truncate text-2xl font-bold text-slate-900">
                {profile.full_name}
              </h1>

              <div className="mt-2 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-slate-500">
                <div className="flex min-w-0 items-center gap-2">
                  <Mail size={15} />

                  <span className="break-all">
                    {profile.email}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <CheckCircle2
                    size={15}
                    className={
                      profile.is_active
                        ? "text-green-600"
                        : "text-red-600"
                    }
                  />

                  {profile.is_active
                    ? "Active Account"
                    : "Inactive"}
                </div>
              </div>
            </div>
          </div>

          <button
            className="
              inline-flex
              shrink-0
              items-center
              gap-2
              rounded-xl
              bg-blue-600
              px-4
              py-2.5
              text-sm
              font-medium
              text-white
              transition
              hover:bg-blue-700
            "
          >
            <Edit size={17} />
            Edit Profile
          </button>
        </div>
      </div>

      {/* Content */}

      <div className="grid gap-5 lg:grid-cols-12">
        {/* Account */}

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-7">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-slate-900">
              Account Information
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Basic details associated with your account.
            </p>
          </div>

          <div className="space-y-5">
            <Info
              icon={<User size={18} />}
              label="Full Name"
              value={profile.full_name}
            />

            <Info
              icon={<Mail size={18} />}
              label="Email Address"
              value={profile.email}
            />

            <Info
              icon={<Calendar size={18} />}
              label="Member Since"
              value={new Date(
                profile.created_at,
              ).toLocaleDateString()}
            />

            <Info
              icon={<Calendar size={18} />}
              label="Last Updated"
              value={new Date(
                profile.updated_at,
              ).toLocaleDateString()}
            />
          </div>
        </div>

        {/* Security */}

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-5">
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-blue-100 p-3">
              <Shield
                size={20}
                className="text-blue-600"
              />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Security
              </h2>

              <p className="text-sm text-slate-500">
                Keep your account protected.
              </p>
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 p-4">
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-slate-900">
                  Password
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  Update your password regularly.
                </p>
              </div>

              <button
                className="
                  inline-flex
                  w-full
                  items-center
                  justify-center
                  gap-2
                  rounded-xl
                  border
                  border-slate-300
                  px-4
                  py-2.5
                  text-sm
                  font-medium
                  transition
                  hover:bg-slate-50
                "
              >
                <Key size={16} />
                Change Password
              </button>
            </div>
          </div>

          <div className="mt-5 rounded-xl border border-green-100 bg-green-50 p-4">
            <p className="flex items-center gap-2 text-sm text-green-700">
              <CheckCircle2 size={16} />
              Your account is active and protected.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

interface InfoProps {
  icon: React.ReactNode;
  label: string;
  value: string;
}

function Info({
  icon,
  label,
  value,
}: InfoProps) {
  return (
    <div className="flex items-start gap-4">
      <div className="rounded-xl bg-slate-100 p-3 text-slate-600">
        {icon}
      </div>

      <div className="min-w-0 flex-1">
        <p className="text-sm text-slate-500">
          {label}
        </p>

        <p className="mt-1 break-words text-base font-semibold text-slate-900">
          {value}
        </p>
      </div>
    </div>
  );
}