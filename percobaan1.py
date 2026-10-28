
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ==========================================
# KONFIGURASI WARNA
# ==========================================
BG = "#F3F6FC"
PRIMARY = "#1E3A8A"
BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
DARK = "#1E293B"
WHITE = "#FFFFFF"
GRAY = "#64748B"


# ==========================================
# KONEKSI DATABASE
# ==========================================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# ==========================================
# APLIKASI LOGIN
# ==========================================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD | Login")
        self.root.geometry("850x520")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.buat_tampilan()

    def buat_tampilan(self):
        # Panel kiri
        left = tk.Frame(self.root, bg=PRIMARY, width=340)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(
            left, text="SIAKAD",
            font=("Arial", 29, "bold"),
            bg=PRIMARY, fg=WHITE
        ).pack(pady=(110, 10))

        tk.Label(
            left,
            text="Sistem Informasi\nAkademik",
            font=("Arial", 16),
            bg=PRIMARY, fg=WHITE,
            justify="center"
        ).pack(pady=10)

        tk.Label(
            left,
            text="Pengelolaan Data Dosen\nLebih Mudah dan Teratur",
            font=("Arial", 10),
            bg=PRIMARY, fg="#CBD5E1",
            justify="center"
        ).pack(pady=20)

        # Panel kanan
        right = tk.Frame(self.root, bg=WHITE)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            right, text="Selamat Datang!",
            font=("Arial", 23, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", padx=55, pady=(85, 5))

        tk.Label(
            right,
            text="Silakan login untuk masuk ke aplikasi.",
            font=("Arial", 10),
            bg=WHITE, fg=GRAY
        ).pack(anchor="w", padx=55, pady=(0, 25))

        tk.Label(
            right, text="Username (NIP)",
            font=("Arial", 10, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", padx=55)

        self.entry_nip = tk.Entry(
            right, font=("Arial", 11),
            relief="solid", bd=1
        )
        self.entry_nip.pack(
            fill="x", padx=55, pady=(7, 17), ipady=8
        )

        tk.Label(
            right, text="Password (Email)",
            font=("Arial", 10, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", padx=55)

        self.entry_password = tk.Entry(
            right, font=("Arial", 11),
            show="*", relief="solid", bd=1
        )
        self.entry_password.pack(
            fill="x", padx=55, pady=(7, 20), ipady=8
        )

        tk.Button(
            right, text="LOGIN",
            font=("Arial", 11, "bold"),
            bg=BLUE, fg=WHITE,
            activebackground=PRIMARY,
            activeforeground=WHITE,
            relief="flat", cursor="hand2",
            command=self.proses_login
        ).pack(fill="x", padx=55, ipady=8)

        tk.Button(
            right, text="Keluar Aplikasi",
            font=("Arial", 9),
            bg=WHITE, fg=RED,
            activebackground="#FEE2E2",
            relief="flat", cursor="hand2",
            command=self.keluar
        ).pack(pady=12)

        self.entry_nip.focus()
        self.root.bind(
            "<Return>", lambda event: self.proses_login()
        )

    def proses_login(self):
        nip = self.entry_nip.get().strip()
        password = self.entry_password.get().strip()

        if not nip or not password:
            messagebox.showwarning(
                "Peringatan",
                "NIP dan password wajib diisi!"
            )
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT nip, nama_dosen, email
                FROM dosen
                WHERE nip = %s AND email = %s
            """
            cursor.execute(query, (nip, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo(
                    "Login Berhasil",
                    f"Selamat datang, {user['nama_dosen']}!"
                )

                self.root.unbind("<Return>")

                for widget in self.root.winfo_children():
                    widget.destroy()

                Dashboard(self.root, user)

            else:
                messagebox.showerror(
                    "Login Gagal",
                    "NIP atau password tidak sesuai!"
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Tidak dapat mengakses database:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def keluar(self):
        if messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin keluar dari aplikasi?"
        ):
            self.root.destroy()


# ==========================================
# DASHBOARD DATA DOSEN
# ==========================================
class Dashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.root.title("SIAKAD | Dashboard Data Dosen")
        self.root.geometry("1120x680")
        self.root.minsize(900, 580)
        self.root.configure(bg=BG)

        self.buat_tampilan()
        self.load_data()

    def buat_tampilan(self):
        # Header utama
        header = tk.Frame(self.root, bg=PRIMARY, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="SIAKAD",
            font=("Arial", 21, "bold"),
            bg=PRIMARY, fg=WHITE
        ).pack(side="left", padx=25)

        tk.Label(
            header,
            text=f"Login: {self.user['nama_dosen']}",
            font=("Arial", 10),
            bg=PRIMARY, fg=WHITE
        ).pack(side="right", padx=25)

        # Judul halaman
        title_frame = tk.Frame(self.root, bg=BG)
        title_frame.pack(fill="x", padx=22, pady=(18, 10))

        tk.Label(
            title_frame, text="Dashboard Data Dosen",
            font=("Arial", 20, "bold"),
            bg=BG, fg=DARK
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Kelola informasi dosen melalui satu halaman.",
            font=("Arial", 10),
            bg=BG, fg=GRAY
        ).pack(anchor="w", pady=(4, 0))

        # Form
        form = tk.LabelFrame(
            self.root,
            text="  FORM DATA DOSEN  ",
            font=("Arial", 10, "bold"),
            bg=WHITE, fg=PRIMARY,
            padx=15, pady=12
        )
        form.pack(fill="x", padx=22, pady=8)

        self.entry_nip = self.buat_entry(
            form, "NIP", 0, 0
        )
        self.entry_nama = self.buat_entry(
            form, "Nama Dosen", 0, 2
        )

        tk.Label(
            form, text="Jenis Kelamin",
            bg=WHITE, fg=DARK
        ).grid(row=1, column=0, sticky="w", pady=7)

        self.combo_jk = ttk.Combobox(
            form,
            values=["Laki-laki", "Perempuan"],
            state="readonly",
            font=("Arial", 10)
        )
        self.combo_jk.grid(
            row=1, column=1, sticky="ew",
            padx=(8, 22), pady=7, ipady=4
        )

        self.entry_email = self.buat_entry(
            form, "Email", 1, 2
        )
        self.entry_tlp = self.buat_entry(
            form, "No. Telepon", 2, 0
        )
        self.entry_pendidikan = self.buat_entry(
            form, "Pendidikan Terakhir", 2, 2
        )
        self.entry_bidang = self.buat_entry(
            form, "Bidang Keahlian", 3, 0
        )

        for col in (1, 3):
            form.grid_columnconfigure(col, weight=1)

        # Tombol operasi
        buttons = tk.Frame(self.root, bg=BG)
        buttons.pack(fill="x", padx=22, pady=8)

        self.buat_tombol(
            buttons, "＋ Tambah", GREEN,
            self.tambah_data
        ).pack(side="left", padx=(0, 8))

        self.buat_tombol(
            buttons, "✎ Edit", BLUE,
            self.edit_data
        ).pack(side="left", padx=8)

        self.buat_tombol(
            buttons, "Hapus", RED,
            self.hapus_data
        ).pack(side="left", padx=8)

        self.buat_tombol(
            buttons, "Clear", GRAY,
            self.clear_fields
        ).pack(side="left", padx=8)

        self.buat_tombol(
            buttons, "↻ Refresh", PRIMARY,
            self.load_data
        ).pack(side="left", padx=8)

        self.buat_tombol(
            buttons, "Keluar", "#991B1B",
            self.keluar
        ).pack(side="right")

        # Tabel data
        table_frame = tk.Frame(self.root, bg=WHITE)
        table_frame.pack(
            fill="both", expand=True,
            padx=22, pady=(8, 20)
        )

        columns = (
            "nip", "nama_dosen", "jenis_kelamin", "email",
            "no_telepon", "pendidikan_terakhir", "bidang_keahlian"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )

        headings = {
            "nip": "NIP",
            "nama_dosen": "Nama Dosen",
            "jenis_kelamin": "Jenis Kelamin",
            "email": "Email",
            "no_telepon": "No. Telepon",
            "pendidikan_terakhir": "Pendidikan",
            "bidang_keahlian": "Bidang Keahlian"
        }

        widths = [100, 170, 115, 190, 120, 130, 160]

        for col, width in zip(columns, widths):
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=width, minwidth=70)

        scroll_y = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.tree.yview
        )
        scroll_x = ttk.Scrollbar(
            table_frame, orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind(
            "<<TreeviewSelect>>", self.select_item
        )

        # Style tabel
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background=WHITE,
            foreground=DARK,
            rowheight=30,
            fieldbackground=WHITE,
            font=("Arial", 9)
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#DBEAFE",
            foreground=PRIMARY,
            font=("Arial", 9, "bold"),
            padding=8
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#BFDBFE")],
            foreground=[("selected", DARK)]
        )

    def buat_entry(self, parent, label, row, col):
        tk.Label(
            parent, text=label,
            bg=WHITE, fg=DARK
        ).grid(
            row=row, column=col,
            sticky="w", pady=7
        )

        entry = tk.Entry(
            parent,
            font=("Arial", 10),
            relief="solid", bd=1
        )
        entry.grid(
            row=row, column=col + 1,
            sticky="ew", padx=(8, 22),
            pady=7, ipady=5
        )
        return entry

    def buat_tombol(self, parent, text, color, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        )

    def clear_fields(self):
        self.entry_nip.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.combo_jk.set("")
        self.entry_email.delete(0, tk.END)
        self.entry_tlp.delete(0, tk.END)
        self.entry_pendidikan.delete(0, tk.END)
        self.entry_bidang.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT nip, nama_dosen, jenis_kelamin, email,
                       no_telepon, pendidikan_terakhir,
                       bidang_keahlian
                FROM dosen
            """)

            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Gagal memuat data:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def tambah_data(self):
        values = (
            self.entry_nip.get().strip(),
            self.entry_nama.get().strip(),
            self.combo_jk.get(),
            self.entry_email.get().strip(),
            self.entry_tlp.get().strip(),
            self.entry_pendidikan.get().strip(),
            self.entry_bidang.get().strip()
        )

        if not values[0] or not values[1]:
            messagebox.showwarning(
                "Peringatan",
                "NIP dan Nama Dosen wajib diisi!"
            )
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO dosen
                (nip, nama_dosen, jenis_kelamin, email,
                 no_telepon, pendidikan_terakhir, bidang_keahlian)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, values)

            conn.commit()
            messagebox.showinfo(
                "Sukses", "Data dosen berhasil ditambahkan!"
            )
            self.clear_fields()
            self.load_data()

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error", f"Gagal menambah data:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def select_item(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.clear_fields()
        self.entry_nip.insert(0, values[0])
        self.entry_nama.insert(0, values[1])
        self.combo_jk.set(values[2])
        self.entry_email.insert(0, values[3])
        self.entry_tlp.insert(0, values[4])
        self.entry_pendidikan.insert(0, values[5])
        self.entry_bidang.insert(0, values[6])

        # Simpan NIP asli sebagai acuan perubahan
        self.selected_nip = values[0]

    def edit_data(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data dosen yang ingin diedit!"
            )
            return

        old_nip = self.tree.item(
            selected[0], "values"
        )[0]

        values = (
            self.entry_nip.get().strip(),
            self.entry_nama.get().strip(),
            self.combo_jk.get(),
            self.entry_email.get().strip(),
            self.entry_tlp.get().strip(),
            self.entry_pendidikan.get().strip(),
            self.entry_bidang.get().strip(),
            old_nip
        )

        if not values[0] or not values[1]:
            messagebox.showwarning(
                "Peringatan",
                "NIP dan Nama Dosen wajib diisi!"
            )
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE dosen
                SET nip=%s, nama_dosen=%s, jenis_kelamin=%s,
                    email=%s, no_telepon=%s,
                    pendidikan_terakhir=%s, bidang_keahlian=%s
                WHERE nip=%s
            """, values)

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Informasi",
                    "Tidak ada perubahan data."
                )
            else:
                messagebox.showinfo(
                    "Sukses", "Data berhasil diperbarui!"
                )

            self.clear_fields()
            self.load_data()

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error", f"Gagal mengedit data:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def hapus_data(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data dosen yang ingin dihapus!"
            )
            return

        nip = self.tree.item(selected[0], "values")[0]

        if not messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus data dosen NIP {nip}?"
        ):
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM dosen WHERE nip = %s",
                (nip,)
            )
            conn.commit()

            if cursor.rowcount:
                messagebox.showinfo(
                    "Sukses", "Data berhasil dihapus!"
                )
            else:
                messagebox.showwarning(
                    "Informasi", "Data tidak ditemukan."
                )

            self.clear_fields()
            self.load_data()

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error", f"Gagal menghapus data:\n{err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def keluar(self):
        if messagebox.askyesno(
            "Keluar Aplikasi",
            "Apakah kamu yakin ingin keluar dari SIAKAD?"
        ):
            self.root.destroy()


# ==========================================
# PROGRAM UTAMA
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
