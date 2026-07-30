import type { DocumentSource } from "../../documents/types/DocumentSource";


interface SourceListProps {
  sources: DocumentSource[];

  onSourceSelect: (
    source: DocumentSource
  ) => void;
}


function SourceList({
  sources,
  onSourceSelect,
}: SourceListProps) {

  if (!sources.length) {
    return null;
  }


  return (
    <div className="space-y-3">

      <p className="text-sm font-semibold text-slate-700">
        Sources
      </p>


      {sources.map((source, index) => (

        <button
          key={`${source.document_id}-${index}`}
          type="button"
          onClick={() => onSourceSelect(source)}
          className="
            group
            w-full
            rounded-xl
            border
            border-slate-200
            bg-white
            p-4
            text-left
            shadow-sm
            transition
            hover:border-blue-400
            hover:bg-blue-50
          "
        >

          <div className="flex items-start gap-3">

            <div
              className="
                flex
                h-10
                w-10
                shrink-0
                items-center
                justify-center
                rounded-lg
                bg-blue-100
                text-lg
                transition
                group-hover:bg-blue-200
              "
            >
              📄
            </div>


            <div className="min-w-0">

              <p className="
                truncate
                font-medium
                text-slate-800
                group-hover:text-blue-700
              ">
                {source.document_name}
              </p>


              <p className="mt-1 text-sm text-slate-500">
                Page {source.page}
              </p>


              <p className="mt-1 text-xs text-slate-400">
                Chunk {source.chunk_index}
              </p>


              {source.section && (
                <p className="mt-1 text-xs text-slate-400">
                  Section: {source.section}
                </p>
              )}

            </div>

          </div>

        </button>

      ))}

    </div>
  );
}


export default SourceList;