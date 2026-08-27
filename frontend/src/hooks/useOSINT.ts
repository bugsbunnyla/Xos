import { useMutation, useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export function useOSINTInvestigate() {
  return useMutation({
    mutationFn: async (data: { target: string; target_type?: string; modules?: string[] }) => {
      const res = await api.post("/api/v1/osint/investigate", null, { params: data });
      return res.data;
    },
  });
}

export function useOSINTReports() {
  return useQuery({
    queryKey: ["osint-reports"],
    queryFn: async () => {
      const res = await api.get("/api/v1/osint/reports");
      return res.data;
    },
  });
}
