import type { DebateRequest, DebateResponse, HealthResponse } from "./types";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type ApiErrorPayload = {
  detail?: unknown;
  message?: unknown;
};

export class ApiError extends Error {
  status: number | null;

  constructor(message: string, status: number | null = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function fetchHealth(signal?: AbortSignal): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`, { signal });
  if (!response.ok) {
    throw new ApiError("The backend is unavailable. Confirm the FastAPI server is running.", response.status);
  }
  return response.json();
}

export async function runDebate(request: DebateRequest): Promise<DebateResponse> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}/debate/run`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch {
    throw new ApiError("The backend is unavailable. Confirm the FastAPI server is running.");
  }

  if (!response.ok) {
    throw new ApiError(await safeErrorMessage(response), response.status);
  }

  return response.json();
}

async function safeErrorMessage(response: Response): Promise<string> {
  const fallback = fallbackErrorMessage(response.status);

  if (!canShowBackendMessage(response.status)) {
    return fallback;
  }

  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.includes("application/json")) {
    return fallback;
  }

  try {
    const payload = (await response.json()) as ApiErrorPayload;
    const detail = payload.detail ?? payload.message;

    if (typeof detail === "string" && isSafeMessage(detail)) {
      return detail;
    }

    if (Array.isArray(detail) && response.status === 422) {
      return "The debate request is invalid. Check the question, mode, and providers.";
    }
  } catch {
    return fallback;
  }

  return fallback;
}

function fallbackErrorMessage(status: number) {
  return status === 422
    ? "The debate request is invalid. Check the question, mode, and providers."
    : "The debate could not be completed. Please check the backend logs and try again.";
}

function canShowBackendMessage(status: number) {
  return status === 400 || status === 422 || status === 502;
}

function isSafeMessage(message: string) {
  const lower = message.toLowerCase();
  const openAiSecretPrefix = ["s", "k-"].join("");
  return (
    !lower.includes("traceback") &&
    !lower.includes("stack trace") &&
    !lower.includes(openAiSecretPrefix)
  );
}
