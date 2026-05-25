import Card from "../ui/Card";

export default function StrengthsWeaknesses() {
	return (
		<Card title="Points forts / faibles">
			<div className="grid gap-4 text-sm text-slate-600">
				<div>
					<p className="font-semibold text-slate-900">Points forts</p>
					<ul className="list-disc pl-4">
						<li>Placeholder</li>
					</ul>
				</div>
				<div>
					<p className="font-semibold text-slate-900">Points faibles</p>
					<ul className="list-disc pl-4">
						<li>Placeholder</li>
					</ul>
				</div>
			</div>
		</Card>
	);
}
