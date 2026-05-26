import Layout from "./components/layout/Layout";
import CVUploader from "./components/upload/CVUploader";
import JobDescriptionInput from "./components/upload/JobDescriptionInput";
import MatchingScore from "./components/analysis/MatchingScore";
import SkillsRadarChart from "./components/analysis/SkillsRadarChart";
import StrengthsWeaknesses from "./components/results/StrengthsWeaknesses";
import ImprovementSuggestions from "./components/results/ImprovementSuggestions";
import { analyzeCv, uploadCv } from "./services/api";
import { useState } from "react";
import type { AnalyzeResponse } from "./types/api.types";

export default function App() {
	const [selectedFile, setSelectedFile] = useState<File | null>(null);
	const [uploading, setUploading] = useState(false);
	const [uploadMessage, setUploadMessage] = useState<string | null>(null);
	const [jobDescription, setJobDescription] = useState("");
	const [analysisResult, setAnalysisResult] = useState<AnalyzeResponse | null>(
		null
	);

	const handleUpload = async () => {
		if (!selectedFile || uploading) {
			return;
		}

		setUploading(true);
		setUploadMessage(null);
		try {
			const result = await uploadCv(selectedFile);
			setUploadMessage("CV upload successful. Running analysis...");
			const analysis = await analyzeCv(jobDescription);
			setAnalysisResult(analysis);
			setUploadMessage("Analyse terminee.");
		} catch (error) {
			console.error("Upload failed", error);
			setUploadMessage("Analyse echouee. Veuillez reessayer.");
		} finally {
			setUploading(false);
		}
	};

	return (
		<Layout>
			<section className="space-y-6">
				<div className="grid gap-6 md:grid-cols-2">
					<CVUploader onFileSelect={setSelectedFile} />
					<JobDescriptionInput
						value={jobDescription}
						onChange={setJobDescription}
					/>
				</div>

				<div className="flex justify-center">
					<button
						type="button"
						className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
						onClick={handleUpload}
						disabled={!selectedFile || uploading || jobDescription.trim().length < 10}
					>
						{uploading ? "Upload en cours..." : "Analyser le CV"}
					</button>
				</div>
				{uploadMessage && (
					<div className="text-center text-sm text-slate-600">
						{uploadMessage}
					</div>
				)}

				<div className="grid gap-6 md:grid-cols-2">
					<MatchingScore score={analysisResult?.score ?? null} />
					<SkillsRadarChart radar={analysisResult?.visualization.radar ?? null} />
				</div>

				<div className="grid gap-6 md:grid-cols-2">
					<StrengthsWeaknesses
						strengths={analysisResult?.strengths ?? []}
						weaknesses={analysisResult?.weaknesses ?? []}
					/>
					<ImprovementSuggestions
						suggestions={analysisResult?.suggestions ?? []}
					/>
				</div>
			</section>
		</Layout>
	);
}
