export const ApiClient = {
  search: async (query: string) => {
    let url = new URL(process.env.SERVER_API_URL + "/api/pictures/search");
    if(!!query) url.searchParams.append("search", query);

    return fetch(url)
      .then((res) => res.json())
      .then((json) => JSON.parse(json));
  },

  upload: async (file: File) => {
    //TODO implement
  },
};
