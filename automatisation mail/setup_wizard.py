"""
Assistant de configuration initial pour le système de tri d'emails
Interface graphique pour simplifier la configuration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from business_questionnaire import BusinessQuestionnaire
from adaptive_classifier import AdaptiveEmailClassifier

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant de Configuration - Tri d'Emails")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.questionnaire = BusinessQuestionnaire()
        self.current_step = 0
        self.config = self.questionnaire.get_default_config()

        self.setup_ui()

    def setup_ui(self):
        """Interface utilisateur principale"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Titre principal
        title_label = ttk.Label(self.main_frame, text="Assistant de Configuration",
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame pour le contenu des étapes
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Frame pour les boutons de navigation
        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(fill=tk.X)

        self.prev_button = ttk.Button(self.nav_frame, text="← Précédent",
                                     command=self.previous_step, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = ttk.Button(self.nav_frame, text="Suivant →",
                                     command=self.next_step)
        self.next_button.pack(side=tk.RIGHT)

        # Barre de progression
        self.progress = ttk.Progressbar(self.main_frame, length=400, mode='determinate')
        self.progress.pack(pady=(10, 0))

        # Démarrer la première étape
        self.show_step()

    def show_step(self):
        """Afficher l'étape actuelle"""
        # Nettoyer le frame de contenu
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Mettre à jour la barre de progression
        self.progress['value'] = (self.current_step / 4) * 100

        # Afficher l'étape correspondante
        if self.current_step == 0:
            self.show_welcome()
        elif self.current_step == 1:
            self.show_company_info()
        elif self.current_step == 2:
            self.show_priority_config()
        elif self.current_step == 3:
            self.show_special_rules()
        elif self.current_step == 4:
            self.show_summary()

        # Gérer les boutons
        self.prev_button['state'] = tk.DISABLED if self.current_step == 0 else tk.NORMAL
        self.next_button['text'] = "Terminer" if self.current_step == 4 else "Suivant →"

    def show_welcome(self):
        """Étape 0: Bienvenue"""
        welcome_frame = ttk.LabelFrame(self.content_frame, text="Bienvenue", padding="20")
        welcome_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(welcome_frame, text="Configuration du Système de Tri d'Emails",
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))

        welcome_text = """
Cet assistant va configurer le système de tri automatique selon les besoins de votre entreprise.

Le processus comprend 4 étapes:

1. Informations sur votre entreprise
2. Configuration des priorités d'emails
3. Règles spéciales (VIP, blocages)
4. Validation et résumé

Durée estimée: 5-10 minutes
        """

        ttk.Label(welcome_frame, text=welcome_text, justify=tk.LEFT).pack()

        # Choix de configuration rapide
        ttk.Label(welcome_frame, text="Configuration rapide par secteur:",
                 font=("Arial", 10, "bold")).pack(pady=(20, 10))

        self.quick_setup_var = tk.StringVar(value="custom")
        quick_options = [
            ("Configuration personnalisée", "custom"),
            ("Conciergerie / Services", "conciergerie"),
            ("E-commerce", "ecommerce"),
            ("Santé / Médical", "healthcare"),
            ("Finance / Banque", "finance")
        ]

        for text, value in quick_options:
            ttk.Radiobutton(welcome_frame, text=text, variable=self.quick_setup_var,
                           value=value).pack(anchor=tk.W, padx=20)

    def show_company_info(self):
        """Étape 1: Informations entreprise"""
        info_frame = ttk.LabelFrame(self.content_frame, text="Informations Entreprise", padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True)

        # Nom de l'entreprise
        ttk.Label(info_frame, text="Nom de l'entreprise:").pack(anchor=tk.W)
        self.company_name = ttk.Entry(info_frame, width=50)
        self.company_name.pack(fill=tk.X, pady=(5, 15))

        # Secteur d'activité
        ttk.Label(info_frame, text="Secteur d'activité:").pack(anchor=tk.W)
        self.industry_var = tk.StringVar()
        industry_combo = ttk.Combobox(info_frame, textvariable=self.industry_var,
                                     values=["Conciergerie/Services", "E-commerce", "Santé/Médical",
                                            "Finance/Banque", "Immobilier", "Tech/IT", "Éducation", "Autre"])
        industry_combo.pack(fill=tk.X, pady=(5, 15))

        # Taille entreprise
        ttk.Label(info_frame, text="Taille de l'entreprise:").pack(anchor=tk.W)
        self.size_var = tk.StringVar()
        ttk.Radiobutton(info_frame, text="TPE (1-9 employés)", variable=self.size_var, value="tpe").pack(anchor=tk.W)
        ttk.Radiobutton(info_frame, text="PME (10-249 employés)", variable=self.size_var, value="pme").pack(anchor=tk.W)
        ttk.Radiobutton(info_frame, text="Grande entreprise (250+ employés)", variable=self.size_var, value="grande").pack(anchor=tk.W)

        # Volume d'emails
        ttk.Label(info_frame, text="Volume d'emails par jour:").pack(anchor=tk.W, pady=(15, 0))
        self.email_volume = ttk.Entry(info_frame, width=20)
        self.email_volume.pack(anchor=tk.W, pady=(5, 0))

    def show_priority_config(self):
        """Étape 2: Configuration des priorités"""
        priority_frame = ttk.LabelFrame(self.content_frame, text="Configuration des Priorités", padding="20")
        priority_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(priority_frame, text="Mots-clés pour chaque niveau de priorité:",
                 font=("Arial", 11, "bold")).pack(pady=(0, 15))

        self.priority_entries = {}
        priorities = [
            ("URGENT", "urgent", "Urgences, pannes, réclamations graves"),
            ("HAUTE", "high", "Nouvelles demandes, clients importants"),
            ("MOYENNE", "medium", "Questions, confirmations, informations"),
            ("BASSE", "low", "Newsletters, promotions, spam")
        ]

        for priority_label, priority_key, description in priorities:
            # Frame pour chaque priorité
            prio_frame = ttk.LabelFrame(priority_frame, text=f"{priority_label} - {description}", padding="10")
            prio_frame.pack(fill=tk.X, pady=(0, 10))

            ttk.Label(prio_frame, text="Mots-clés (séparés par des virgules):").pack(anchor=tk.W)
            entry = ttk.Entry(prio_frame, width=70)
            entry.pack(fill=tk.X, pady=(5, 0))
            self.priority_entries[priority_key] = entry

            # Pré-remplir selon le secteur choisi
            if hasattr(self, 'industry_var') and self.industry_var.get():
                self.prefill_keywords(priority_key, entry)

    def show_special_rules(self):
        """Étape 3: Règles spéciales"""
        rules_frame = ttk.LabelFrame(self.content_frame, text="Règles Spéciales", padding="20")
        rules_frame.pack(fill=tk.BOTH, expand=True)

        # Clients VIP
        vip_frame = ttk.LabelFrame(rules_frame, text="Clients VIP", padding="10")
        vip_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(vip_frame, text="Emails ou domaines de clients VIP (ex: @client-important.com):").pack(anchor=tk.W)
        self.vip_clients = ttk.Entry(vip_frame, width=70)
        self.vip_clients.pack(fill=tk.X, pady=(5, 0))

        # Expéditeurs bloqués
        blocked_frame = ttk.LabelFrame(rules_frame, text="Expéditeurs Bloqués", padding="10")
        blocked_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(blocked_frame, text="Expéditeurs à bloquer/marquer comme spam:").pack(anchor=tk.W)
        self.blocked_senders = ttk.Entry(blocked_frame, width=70)
        self.blocked_senders.pack(fill=tk.X, pady=(5, 0))

        # Horaires de travail
        hours_frame = ttk.LabelFrame(rules_frame, text="Horaires de Travail", padding="10")
        hours_frame.pack(fill=tk.X)

        hours_sub_frame = ttk.Frame(hours_frame)
        hours_sub_frame.pack(fill=tk.X)

        ttk.Label(hours_sub_frame, text="Début:").pack(side=tk.LEFT)
        self.start_time = ttk.Entry(hours_sub_frame, width=10)
        self.start_time.insert(0, "09:00")
        self.start_time.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(hours_sub_frame, text="Fin:").pack(side=tk.LEFT)
        self.end_time = ttk.Entry(hours_sub_frame, width=10)
        self.end_time.insert(0, "18:00")
        self.end_time.pack(side=tk.LEFT, padx=5)

    def show_summary(self):
        """Étape 4: Résumé et validation"""
        summary_frame = ttk.LabelFrame(self.content_frame, text="Résumé de la Configuration", padding="20")
        summary_frame.pack(fill=tk.BOTH, expand=True)

        # Collecter toutes les données
        self.collect_all_data()

        # Afficher le résumé
        summary_text = f"""
Entreprise: {self.config['company_info']['name']}
Secteur: {self.config['company_info']['industry']}
Taille: {self.config['company_info']['size']}
Volume d'emails/jour: {self.config['company_info']['email_volume']}

Horaires de travail: {self.config['business_hours']['start']} - {self.config['business_hours']['end']}

Clients VIP configurés: {len(self.config['special_rules']['vip_clients'])}
Expéditeurs bloqués: {len(self.config['special_rules']['blocked_senders'])}

Mots-clés par priorité:
"""

        for priority, rules in self.config['priority_rules'].items():
            keywords_count = len(rules['keywords'])
            summary_text += f"  {priority.upper()}: {keywords_count} mots-clés\n"

        summary_label = ttk.Label(summary_frame, text=summary_text, justify=tk.LEFT)
        summary_label.pack(anchor=tk.W)

        # Bouton de test
        test_button = ttk.Button(summary_frame, text="Tester la Configuration",
                                command=self.test_configuration)
        test_button.pack(pady=(20, 0))

    def prefill_keywords(self, priority_key, entry):
        """Pré-remplir les mots-clés selon le secteur"""
        industry_map = {
            "Conciergerie/Services": "conciergerie",
            "E-commerce": "ecommerce",
            "Santé/Médical": "healthcare",
            "Finance/Banque": "finance"
        }

        industry = industry_map.get(self.industry_var.get(), "conciergerie")
        keywords_dict = {
            "conciergerie": {
                "urgent": "urgent, urgence, panne, broken, réclamation, problème grave, incident",
                "high": "réservation, booking, nouveau client, demande, rdv, maintenance",
                "medium": "confirmation, information, question, facture, planning",
                "low": "newsletter, promo, marketing, publicité, spam"
            },
            "ecommerce": {
                "urgent": "fraude, chargeback, réclamation, retour urgent, problème paiement",
                "high": "nouvelle commande, paiement, livraison, stock, client vip",
                "medium": "question produit, suivi commande, disponibilité, sav",
                "low": "newsletter, catalogue, promotion, marketing"
            }
        }

        if industry in keywords_dict and priority_key in keywords_dict[industry]:
            entry.insert(0, keywords_dict[industry][priority_key])

    def collect_all_data(self):
        """Collecter toutes les données saisies"""
        # Informations entreprise
        self.config['company_info']['name'] = getattr(self, 'company_name', ttk.Entry(self.root)).get()
        self.config['company_info']['industry'] = getattr(self, 'industry_var', tk.StringVar()).get()
        self.config['company_info']['size'] = getattr(self, 'size_var', tk.StringVar()).get()
        self.config['company_info']['email_volume'] = getattr(self, 'email_volume', ttk.Entry(self.root)).get()

        # Priorités
        if hasattr(self, 'priority_entries'):
            for priority_key, entry in self.priority_entries.items():
                keywords_str = entry.get().strip()
                if keywords_str:
                    keywords = [k.strip().lower() for k in keywords_str.split(',')]
                    self.config['priority_rules'][priority_key]['keywords'] = keywords

        # Règles spéciales
        if hasattr(self, 'vip_clients'):
            vip_str = self.vip_clients.get().strip()
            if vip_str:
                self.config['special_rules']['vip_clients'] = [v.strip() for v in vip_str.split(',')]

        if hasattr(self, 'blocked_senders'):
            blocked_str = self.blocked_senders.get().strip()
            if blocked_str:
                self.config['special_rules']['blocked_senders'] = [b.strip() for b in blocked_str.split(',')]

        # Horaires
        if hasattr(self, 'start_time'):
            self.config['business_hours']['start'] = self.start_time.get()
        if hasattr(self, 'end_time'):
            self.config['business_hours']['end'] = self.end_time.get()

    def test_configuration(self):
        """Tester la configuration avec des emails d'exemple"""
        test_emails = [
            ("urgent@client.com", "URGENT - Problème grave", "Nous avons un problème urgent"),
            ("nouveau@client.fr", "Demande de réservation", "Je souhaite faire une réservation"),
            ("info@newsletter.com", "Offres spéciales", "Découvrez nos promotions"),
            ("admin@system.com", "Confirmation intervention", "Intervention programmée demain")
        ]

        # Sauvegarder temporairement la config
        temp_file = "temp_config.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

        # Tester
        classifier = AdaptiveEmailClassifier(temp_file)
        results = []

        for sender, subject, body in test_emails:
            priority_num, priority_label = classifier.classify_email_priority(subject, sender, body)
            results.append(f"{subject} → {priority_label}")

        # Nettoyer
        import os
        os.remove(temp_file)

        # Afficher les résultats
        result_text = "Résultats du test:\n\n" + "\n".join(results)
        messagebox.showinfo("Test de Configuration", result_text)

    def next_step(self):
        """Passer à l'étape suivante"""
        if self.current_step < 4:
            self.current_step += 1
            self.show_step()
        else:
            # Terminer la configuration
            self.finish_setup()

    def previous_step(self):
        """Revenir à l'étape précédente"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()

    def finish_setup(self):
        """Terminer la configuration"""
        self.collect_all_data()

        # Sauvegarder la configuration
        self.questionnaire.save_config(self.config)

        messagebox.showinfo("Configuration Terminée",
                           "La configuration a été sauvegardée avec succès!\n\n"
                           "Vous pouvez maintenant utiliser le système de tri d'emails.\n"
                           "Lancez 'python interface.py' pour commencer.")

        self.root.quit()

def main():
    root = tk.Tk()
    wizard = SetupWizard(root)
    root.mainloop()

if __name__ == "__main__":
    main()