"""
Main GUI application for SoloCraft.
Built with Tkinter for desktop application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from data_models import Mission, InsightDebt, UserProgress, Difficulty
from storage_manager import StorageManager


class SoloCraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SoloCraft - Independent Project Builder")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize storage manager
        self.storage = StorageManager()
        
        # Load user progress
        self.user_progress = self.storage.load_user_progress()
        
        # Check if tickets need reset
        if self.user_progress.should_reset_tickets():
            self.user_progress.reset_tickets()
            self.storage.save_user_progress(self.user_progress)
            messagebox.showinfo("Tickets Reset", "Your weekly tickets have been reset!")
        
        self.setup_ui()
        self.refresh_all_displays()

    def setup_ui(self):
        """Set up the main user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header with user stats
        self.setup_header(main_frame)
        
        # Left panel - Mission management
        self.setup_mission_panel(main_frame)
        
        # Right panel - Tickets and Insight Debt
        self.setup_tickets_panel(main_frame)

    def setup_header(self, parent):
        """Set up the header with user statistics."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="we", pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="SoloCraft", font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # User stats
        stats_frame = ttk.Frame(header_frame)
        stats_frame.grid(row=0, column=1, sticky=tk.E)
        
        self.xp_label = ttk.Label(stats_frame, text="XP: 0", font=("Arial", 12))
        self.xp_label.grid(row=0, column=0, padx=10)
        
        self.level_label = ttk.Label(stats_frame, text="Level: 1", font=("Arial", 12))
        self.level_label.grid(row=0, column=1, padx=10)
        
        self.help_tickets_label = ttk.Label(stats_frame, text="Help Tickets: 3", font=("Arial", 12))
        self.help_tickets_label.grid(row=0, column=2, padx=10)
        
        self.tutorial_tickets_label = ttk.Label(stats_frame, text="Tutorial Tickets: 2", font=("Arial", 12))
        self.tutorial_tickets_label.grid(row=0, column=3, padx=10)

    def setup_mission_panel(self, parent):
        """Set up the mission management panel."""
        mission_frame = ttk.LabelFrame(parent, text="Missions", padding="5")
        mission_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        mission_frame.grid_rowconfigure(1, weight=1)
        mission_frame.grid_columnconfigure(0, weight=1)
        
        # Mission buttons
        button_frame = ttk.Frame(mission_frame)
        button_frame.grid(row=0, column=0, sticky="we", pady=(0, 5))
        
        ttk.Button(button_frame, text="Create Mission", command=self.create_mission).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Complete Mission", command=self.complete_mission).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Mission", command=self.delete_mission).grid(row=0, column=2, padx=5)
        
        # Mission list
        self.mission_tree = ttk.Treeview(mission_frame, columns=("title", "difficulty", "rewards", "status"), show="headings")
        self.mission_tree.grid(row=1, column=0, sticky="nsew")
        
        # Configure columns
        self.mission_tree.heading("title", text="Title")
        self.mission_tree.heading("difficulty", text="Difficulty")
        self.mission_tree.heading("rewards", text="XP Reward")
        self.mission_tree.heading("status", text="Status")
        
        self.mission_tree.column("title", width=200)
        self.mission_tree.column("difficulty", width=80)
        self.mission_tree.column("rewards", width=80)
        self.mission_tree.column("status", width=100)
        
        # Scrollbar for mission list
        mission_scrollbar = ttk.Scrollbar(mission_frame, orient=tk.VERTICAL, command=self.mission_tree.yview)
        mission_scrollbar.grid(row=1, column=1, sticky="ns")
        self.mission_tree.configure(yscrollcommand=mission_scrollbar.set)

    def setup_tickets_panel(self, parent):
        """Set up the tickets and insight debt panel."""
        right_frame = ttk.Frame(parent)
        right_frame.grid(row=1, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Ticket usage frame
        ticket_frame = ttk.LabelFrame(right_frame, text="Use Tickets", padding="5")
        ticket_frame.grid(row=0, column=0, sticky="we", pady=(0, 5))
        ticket_frame.grid_columnconfigure(0, weight=1)
        
        button_frame = ttk.Frame(ticket_frame)
        button_frame.grid(row=0, column=0, pady=5)
        
        ttk.Button(button_frame, text="Use Help Ticket", command=self.use_help_ticket).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Use Tutorial Ticket", command=self.use_tutorial_ticket).grid(row=0, column=1, padx=5)
        
        # Insight debt frame
        debt_frame = ttk.LabelFrame(right_frame, text="Insight Debt", padding="5")
        debt_frame.grid(row=1, column=0, sticky="nsew")
        debt_frame.grid_rowconfigure(1, weight=1)
        debt_frame.grid_columnconfigure(0, weight=1)
        
        # Debt buttons
        debt_button_frame = ttk.Frame(debt_frame)
        debt_button_frame.grid(row=0, column=0, sticky="we", pady=(0, 5))
        
        ttk.Button(debt_button_frame, text="Write Insight", command=self.write_insight).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(debt_button_frame, text="View Insights", command=self.view_insights).grid(row=0, column=1, padx=5)
        
        # Debt list
        self.debt_tree = ttk.Treeview(debt_frame, columns=("type", "used_for", "status"), show="headings")
        self.debt_tree.grid(row=1, column=0, sticky="nsew")
        
        # Configure debt columns
        self.debt_tree.heading("type", text="Ticket Type")
        self.debt_tree.heading("used_for", text="Used For")
        self.debt_tree.heading("status", text="Status")
        
        self.debt_tree.column("type", width=100)
        self.debt_tree.column("used_for", width=150)
        self.debt_tree.column("status", width=80)
        
        # Scrollbar for debt list
        debt_scrollbar = ttk.Scrollbar(debt_frame, orient=tk.VERTICAL, command=self.debt_tree.yview)
        debt_scrollbar.grid(row=1, column=1, sticky="ns")
        self.debt_tree.configure(yscrollcommand=debt_scrollbar.set)

    def refresh_all_displays(self):
        """Refresh all UI displays with current data."""
        self.refresh_header()
        self.refresh_missions()
        self.refresh_debt()

    def refresh_header(self):
        """Update header statistics."""
        self.xp_label.config(text=f"XP: {self.user_progress.xp}")
        self.level_label.config(text=f"Level: {self.user_progress.level}")
        self.help_tickets_label.config(text=f"Help Tickets: {self.user_progress.help_tickets}")
        self.tutorial_tickets_label.config(text=f"Tutorial Tickets: {self.user_progress.tutorial_tickets}")

    def refresh_missions(self):
        """Refresh the mission list display."""
        # Clear existing items
        for item in self.mission_tree.get_children():
            self.mission_tree.delete(item)
        
        # Load and display missions
        missions = self.storage.load_missions()
        for mission in missions:
            status = "Completed" if mission.completed else "Active"
            self.mission_tree.insert("", "end", values=(
                mission.title,
                mission.difficulty,
                mission.rewards,
                status
            ), tags=(mission.id,))

    def refresh_debt(self):
        """Refresh the insight debt list display."""
        # Clear existing items
        for item in self.debt_tree.get_children():
            self.debt_tree.delete(item)
        
        # Load and display active debts
        debts = self.storage.get_active_debts()
        for debt in debts:
            self.debt_tree.insert("", "end", values=(
                debt.ticket_type,
                debt.used_for,
                "Outstanding"
            ), tags=(debt.id,))

    def create_mission(self):
        """Open dialog to create a new mission."""
        dialog = MissionCreateDialog(self.root, self)
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            mission = Mission(**dialog.result)
            self.storage.save_mission(mission)
            self.refresh_missions()
            messagebox.showinfo("Success", "Mission created successfully!")

    def complete_mission(self):
        """Complete the selected mission."""
        selection = self.mission_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a mission to complete.")
            return
        
        # Get mission ID from tags
        item_tags = self.mission_tree.item(selection[0])['tags']
        if not item_tags:
            return
        
        mission_id = item_tags[0]
        missions = self.storage.load_missions()
        
        for mission in missions:
            if mission.id == mission_id and not mission.completed:
                mission.complete_mission()
                self.storage.save_mission(mission)
                
                # Award XP
                level_up = self.user_progress.add_xp(mission.rewards)
                self.storage.save_user_progress(self.user_progress)
                
                msg = f"Mission completed! You earned {mission.rewards} XP."
                if level_up:
                    msg += f" You leveled up to Level {self.user_progress.level}!"
                
                messagebox.showinfo("Mission Completed", msg)
                self.refresh_all_displays()
                return
        
        messagebox.showwarning("Cannot Complete", "Mission is already completed or not found.")

    def delete_mission(self):
        """Delete the selected mission."""
        selection = self.mission_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a mission to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this mission?"):
            item_tags = self.mission_tree.item(selection[0])['tags']
            if item_tags:
                mission_id = item_tags[0]
                self.storage.delete_mission(mission_id)
                self.refresh_missions()
                messagebox.showinfo("Success", "Mission deleted successfully!")

    def use_help_ticket(self):
        """Use a help ticket and create insight debt."""
        if self.user_progress.help_tickets <= 0:
            messagebox.showwarning("No Tickets", "You have no help tickets remaining.")
            return
        
        purpose = simpledialog.askstring("Use Help Ticket", "What do you need help with?")
        if purpose:
            self.user_progress.use_help_ticket()
            self.storage.save_user_progress(self.user_progress)
            
            debt = InsightDebt("Help", purpose)
            self.storage.save_insight_debt(debt)
            
            self.refresh_all_displays()
            messagebox.showinfo("Ticket Used", "Help ticket used! You now have an insight debt to clear.")

    def use_tutorial_ticket(self):
        """Use a tutorial ticket and create insight debt."""
        if self.user_progress.tutorial_tickets <= 0:
            messagebox.showwarning("No Tickets", "You have no tutorial tickets remaining.")
            return
        
        purpose = simpledialog.askstring("Use Tutorial Ticket", "What tutorial do you need?")
        if purpose:
            self.user_progress.use_tutorial_ticket()
            self.storage.save_user_progress(self.user_progress)
            
            debt = InsightDebt("Tutorial", purpose)
            self.storage.save_insight_debt(debt)
            
            self.refresh_all_displays()
            messagebox.showinfo("Ticket Used", "Tutorial ticket used! You now have an insight debt to clear.")

    def write_insight(self):
        """Open dialog to write insight and clear debt."""
        debts = self.storage.get_active_debts()
        if not debts:
            messagebox.showinfo("No Debts", "You have no outstanding insight debts!")
            return
        
        # Let user select which debt to clear
        debt_options = [f"{debt.ticket_type} - {debt.used_for}" for debt in debts]
        
        dialog = InsightWriteDialog(self.root, debt_options, debts)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            selected_debt, insight_text = dialog.result
            selected_debt.clear_debt(insight_text)
            self.storage.save_insight_debt(selected_debt)
            
            self.refresh_debt()
            messagebox.showinfo("Insight Recorded", "Your insight has been recorded and the debt cleared!")

    def view_insights(self):
        """View all recorded insights."""
        debts = self.storage.get_cleared_debts()
        if not debts:
            messagebox.showinfo("No Insights", "You haven't recorded any insights yet.")
            return
        
        # Create a new window to display insights
        insight_window = tk.Toplevel(self.root)
        insight_window.title("Your Insights")
        insight_window.geometry("600x500")
        
        text_area = scrolledtext.ScrolledText(insight_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for debt in debts:
            text_area.insert(tk.END, f"=== {debt.ticket_type} Ticket - {debt.used_for} ===\n")
            text_area.insert(tk.END, f"Cleared on: {debt.cleared_at}\n\n")
            text_area.insert(tk.END, f"{debt.insight_entry}\n\n")
            text_area.insert(tk.END, "-" * 50 + "\n\n")
        
        text_area.config(state=tk.DISABLED)


class MissionCreateDialog:
    def __init__(self, parent, app):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Mission")
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the mission creation dialog."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Mission Title:").pack(anchor=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        ttk.Label(main_frame, text="Description:").pack(anchor=tk.W, pady=(0, 5))
        self.description_text = tk.Text(main_frame, height=5, width=40)
        self.description_text.pack(fill=tk.X, pady=(0, 10))
        
        # Difficulty
        ttk.Label(main_frame, text="Difficulty:").pack(anchor=tk.W, pady=(0, 5))
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_frame = ttk.Frame(main_frame)
        difficulty_frame.pack(fill=tk.X, pady=(0, 10))
        
        for difficulty in ["Easy", "Medium", "Hard"]:
            ttk.Radiobutton(difficulty_frame, text=difficulty, variable=self.difficulty_var, 
                           value=difficulty).pack(side=tk.LEFT, padx=(0, 10))
        
        # Constraints
        ttk.Label(main_frame, text="Constraints (e.g., max 2 help tickets):").pack(anchor=tk.W, pady=(0, 5))
        self.constraints_entry = ttk.Entry(main_frame, width=40)
        self.constraints_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Rewards
        ttk.Label(main_frame, text="XP Reward:").pack(anchor=tk.W, pady=(0, 5))
        self.rewards_var = tk.IntVar(value=50)
        rewards_frame = ttk.Frame(main_frame)
        rewards_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Spinbox(rewards_frame, from_=10, to=500, textvariable=self.rewards_var, width=10).pack(side=tk.LEFT)
        
        # Punishment (optional)
        ttk.Label(main_frame, text="Punishment (optional):").pack(anchor=tk.W, pady=(0, 5))
        self.punishment_entry = ttk.Entry(main_frame, width=40)
        self.punishment_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Create", command=self.create_mission).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)

    def create_mission(self):
        """Create the mission with entered data."""
        title = self.title_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not title or not description:
            messagebox.showwarning("Missing Information", "Please fill in title and description.")
            return
        
        self.result = {
            'title': title,
            'description': description,
            'difficulty': self.difficulty_var.get(),
            'constraints': self.constraints_entry.get().strip(),
            'rewards': self.rewards_var.get(),
            'punishment': self.punishment_entry.get().strip() or None
        }
        
        self.dialog.destroy()


class InsightWriteDialog:
    def __init__(self, parent, debt_options, debts):
        self.result = None
        self.debts = debts
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Write Insight Entry")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog(debt_options)

    def setup_dialog(self, debt_options):
        """Set up the insight writing dialog."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Debt selection
        ttk.Label(main_frame, text="Select debt to clear:").pack(anchor=tk.W, pady=(0, 5))
        self.debt_var = tk.StringVar(value=debt_options[0] if debt_options else "")
        debt_combo = ttk.Combobox(main_frame, textvariable=self.debt_var, values=debt_options, 
                                 state="readonly", width=50)
        debt_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Insight entry
        ttk.Label(main_frame, text="Write your insight:").pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(main_frame, text="What did you learn? How will you apply this knowledge?", 
                 font=("Arial", 9, "italic")).pack(anchor=tk.W, pady=(0, 5))
        
        self.insight_text = scrolledtext.ScrolledText(main_frame, height=15, width=50)
        self.insight_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save Insight", command=self.save_insight).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)

    def save_insight(self):
        """Save the insight entry."""
        insight_text = self.insight_text.get("1.0", tk.END).strip()
        
        if not insight_text:
            messagebox.showwarning("Empty Insight", "Please write your insight before saving.")
            return
        
        # Find selected debt
        selected_option = self.debt_var.get()
        debt_index = 0
        
        for i, debt in enumerate(self.debts):
            if f"{debt.ticket_type} - {debt.used_for}" == selected_option:
                debt_index = i
                break
        
        self.result = (self.debts[debt_index], insight_text)
        self.dialog.destroy()


def main():
    """Main entry point for the SoloCraft application."""
    root = tk.Tk()
    app = SoloCraftApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()