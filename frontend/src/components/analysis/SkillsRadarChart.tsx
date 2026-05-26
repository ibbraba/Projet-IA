import Card from "../ui/Card";

type RadarData = {
	labels: string[];
	cv_data: number[];
	job_data: number[];
	max_value: number;
};

type SkillsRadarChartProps = {
	radar: RadarData | null;
};

export default function SkillsRadarChart({ radar }: SkillsRadarChartProps) {
	return (
		<Card title="Radar competences">
			{!radar ? (
				<div className="flex h-56 items-center justify-center rounded-md border border-dashed border-slate-300 text-sm text-slate-500">
					Radar chart (placeholder)
				</div>
			) : (
				<ul className="space-y-2 text-sm text-slate-600">
					{radar.labels.map((label, index) => (
						<li key={label} className="flex items-center justify-between">
							<span>{label}</span>
							<span className="font-semibold text-slate-900">
								{Math.round(radar.cv_data[index] ?? 0)} / {radar.max_value}
							</span>
						</li>
					))}
				</ul>
			)}
		</Card>
	);
}
