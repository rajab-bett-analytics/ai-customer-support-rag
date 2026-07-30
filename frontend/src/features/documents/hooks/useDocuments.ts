import { useEffect, useMemo, useState } from "react";

import {
  deleteDocument,
  getDocuments,
  uploadDocument,
  type Document,
} from "../documentService";

export function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [search, setSearch] = useState("");

  async function loadDocuments() {
    try {
      setLoading(true);

      const data = await getDocuments();

      setDocuments(data);
    } catch (error) {
      console.error("Failed to load documents:", error);
    } finally {
      setLoading(false);
    }
  }

  async function upload(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    try {
      setUploading(true);

      await uploadDocument(file);

      await loadDocuments();

      event.target.value = "";
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setUploading(false);
    }
  }

  async function remove(documentId: number) {
    const confirmed = window.confirm(
      "Delete this document?",
    );

    if (!confirmed) return;

    try {
      await deleteDocument(documentId);

      setDocuments((previous) =>
        previous.filter(
          (document) =>
            document.id !== documentId,
        ),
      );
    } catch (error) {
      console.error("Delete failed:", error);
    }
  }

  const filteredDocuments = useMemo(() => {
    return documents.filter((document) =>
      document.filename
        .toLowerCase()
        .includes(search.toLowerCase()),
    );
  }, [documents, search]);

  useEffect(() => {
    void loadDocuments();
  }, []);

  return {
    documents,
    filteredDocuments,

    loading,
    uploading,

    search,
    setSearch,

    loadDocuments,

    upload,

    remove,
  };
}