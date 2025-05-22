import customtkinter as ctk
from tkinter import messagebox
import json

# Inisialisasi CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class SalesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kasir Piscok App")
        self.geometry("600x400")

        # Variabel
        self.username = "admin"
        self.password = "admin123"
        self.saldo_awal = 0
        self.total_transaksi = 0
        self.member_data_file = "member_data.json"
        self.balance_file = "balance.json"
        self.member_data = self.load_member_data()
        self.saldo_diinput = False
        self.total_pembeli = 0


        # Muat saldo awal dan total transaksi dari file JSON
        self.load_balance()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Halaman Login
        self.create_login_page()

    def on_close(self):
        self.saldo_awal = 0
        self.total_transaksi = 0
        self.save_balance()  # Simpan perubahan ke file JSON
        
        # Tutup aplikasi
        self.destroy()

        

    def load_balance(self):
        try:
            with open(self.balance_file, "r") as file:
                balance_data = json.load(file)
                self.saldo_awal = float(balance_data.get("initial_balance", 0))
                self.total_transaksi = float(balance_data.get("total_transaksi", 0))
        except FileNotFoundError:
            pass

        # Muat total transaksi dari transaksi_data.json
        try:
            with open("transaksi_data.json", "r") as file:
                transaksi_data = json.load(file)
                self.total_transaksi = float(transaksi_data.get("total_transaksi", 0))
        except FileNotFoundError:
            pass

    def save_balance(self):
        balance_data = {
            "initial_balance": self.saldo_awal,
            "total_transaksi": self.total_transaksi,
            "saldo_akhir": self.saldo_awal + self.total_transaksi
        }
        with open(self.balance_file, "w") as file:
            json.dump(balance_data, file, indent=4)

        # Simpan saldo awal, total transaksi, dan saldo akhir ke file transaksi_data.json
        transaksi_data = {
            "initial_balance": self.saldo_awal,
            "total_transaksi": self.total_transaksi,
            "saldo_akhir": self.saldo_awal + self.total_transaksi
        }
        with open("transaksi_data.json", "w") as file:
            json.dump(transaksi_data, file, indent=4)

    def load_member_data(self):
        try:
            with open(self.member_data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_member_data(self):
        with open(self.member_data_file, "w") as file:
            json.dump(self.member_data, file, indent=4)

    def create_login_page(self):
        # Membersihkan frame
        for widget in self.winfo_children():
            widget.destroy()

        self.label_title = ctk.CTkLabel(self, text="Login", font=("Arial", 24))
        self.label_title.pack(pady=20)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="Masuk", command=self.login)
        self.btn_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == self.username and password == self.password:
            messagebox.showinfo("Login Berhasil", "Selamat datang!")
            self.create_main_menu()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah.")

    def create_main_menu(self):
        # Membersihkan frame
        for widget in self.winfo_children():
            widget.destroy()

        self.label_title = ctk.CTkLabel(self, text="Menu Utama", font=("Arial", 24))
        self.label_title.pack(pady=20)

        if not self.saldo_diinput:
            self.btn_saldo = ctk.CTkButton(self, text="Input Saldo Awal", command=self.input_saldo_awal)
            self.btn_saldo.pack(pady=10)

        self.btn_penjualan = ctk.CTkButton(self, text="Mulai Penjualan", command=self.start_sales)
        self.btn_penjualan.pack(pady=10)

        self.btn_laporan = ctk.CTkButton(self, text="Lihat Laporan", command=self.show_report)
        self.btn_laporan.pack(pady=10)

        self.btn_keluar = ctk.CTkButton(self, text="Akhiri Penjualan", command=self.quit)
        self.btn_keluar.pack(pady=20)

    def input_saldo_awal(self):
        def submit_saldo():
            try:
                self.saldo_awal = float(entry_saldo.get())
                self.saldo_diinput = True
                messagebox.showinfo("Saldo Awal", f"Saldo awal berhasil diinput: Rp {self.saldo_awal}")
                top.destroy()
                self.create_main_menu()  # Refresh menu utama
            except ValueError:
                messagebox.showerror("Error", "Input saldo harus berupa angka.")

        top = ctk.CTkToplevel(self)
        top.title("Input Saldo Awal")
        top.geometry("300x200")

        label_saldo = ctk.CTkLabel(top, text="Masukkan Saldo Awal:")
        label_saldo.pack(pady=10)

        entry_saldo = ctk.CTkEntry(top)
        entry_saldo.pack(pady=10)

        btn_submit = ctk.CTkButton(top, text="Submit", command=submit_saldo)
        btn_submit.pack(pady=20)

    def start_sales(self):
        def proceed_to_membership(total_harga):
            top.destroy()
            self.handle_membership(total_harga)

        def calculate_total():
            try:
                menu_choice = menu_var.get()
                jumlah = int(entry_jumlah.get())

                if menu_choice == "Piscox Ori 5.000/box":
                    harga = 5000
                elif menu_choice == "Piscox Rasa 10.000/box":
                    harga = 10000
                else:
                    messagebox.showerror("Error", "Pilih menu yang tersedia.")
                    return

                total_harga = harga * jumlah

                self.total_pembeli += 1

                # Hapus penambahan self.total_transaksi di sini
                proceed_to_membership(total_harga)
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka.")



        top = ctk.CTkToplevel(self)
        top.title("Mulai Penjualan")
        top.geometry("400x300")

        label_menu = ctk.CTkLabel(top, text="Pilih Menu:")
        label_menu.pack(pady=10)

        menu_var = ctk.StringVar(value="Pilih Menu")
        menu_dropdown = ctk.CTkOptionMenu(top, values=["Piscox Ori 5.000/box", "Piscox Rasa 10.000/box"], variable=menu_var)
        menu_dropdown.pack(pady=10)

        label_jumlah = ctk.CTkLabel(top, text="Jumlah:")
        label_jumlah.pack(pady=10)

        entry_jumlah = ctk.CTkEntry(top)
        entry_jumlah.pack(pady=10)

        btn_calculate = ctk.CTkButton(top, text="Hitung Total", command=calculate_total)
        btn_calculate.pack(pady=20)

    
    def handle_membership(self, total_harga):
        def check_membership():
            nomor = entry_nomor.get()

            if nomor in self.member_data:
                poin = total_harga // 1000
                self.member_data[nomor]["poin"] += poin
                messagebox.showinfo("Member Terdaftar", f"Poin ditambahkan: {poin}. Total Poin: {self.member_data[nomor]['poin']}")
                self.save_member_data()
                ask_redeem(nomor)
            else:
                messagebox.showerror("Error", "Nomor tidak terdaftar.")

        def register_member():
            nama = entry_nama.get()
            nomor = entry_nomor.get()

            if not nama or not nomor:
                messagebox.showerror("Error", "Nama dan Nomor tidak boleh kosong.")
                return

            if nomor in self.member_data:
                messagebox.showerror("Error", "Nomor sudah terdaftar.")
                return

            self.member_data[nomor] = {"nama": nama, "poin": total_harga // 1000}
            self.save_member_data()
            messagebox.showinfo("Sukses", f"Member {nama} berhasil didaftarkan.")
            ask_redeem(nomor)

        
    

        

        def save_balance(self):
            balance_data = {
                "initial_balance": self.saldo_awal,
                "total_transaksi": self.total_transaksi,
                "saldo_akhir": self.saldo_awal + self.total_transaksi
            }
            with open(self.balance_file, "w") as file:
                json.dump(balance_data, file, indent=4)

            # Simpan total transaksi ke file transaksi_data.json
            transaksi_data = {
                "total_transaksi": self.total_transaksi
            }
            with open("transaksi_data.json", "w") as file:
                json.dump(transaksi_data, file, indent=4)

        def langsung_bayar():
            # Tambahkan total_harga ke total_transaksi tanpa membership
            self.total_transaksi += total_harga
            self.save_balance()  # Simpan perubahan ke file JSON
            messagebox.showinfo("Info", f"Total Bayar: Rp {total_harga}\nTransaksi berhasil!")
            top.destroy()  # Tutup jendela setelah pembayaran selesai        

        def ask_redeem(nomor):
            def redeem_poin(diskon_persen, poin_dikurangi):
                poin = self.member_data[nomor]["poin"]

                if poin >= poin_dikurangi:
                    diskon = diskon_persen * total_harga
                    self.member_data[nomor]["poin"] -= poin_dikurangi
                    total_harga_after_diskon = total_harga - diskon

                    # Tambahkan ke total_transaksi
                    self.total_transaksi += total_harga_after_diskon
                    self.save_member_data()
                    self.save_balance()

                    messagebox.showinfo("Redeem Sukses", f"Total harga: Rp {total_harga} \nDiskon: Rp {diskon}\nTotal Bayar: Rp {total_harga_after_diskon}\nSisa Poin: {self.member_data[nomor]['poin']}")

                    # Tutup jendela redeem jika sudah sukses
                    if top:
                        top.destroy()
                else:
                    messagebox.showerror("Error", "Poin tidak mencukupi untuk redeem.")



            def show_redeem_options():
    # Deklarasikan redeem_window
                redeem_window = ctk.CTkToplevel(self)
                redeem_window.geometry("400x300")
                redeem_window.title("Redeem Poin")

                label_redeem = ctk.CTkLabel(redeem_window, text="Pilih Opsi Redeem:", font=("Arial", 18))
                label_redeem.pack(pady=20)

                redeem_options = [
                    "1. 100 poin diskon 10%",
                    "2. 200 poin diskon 20%",
                    "3. 300 poin diskon 30%"
                ]
                for option in redeem_options:
                    label_option = ctk.CTkLabel(redeem_window, text=option, font=("Arial", 14))
                    label_option.pack(pady=5)

                entry_choice = ctk.CTkEntry(redeem_window, placeholder_text="Masukkan pilihan")
                entry_choice.pack(pady=10)

                def handle_redeem_choice():
                    choice = entry_choice.get()
                    if choice == "1":
                        redeem_poin(0.1, 100)
                    elif choice == "2":
                        redeem_poin(0.2, 200)
                    elif choice == "3":
                        redeem_poin(0.3, 300)
                    else:
                        messagebox.showerror("Error", "Pilihan tidak valid!")
                    redeem_window.destroy()

                choose_button = ctk.CTkButton(redeem_window, text="Pilih", command=handle_redeem_choice)
                choose_button.pack(pady=20)

                redeem_window.mainloop()

            def ask_redeem_question():
                response = messagebox.askyesno("Redeem Poin", "Apakah Anda ingin redeem poin?")
                if response:
                    show_redeem_options()
                else:
                    # Tambahkan total_harga ke total_transaksi jika tidak melakukan redeem
                    self.total_transaksi += total_harga
                    self.save_balance()  # Simpan perubahan ke file JSON
                    messagebox.showinfo("Info", f"Total Bayar: Rp {total_harga} \n Total poin: {self.member_data[nomor]['poin']} \nTransaksi berhasil!")
                    top.destroy()  # Tutup jendela setelah total transaksi ditambahkan


            ask_redeem_question()

        top = ctk.CTkToplevel(self)
        top.title("Membership")
        top.geometry("400x400")

        label_title = ctk.CTkLabel(top, text="Membership")
        label_title.pack(pady=10)

        label_nomor = ctk.CTkLabel(top, text="Masukkan Nomor HP:")
        label_nomor.pack(pady=5)

        entry_nomor = ctk.CTkEntry(top)
        entry_nomor.pack(pady=5)

        btn_check = ctk.CTkButton(top, text="Cek Membership", command=check_membership)
        btn_check.pack(pady=10)

        label_or = ctk.CTkLabel(top, text="-- atau --")
        label_or.pack(pady=5)

        label_nama = ctk.CTkLabel(top, text="Nama (untuk Daftar Baru):")
        label_nama.pack(pady=5)

        entry_nama = ctk.CTkEntry(top)
        entry_nama.pack(pady=5)

        btn_register = ctk.CTkButton(top, text="Daftar Membership", command=register_member)
        btn_register.pack(pady=10)

        btn_langsung_bayar = ctk.CTkButton(top, text="Langsung Bayar", command=langsung_bayar)
        btn_langsung_bayar.pack(pady=10)
    
    
    
    def show_report(self):
        # Laporan penjualan
        report_message = f"""
        Saldo Awal: Rp {self.saldo_awal}
        Total Transaksi: Rp {self.total_transaksi}
        Saldo Akhir: Rp {self.saldo_awal + self.total_transaksi}
        """
        messagebox.showinfo("Laporan Penjualan", report_message)

    

    def quit(self):
        from datetime import datetime
        # Hitung saldo akhir
        saldo_akhir = self.saldo_awal + self.total_transaksi
        
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

        # Buat file saldo_akhir.txt
        with open("saldo_akhir.txt", "w") as file:
            file.write(f"=== Laporan Akhir Penjualan ===\n")
            file.write(f"Saldo Akhir: Rp {saldo_akhir}\n")
            file.write(f"Total Transaksi: Rp {self.total_transaksi}\n")
            file.write(f"Total Pembeli: {self.total_pembeli}\n")
            file.write(f"Tanggal dan Waktu: {waktu_sekarang}\n")

        laporan = f"""
        === Penjualan Berakhir ===
        Saldo Akhir: Rp {saldo_akhir}
        Total Transaksi: Rp {self.total_transaksi}
        Total Pembeli hari ini: {self.total_pembeli}
        Tanggal dan Waktu: {waktu_sekarang}
        """
        
        
        messagebox.showinfo("Laporan Akhir Penjualan", laporan)    

        # Reset saldo awal, total transaksi, dan saldo akhir
        self.saldo_awal = 0
        self.total_transaksi = 0
        self.total_pembeli = 0
        self.save_balance()  # Simpan perubahan ke file JSON

        # Tutup aplikasi
        self.destroy()
    

# Jalankan aplikasi
if __name__ == "__main__":
    app = SalesApp()
    app.mainloop()
