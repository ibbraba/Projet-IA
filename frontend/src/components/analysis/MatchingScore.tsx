import Card from "../ui/Card";
import Progress from "../ui/Progress";

export default function MatchingScore() {
	return (
		<Card title="Score global">
			<div className="space-y-4">
				<div className="text-4xl font-semibold text-slate-900">0%</div>
				<Progress value={0} />
				<p className="text-sm text-slate-600">
					Score de compatibilite global.
				</p>
			</div>
		</Card>
	);
}
