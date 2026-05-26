import React, { useRef, useState } from "react";
import Card from "../ui/Card";
import Button from "../ui/Button";

type CVUploaderProps = {
	onFileSelect?: (file: File | null) => void;
};

export default function CVUploader({ onFileSelect }: CVUploaderProps) {
	const inputRef = useRef<HTMLInputElement | null>(null);
	const [selectedFile, setSelectedFile] = useState<string | null>(null);

	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0] || null;
		setSelectedFile(file?.name || null);
		onFileSelect?.(file);
	};

	return (
		<Card title="Votre CV">
			<div className="space-y-3">
				<p className="text-sm text-slate-600">Deposez un fichier PDF ou DOCX.</p>
				<div className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-sm text-slate-500">
					Zone de depose (PDF / DOCX)
				</div>
				{selectedFile && (
					<div className="rounded-lg bg-green-50 p-3 text-sm text-green-700">
						Fichier sélectionné: <strong>{selectedFile}</strong>
					</div>
				)}
				<input
					ref={inputRef}
					type="file"
					accept=".pdf,.docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword"
					className="hidden"
					onChange={handleFileChange}
				/>
				<Button onClick={() => inputRef.current?.click()}>Choisir un fichier</Button>
			</div>
		</Card>
	);
}
