import { useEffect, useState } from "react";

import { getProfile } from "../features/profile/types/services/profileService";
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

        setError(
          "Unable to load profile.",
        );

      } finally {

        setLoading(false);

      }

    }


    loadProfile();

  }, []);



  if (loading) {
    return (
      <div className="flex min-h-full items-center justify-center">
        Loading profile...
      </div>
    );
  }



  if (!profile || error) {
    return (
      <div className="flex min-h-full items-center justify-center text-red-600">
        {error}
      </div>
    );
  }



  return (

    <div className="min-h-full bg-slate-100 p-8">


      <div className="mx-auto max-w-6xl">


        {/* Header */}

        <div className="mb-8">

          <h1 className="text-4xl font-bold text-slate-900">
            My Profile
          </h1>

          <p className="mt-2 text-gray-600">
            Manage your account and view your activity.
          </p>

        </div>




        <div className="grid gap-8 lg:grid-cols-3">



          {/* Profile Card */}

          <div className="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">


            <div className="flex flex-col items-center">


              <div className="flex h-32 w-32 items-center justify-center rounded-full bg-blue-600 text-6xl shadow-lg">
                👤
              </div>


              <h2 className="mt-6 text-center text-2xl font-bold text-slate-900">
                {profile.full_name}
              </h2>


              <p className="mt-1 text-gray-500">
                {profile.email}
              </p>



              <span
                className={`mt-4 rounded-full px-5 py-2 text-sm font-semibold ${
                  profile.is_active
                    ? "bg-green-100 text-green-700"
                    : "bg-red-100 text-red-700"
                }`}
              >
                {profile.is_active
                  ? "Active Account"
                  : "Inactive"}
              </span>


            </div>



            <button
              className="
              mt-8
              w-full
              rounded-xl
              bg-blue-600
              py-3
              font-semibold
              text-white
              transition
              hover:bg-blue-700
              "
            >
              Edit Profile
            </button>



          </div>






          {/* Details */}

          <div className="lg:col-span-2 space-y-8">



            <div className="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">


              <h2 className="mb-6 text-2xl font-bold text-slate-900">
                Account Information
              </h2>



              <div className="grid gap-6 md:grid-cols-2">


                <div>
                  <p className="text-sm text-gray-500">
                    Full Name
                  </p>

                  <p className="mt-1 text-lg font-semibold">
                    {profile.full_name}
                  </p>
                </div>



                <div>
                  <p className="text-sm text-gray-500">
                    Email Address
                  </p>

                  <p className="mt-1 text-lg font-semibold">
                    {profile.email}
                  </p>
                </div>



                <div>
                  <p className="text-sm text-gray-500">
                    Member Since
                  </p>

                  <p className="mt-1 text-lg font-semibold">
                    {new Date(
                      profile.created_at
                    ).toLocaleDateString()}
                  </p>
                </div>



                <div>
                  <p className="text-sm text-gray-500">
                    Last Updated
                  </p>

                  <p className="mt-1 text-lg font-semibold">
                    {new Date(
                      profile.updated_at
                    ).toLocaleDateString()}
                  </p>
                </div>



              </div>


            </div>






            {/* Security */}

            <div className="rounded-3xl bg-white p-8 shadow-sm border border-gray-200">


              <h2 className="mb-5 text-2xl font-bold text-slate-900">
                Security
              </h2>



              <div className="flex items-center justify-between">


                <div>

                  <p className="font-semibold">
                    Password
                  </p>

                  <p className="text-sm text-gray-500">
                    Last changed recently
                  </p>

                </div>



                <button
                  className="
                  rounded-xl
                  border
                  border-gray-300
                  px-5
                  py-2
                  font-medium
                  hover:bg-gray-100
                  "
                >
                  Change Password
                </button>


              </div>


            </div>





          </div>


        </div>


      </div>


    </div>

  );
}