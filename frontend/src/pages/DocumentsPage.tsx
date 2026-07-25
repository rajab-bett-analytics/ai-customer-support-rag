import { useEffect, useState } from "react";

import {
  getDocuments,
  deleteDocument,
  uploadDocument,
  type Document,
} from "../features/documents/documentService";

function DocumentsPage() {
  const [documents, setDocuments] = useState<
    Document[]
  >([]);

  const [loading, setLoading] =
    useState(true);

  const [uploading, setUploading] =
    useState(false);

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

  async function handleDelete(
    documentId: number,
  ) {
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

  useEffect(() => {
    void loadDocuments();
  }, []);

  return (
    <div className="mx-auto max-w-6xl space-y-6 p-8">
      <h1 className="text-3xl font-bold">
        Knowledge Base
      </h1>

      <p className="text-gray-600">
        Upload PDF documents that your AI
        assistant will use to answer customer
        questions.
      </p>

      <div className="space-y-2">
        <input
          type="file"
          accept=".pdf"
          disabled={uploading}
          onChange={handleUpload}
        />

        {uploading && (
          <p className="text-blue-600">
            Uploading document...
          </p>
        )}
      </div>

      {loading ? (
        <p className="text-gray-500">
          Loading documents...
        </p>
      ) : documents.length === 0 ? (
        <p className="text-gray-500">
          No documents uploaded yet.
        </p>
      ) : (
        <div className="overflow-hidden rounded-lg border bg-white">
          <table className="min-w-full">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-3 text-left">
                  Filename
                </th>

                <th className="px-4 py-3 text-left">
                  Status
                </th>

                <th className="px-4 py-3 text-left">
                  Size
                </th>

                <th className="px-4 py-3 text-left">
                  Uploaded
                </th>

                <th className="px-4 py-3 text-center">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              {documents.map((document) => (
                <tr
                  key={document.id}
                  className="border-t"
                >
                  <td className="px-4 py-3">
                    {document.filename}
                  </td>

                  <td className="px-4 py-3 capitalize">
                    {document.status}
                  </td>

                  <td className="px-4 py-3">
                    {(
                      document.file_size / 1024
                    ).toFixed(2)}{" "}
                    KB
                  </td>

                  <td className="px-4 py-3">
                    {new Date(
                      document.created_at,
                    ).toLocaleString()}
                  </td>

                  <td className="px-4 py-3 text-center">
                    <button
                      onClick={() =>
                        handleDelete(
                          document.id,
                        )
                      }
                      className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700"
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