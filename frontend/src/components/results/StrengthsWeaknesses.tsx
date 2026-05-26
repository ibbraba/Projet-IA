import Card from "../ui/Card";

type StrengthsWeaknessesProps = {
	strengths: string[];
	weaknesses: string[];
};

export default function StrengthsWeaknesses({
	strengths,
	weaknesses,
}: StrengthsWeaknessesProps) {
	return (
		<Card title="Points forts / faibles">
			<div className="grid gap-4 text-sm text-slate-600">
				<div>
					<p className="font-semibold text-slate-900">Points forts</p>
					<ul className="list-disc pl-4">
						{strengths.length === 0 ? (
							<li>En attente de resultat.</li>
						) : (
							strengths.slice(0, 6).map((item) => (
								<li key={`strength-${item}`}>{item}</li>
							))
						)}
					</ul>
				</div>
				<div>
					<p className="font-semibold text-slate-900">Points faibles</p>
					<ul className="list-disc pl-4">
						{weaknesses.length === 0 ? (
							<li>En attente de resultat.</li>
						) : (
							weaknesses.slice(0, 6).map((item) => (
								<li key={`weak-${item}`}>{item}</li>
							))
						)}
					</ul>
				</div>
			</div>
		</Card>
	);
}
