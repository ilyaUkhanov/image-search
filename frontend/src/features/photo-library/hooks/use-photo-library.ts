import { useState } from "react";
import { ApiClient } from "../api-client/api-client";

type PhotoLibraryResult = string;

export function usePhotoLibrary(): [
  string[],
  (query: string, currentPage: number) => void,
  (file: File) => Promise<void>
] {
  const [results, setResults] = useState<PhotoLibraryResult[]>([]);

  const search = async (query: string, currentPage: number) => {
    setResults(await ApiClient.search(query, currentPage));
  };

  const upload = async (file: File) => {
    await ApiClient.upload(file);
  };

  return [results, search, upload];
};
