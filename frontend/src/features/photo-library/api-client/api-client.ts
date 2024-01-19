export const ApiClient = {
  search: async (query: string): Promise<string[]> => {
    let url = process.env.SERVER_API_URL + "/search"
    if(!!query)  url += "&search=" + query;

    return (await fetch(url)).json();
  },

  upload: async (file: File) => {
    //TODO implement
  },
};
