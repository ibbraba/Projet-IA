import Card from "../ui/Card";
import Progress from "../ui/Progress";

type MatchingScoreProps = {
	score: number | null;
};

export default function MatchingScore({ score }: MatchingScoreProps) {
	const safeScore = score ?? 0;
	return (
		<Card title="Score global">
			<div className="space-y-4">
				<div className="text-4xl font-semibold text-slate-900">
					{Math.round(safeScore)}%
				</div>
				<Progress value={safeScore} />
				<p className="text-sm text-slate-600">
					Score de compatibilite global.
				</p>
			</div>
		</Card>
	);
}
