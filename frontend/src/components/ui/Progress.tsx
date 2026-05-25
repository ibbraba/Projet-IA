type ProgressProps = {
	value: number;
};

export default function Progress({ value }: ProgressProps) {
	const clamped = Math.max(0, Math.min(100, value));
	return (
		<div className="h-2 w-full rounded-full bg-slate-100">
			<div
				className="h-2 rounded-full bg-slate-900"
				style={{ width: `${clamped}%` }}
			/>
		</div>
	);
}
