import type { UserProfile } from "../../profile/types/UserProfile";

interface ProfileCardProps {
  profile: UserProfile;
}

function ProfileCard({
  profile,
}: ProfileCardProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">
        Profile
      </h2>

      <p className="mt-1 mb-6 text-sm text-slate-500">
        Your account information.
      </p>

      <div className="grid gap-6 md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Full Name
          </label>

          <input
            type="text"
            value={profile.full_name}
            readOnly
            className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 text-slate-700"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Email Address
          </label>

          <input
            type="email"
            value={profile.email}
            readOnly
            className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 text-slate-700"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Account Status
          </label>

          <input
            type="text"
            value={profile.is_active ? "Active" : "Inactive"}
            readOnly
            className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4-2 text-slate-700"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Member Since
          </label>

          <input
            type="text"
            value={new Date(
              profile.created_at,
            ).toLocaleDateString()}
            readOnly
            className="w-full rounded-lg border border-slate-300 bg-slate-50 px-4-2 text-slate-700"
          />
        </div>
      </div>
    </section>
  );
}

export default ProfileCard;