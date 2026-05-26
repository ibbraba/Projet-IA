import Card from "../ui/Card";

type JobDescriptionInputProps = {
	value: string;
	onChange: (value: string) => void;
};

export default function JobDescriptionInput({
	value,
	onChange,
}: JobDescriptionInputProps) {
	return (
		<Card title="Offre d'emploi">
			<div className="space-y-3">
				<p className="text-sm text-slate-600">
					Collez la description du poste.
				</p>
				<textarea
					className="min-h-[180px] w-full rounded-md border border-slate-300 bg-white p-3 text-sm focus:border-slate-400 focus:outline-none"
					placeholder="Description de l'offre..."
					value={value}
					onChange={(event) => onChange(event.target.value)}
				/>
			</div>
		</Card>
	);
}
