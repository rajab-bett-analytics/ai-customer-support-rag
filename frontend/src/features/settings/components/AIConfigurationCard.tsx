import type {
  Settings,
} from "../types/Settings";


interface AIConfigurationCardProps {

  settings: Settings;


  onChange: <
    K extends keyof Settings
  >(
    field: K,
    value: Settings[K],
  ) => void;

}



function AIConfigurationCard({
  settings,
  onChange,
}: AIConfigurationCardProps) {


  return (

    <section className="
      rounded-2xl
      border
      border-slate-200
      bg-white
      p-6
      shadow-sm
    ">

      <h2 className="
        text-lg
        font-semibold
        text-slate-900
      ">
        AI Configuration
      </h2>


      <p className="
        mt-1
        mb-6
        text-sm
        text-slate-500
      ">
        Configure your AI provider and language models.
      </p>



      <div className="
        grid
        gap-6
        md:grid-cols-2
      ">


        <div>

          <label className="
            mb-2
            block
            text-sm
            font-medium
            text-slate-700
          ">
            AI Provider
          </label>


          <select

            value={settings.ai_provider}

            onChange={(event) =>
              onChange(
                "ai_provider",
                event.target.value,
              )
            }

            className="
              w-full
              rounded-lg
              border
              border-slate-300
              bg-white
              px-4
              py-2
              text-slate-700
            "

          >

            <option value="google">
              Google Gemini
            </option>


            <option value="openai">
              OpenAI
            </option>


            <option value="anthropic">
              Anthropic Claude
            </option>


          </select>

        </div>




        <div>

          <label className="
            mb-2
            block
            text-sm
            font-medium
            text-slate-700
          ">
            Chat Model
          </label>


          <input

            type="text"

            value={settings.chat_model}

            onChange={(event) =>
              onChange(
                "chat_model",
                event.target.value,
              )
            }


            className="
              w-full
              rounded-lg
              border
              border-slate-300
              px-4
              py-2
              text-slate-700
            "


            placeholder="gemini-2.5-flash"

          />

        </div>




        <div>

          <label className="
            mb-2
            block
            text-sm
            font-medium
            text-slate-700
          ">
            Embedding Model
          </label>


          <input

            type="text"

            value={settings.embedding_model}

            onChange={(event) =>
              onChange(
                "embedding_model",
                event.target.value,
              )
            }


            className="
              w-full
              rounded-lg
              border
              border-slate-300
              px-4
              py-2
              text-slate-700
            "


            placeholder="gemini-embedding-001"

          />

        </div>



      </div>


    </section>

  );

}


export default AIConfigurationCard;