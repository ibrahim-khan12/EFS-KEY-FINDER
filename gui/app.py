from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from modules.collector import EFSArtifactCollector
from reports.exporter import ReportExporter


class MetricCard(ttk.Frame):
    def __init__(self, master: tk.Misc, title: str, accent: str) -> None:
        super().__init__(master, style="Card.TFrame", padding=14)
        self.configure(style="Card.TFrame")
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text=title.upper(), style="MetricTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.value_label = ttk.Label(self, text="0", style="MetricValue.TLabel")
        self.value_label.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.note_label = ttk.Label(self, text="Awaiting scan", style="MetricNote.TLabel")
        self.note_label.grid(row=2, column=0, sticky="w", pady=(8, 0))
        accent_bar = tk.Frame(self, bg=accent, height=4)
        accent_bar.grid(row=3, column=0, sticky="ew", pady=(12, 0))

    def set_value(self, value: str, note: str) -> None:
        self.value_label.configure(text=value)
        self.note_label.configure(text=note)


class ForensicDashboard(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("EFS Key Finder / EFS Key Extractor")
        self.geometry("1400x860")
        self.minsize(1180, 760)
        self.configure(bg="#07111f")
        self.results: dict | None = None
        self.status_var = tk.StringVar(value="Ready. Select a source and start a scan.")
        self.source_var = tk.StringVar(value="D:/8th SEMESTER/DF/PROJECT/demo/RealEfsDataset")
        self.mode_var = tk.StringVar(value="live")
        self.case_var = tk.StringVar(value="CASE-001")
        self.examiner_var = tk.StringVar(value="Examiner")

        self._build_theme()
        self._build_layout()

    def _build_theme(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Root.TFrame", background="#07111f")
        style.configure("Card.TFrame", background="#0d1b2a", relief="flat")
        style.configure("Panel.TFrame", background="#0b1725")
        style.configure("TLabel", background="#07111f", foreground="#dce7f3", font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background="#07111f", foreground="#8ca1b6", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#07111f", foreground="#f3f7fb", font=("Bahnschrift SemiBold", 26))
        style.configure("SubHeader.TLabel", background="#07111f", foreground="#7fb7ff", font=("Segoe UI Semibold", 11))
        style.configure("Section.TLabel", background="#07111f", foreground="#9dd6ff", font=("Segoe UI Semibold", 12))
        style.configure("MetricTitle.TLabel", background="#0d1b2a", foreground="#7f93a8", font=("Segoe UI Semibold", 9))
        style.configure("MetricValue.TLabel", background="#0d1b2a", foreground="#f8fbff", font=("Bahnschrift SemiBold", 24))
        style.configure("MetricNote.TLabel", background="#0d1b2a", foreground="#9ab1c8", font=("Segoe UI", 9))
        style.configure("CardText.TLabel", background="#0d1b2a", foreground="#dce7f3", font=("Segoe UI", 10))
        style.configure("Field.TEntry", fieldbackground="#0f2234", foreground="#ecf3fb", bordercolor="#163149", lightcolor="#163149", darkcolor="#163149")
        style.configure("TCombobox", fieldbackground="#0f2234", background="#0f2234", foreground="#ecf3fb", arrowcolor="#9dd6ff")
        style.configure("Primary.TButton", background="#0086d1", foreground="white", padding=(16, 10), borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#0a9ae9")])
        style.configure("Secondary.TButton", background="#183047", foreground="#dce7f3", padding=(14, 9), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#21415e")])
        style.configure("Treeview", background="#0b1725", fieldbackground="#0b1725", foreground="#e7eef7", rowheight=28, bordercolor="#173048")
        style.configure("Treeview.Heading", background="#12263a", foreground="#8fd4ff", font=("Segoe UI Semibold", 10))
        style.map("Treeview", background=[("selected", "#124a73")], foreground=[("selected", "#ffffff")])
        style.configure("TNotebook", background="#07111f", borderwidth=0)
        style.configure("TNotebook.Tab", background="#102131", foreground="#93a7bc", padding=(12, 8))
        style.map("TNotebook.Tab", background=[("selected", "#0d1b2a")], foreground=[("selected", "#f5fbff")])
        style.configure("TLabelframe", background="#0b1725", foreground="#93cfff")
        style.configure("TLabelframe.Label", background="#0b1725", foreground="#93cfff")

    def _build_layout(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame", padding=18)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(3, weight=1)

        self._build_header(root)
        self._build_controls(root)
        self._build_metrics(root)
        self._build_content(root)
        self._build_status(root)

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="Root.TFrame")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="EFS Key Finder / EFS Key Extractor", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Windows forensic console for confirmed EFS detection, certificate correlation, and evidence reporting.",
            style="SubHeader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        legal = ttk.Frame(header, style="Card.TFrame", padding=(14, 10))
        legal.grid(row=0, column=1, rowspan=2, sticky="e")
        ttk.Label(legal, text="AUTHORIZED FORENSIC USE ONLY", style="MetricTitle.TLabel").pack(anchor="w")
        ttk.Label(
            legal,
            text="Read-only handling, chain of custody, privacy compliance, court-ready reporting.",
            style="CardText.TLabel",
            wraplength=350,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def _build_controls(self, parent: ttk.Frame) -> None:
        controls = ttk.Frame(parent, style="Card.TFrame", padding=16)
        controls.grid(row=1, column=0, sticky="ew", pady=(18, 14))
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)

        ttk.Label(controls, text="Evidence Source", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(controls, textvariable=self.source_var, style="Field.TEntry").grid(row=1, column=0, columnspan=3, sticky="ew", padx=(0, 12), pady=(6, 0))
        ttk.Button(controls, text="Browse", style="Secondary.TButton", command=self._browse_source).grid(row=1, column=3, sticky="e", pady=(6, 0))

        ttk.Label(controls, text="Mode", style="Section.TLabel").grid(row=2, column=0, sticky="w", pady=(14, 0))
        ttk.Label(controls, text="Case ID", style="Section.TLabel").grid(row=2, column=1, sticky="w", pady=(14, 0))
        ttk.Label(controls, text="Examiner", style="Section.TLabel").grid(row=2, column=2, sticky="w", pady=(14, 0))

        ttk.Combobox(controls, textvariable=self.mode_var, values=["auto", "live", "image"], state="readonly", width=14).grid(row=3, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(controls, textvariable=self.case_var, style="Field.TEntry").grid(row=3, column=1, sticky="ew", padx=(0, 12), pady=(6, 0))
        ttk.Entry(controls, textvariable=self.examiner_var, style="Field.TEntry").grid(row=3, column=2, sticky="ew", padx=(0, 12), pady=(6, 0))

        action_bar = ttk.Frame(controls, style="Card.TFrame")
        action_bar.grid(row=3, column=3, sticky="e", pady=(6, 0))
        ttk.Button(action_bar, text="Load Real EFS Demo", style="Secondary.TButton", command=self._load_real_demo).pack(side="left", padx=(0, 8))
        ttk.Button(action_bar, text="Scan Evidence", style="Primary.TButton", command=self._scan).pack(side="left", padx=(0, 8))
        ttk.Button(action_bar, text="Export Report", style="Secondary.TButton", command=self._export).pack(side="left")

    def _build_metrics(self, parent: ttk.Frame) -> None:
        metrics = ttk.Frame(parent, style="Root.TFrame")
        metrics.grid(row=2, column=0, sticky="ew")
        for column in range(4):
            metrics.columnconfigure(column, weight=1)

        self.metric_files = MetricCard(metrics, "EFS Files", "#00c2ff")
        self.metric_files.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.metric_confirmed = MetricCard(metrics, "Confirmed EFS", "#2dd4bf")
        self.metric_confirmed.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        self.metric_certs = MetricCard(metrics, "Certificates", "#f59e0b")
        self.metric_certs.grid(row=0, column=2, sticky="ew", padx=(0, 12))
        self.metric_alerts = MetricCard(metrics, "Alerts", "#ef4444")
        self.metric_alerts.grid(row=0, column=3, sticky="ew")

    def _build_content(self, parent: ttk.Frame) -> None:
        content = ttk.Panedwindow(parent, orient="horizontal")
        content.grid(row=3, column=0, sticky="nsew", pady=(14, 0))

        left = ttk.Frame(content, style="Panel.TFrame", padding=14)
        right = ttk.Frame(content, style="Panel.TFrame", padding=14)
        content.add(left, weight=3)
        content.add(right, weight=4)

        ttk.Label(left, text="Evidence Navigator", style="Section.TLabel").pack(anchor="w")
        ttk.Label(left, text="Browse findings by category and click an item for structured detail.", style="Muted.TLabel").pack(anchor="w", pady=(4, 10))
        self.tree = ttk.Treeview(left, columns=("summary", "status"), show="tree headings")
        self.tree.heading("#0", text="Artifact")
        self.tree.heading("summary", text="Summary")
        self.tree.heading("status", text="Status")
        self.tree.column("#0", width=260, stretch=True)
        self.tree.column("summary", width=360, stretch=True)
        self.tree.column("status", width=120, stretch=False, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        notebook = ttk.Notebook(right)
        notebook.pack(fill="both", expand=True)

        summary_tab = ttk.Frame(notebook, style="Panel.TFrame", padding=12)
        detail_tab = ttk.Frame(notebook, style="Panel.TFrame", padding=12)
        raw_tab = ttk.Frame(notebook, style="Panel.TFrame", padding=12)
        notebook.add(summary_tab, text="Case Summary")
        notebook.add(detail_tab, text="Selected Artifact")
        notebook.add(raw_tab, text="Raw JSON")

        ttk.Label(summary_tab, text="Investigation Summary", style="Section.TLabel").pack(anchor="w")
        self.summary_text = tk.Text(summary_tab, bg="#081521", fg="#e7eef7", relief="flat", wrap="word", font=("Consolas", 10), insertbackground="#ffffff")
        self.summary_text.pack(fill="both", expand=True, pady=(10, 0))

        ttk.Label(detail_tab, text="Artifact Detail", style="Section.TLabel").pack(anchor="w")
        self.detail_text = tk.Text(detail_tab, bg="#081521", fg="#e7eef7", relief="flat", wrap="word", font=("Consolas", 10), insertbackground="#ffffff")
        self.detail_text.pack(fill="both", expand=True, pady=(10, 0))

        ttk.Label(raw_tab, text="Raw Result JSON", style="Section.TLabel").pack(anchor="w")
        self.raw_text = tk.Text(raw_tab, bg="#081521", fg="#e7eef7", relief="flat", wrap="word", font=("Consolas", 10), insertbackground="#ffffff")
        self.raw_text.pack(fill="both", expand=True, pady=(10, 0))

        self.tree_payloads: dict[str, dict] = {}

    def _build_status(self, parent: ttk.Frame) -> None:
        status = ttk.Frame(parent, style="Card.TFrame", padding=(12, 10))
        status.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        ttk.Label(status, textvariable=self.status_var, style="CardText.TLabel").pack(anchor="w")

    def _browse_source(self) -> None:
        selected = filedialog.askopenfilename(title="Select forensic image or evidence file")
        if not selected:
            selected = filedialog.askdirectory(title="Select live evidence path")
        if selected:
            self.source_var.set(selected)
            self.status_var.set(f"Evidence source set to {selected}")

    def _load_real_demo(self) -> None:
        self.source_var.set(str(Path.cwd() / "demo" / "RealEfsDataset"))
        self.mode_var.set("live")
        self.status_var.set("Loaded the real EFS demo dataset path.")

    def _scan(self) -> None:
        self.status_var.set("Scanning evidence source...")
        self.update_idletasks()
        try:
            collector = EFSArtifactCollector(case_id=self.case_var.get(), investigator=self.examiner_var.get())
            self.results = collector.run(source=self.source_var.get(), mode=self.mode_var.get())
            self._populate_tree(self.results)
            self._populate_summary(self.results)
            self.raw_text.delete("1.0", tk.END)
            self.raw_text.insert(tk.END, json.dumps(self.results, indent=2, default=str))
            self.status_var.set("Scan completed successfully.")
            messagebox.showinfo("Scan complete", "Forensic scan completed successfully.")
        except Exception as exc:
            self.status_var.set(f"Scan failed: {exc}")
            messagebox.showerror("Scan failed", f"The scan could not complete.\n\n{exc}")

    def _populate_tree(self, results: dict) -> None:
        self.tree_payloads.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

        sections = [
            ("Encrypted Files", results.get("encrypted_files", []), "file"),
            ("Certificates", results.get("certificates", []), "certificate"),
            ("Registry", results.get("registry", []), "registry"),
            ("Timeline", results.get("timeline", []), "timeline"),
            ("Alerts", results.get("alerts", []), "alert"),
        ]

        for section_name, values, section_type in sections:
            parent = self.tree.insert("", "end", text=section_name, values=(f"{len(values)} item(s)", "section"), open=True)
            for index, value in enumerate(values[:300]):
                item_id = f"{section_type}-{index}"
                label, summary, status = self._tree_row(section_type, value)
                self.tree.insert(parent, "end", iid=item_id, text=label, values=(summary, status))
                self.tree_payloads[item_id] = value if isinstance(value, dict) else {"value": value}

        self._update_metrics(results)

    def _populate_summary(self, results: dict) -> None:
        case = results.get("case", {})
        encrypted_files = results.get("encrypted_files", [])
        confirmed = [item for item in encrypted_files if item.get("efs_status") == "confirmed"]
        certificates = results.get("certificates", [])
        alerts = results.get("alerts", [])

        lines = [
            f"Case ID: {case.get('case_id', '')}",
            f"Investigator: {case.get('investigator', '')}",
            f"Source: {case.get('source', '')}",
            f"Mode: {case.get('mode', '')}",
            "",
            f"Encrypted file findings: {len(encrypted_files)}",
            f"Confirmed EFS files: {len(confirmed)}",
            f"Certificate / key artifacts: {len(certificates)}",
            f"Registry artifacts: {len(results.get('registry', []))}",
            f"Timeline entries: {len(results.get('timeline', []))}",
            "",
            "Alerts:",
        ]
        if alerts:
            lines.extend(f"- {alert}" for alert in alerts)
        else:
            lines.append("- No high-priority alerts generated.")

        if confirmed:
            lines.extend(["", "Confirmed EFS sample(s):"])
            lines.extend(f"- {item.get('path')} [{item.get('algorithm', 'Unknown')} / {item.get('key_length', 'Unknown')}]" for item in confirmed[:8])

        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, "\n".join(lines))
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, "Select an artifact from the Evidence Navigator to inspect it here.")

    def _update_metrics(self, results: dict) -> None:
        encrypted_files = results.get("encrypted_files", [])
        confirmed = [item for item in encrypted_files if item.get("efs_status") == "confirmed"]
        certificates = results.get("certificates", [])
        alerts = results.get("alerts", [])

        self.metric_files.set_value(str(len(encrypted_files)), "All suspected and confirmed EFS-related files")
        self.metric_confirmed.set_value(str(len(confirmed)), "Files verified via Windows encryption metadata")
        self.metric_certs.set_value(str(len(certificates)), "Certificate and key container artifacts")
        self.metric_alerts.set_value(str(len(alerts)), "High-value or suspicious encryption indicators")

    def _tree_row(self, section_type: str, value: dict | str) -> tuple[str, str, str]:
        if isinstance(value, str):
            return value, "Alert", "review"
        if section_type == "file":
            label = Path(value.get("path", "artifact")).name
            summary = value.get("path", "")
            status = value.get("efs_status", "suspected")
            return label, summary, status
        if section_type == "certificate":
            label = value.get("subject", "certificate")
            summary = value.get("thumbprint", "")
            return label, summary, value.get("user", "")
        if section_type == "registry":
            label = value.get("value_name", "registry")
            summary = value.get("key_path", "")
            return label, summary, value.get("hive", "")
        if section_type == "timeline":
            label = value.get("artifact_type", "timeline")
            summary = value.get("description", "")
            return label, summary, value.get("timestamp", "")
        return "Artifact", json.dumps(value, default=str)[:80], ""

    def _on_tree_select(self, _event: object) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        payload = self.tree_payloads.get(selection[0])
        if not payload:
            return
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, json.dumps(payload, indent=2, default=str))

    def _export(self) -> None:
        if not self.results:
            messagebox.showwarning("No results", "Run a scan before exporting.")
            return
        out_dir = Path(filedialog.askdirectory(title="Select export directory") or ".")
        exporter = ReportExporter(out_dir)
        generated = exporter.export(self.results, formats=["json", "csv", "html", "pdf"])
        self.status_var.set(f"Exported {len(generated)} report artifact(s) to {out_dir}")
        messagebox.showinfo("Export complete", "Generated:\n" + "\n".join(str(item) for item in generated))


def launch() -> None:
    app = ForensicDashboard()
    app.mainloop()


if __name__ == "__main__":
    launch()
