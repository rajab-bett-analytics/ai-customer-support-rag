import api from "../../api/client";


export interface Document {

  // Identity
  id: number;


  // File information
  filename: string;
  stored_filename: string;
  mime_type: string;
  file_size: number;


  // Processing information
  status: string;

  page_count: number;
  chunk_count: number;
  embedding_count: number;

  indexed_at: string | null;
  error_message: string | null;


  // Ownership
  uploaded_by: number;


  // Timestamps
  created_at: string;
  updated_at: string;
}



export interface UploadDocumentResponse {

  document_id: number;

  filename: string;

  status: string;


  pages: number;

  chunks_created: number;

  embeddings_created: number;


  file_size: number;
}



export async function getDocuments(): Promise<
  Document[]
> {

  const response = await api.get<Document[]>(
    "/documents",
  );


  return response.data;
}




export async function uploadDocument(
  file: File,
): Promise<UploadDocumentResponse> {


  const formData = new FormData();


  formData.append(
    "file",
    file,
  );


  const response = await api.post(
    "/documents/upload",
    formData,
    {
      headers: {
        "Content-Type":
          "multipart/form-data",
      },
    },
  );


  return response.data;
}




export async function deleteDocument(
  documentId: number,
): Promise<void> {


  await api.delete(
    `/documents/${documentId}`,
  );

}