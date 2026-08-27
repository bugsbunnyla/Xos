import { useMutation, useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export function useSearch() {
  return useMutation({
    mutationFn: async ({ query, search_type = "hybrid" }: { query: string; search_type?: string }) => {
      const res = await api.post("/api/v1/search/", null, { params: { query, search_type } });
      return res.data;
    },
  });
}

export function useSearchSuggestions(q: string) {
  return useQuery({
    queryKey: ["suggestions", q],
    queryFn: async () => {
      const res = await api.get("/api/v1/search/suggest", { params: { q } });
      return res.data.suggestions;
    },
    enabled: q.length >= 2,
  });
}
