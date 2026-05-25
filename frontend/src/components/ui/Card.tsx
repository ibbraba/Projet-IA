import type { ReactNode } from "react";

type CardProps = {
	title?: string;
	children: ReactNode;
};

export default function Card({ title, children }: CardProps) {
	return (
		<section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
			{title && <h2 className="mb-4 text-lg font-semibold">{title}</h2>}
			{children}
		</section>
	);
}
