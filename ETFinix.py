import tkinter as tk
import customtkinter as ctk
import subprocess
import threading
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ETFinixApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ETFinix Mobile Unlocking Tool v1.0")
        self.geometry("700x500")

        # Create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ETFinix", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="MTK Tools", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label_title = ctk.CTkLabel(self.main_frame, text="MediaTek (MTK) Operations", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title.pack(pady=10)

        # Buttons for operations
        self.btn_frp = ctk.CTkButton(self.main_frame, text="Unlock FRP", command=lambda: self.run_operation("e frp"))
        self.btn_frp.pack(pady=10)

        self.btn_unlock_bl = ctk.CTkButton(self.main_frame, text="Unlock Bootloader", command=lambda: self.run_operation("e bmt.bin"))
        self.btn_unlock_bl.pack(pady=10)

        self.btn_factory_reset = ctk.CTkButton(self.main_frame, text="Factory Reset (Wipe Data)", command=lambda: self.run_operation("e userdata"))
        self.btn_factory_reset.pack(pady=10)

        self.btn_dump_preloader = ctk.CTkButton(self.main_frame, text="Dump Preloader", command=lambda: self.run_operation("r preloader preloader.bin"))
        self.btn_dump_preloader.pack(pady=10)

        # Console output
        self.textbox = ctk.CTkTextbox(self.main_frame, width=400, height=150)
        self.textbox.pack(pady=20, padx=20, fill="both", expand=True)
        self.textbox.insert("0.0", "Welcome to ETFinix Tool.\nConnect your device in BROM mode to start.\n\n")

    def sidebar_button_event(self):
        print("Sidebar button clicked")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def log(self, message):
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")

    def run_operation(self, command_args):
        self.log(f"Starting operation: {command_args}...")
        # Run in a separate thread to keep GUI responsive
        thread = threading.Thread(target=self.execute_mtk_command, args=(command_args,))
        thread.start()

    def execute_mtk_command(self, args):
        try:
            # Note: In a real scenario, 'python mtk' would be called. 
            # We assume mtkclient is in the same directory or installed.
            process = subprocess.Popen(
                f"python mtk {args}", 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True
            )
            
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            if process.returncode == 0:
                self.log("Operation completed successfully!")
            else:
                self.log("Operation failed. Check connection and drivers.")
        except Exception as e:
            self.log(f"Error: {str(e)}")

if __name__ == "__main__":
    app = ETFinixApp()
    app.mainloop()
