export interface DocumentSource {
  document_id: number;

  document_name: string;

  document_url: string;

  page: number;

  chunk_index: number;

  section?: string;

  chunk_text?: string;
}