import Card from "../ui/Card";
import Badge from "../ui/Badge";

export default function KeywordsCloud() {
	return (
		<Card title="Mots-cles">
			<div className="flex flex-wrap gap-2">
				<Badge label="Placeholder" />
				<Badge label="Keyword" />
				<Badge label="Skill" />
			</div>
		</Card>
	);
}
