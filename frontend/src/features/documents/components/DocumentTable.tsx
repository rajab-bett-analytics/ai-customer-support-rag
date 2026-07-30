import { FileText, Trash2 } from "lucide-react";

import type { Document } from "../documentService";

interface DocumentTableProps {
  documents: Document[];
  onDelete: (documentId: number) => void;
}

function DocumentTable({
  documents,
  onDelete,
}: DocumentTableProps) {
  function getStatusBadge(status: string) {
    switch (status.toLowerCase()) {
      case "processed":
        return (
          <span className="rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-700">
            Ready
          </span>
        );

      case "processing":
        return (
          <span className="rounded-full bg-yellow-100 px-2 py-1 text-xs font-medium text-yellow-700">
            Processing
          </span>
        );

      default:
        return (
          <span className="rounded-full bg-red-100 px-2 py-1 text-xs font-medium text-red-700">
            Failed
          </span>
        );
    }
  }

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-5 py-4">
        <h2 className="text-lg font-semibold text-slate-900">
          Documents
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          {documents.length} document
          {documents.length === 1 ? "" : "s"} in your
          knowledge base
        </p>
      </div>

      <div className="flex-1 overflow-auto">
        <div className="min-w-[900px]">
          <table className="w-full border-collapse">
            <thead className="sticky top-0 z-10 bg-slate-50">
              <tr className="border-b border-slate-200">
                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Document
                </th>

                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Status
                </th>

                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Size
                </th>

                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Statistics
                </th>

                <th className="px-5 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Indexed
                </th>

                <th className="w-20 px-5 py-3 text-center text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              {documents.length === 0 ? (
                <tr>
                  <td
                    colSpan={6}
                    className="py-20 text-center text-slate-500"
                  >
                    No documents uploaded.
                  </td>
                </tr>
              ) : (
                documents.map((document) => (
                  <tr
                    key={document.id}
                    className="border-b border-slate-100 transition-colors hover:bg-slate-50"
                  >
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-3">
                        <div className="rounded-lg bg-blue-100 p-2">
                          <FileText
                            size={18}
                            className="text-blue-600"
                          />
                        </div>

                        <div className="min-w-0 flex-1">
                          <p className="truncate font-medium text-slate-900">
                            {document.filename}
                          </p>

                          <p className="text-xs text-slate-500">
                            {document.mime_type}
                          </p>
                        </div>
                      </div>
                    </td>

                    <td className="px-5 py-4">
                      {getStatusBadge(document.status)}
                    </td>

                    <td className="whitespace-nowrap px-5 py-4 text-sm text-slate-600">
                      {(document.file_size / 1024 / 1024).toFixed(2)} MB
                    </td>

                    <td className="px-5 py-4">
                      <div className="space-y-1 text-sm text-slate-600">
                        <div>
                          Pages:{" "}
                          <span className="font-medium">
                            {document.page_count}
                          </span>
                        </div>

                        <div>
                          Chunks:{" "}
                          <span className="font-medium">
                            {document.chunk_count}
                          </span>
                        </div>

                        <div>
                          Vectors:{" "}
                          <span className="font-medium">
                            {document.embedding_count}
                          </span>
                        </div>
                      </div>
                    </td>

                    <td className="whitespace-nowrap px-5 py-4 text-sm text-slate-500">
                      {document.indexed_at
                        ? new Date(
                            document.indexed_at,
                          ).toLocaleDateString()
                        : "-"}
                    </td>

                    <td className="px-5 py-4 text-center">
                      <button
                        onClick={() =>
                          onDelete(document.id)
                        }
                        className="rounded-lg p-2 text-slate-400 transition hover:bg-red-50 hover:text-red-600"
                      >
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default DocumentTable;