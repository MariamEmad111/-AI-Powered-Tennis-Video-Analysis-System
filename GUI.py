import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import os
import subprocess
import main

# =========================
# APP CONFIG
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class TennisAnalyticsDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================
        self.title("Zewail City | Tennis Performance Analytics")
        self.geometry("1400x850")
        self.minsize(1200, 750)

        # =========================
        # COLORS
        # =========================
        self.bg_color = "#0B0B0D"
        self.card_color = "#17171A"
        self.gold = "#FFD700"
        self.blue = "#1E3A8A"
        self.gray = "#A1A1AA"

        self.configure(fg_color=self.bg_color)

        # =========================
        # VARIABLES
        # =========================
        self.video_path = None
        self.heatmap_image = None

        # =========================
        # LAYOUT
        # =========================
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.wrapper = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.wrapper.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=30,
            pady=25
        )

        self.build_header()
        self.build_tabs()

    # =========================================================
    # HEADER
    # =========================================================
    def build_header(self):

        header = ctk.CTkFrame(
            self.wrapper,
            fg_color="transparent"
        )

        header.pack(fill="x", pady=(0, 25))

        title = ctk.CTkLabel(
            header,
            text="NEURAL TENNIS ANALYTICS",
            font=ctk.CTkFont(
                size=36,
                weight="bold"
            ),
            text_color=self.gold
        )

        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header,
            text="AIE 501 | Graduate Studies",
            font=ctk.CTkFont(size=14),
            text_color=self.gray
        )

        subtitle.pack(
            side="right",
            pady=(12, 0)
        )

    # =========================================================
    # TABS
    # =========================================================
    def build_tabs(self):

        self.tabs = ctk.CTkTabview(
            self.wrapper,
            fg_color=self.card_color,
            corner_radius=18,
            segmented_button_selected_color=self.gold,
            segmented_button_selected_hover_color="#E6C200",
            segmented_button_unselected_color="#101012"
        )

        self.tabs.pack(
            expand=True,
            fill="both"
        )

        self.control_tab = self.tabs.add("ENGINE")
        self.result_tab = self.tabs.add("VISION ANALYTICS")

        self.build_control_tab()
        self.build_result_tab()

    # =========================================================
    # CONTROL TAB
    # =========================================================
    def build_control_tab(self):

        container = ctk.CTkFrame(
            self.control_tab,
            fg_color="transparent"
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        desc = ctk.CTkLabel(
            container,
            text="YOLOv8 + Court Mapping + Vision Analytics",
            font=ctk.CTkFont(size=16),
            text_color=self.gray
        )

        desc.pack(pady=(0, 35))

        # =========================
        # UPLOAD AREA
        # =========================
        upload_box = ctk.CTkFrame(
            container,
            width=700,
            height=210,
            fg_color="#101014",
            corner_radius=16,
            border_width=1,
            border_color="#2A2A2F"
        )

        upload_box.pack()
        upload_box.pack_propagate(False)

        self.upload_btn = ctk.CTkButton(
            upload_box,
            text="IMPORT MATCH VIDEO",
            command=self.select_video,
            width=300,
            height=55,
            fg_color=self.blue,
            hover_color="#2949B6",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.upload_btn.place(
            relx=0.5,
            rely=0.42,
            anchor="center"
        )

        self.status_label = ctk.CTkLabel(
            upload_box,
            text="SYSTEM STATUS : WAITING FOR INPUT",
            text_color="#666"
        )

        self.status_label.place(
            relx=0.5,
            rely=0.72,
            anchor="center"
        )

        # =========================
        # RUN BUTTON
        # =========================
        self.run_btn = ctk.CTkButton(
            container,
            text="INITIALIZE PIPELINE",
            command=self.start_pipeline,
            state="disabled",
            width=450,
            height=60,
            fg_color=self.gold,
            hover_color="#D4AF37",
            text_color="black",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.run_btn.pack(pady=40)

        # =========================
        # PROGRESS BAR
        # =========================
        self.progress = ctk.CTkProgressBar(
            container,
            width=600,
            height=12,
            progress_color=self.gold
        )

        self.progress.pack()
        self.progress.set(0)

    # =========================================================
    # RESULT TAB
    # =========================================================
    def build_result_tab(self):

        wrapper = ctk.CTkFrame(
            self.result_tab,
            fg_color="transparent"
        )

        wrapper.pack(
            expand=True,
            fill="both",
            padx=25,
            pady=25
        )

        # =========================
        # LEFT PANEL
        # =========================
        left = ctk.CTkFrame(
            wrapper,
            fg_color="#101014",
            corner_radius=20
        )

        left.pack(
            side="left",
            expand=True,
            fill="both",
            padx=(0, 20)
        )

        title = ctk.CTkLabel(
            left,
            text="SPATIAL HEATMAP",
            text_color=self.gold,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(pady=15)

        self.image_label = ctk.CTkLabel(
            left,
            text="HEATMAP OUTPUT WILL APPEAR HERE",
            text_color="#444"
        )

        self.image_label.pack(expand=True)

        # =========================
        # RIGHT PANEL
        # =========================
        right = ctk.CTkFrame(
            wrapper,
            width=350,
            fg_color="transparent"
        )

        right.pack(
            side="right",
            fill="y"
        )

        stats = ctk.CTkFrame(
            right,
            fg_color="#1A1A1E",
            corner_radius=16,
            border_width=1,
            border_color="#2B2B31"
        )

        stats.pack(
            fill="x",
            pady=(0, 20)
        )

        stats_title = ctk.CTkLabel(
            stats,
            text="MATCH INSIGHTS",
            text_color=self.gold,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        stats_title.pack(pady=15)

        self.summary = ctk.CTkLabel(
            stats,
            justify="left",
            anchor="w",
            padx=20,
            text=(
                "• Player Tracking : Idle\n"
                "• Ball Detection : Idle\n"
                "• Heatmap Engine : Waiting\n"
                "• System State : Standby"
            )
        )

        self.summary.pack(
            fill="x",
            pady=(0, 20)
        )

        # =========================
        # VIDEO BUTTON
        # =========================
        self.video_btn = ctk.CTkButton(
            right,
            text="OPEN PROCESSED VIDEO",
            command=self.open_output_video,
            height=55,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            font=ctk.CTkFont(weight="bold")
        )

        self.video_btn.pack(fill="x")

    # =========================================================
    # SELECT VIDEO
    # =========================================================
    def select_video(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov")
            ]
        )

        if not path:
            return

        self.video_path = path

        filename = os.path.basename(path)

        self.status_label.configure(
            text=f"VIDEO LOADED : {filename}",
            text_color=self.gold
        )

        self.run_btn.configure(state="normal")

    # =========================================================
    # START PIPELINE
    # =========================================================
    def start_pipeline(self):

        if not self.video_path:

            messagebox.showerror(
                "Input Error",
                "Please select a video first."
            )

            return

        self.run_btn.configure(
            state="disabled",
            text="PROCESSING..."
        )

        self.progress.start()

        thread = threading.Thread(
            target=self.run_pipeline,
            daemon=True
        )

        thread.start()

    # =========================================================
    # RUN PIPELINE
    # =========================================================
    def run_pipeline(self):

        try:

            # =========================
            # IMPORTANT FIX
            # =========================
            main.main(self.video_path)

            self.after(
                0,
                self.pipeline_finished
            )

        except Exception as e:

            self.after(
                0,
                lambda: messagebox.showerror(
                    "Pipeline Error",
                    str(e)
                )
            )

            self.after(
                0,
                lambda: self.run_btn.configure(
                    state="normal",
                    text="INITIALIZE PIPELINE"
                )
            )

    # =========================================================
    # FINISH
    # =========================================================
    def pipeline_finished(self):

        self.progress.stop()
        self.progress.set(1)

        self.tabs.set("VISION ANALYTICS")

        # =========================
        # LOAD HEATMAP
        # =========================
        heatmap_path = "output_videos/heatmap.jpg"

        if os.path.exists(heatmap_path):

            image = Image.open(heatmap_path)

            self.heatmap_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(780, 520)
            )

            self.image_label.configure(
                image=self.heatmap_image,
                text=""
            )

        # =========================
        # LOAD REPORT
        # =========================
        report_path = "output_videos/final_report.txt"

        if os.path.exists(report_path):

            with open(report_path, "r") as file:

                report_text = file.read()

            self.summary.configure(
                text=report_text,
                text_color="#00FF99"
            )

        else:

            self.summary.configure(
                text=(
                    "Analysis Completed\n"
                    "But report file was not found."
                ),
                text_color="#00FF99"
            )

        self.run_btn.configure(
            state="normal",
            text="RUN AGAIN"
        )

    # =========================================================
    # OPEN VIDEO
    # =========================================================
    def open_output_video(self):

        path = os.path.abspath(
            "output_videos/output_video.avi"
        )

        if not os.path.exists(path):

            messagebox.showerror(
                "File Error",
                "Processed video not found."
            )

            return

        try:

            os.startfile(path)

        except:

            subprocess.Popen(
                ["xdg-open", path]
            )


# =============================================================
# RUN APP
# =============================================================
if __name__ == "__main__":

    app = TennisAnalyticsDashboard()
    app.mainloop()