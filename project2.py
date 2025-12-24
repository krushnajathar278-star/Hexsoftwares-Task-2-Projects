# modern_rent_calculator.py
# pip install customtkinter

import customtkinter as ctk
from tkinter import messagebox

# ------------------ APP CONFIG ------------------ #

ctk.set_appearance_mode("dark")          # "dark" or "light"
ctk.set_default_color_theme("blue")      # "blue", "green", "dark-blue", or custom

class RentCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window
        self.title("Modern Rent Calculator")
        self.geometry("900x520")
        self.minsize(850, 500)

        # Grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # UI
        self._create_header()
        self._create_left_panel()
        self._create_right_panel()
        self._create_footer()

    # ------------------ UI SECTIONS ------------------ #

    def _create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        title = ctk.CTkLabel(
            header,
            text="Rent & Utilities Splitter",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Calculate total cost and split it fairly between roommates.",
            font=ctk.CTkFont(size=13)
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.theme_button = ctk.CTkSegmentedButton(
            header,
            values=["Dark", "Light"],
            command=self._toggle_theme
        )
        self.theme_button.set("Dark")
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e")

    def _create_left_panel(self):
        left = ctk.CTkFrame(self, corner_radius=18)
        left.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(5, 10))
        left.grid_columnconfigure(0, weight=1)

        # Section title
        section_label = ctk.CTkLabel(
            left,
            text="Inputs",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        # ---- Rent & Food card ----
        rent_card = ctk.CTkFrame(left, corner_radius=14)
        rent_card.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 12))
        rent_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            rent_card, text="Base Costs", font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 4))

        self.rent_entry = self._labeled_entry(
            parent=rent_card,
            row=1,
            col=0,
            label="Monthly Rent (₹)",
            placeholder="e.g. 18000"
        )
        self.food_entry = self._labeled_entry(
            parent=rent_card,
            row=1,
            col=1,
            label="Food / Groceries (₹ / month)",
            placeholder="e.g. 6000"
        )

        # ---- Electricity card ----
        elec_card = ctk.CTkFrame(left, corner_radius=14)
        elec_card.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 12))
        elec_card.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            elec_card, text="Electricity", font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(12, 4))

        self.units_entry = self._labeled_entry(
            parent=elec_card,
            row=1,
            col=0,
            label="Units Used",
            placeholder="e.g. 180"
        )
        self.rate_entry = self._labeled_entry(
            parent=elec_card,
            row=1,
            col=1,
            label="Rate per Unit (₹)",
            placeholder="e.g. 8"
        )
        self.fixed_elec_entry = self._labeled_entry(
            parent=elec_card,
            row=1,
            col=2,
            label="Fixed Elec. Charge (₹)",
            placeholder="0 if none"
        )

        # ---- Period & People card ----
        other_card = ctk.CTkFrame(left, corner_radius=14)
        other_card.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 12))
        other_card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            other_card, text="Period & Roommates", font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 4))

        self.months_entry = self._labeled_entry(
            parent=other_card,
            row=1,
            col=0,
            label="Number of Months",
            placeholder="1"
        )
        self.persons_entry = self._labeled_entry(
            parent=other_card,
            row=1,
            col=1,
            label="Number of Persons",
            placeholder="2"
        )

        # ---- Buttons ----
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 15))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        calc_btn = ctk.CTkButton(
            btn_frame,
            text="Calculate",
            corner_radius=20,
            height=38,
            command=self._on_calculate
        )
        calc_btn.grid(row=0, column=0, padx=(0, 7), pady=(5, 0), sticky="ew")

        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear",
            corner_radius=20,
            height=38,
            fg_color="#444444",
            hover_color="#555555",
            command=self._on_clear
        )
        clear_btn.grid(row=0, column=1, padx=(7, 0), pady=(5, 0), sticky="ew")

    def _create_right_panel(self):
        right = ctk.CTkFrame(self, corner_radius=18)
        right.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(5, 10))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        # Section header
        ctk.CTkLabel(
            right,
            text="Summary",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        # High-level numbers
        top_card = ctk.CTkFrame(right, corner_radius=14)
        top_card.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        top_card.grid_columnconfigure((0, 1), weight=1)

        self.total_monthly_label = ctk.CTkLabel(
            top_card,
            text="Total Monthly: ₹0",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.total_monthly_label.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 4))

        self.total_period_label = ctk.CTkLabel(
            top_card,
            text="Total for Period: ₹0",
            font=ctk.CTkFont(size=14)
        )
        self.total_period_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 12))

        self.per_person_monthly_label = ctk.CTkLabel(
            top_card,
            text="Per Person / Month: ₹0",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.per_person_monthly_label.grid(row=0, column=1, sticky="e", padx=15, pady=(12, 4))

        self.per_person_total_label = ctk.CTkLabel(
            top_card,
            text="Per Person Total: ₹0",
            font=ctk.CTkFont(size=14)
        )
        self.per_person_total_label.grid(row=1, column=1, sticky="e", padx=15, pady=(0, 12))

        # Detailed breakdown card
        detail_card = ctk.CTkFrame(right, corner_radius=14)
        detail_card.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 10))
        detail_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            detail_card,
            text="Breakdown",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 4))

        self.breakdown_text = ctk.CTkTextbox(
            detail_card,
            height=180,
            wrap="word",
            activate_scrollbars=True
        )
        self.breakdown_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 12))
        self.breakdown_text.configure(state="disabled")

        self._set_breakdown("Enter values on the left and click Calculate.")

    def _create_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=0)

        tip = ctk.CTkLabel(
            footer,
            text="Tip: Keep rents fair by using the per-person monthly value. You can export or connect this to a DB later.",
            font=ctk.CTkFont(size=11)
        )
        tip.grid(row=0, column=0, sticky="w")

        credit = ctk.CTkLabel(
            footer,
            text="Modern UI using CustomTkinter",
            font=ctk.CTkFont(size=11, slant="italic")
        )
        credit.grid(row=0, column=1, sticky="e")

    # ------------------ HELPERS ------------------ #

    def _labeled_entry(self, parent, row, col, label, placeholder=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, sticky="ew", padx=10, pady=(4, 10))
        frame.grid_columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(frame, text=label, anchor="w")
        lbl.grid(row=0, column=0, sticky="w")

        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        return entry

    def _toggle_theme(self, value):
        ctk.set_appearance_mode("dark" if value == "Dark" else "light")

    def _set_breakdown(self, text: str):
        self.breakdown_text.configure(state="normal")
        self.breakdown_text.delete("1.0", "end")
        self.breakdown_text.insert("1.0", text)
        self.breakdown_text.configure(state="disabled")

    # ------------------ LOGIC ------------------ #

    def _get_float(self, entry, default=0.0):
        val = entry.get().strip()
        if val == "":
            return default
        return float(val)

    def _get_int(self, entry, default=1):
        val = entry.get().strip()
        if val == "":
            return default
        return int(val)

    def _on_clear(self):
        for e in [
            self.rent_entry,
            self.food_entry,
            self.units_entry,
            self.rate_entry,
            self.fixed_elec_entry,
            self.months_entry,
            self.persons_entry,
        ]:
            e.delete(0, "end")

        self.total_monthly_label.configure(text="Total Monthly: ₹0")
        self.total_period_label.configure(text="Total for Period: ₹0")
        self.per_person_monthly_label.configure(text="Per Person / Month: ₹0")
        self.per_person_total_label.configure(text="Per Person Total: ₹0")
        self._set_breakdown("Inputs cleared. Enter new values and click Calculate.")

    def _on_calculate(self):
        try:
            rent = self._get_float(self.rent_entry, 0.0)
            food = self._get_float(self.food_entry, 0.0)
            units = self._get_float(self.units_entry, 0.0)
            rate = self._get_float(self.rate_entry, 0.0)
            fixed_elec = self._get_float(self.fixed_elec_entry, 0.0)
            months = self._get_int(self.months_entry, 1)
            persons = self._get_int(self.persons_entry, 1)

            if months <= 0 or persons <= 0:
                raise ValueError("Months and persons must be greater than 0.")

            electricity = units * rate + fixed_elec
            total_monthly = rent + food + electricity
            total_period = total_monthly * months

            per_person_monthly = total_monthly / persons
            per_person_total = total_period / persons

            # Update high-level labels
            self.total_monthly_label.configure(
                text=f"Total Monthly: ₹{total_monthly:,.2f}"
            )
            self.total_period_label.configure(
                text=f"Total for Period: ₹{total_period:,.2f} (for {months} month{'s' if months > 1 else ''})"
            )
            self.per_person_monthly_label.configure(
                text=f"Per Person / Month: ₹{per_person_monthly:,.2f} (for {persons} person{'s' if persons > 1 else ''})"
            )
            self.per_person_total_label.configure(
                text=f"Per Person Total: ₹{per_person_total:,.2f}"
            )

            breakdown = (
                f"➤ Inputs\n"
                f"   • Rent (monthly): ₹{rent:,.2f}\n"
                f"   • Food / Groceries (monthly): ₹{food:,.2f}\n"
                f"   • Electricity: units = {units:,.2f}, rate = ₹{rate:,.2f}, fixed = ₹{fixed_elec:,.2f}\n"
                f"   • Months: {months}\n"
                f"   • Persons: {persons}\n\n"
                f"➤ Calculations\n"
                f"   • Electricity bill / month = ₹{electricity:,.2f}\n"
                f"   • Total monthly cost = ₹{total_monthly:,.2f}\n"
                f"   • Total for period = ₹{total_period:,.2f}\n"
                f"   • Per person / month = ₹{per_person_monthly:,.2f}\n"
                f"   • Per person total = ₹{per_person_total:,.2f}\n"
            )
            self._set_breakdown(breakdown)

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid numbers.\n\nDetails: {e}")

# ------------------ MAIN ------------------ #

if __name__ == "__main__":
    app = RentCalculatorApp()
    app.mainloop()
