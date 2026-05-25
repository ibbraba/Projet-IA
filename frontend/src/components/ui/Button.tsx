import type { ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement>;

export default function Button({ className = "", ...props }: ButtonProps) {
	return (
		<button
			className={
				"inline-flex items-center justify-center rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 " +
				className
			}
			{...props}
		/>
	);
}
