import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export function useSkills(category?: string) {
  return useQuery({
    queryKey: ["skills", category],
    queryFn: async () => {
      const res = await api.get("/api/v1/skills/", { params: { category } });
      return res.data;
    },
  });
}

export function useInvokeSkill() {
  return useMutation({
    mutationFn: async ({ skill_id, query, context }: { skill_id: string; query: string; context?: object }) => {
      const res = await api.post(`/api/v1/skills/${skill_id}/invoke`, null, { params: { query }, data: { context } });
      return res.data;
    },
  });
}
