interface DocumentHeaderProps {
  totalDocuments?: number;
}

function DocumentHeader({
  totalDocuments = 0,
}: DocumentHeaderProps) {
  return (
    <div
      className="
        flex
        flex-col
        gap-4

        md:flex-row
        md:items-center
        md:justify-between
      "
    >
      <div>
        <h1
          className="
            text-3xl
            font-bold
            tracking-tight
            text-slate-900

            lg:text-4xl
          "
        >
          Knowledge Base
        </h1>

        <p
          className="
            mt-1
            max-w-2xl
            text-sm
            text-slate-500

            sm:text-base
          "
        >
          Upload, organize, and manage documents used by your
          AI Retrieval-Augmented Generation (RAG) system.
        </p>
      </div>

      <div
        className="
          inline-flex
          items-center
          gap-2
          self-start

          rounded-full
          border
          border-slate-200
          bg-white

          px-4
          py-2

          text-sm
          font-medium
          text-slate-600

          shadow-sm
        "
      >
        <span className="text-lg">📚</span>

        <span>
          {totalDocuments} Document
          {totalDocuments === 1 ? "" : "s"}
        </span>
      </div>
    </div>
  );
}

export default DocumentHeader;