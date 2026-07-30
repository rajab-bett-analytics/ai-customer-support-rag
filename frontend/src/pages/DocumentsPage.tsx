import { Search, Upload } from "lucide-react";

import { useDocuments } from "../features/documents/hooks/useDocuments";

import DocumentStats from "../features/documents/components/DocumentStats";
import DocumentLoading from "../features/documents/components/DocumentLoading";
import DocumentEmptyState from "../features/documents/components/DocumentEmptyState";
import DocumentTable from "../features/documents/components/DocumentTable";

import PageHeader from "../components/ui/PageHeader";
import Button from "../components/ui/Button";

function DocumentsPage() {
  const {
    documents,
    filteredDocuments,
    loading,
    uploading,
    search,
    setSearch,
    upload,
    remove,
  } = useDocuments();

  return (
    <div
      className="
        mx-auto
        flex
        h-full
        min-h-0
        w-full
        max-w-[1500px]
        flex-col
        gap-6
        px-4
        py-6
        sm:px-6
        lg:px-8
        xl:px-10
      "
    >
      {/* Hidden file input */}
      <input
        id="document-upload"
        type="file"
        accept=".pdf"
        hidden
        disabled={uploading}
        onChange={upload}
      />

      <PageHeader
        title="Knowledge Base"
        description="Manage the PDF documents used by your AI assistant for Retrieval-Augmented Generation (RAG)."
        action={
          <div className="flex items-center gap-3">
            <div className="relative w-80">
              <Search
                size={18}
                className="
                  absolute
                  left-3
                  top-1/2
                  -translate-y-1/2
                  text-slate-400
                "
              />

              <input
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
                placeholder="Search documents..."
                className="
                  h-11
                  w-full
                  rounded-lg
                  border
                  border-slate-300
                  bg-white
                  pl-10
                  pr-4
                  text-sm
                  outline-none
                  transition
                  focus:border-blue-500
                  focus:ring-2
                  focus:ring-blue-100
                "
              />
            </div>

            <Button
              variant="primary"
              onClick={() =>
                document
                  .getElementById("document-upload")
                  ?.click()
              }
            >
              <Upload size={18} />
              {uploading
                ? "Uploading..."
                : "Upload PDF"}
            </Button>
          </div>
        }
      />

      <DocumentStats
        documents={documents}
      />

      <div
        className="
          flex-1
          min-h-0
          overflow-hidden
          rounded-2xl
          border
          border-slate-200
          bg-white
          shadow-sm
        "
      >
        {loading ? (
          <DocumentLoading />
        ) : filteredDocuments.length === 0 ? (
          <DocumentEmptyState />
        ) : (
          <DocumentTable
            documents={filteredDocuments}
            onDelete={remove}
          />
        )}
      </div>
    </div>
  );
}

export default DocumentsPage;