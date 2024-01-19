export const ApiClient = {
  search: async (query: string, currentPage: number) => {
    let url = new URL(process.env.SERVER_API_URL + "/api/pictures/search");
    if(!!query) url.searchParams.append("search", query);
    if(currentPage === 0 || !!currentPage) url.searchParams.append("page", currentPage.toString());

    return fetch(url)
      .then((res) => res.json())
      .then((json) => JSON.parse(json));
  },

  upload: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    let url = new URL(process.env.SERVER_API_URL + "/api/pictures/upload");

    return fetch(url, {
      method: "POST",
      body: formData,
    });
  },
};
