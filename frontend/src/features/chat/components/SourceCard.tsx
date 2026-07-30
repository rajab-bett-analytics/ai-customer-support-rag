import type { DocumentSource } from "../../documents/types/DocumentSource";

interface SourceCardProps {
  source: DocumentSource;
}

function SourceCard({
  source,
}: SourceCardProps) {
  return (
    <div
      className="
        group
        rounded-xl
        border
        border-slate-200
        bg-white
        p-4
        shadow-sm
        transition-all
        duration-200
        hover:border-blue-300
        hover:bg-blue-50
        hover:shadow-md
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

        <div className="min-w-0 flex-1">
          <h3
            className="
              truncate
              font-semibold
              text-slate-800
              transition-colors
              group-hover:text-blue-700
            "
          >
            {source.document_name}
          </h3>

          <div className="mt-3 flex flex-wrap gap-2">
            <span className="rounded-full bg-slate-100 px-2 py-1 text-xs text-slate-600">
              Page {source.page}
            </span>

            <span className="rounded-full bg-slate-100 px-2 py-1 text-xs text-slate-600">
              Chunk {source.chunk_index}
            </span>
          </div>

          {source.section && (
            <div className="mt-3">
              <span className="inline-flex rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">
                {source.section}
              </span>
            </div>
          )}

          {source.chunk_text && (
            <p className="mt-3 line-clamp-3 text-sm text-slate-600">
              {source.chunk_text}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default SourceCard;