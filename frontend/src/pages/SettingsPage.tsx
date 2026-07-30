import {
  useEffect,
  useState,
} from "react";


import ProfileCard from "../features/settings/components/ProfileCard";
import AIConfigurationCard from "../features/settings/components/AIConfigurationCard";
import RetrievalSettingsCard from "../features/settings/components/RetrievalSettingsCard";
import SecurityCard from "../features/settings/components/SecurityCard";


import {
  getProfile,
} from "../features/profile/services/profileService";


import {
  getSettings,
  updateSettings,
} from "../features/settings/services/settingsService";


import type {
  UserProfile,
} from "../features/profile/types/UserProfile";


import type {
  Settings,
} from "../features/settings/types/Settings";


function SettingsPage() {

  const [profile, setProfile] =
    useState<UserProfile | null>(null);


  const [settings, setSettings] =
    useState<Settings | null>(null);


  const [loading, setLoading] =
    useState(true);


  const [saving, setSaving] =
    useState(false);


  const [error, setError] =
    useState<string | null>(null);



  useEffect(() => {

    async function loadSettings() {

      try {

        const [
          profileData,
          settingsData,
        ] =
          await Promise.all([
            getProfile(),
            getSettings(),
          ]);


        setProfile(profileData);

        setSettings(settingsData);


      } catch {

        setError(
          "Unable to load settings."
        );

      } finally {

        setLoading(false);

      }

    }


    void loadSettings();


  }, []);




  function handleChange<
    K extends keyof Settings
  >(
    field: K,
    value: Settings[K],
  ) {

    if (!settings) return;


    setSettings({

      ...settings,

      [field]: value,

    });

  }





  async function handleSave() {

    if (!settings) return;


    try {

      setSaving(true);


      const updated =
        await updateSettings(
          settings
        );


      setSettings(updated);


      alert(
        "Settings updated successfully."
      );


    } catch {


      alert(
        "Failed to save settings."
      );


    } finally {

      setSaving(false);

    }

  }





  if (loading) {

    return (

      <div className="
        flex
        h-full
        items-center
        justify-center
        text-slate-500
      ">
        Loading settings...
      </div>

    );

  }





  if (
    error ||
    !profile ||
    !settings
  ) {

    return (

      <div className="
        flex
        h-full
        items-center
        justify-center
        text-red-600
      ">
        {error}
      </div>

    );

  }





  return (

    <div className="
      mx-auto
      w-full
      max-w-6xl
      space-y-8
      px-6
      py-8
    ">


      <div>

        <h1 className="
          text-3xl
          font-bold
          text-slate-900
        ">
          Settings
        </h1>


        <p className="
          mt-2
          text-slate-600
        ">
          Configure your AI Customer Support Platform.
        </p>

      </div>



      <ProfileCard
        profile={profile}
      />



      <AIConfigurationCard

        settings={settings}

        onChange={
          handleChange
        }

      />



      <RetrievalSettingsCard

        settings={settings}

        onChange={
          handleChange
        }

      />



      <SecurityCard />




      <div className="
        flex
        justify-end
      ">

        <button

          onClick={() => {
            void handleSave();
          }}

          disabled={saving}

          className="
            rounded-xl
            bg-blue-600
            px-6
            py-3
            font-medium
            text-white
            transition
            hover:bg-blue-700
            disabled:opacity-50
          "

        >

          {
            saving
              ? "Saving..."
              : "Save Changes"
          }

        </button>


      </div>


    </div>

  );

}


export default SettingsPage;