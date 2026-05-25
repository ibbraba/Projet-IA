export default function Header() {
	return (
		<header className="border-b border-slate-200 bg-white">
			<div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
				<div>
					<p className="text-sm uppercase tracking-widest text-slate-500">CV Analyzer</p>
					<h1 className="text-xl font-semibold text-slate-900">
						Matching CV & Offre
					</h1>
				</div>
				<span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">
					Beta
				</span>
			</div>
		</header>
	);
}
