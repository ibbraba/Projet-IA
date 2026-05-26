import Card from "../ui/Card";

type Suggestion = {
	title: string;
	description: string;
	priority: "low" | "medium" | "high";
};

type ImprovementSuggestionsProps = {
	suggestions: Suggestion[];
};

export default function ImprovementSuggestions({
	suggestions,
}: ImprovementSuggestionsProps) {
	return (
		<Card title="Suggestions d'amelioration">
			<ul className="space-y-2 text-sm text-slate-600">
				{suggestions.length === 0 ? (
					<li>En attente de suggestions.</li>
				) : (
					suggestions.slice(0, 6).map((suggestion) => (
						<li key={`${suggestion.priority}-${suggestion.title}`}>
							<span className="font-semibold text-slate-900">
								{suggestion.title}
							</span>
							{": "}{suggestion.description}
						</li>
					))
				)}
			</ul>
		</Card>
	);
}
