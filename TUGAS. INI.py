
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ================= KONEKSI DATABASE =================

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# ================= STRUKTUR 6 TABEL =================

TABLES = {
    "Dosen": {
        "table": "dosen",
        "pk": "nip",
        "columns": [
            "nip", "nama_dosen", "jenis_kelamin", "email",
            "no_telepon", "pendidikan_terakhir", "bidang_keahlian"
        ]
    },

    "Mahasiswa": {
        "table": "mahasiswa",
        "pk": "nim",
        "columns": [
            "nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir",
            "tempat_lahir", "alamat", "no_telepon", "email",
            "jurusan", "angkatan", "status"
        ]
    },

    "Jadwal Kuliah": {
        "table": "jadwal_kuliah",
        "pk": "id_jadwal",
        "columns": [
            "id_jadwal", "kode_mk", "hari", "jam_mulai",
            "jam_selesai", "ruangan"
        ]
    },

    "KRS": {
        "table": "krs",
        "pk": "id_krs",
        "columns": [
            "id_krs", "nim", "kode_mk", "semester_ambil",
            "tahun_ajaran", "nilai_huruf", "nilai_angka"
        ]
    },

    "Pembayaran UKT": {
        "table": "pembayaran_ukt",
        "pk": "id_pembayaran",
        "columns": [
            "id_pembayaran", "nim", "semester", "tahun_ajaran",
            "jumlah_bayar", "tanggal_bayar",
            "metode_pembayaran", "status"
        ]
    },

    "Mata Kuliah": {
        "table": "mata_kuliah",
        "pk": "kode_mk",
        "columns": [
            "kode_mk", "nama_mk", "sks", "semester", "nip_dosen"
        ]
    }
}


# ================= APLIKASI UTAMA =================

class SIAKAD:
    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD - Sistem Informasi Akademik")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)
        self.root.configure(bg="#f1f5f9")

        self.selected_table = None
        self.selected_pk = None
        self.entries = {}

        self.show_login()

    # ================= HALAMAN LOGIN =================

    def show_login(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="white",
                         padx=45, pady=35)
        frame.place(relx=0.5, rely=0.5,
                    anchor="center", width=390, height=430)

        tk.Label(
            frame, text="SIAKAD",
            font=("Arial", 27, "bold"),
            fg="#2563eb", bg="white"
        ).pack(pady=(15, 5))

        tk.Label(
            frame, text="Sistem Informasi Akademik",
            font=("Arial", 10),
            fg="#64748b", bg="white"
        ).pack(pady=(0, 25))

        tk.Label(
            frame, text="NIP DOSEN",
            bg="white", fg="#334155",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.nip_entry = tk.Entry(
            frame, font=("Arial", 11),
            relief="solid", bd=1
        )
        self.nip_entry.pack(fill="x", ipady=9, pady=(6, 17))

        tk.Label(
            frame, text="EMAIL",
            bg="white", fg="#334155",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.email_entry = tk.Entry(
            frame, font=("Arial", 11),
            relief="solid", bd=1
        )
        self.email_entry.pack(fill="x", ipady=9, pady=(6, 22))

        tk.Button(
            frame, text="MASUK",
            bg="#2563eb", fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2",
            command=self.login
        ).pack(fill="x", ipady=10)

        tk.Label(
            frame, text="© 2026 SIAKAD",
            bg="white", fg="#94a3b8",
            font=("Arial", 9)
        ).pack(pady=22)

    def login(self):
        nip = self.nip_entry.get().strip()
        email = self.email_entry.get().strip()

        if not nip or not email:
            messagebox.showwarning(
                "Peringatan", "NIP dan email harus diisi!"
            )
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "SELECT nip FROM dosen WHERE nip=%s AND email=%s",
                (nip, email)
            )

            user = cursor.fetchone()
            cursor.close()
            db.close()

            if user:
                self.show_dashboard()
            else:
                messagebox.showerror(
                    "Login Gagal",
                    "NIP atau email tidak sesuai!"
                )

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # ================= DASHBOARD =================

    def show_dashboard(self):
        self.clear_window()

        header = tk.Frame(self.root, bg="#1e3a8a", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="SIAKAD",
            bg="#1e3a8a", fg="white",
            font=("Arial", 22, "bold")
        ).pack(side="left", padx=25)

        tk.Label(
            header, text="Sistem Informasi Akademik",
            bg="#1e3a8a", fg="#dbeafe",
            font=("Arial", 10)
        ).pack(side="left", padx=5)

        tk.Button(
            header, text="Keluar",
            bg="#dc2626", fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            font=("Arial", 9, "bold"),
            relief="flat", cursor="hand2",
            command=self.logout
        ).pack(side="right", padx=20, pady=20)

        content = tk.Frame(self.root, bg="#f1f5f9")
        content.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(
            content, text="Dashboard SIAKAD",
            bg="#f1f5f9", fg="#0f172a",
            font=("Arial", 20, "bold")
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Silakan pilih menu data yang ingin dikelola.",
            bg="#f1f5f9", fg="#64748b",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(5, 25))

        menu_frame = tk.Frame(content, bg="#f1f5f9")
        menu_frame.pack(fill="both", expand=True)

        menus = [
            ("Data Dosen", "Dosen", "#2563eb"),
            ("Data Mahasiswa", "Mahasiswa", "#0891b2"),
            ("Jadwal Kuliah", "Jadwal Kuliah", "#7c3aed"),
            ("Data KRS", "KRS", "#059669"),
            ("Pembayaran UKT", "Pembayaran UKT", "#d97706"),
            ("Mata Kuliah", "Mata Kuliah", "#db2777")
        ]

        for i, (label, table_name, color) in enumerate(menus):
            row = i // 3
            col = i % 3

            menu_frame.grid_columnconfigure(col, weight=1)
            menu_frame.grid_rowconfigure(row, weight=1)

            card = tk.Frame(
                menu_frame, bg="white",
                highlightbackground="#e2e8f0",
                highlightthickness=1
            )
            card.grid(
                row=row, column=col,
                padx=10, pady=10,
                sticky="nsew"
            )

            tk.Label(
                card, text=label,
                bg="white", fg="#0f172a",
                font=("Arial", 13, "bold")
            ).pack(pady=(25, 15))

            tk.Button(
                card, text="Buka Data",
                bg=color, fg="white",
                activebackground=color,
                activeforeground="white",
                font=("Arial", 10, "bold"),
                relief="flat", cursor="hand2",
                command=lambda t=table_name: self.show_table(t)
            ).pack(pady=(0, 25), ipadx=20, ipady=7)

    # ================= HALAMAN DATA =================

    def show_table(self, table_name):
        self.selected_table = table_name
        self.selected_pk = None
        self.clear_window()
        self.entries = {}

        info = TABLES[table_name]
        columns = info["columns"]

        header = tk.Frame(self.root, bg="#1e3a8a", height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text=table_name,
            bg="#1e3a8a", fg="white",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=20)

        tk.Button(
            header, text="← Dashboard",
            bg="#334155", fg="white",
            relief="flat", cursor="hand2",
            command=self.show_dashboard
        ).pack(side="right", padx=20, pady=15)

        main = tk.Frame(self.root, bg="#f1f5f9")
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Form input
        form = tk.LabelFrame(
            main, text="Form Data",
            bg="white", fg="#1e293b",
            font=("Arial", 10, "bold"),
            padx=12, pady=10
        )
        form.pack(fill="x", pady=(0, 12))

        for i, col in enumerate(columns):
            row = i // 4
            position = i % 4

            form.grid_columnconfigure(position * 2 + 1, weight=1)

            tk.Label(
                form, text=col.replace("_", " ").title(),
                bg="white", fg="#334155",
                font=("Arial", 9)
            ).grid(
                row=row, column=position * 2,
                sticky="w", padx=(5, 5), pady=7
            )

            entry = tk.Entry(
                form, font=("Arial", 9),
                relief="solid", bd=1
            )
            entry.grid(
                row=row, column=position * 2 + 1,
                sticky="ew", padx=(0, 12), pady=7,
                ipady=5
            )

            self.entries[col] = entry

        # Tombol CRUD
        actions = tk.Frame(main, bg="#f1f5f9")
        actions.pack(fill="x", pady=(0, 10))

        buttons = [
            ("Tambah", "#16a34a", self.tambah_data),
            ("Edit", "#2563eb", self.edit_data),
            ("Hapus", "#dc2626", self.hapus_data),
            ("Bersihkan", "#64748b", self.clear_form),
            ("Refresh", "#0891b2", self.load_data)
        ]

        for label, color, command in buttons:
            tk.Button(
                actions, text=label,
                bg=color, fg="white",
                activebackground=color,
                activeforeground="white",
                font=("Arial", 9, "bold"),
                relief="flat", cursor="hand2",
                command=command
            ).pack(side="left", padx=4, ipadx=10, ipady=6)

        # Tabel data
        table_frame = tk.Frame(main, bg="white")
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=125, minwidth=90, anchor="center")

        scrollbar_y = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.tree.yview
        )
        scrollbar_x = ttk.Scrollbar(
            table_frame, orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        self.load_data()

    # ================= TAMPILKAN DATA =================

    def load_data(self):
        info = TABLES[self.selected_table]

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                f"SELECT * FROM {info['table']} ORDER BY {info['pk']}"
            )

            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:
                self.tree.insert("", "end", values=row)

            cursor.close()
            db.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # ================= PILIH DATA =================

    def select_item(self, event):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        columns = TABLES[self.selected_table]["columns"]

        self.selected_pk = values[
            columns.index(TABLES[self.selected_table]["pk"])
        ]

        for col, value in zip(columns, values):
            self.entries[col].delete(0, tk.END)
            self.entries[col].insert(0, value)

    # ================= TAMBAH DATA =================

    def tambah_data(self):
        info = TABLES[self.selected_table]
        columns = info["columns"]

        values = [
            self.entries[col].get().strip()
            for col in columns
        ]

        if any(value == "" for value in values):
            messagebox.showwarning(
                "Peringatan", "Semua kolom harus diisi!"
            )
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            col_sql = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))

            query = (
                f"INSERT INTO {info['table']} "
                f"({col_sql}) VALUES ({placeholders})"
            )

            cursor.execute(query, values)
            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo("Berhasil", "Data berhasil ditambahkan!")
            self.clear_form()
            self.load_data()

        except mysql.connector.Error as e:
            messagebox.showerror("Gagal Menambah Data", str(e))

    # ================= EDIT DATA =================

    def edit_data(self):
        if self.selected_pk is None:
            messagebox.showwarning(
                "Peringatan", "Pilih data yang ingin diedit!"
            )
            return

        info = TABLES[self.selected_table]
        columns = info["columns"]
        pk = info["pk"]

        values = [
            self.entries[col].get().strip()
            for col in columns
        ]

        if any(value == "" for value in values):
            messagebox.showwarning(
                "Peringatan", "Semua kolom harus diisi!"
            )
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            set_sql = ", ".join(
                [f"{col}=%s" for col in columns if col != pk]
            )

            update_values = [
                self.entries[col].get().strip()
                for col in columns if col != pk
            ]

            query = (
                f"UPDATE {info['table']} SET {set_sql} "
                f"WHERE {pk}=%s"
            )

            cursor.execute(
                query, update_values + [self.selected_pk]
            )
            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo("Berhasil", "Data berhasil diperbarui!")
            self.clear_form()
            self.load_data()

        except mysql.connector.Error as e:
            messagebox.showerror("Gagal Mengedit Data", str(e))

    # ================= HAPUS DATA =================

    def hapus_data(self):
        if self.selected_pk is None:
            messagebox.showwarning(
                "Peringatan", "Pilih data yang ingin dihapus!"
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi", "Yakin ingin menghapus data ini?"
        ):
            return

        info = TABLES[self.selected_table]

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                f"DELETE FROM {info['table']} WHERE {info['pk']}=%s",
                (self.selected_pk,)
            )

            db.commit()
            cursor.close()
            db.close()

            messagebox.showinfo("Berhasil", "Data berhasil dihapus!")
            self.clear_form()
            self.load_data()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Gagal Menghapus Data",
                "Data mungkin masih digunakan oleh tabel lain.\n\n" + str(e)
            )

    # ================= BERSIHKAN FORM =================

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.selected_pk = None

        if hasattr(self, "tree"):
            for item in self.tree.selection():
                self.tree.selection_remove(item)

    # ================= LOGOUT =================

    def logout(self):
        if messagebox.askyesno(
            "Konfirmasi Keluar",
            "Apakah kamu yakin ingin keluar dari aplikasi?"
        ):
            self.show_login()

    # ================= BERSIHKAN WINDOW =================

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ================= JALANKAN APLIKASI =================

if __name__ == "__main__":
    root = tk.Tk()
    app = SIAKAD(root)
    root.mainloop()
