import Layout from "./components/layout/Layout";
import CVUploader from "./components/upload/CVUploader";
import JobDescriptionInput from "./components/upload/JobDescriptionInput";
import MatchingScore from "./components/analysis/MatchingScore";
import SkillsRadarChart from "./components/analysis/SkillsRadarChart";
import StrengthsWeaknesses from "./components/results/StrengthsWeaknesses";
import ImprovementSuggestions from "./components/results/ImprovementSuggestions";

export default function App() {
	return (
		<Layout>
			<section className="space-y-6">
				<div className="grid gap-6 md:grid-cols-2">
					<CVUploader />
					<JobDescriptionInput />
				</div>

				<div className="grid gap-6 md:grid-cols-2">
					<MatchingScore />
					<SkillsRadarChart />
				</div>

				<div className="grid gap-6 md:grid-cols-2">
					<StrengthsWeaknesses />
					<ImprovementSuggestions />
				</div>
			</section>
		</Layout>
	);
}
