export type AnalyzeResponse = {
	score: number;
	message: string;
	visualization: {
		score: number;
		radar: {
			labels: string[];
			cv_data: number[];
			job_data: number[];
			max_value: number;
		};
		breakdown: {
			technical_skills: number;
			soft_skills: number;
			experience: number;
			education: number;
			keywords_ats: number;
		};
	};
	strengths: string[];
	weaknesses: string[];
	suggestions: {
		title: string;
		description: string;
		priority: "low" | "medium" | "high";
	}[];
};

export type UploadResponse = {
	upload_id: string;
	extracted_text?: string | null;
};
