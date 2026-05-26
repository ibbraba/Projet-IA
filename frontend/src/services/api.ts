import axios from "axios";

import type { AnalyzeResponse, UploadResponse } from "../types/api.types";

console.log("API base URL:", (import.meta as any).env.VITE_API_BASE_URL);
const api = axios.create({
	baseURL: (import.meta as any).env.VITE_API_BASE_URL || "http://localhost:8000",
});

export async function uploadCv(file: File): Promise<UploadResponse> {
	console.log("Uploading file:", file.name, file.size, file.type);
	const formData = new FormData();
	formData.append("file", file);

	const response = await api.post<UploadResponse>("/api/v1/upload/", formData, {
		headers: {
			"Content-Type": "multipart/form-data",
		},
	});

	return response.data;
}

export async function analyzeCv(jobDescription: string): Promise<AnalyzeResponse> {
	const response = await api.post<AnalyzeResponse>("/api/v1/analysis/", {
		job_description: jobDescription,
	});

	return response.data;
}

export default api;
