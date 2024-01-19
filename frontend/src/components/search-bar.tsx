import { useEffect, useState } from "react";
import { delayRequest } from "../features/utils";

export const SearchBar = ({
  onSearch,
  onUpload,
}: {
  onSearch: (search: string, currentPage: number) => void;
  onUpload: (file: File) => Promise<void>;
}) => {
  const [search, setSearch] = useState("");
  const [currentPage, setCurrentPage] = useState<number>(0);
  const [loadingUpload, setLoadingUpload] = useState(false);

  useEffect(() => {
    delayRequest("search", () => {
      onSearch(search, currentPage);
    });
  }, [search, currentPage]);

  const chooseFile = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.onchange = async (e) => {
      const target = e.target as HTMLInputElement;
      const file: File = (target.files as FileList)[0];
      setLoadingUpload(true);
      await onUpload(file);
      setLoadingUpload(false);
    };
    input.click();
  };

  return (
    <div>
      <div className="flex items-center">
        <div className="relative w-full">
          <input
            type="text"
            className="bg-gray-200 outline-none text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="Search photos, objects..."
            value={search}
            onChange={(e) => { setSearch(e.target.value) }}
          />
        </div>
        <button
          disabled={loadingUpload}
          onClick={() => chooseFile()}
          className="inline-flex items-center py-2.5 px-3 ml-2 text-sm font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:bg-blue-700"
        >
          {loadingUpload ? "Loading..." : "Upload"}
        </button>
      </div>

      <div className="w-full grid grid-cols-3 gap-4 mt-4">
        <div> { currentPage > 0 && 
            <button onClick={() => setCurrentPage(page => page-1)} 
                    className="inline-flex items-center py-2.5 px-3 ml-2 text-sm font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:bg-blue-700">
              Previous
            </button> 
            } 
          </div>
          <div>
            <button onClick={() => setCurrentPage(page => page+1)}
                    className="inline-flex items-center py-2.5 px-3 ml-2 text-sm font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:bg-blue-700">
              Next
            </button>
        </div>
      </div>  
    </div>
  );
};
