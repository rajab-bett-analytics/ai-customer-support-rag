import { useState } from "react";

import {
  changePassword,
} from "../../profile/services/profileService";


function SecurityCard() {
  const [currentPassword, setCurrentPassword] =
    useState("");

  const [newPassword, setNewPassword] =
    useState("");

  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [loading, setLoading] =
    useState(false);



  async function handleChangePassword() {
    setMessage("");

    if (newPassword !== confirmPassword) {
      setMessage(
        "New passwords do not match.",
      );

      return;
    }


    try {
      setLoading(true);


      await changePassword({
        current_password: currentPassword,

        new_password: newPassword,

        confirm_password: confirmPassword,
      });


      setMessage(
        "Password changed successfully.",
      );


      setCurrentPassword("");

      setNewPassword("");

      setConfirmPassword("");


    } catch (error) {

      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to change password.",
      );

    } finally {

      setLoading(false);

    }
  }



  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      <h2 className="text-lg font-semibold text-slate-900">
        Security
      </h2>


      <p className="mt-1 mb-6 text-sm text-slate-500">
        Update your account password.
      </p>



      <div className="space-y-5">


        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Current Password
          </label>

          <input
            type="password"
            value={currentPassword}
            onChange={(event) =>
              setCurrentPassword(
                event.target.value,
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
          />
        </div>



        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            New Password
          </label>

          <input
            type="password"
            value={newPassword}
            onChange={(event) =>
              setNewPassword(
                event.target.value,
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
          />
        </div>



        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Confirm New Password
          </label>

          <input
            type="password"
            value={confirmPassword}
            onChange={(event) =>
              setConfirmPassword(
                event.target.value,
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
          />
        </div>



        <button
          type="button"
          onClick={handleChangePassword}
          disabled={loading}
          className="rounded-lg bg-slate-900 px-5 py-2 text-white transition hover:bg-slate-700 disabled:opacity-50"
        >
          {loading
            ? "Changing..."
            : "Change Password"}
        </button>



        {message && (
          <p className="text-sm text-slate-600">
            {message}
          </p>
        )}


      </div>

    </section>
  );
}


export default SecurityCard;