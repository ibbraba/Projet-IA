import type { ReactNode } from "react";

import Footer from "./Footer";
import Header from "./Header";

type LayoutProps = {
	children: ReactNode;
};

export default function Layout({ children }: LayoutProps) {
	return (
		<div className="min-h-screen bg-slate-50 text-slate-900">
			<Header />
			<main className="mx-auto w-full max-w-6xl px-6 py-10">{children}</main>
			<Footer />
		</div>
	);
}
