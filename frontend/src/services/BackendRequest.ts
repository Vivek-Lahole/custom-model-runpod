import axios, { CancelTokenSource } from "axios";

axios.defaults.withCredentials = true;

export const BACKEND_URL =
  process.env.BACKEND_URL || "http://localhost:8000/api/v1";

const client = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
});

export default function backendRequest(
  method: string,
  path = "",
  payload: any = {}
) {
  const options = {
    method,
    url: path,
    data: payload,
    responseType: "json",
    headers: {
      "Content-Type": "application/json",
    },
    withCredentials: true,
  };

  return client(options as any).catch((error) => {
    console.error("Error", error);
    throw error;
  });
}
