import Card from "../ui/Card";
import Button from "../ui/Button";

export default function CVUploader() {
	return (
		<Card title="Votre CV">
			<div className="space-y-3">
				<p className="text-sm text-slate-600">Deposez un fichier PDF.</p>
				<div className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-sm text-slate-500">
					Zone de depose (PDF)
				</div>
				<Button>Choisir un fichier</Button>
			</div>
		</Card>
	);
}
