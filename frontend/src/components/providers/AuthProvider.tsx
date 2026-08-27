"use client";
import { createContext, useContext, useEffect, useState } from "react";
import axios from "axios";

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  company_id?: string;
  department?: string;
  job_title?: string;
  role: string;
  subscription_tier: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("phdxpert_token");
    if (stored) {
      setToken(stored);
      fetchUser(stored);
    } else {
      setIsLoading(false);
    }
  }, []);

  const fetchUser = async (t: string) => {
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${t}` },
      });
      setUser(res.data);
    } catch {
      localStorage.removeItem("phdxpert_token");
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, form);
    const { access_token, user } = res.data;
    localStorage.setItem("phdxpert_token", access_token);
    setToken(access_token);
    setUser(user);
  };

  const logout = () => {
    localStorage.removeItem("phdxpert_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
