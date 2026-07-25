import { useEffect, useState } from "react";

import {
  getDocuments,
  deleteDocument,
  uploadDocument,
  type Document,
} from "../features/documents/documentService";

function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setUploading(true);

    try {
      await uploadDocument(file);

      await loadDocuments();

      event.target.value = "";
    } catch (error) {
      console.error(error);
    } finally {
      setUploading(false);
    }
  }

  async function handleDelete(documentId: number) {
    const confirmed = window.confirm(
      "Delete this document?",
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteDocument(documentId);
      await loadDocuments();
    } catch (error) {
      console.error(error);
    }
  }

  function getStatusBadge(status: string) {
    switch (status.toLowerCase()) {
      case "processed":
        return (
          <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
            🟢 Processed
          </span>
        );

      case "processing":
        return (
          <span className="rounded-full bg-yellow-100 px-3 py-1 text-sm font-medium text-yellow-700">
            🟡 Processing
          </span>
        );

      default:
        return (
          <span className="rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-700">
            🔴 Failed
          </span>
        );
    }
  }

  useEffect(() => {
    void loadDocuments();
  }, []);

  return (
    <div className="mx-auto max-w-6xl space-y-8 p-8">
      {/* Page Header */}
      <div>
        <h1 className="text-4xl font-bold">
          Knowledge Base
        </h1>

        <p className="mt-2 text-gray-600">
          Upload PDF documents that your AI assistant
          will use to answer customer questions.
        </p>
      </div>

      {/* Upload Card */}
      <div className="rounded-xl border border-dashed border-gray-300 bg-gray-50 p-6">
        <h2 className="mb-4 text-lg font-semibold">
          Upload PDF Document
        </h2>

        <input
          type="file"
          accept=".pdf"
          disabled={uploading}
          onChange={handleUpload}
          className="block w-full text-sm
          file:mr-4
          file:rounded-lg
          file:border-0
          file:bg-blue-600
          file:px-4
          file:py-2
          file:text-white
          file:hover:bg-blue-700"
        />

        <p className="mt-3 text-sm text-gray-500">
          Supported format: PDF
        </p>

        {uploading && (
          <div className="mt-4 rounded-lg bg-blue-100 p-3 text-blue-700">
            Uploading document...
          </div>
        )}
      </div>

      {/* Documents */}
      {loading ? (
        <div className="rounded-lg bg-white p-8 text-center shadow">
          Loading documents...
        </div>
      ) : documents.length === 0 ? (
        <div className="rounded-xl border border-dashed p-12 text-center">
          <div className="mb-4 text-6xl">📂</div>

          <h2 className="text-2xl font-semibold">
            No documents uploaded
          </h2>

          <p className="mt-2 text-gray-500">
            Upload your first PDF to build your AI
            knowledge base.
          </p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
          <table className="min-w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-4 text-left font-semibold">
                  Filename
                </th>

                <th className="px-6 py-4 text-left font-semibold">
                  Status
                </th>

                <th className="px-6 py-4 text-left font-semibold">
                  Size
                </th>

                <th className="px-6 py-4 text-left font-semibold">
                  Uploaded
                </th>

                <th className="px-6 py-4 text-center font-semibold">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              {documents.map((document) => (
                <tr
                  key={document.id}
                  className="border-t transition hover:bg-gray-50"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <span className="text-xl">
                        📄
                      </span>

                      <span className="font-medium">
                        {document.filename}
                      </span>
                    </div>
                  </td>

                  <td className="px-6 py-4">
                    {getStatusBadge(document.status)}
                  </td>

                  <td className="px-6 py-4">
                    {(
                      document.file_size / 1024
                    ).toFixed(2)}{" "}
                    KB
                  </td>

                  <td className="px-6 py-4 text-gray-600">
                    {new Date(
                      document.created_at,
                    ).toLocaleString()}
                  </td>

                  <td className="px-6 py-4 text-center">
                    <button
                      onClick={() =>
                        handleDelete(document.id)
                      }
                      className="rounded-lg border border-red-500 px-4 py-2 text-sm font-medium text-red-600 transition hover:bg-red-600 hover:text-white"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default DocumentsPage;