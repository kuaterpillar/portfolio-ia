import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import threading
from email_classifier import EmailClassifier

class EmailManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire d'Emails - Conciergerie")
        self.root.geometry("1200x800")

        self.classifier = EmailClassifier()
        self.setup_ui()
        self.load_emails()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Titre
        title_label = ttk.Label(main_frame, text="Gestionnaire d'Emails - Conciergerie",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame des boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Boutons
        ttk.Button(button_frame, text="Actualiser", command=self.refresh_emails).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Traiter Nouveaux Emails", command=self.process_new_emails).pack(side=tk.LEFT, padx=(0, 10))

        # Filtre par priorité
        ttk.Label(button_frame, text="Filtrer par:").pack(side=tk.LEFT, padx=(20, 5))
        self.priority_filter = ttk.Combobox(button_frame, values=["Tous", "URGENT", "HAUTE", "MOYENNE", "BASSE"])
        self.priority_filter.set("Tous")
        self.priority_filter.pack(side=tk.LEFT, padx=(0, 10))
        self.priority_filter.bind("<<ComboboxSelected>>", self.filter_emails)

        # Statistiques
        self.stats_frame = ttk.LabelFrame(main_frame, text="Statistiques", padding="10")
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.stats_label = ttk.Label(self.stats_frame, text="")
        self.stats_label.pack()

        # Treeview pour les emails
        columns = ("ID", "Priorité", "Date", "Expéditeur", "Sujet")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

        # Configuration des colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Priorité", text="Priorité")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Expéditeur", text="Expéditeur")
        self.tree.heading("Sujet", text="Sujet")

        self.tree.column("ID", width=50)
        self.tree.column("Priorité", width=100)
        self.tree.column("Date", width=150)
        self.tree.column("Expéditeur", width=200)
        self.tree.column("Sujet", width=400)

        # Couleurs par priorité
        self.tree.tag_configure("URGENT", background="#ffcccc")
        self.tree.tag_configure("HAUTE", background="#fff2cc")
        self.tree.tag_configure("MOYENNE", background="#e6f3ff")
        self.tree.tag_configure("BASSE", background="#f0f0f0")

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack treeview et scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Frame pour détails de l'email sélectionné
        details_frame = ttk.LabelFrame(main_frame, text="Détails de l'Email", padding="10")
        details_frame.pack(fill=tk.X, pady=(10, 0))

        self.details_text = tk.Text(details_frame, height=6, wrap=tk.WORD)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)

        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind événement de sélection
        self.tree.bind("<<TreeviewSelect>>", self.show_email_details)

    def load_emails(self):
        """Charger les emails depuis la base de données"""
        try:
            conn = sqlite3.connect('emails_trie.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM emails ORDER BY priority DESC, processed_date DESC')
            self.all_emails = cursor.fetchall()
            conn.close()

            self.display_emails(self.all_emails)
            self.update_stats()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les emails: {e}")

    def display_emails(self, emails):
        """Afficher les emails dans le treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for email in emails:
            id_email, sender, subject, content, priority_num, priority_label, date_received, processed_date = email

            # Formatter la date
            try:
                date_str = processed_date[:16] if processed_date else "N/A"
            except:
                date_str = "N/A"

            # Limiter la longueur du sujet et de l'expéditeur
            sender_short = sender[:30] + "..." if len(sender) > 30 else sender
            subject_short = subject[:50] + "..." if len(subject) > 50 else subject

            item = self.tree.insert("", tk.END, values=(
                id_email,
                priority_label,
                date_str,
                sender_short,
                subject_short
            ), tags=[priority_label])

    def filter_emails(self, event=None):
        """Filtrer les emails par priorité"""
        filter_priority = self.priority_filter.get()

        if filter_priority == "Tous":
            filtered_emails = self.all_emails
        else:
            filtered_emails = [email for email in self.all_emails if email[5] == filter_priority]

        self.display_emails(filtered_emails)

    def show_email_details(self, event):
        """Afficher les détails de l'email sélectionné"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        email_id = self.tree.item(selected_item[0])['values'][0]

        # Trouver l'email correspondant
        selected_email = None
        for email in self.all_emails:
            if email[0] == email_id:
                selected_email = email
                break

        if selected_email:
            details = f"Expéditeur: {selected_email[1]}\n\n"
            details += f"Sujet: {selected_email[2]}\n\n"
            details += f"Priorité: {selected_email[5]}\n\n"
            details += f"Date reçue: {selected_email[6]}\n\n"
            details += f"Contenu:\n{selected_email[3][:500]}..."

            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)

    def update_stats(self):
        """Mettre à jour les statistiques"""
        if not self.all_emails:
            self.stats_label.config(text="Aucun email traité")
            return

        total = len(self.all_emails)
        urgent = len([e for e in self.all_emails if e[5] == "URGENT"])
        haute = len([e for e in self.all_emails if e[5] == "HAUTE"])
        moyenne = len([e for e in self.all_emails if e[5] == "MOYENNE"])
        basse = len([e for e in self.all_emails if e[5] == "BASSE"])

        stats_text = f"Total: {total} emails | URGENT: {urgent} | HAUTE: {haute} | MOYENNE: {moyenne} | BASSE: {basse}"
        self.stats_label.config(text=stats_text)

    def refresh_emails(self):
        """Actualiser la liste des emails"""
        self.load_emails()
        messagebox.showinfo("Info", "Liste des emails actualisée")

    def process_new_emails(self):
        """Traiter de nouveaux emails en arrière-plan"""
        def process():
            try:
                # Ici vous devriez configurer vos identifiants
                EMAIL = "votre@email.com"
                PASSWORD = "votre_mot_de_passe"

                if self.classifier.process_emails(EMAIL, PASSWORD):
                    self.root.after(0, lambda: messagebox.showinfo("Succès", "Nouveaux emails traités!"))
                    self.root.after(0, self.load_emails)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Erreur", "Impossible de traiter les emails"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur: {e}"))

        threading.Thread(target=process, daemon=True).start()

def main():
    root = tk.Tk()
    app = EmailManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()