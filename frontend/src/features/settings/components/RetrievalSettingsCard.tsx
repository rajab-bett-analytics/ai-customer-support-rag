import type { Settings } from "../types/Settings";


interface RetrievalSettingsCardProps {
  settings: Settings;

  onChange: (
    field: keyof Settings,
    value: string | number,
  ) => void;
}


function RetrievalSettingsCard({
  settings,
  onChange,
}: RetrievalSettingsCardProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      <h2 className="text-lg font-semibold text-slate-900">
        Retrieval Settings
      </h2>

      <p className="mt-1 mb-6 text-sm text-slate-500">
        Configure document search and AI response behavior.
      </p>


      <div className="grid gap-6 md:grid-cols-2">

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Top K Results
          </label>

          <input
            type="number"
            value={settings.top_k}
            onChange={(event) =>
              onChange(
                "top_k",
                Number(event.target.value),
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
            min={1}
            max={20}
          />
        </div>


        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Similarity Threshold
          </label>

          <input
            type="number"
            step="0.01"
            value={settings.similarity_threshold}
            onChange={(event) =>
              onChange(
                "similarity_threshold",
                Number(event.target.value),
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
            min={0}
            max={1}
          />
        </div>


        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Temperature
          </label>

          <input
            type="number"
            step="0.1"
            value={settings.temperature}
            onChange={(event) =>
              onChange(
                "temperature",
                Number(event.target.value),
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
            min={0}
            max={2}
          />
        </div>


        <div>
          <label className="mb-2 block text-sm font-medium text-slate-700">
            Max Tokens
          </label>

          <input
            type="number"
            value={settings.max_tokens}
            onChange={(event) =>
              onChange(
                "max_tokens",
                Number(event.target.value),
              )
            }
            className="w-full rounded-lg border border-slate-300 px-4 py-2"
          />
        </div>

      </div>


      <div className="mt-6">

        <label className="mb-2 block text-sm font-medium text-slate-700">
          System Prompt
        </label>

        <textarea
          value={settings.system_prompt}
          onChange={(event) =>
            onChange(
              "system_prompt",
              event.target.value,
            )
          }
          rows={6}
          className="w-full rounded-lg border border-slate-300 px-4 py-3 text-slate-700"
          placeholder="Define how your AI assistant should behave..."
        />

      </div>

    </section>
  );
}


export default RetrievalSettingsCard;