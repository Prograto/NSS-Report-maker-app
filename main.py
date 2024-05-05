import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import shutil

class CombinedNSSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NSS Combined App")
        self.geometry("800x600")

        self.all_events_data = []

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.nss_unit_code_var = tk.StringVar()
        self.event_type_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.event_pic_paths = [tk.StringVar() for _ in range(4)]
        self.clipping_paths = [tk.StringVar() for _ in range(2)]
        self.event_folder_path = None

        self.create_combined_login_screen()

    def create_combined_login_screen(self):
        login_frame = ttk.Frame(self, padding="10")
        login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        login_label = ttk.Label(login_frame, text="Login")
        login_label.grid(row=0, column=0, columnspan=2, pady=10)

        username_label = ttk.Label(login_frame, text="Username:")
        username_label.grid(row=1, column=0, pady=5)
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var)
        username_entry.grid(row=1, column=1, pady=5)

        password_label = ttk.Label(login_frame, text="Password:")
        password_label.grid(row=2, column=0, pady=5)
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1, pady=5)

        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_combined_event_form(self):
        self.withdraw()
        form_window = tk.Toplevel(self)

        form_frame = ttk.Frame(form_window, padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        heading_label = ttk.Label(form_frame, text="NSS Combined Event Form", font=("Helvetica", 16))
        heading_label.grid(row=0, column=0, columnspan=2, pady=10)

        nss_unit_code_label = ttk.Label(form_frame, text="NSS Unit Code:")
        nss_unit_code_label.grid(row=1, column=0, pady=5)
        nss_unit_code_entry = ttk.Entry(form_frame, textvariable=self.nss_unit_code_var)
        nss_unit_code_entry.grid(row=1, column=1, pady=5)

        event_type_label = ttk.Label(form_frame, text="Event Type:")
        event_type_label.grid(row=2, column=0, pady=5)
        event_type_entry = ttk.Entry(form_frame, textvariable=self.event_type_var)
        event_type_entry.grid(row=2, column=1, pady=5)

        title_label = ttk.Label(form_frame, text="Title of the Event:")
        title_label.grid(row=3, column=0, pady=5)
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var)
        title_entry.grid(row=3, column=1, pady=5)

        start_date_label = ttk.Label(form_frame, text="Event Start Date:")
        start_date_label.grid(row=4, column=0, pady=5)
        start_date_entry = ttk.Entry(form_frame, textvariable=self.start_date_var)
        start_date_entry.grid(row=4, column=1, pady=5)

        end_date_label = ttk.Label(form_frame, text="Event End Date:")
        end_date_label.grid(row=5, column=0, pady=5)
        end_date_entry = ttk.Entry(form_frame, textvariable=self.end_date_var)
        end_date_entry.grid(row=5, column=1, pady=5)

        description_label = ttk.Label(form_frame, text="Description (up to 500 words):")
        description_label.grid(row=6, column=0, pady=5)
        self.description_entry = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, width=40, height=5)
        self.description_entry.grid(row=6, column=1, pady=5)

        for i in range(4):
            event_pic_label = ttk.Label(form_frame, text=f"Event Pic-{i + 1}:")
            event_pic_label.grid(row=7 + i, column=0, pady=5)
            event_pic_entry = ttk.Entry(form_frame, textvariable=self.event_pic_paths[i], state="readonly")
            event_pic_entry.grid(row=7 + i, column=1, pady=5)
            upload_event_pic_button = ttk.Button(
                form_frame, text="Upload", command=lambda i=i: self.upload_event_pic(i)
            )
            upload_event_pic_button.grid(row=7 + i, column=2, pady=5)

        for i in range(2):
            clipping_label = ttk.Label(form_frame, text=f"Paper Clipping-{i + 1}:")
            clipping_label.grid(row=11 + i, column=0, pady=5)
            clipping_entry = ttk.Entry(form_frame, textvariable=self.clipping_paths[i], state="readonly")
            clipping_entry.grid(row=11 + i, column=1, pady=5)
            upload_clipping_button = ttk.Button(
                form_frame, text="Upload", command=lambda i=i: self.upload_clipping(i)
            )
            upload_clipping_button.grid(row=11 + i, column=2, pady=5)

        save_button = ttk.Button(form_frame, text="Save", command=self.save_form)
        save_button.grid(row=13, column=0, pady=10)

        cancel_button = ttk.Button(form_frame, text="Cancel", command=form_window.destroy)
        cancel_button.grid(row=13, column=1, pady=10)

    def limit_description_length(self, event, max_words):
        current_text = self.description_entry.get("1.0", "end-1c")
        words = current_text.split()
        if len(words) > max_words:
            new_text = " ".join(words[:max_words])
            self.description_entry.delete("1.0", tk.END)
            self.description_entry.insert(tk.END, new_text)
            messagebox.showwarning("Word Limit Exceeded", f"Maximum {max_words} words allowed for description.")

    def login(self):
        if self.username_var.get() == "admin" and self.password_var.get() == "password":
            self.create_combined_event_form()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def upload_event_pic(self, index):
        file_path = filedialog.askopenfilename(
            title=f"Select Event Pic-{index + 1}", filetypes=[("Image files", "*.jpg;*.png")]
        )
        self.event_pic_paths[index].set(file_path)

    def upload_clipping(self, index):
        file_path = filedialog.askopenfilename(
            title=f"Select Paper Clipping-{index + 1}", filetypes=[("Image files", "*.jpg;*.png")]
        )
        self.clipping_paths[index].set(file_path)

    def save_form(self):
        try:
            self.event_folder_path = os.path.join(os.getcwd(), self.title_var.get().replace(" ", "_"))
            os.makedirs(self.event_folder_path, exist_ok=True)

            form_data_path = os.path.join(self.event_folder_path, "form_data.txt")
            description_text = self.description_entry.get("1.0", "end-1c")

            with open(form_data_path, "w") as file:
                file.write(f"NSS Unit Code: {self.nss_unit_code_var.get()}\n")
                file.write(f"Event Type: {self.event_type_var.get()}\n")
                file.write(f"Title of the Event: {self.title_var.get()}\n")
                file.write(f"Event Start Date: {self.start_date_var.get()}\n")
                file.write(f"Event End Date: {self.end_date_var.get()}\n")
                file.write(f"Description:\n{description_text}\n")

            image_folder_path = os.path.join(self.event_folder_path, "images")
            os.makedirs(image_folder_path, exist_ok=True)

            for i, pic_path_var in enumerate(self.event_pic_paths):
                pic_path = pic_path_var.get()
                if pic_path:
                    pic_name = f"event_pic_{i + 1}.jpg"
                    pic_dest_path = os.path.join(image_folder_path, pic_name)
                    shutil.copy(pic_path, pic_dest_path)

            for i, clipping_path_var in enumerate(self.clipping_paths):
                clipping_path = clipping_path_var.get()
                if clipping_path:
                    clipping_name = f"paper_clipping_{i + 1}.jpg"
                    clipping_dest_path = os.path.join(image_folder_path, clipping_name)
                    shutil.copy(clipping_path, clipping_dest_path)

            pdf_path = os.path.join(self.event_folder_path, "event_form.pdf")
            self.create_pdf(pdf_path)

            event_data = {
                "NSS Unit Code": self.nss_unit_code_var.get(),
                "Event Type": self.event_type_var.get(),
                "Title of the Event": self.title_var.get(),
                "Event Start Date": self.start_date_var.get(),
                "Event End Date": self.end_date_var.get(),
                "Description": description_text,
            }
            self.all_events_data.append(event_data)

            messagebox.showinfo("Save Successful", "Form data and photos saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def draw_page_header(self, c, page_number):
        header_text = f"Page {page_number}"
        c.setFont("Helvetica", 10)
        c.drawRightString(200, 780, header_text)

    def create_pdf(self, pdf_path):
        try:
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica", 12)

            form_data_path = os.path.join(self.event_folder_path, "form_data.txt")
            with open(form_data_path, "r") as file:
                form_data = file.readlines()

            y_position = 750
            page_number = 1

            for line in form_data:
                if y_position < 50:
                    c.showPage()
                    y_position = 750
                    page_number += 1
                    self.draw_page_header(c, page_number)

                split_line = line.strip().split(":")
                if len(split_line) == 2:
                    label, value = split_line
                    c.drawString(100, y_position, f"{label}: {value}")
                    y_position -= 15

            # Add some spacing before description
            y_position -= 20

            description_label = "Description:"
            c.drawString(100, y_position, description_label)
            y_position -= 15

            description_text = self.description_entry.get("1.0", "end-1c")
            lines = description_text.split("\n")

            for line in lines:
                if y_position < 50:
                    c.showPage()
                    y_position = 750
                    page_number += 1
                    self.draw_page_header(c, page_number)

                c.drawString(120, y_position, line)
                y_position -= 15

            # Add some spacing before images
            y_position -= 20

            image_folder_path = os.path.join(self.event_folder_path, "images")
            image_files = [f for f in os.listdir(image_folder_path) if f.endswith(".jpg")]

            # Add some spacing before clippings
            y_position -= 20

            if image_files:
                c.drawString(100, y_position - 20, "Event Images:")
                y_position -= 35
                for image_file in image_files:
                    if y_position < 150:
                        c.showPage()
                        y_position = 750
                        page_number += 1
                        self.draw_page_header(c, page_number)

                    image_path = os.path.join(image_folder_path, image_file)
                    image_label = f"Event Pic-{image_file.split('_')[-1][0]}:"
                    c.drawString(120, y_position, image_label)
                    c.drawInlineImage(image_path, 200, y_position - 35, width=100, height=100)
                    y_position -= 120

            clipping_files = [f for f in os.listdir(image_folder_path) if f.startswith("paper_clipping")]

            if clipping_files:
                c.drawString(100, y_position - 20, "Event Clippings:")
                y_position -= 35
                for clipping_file in clipping_files:
                    if y_position < 150:
                        c.showPage()
                        y_position = 750
                        page_number += 1
                        self.draw_page_header(c, page_number)

                    clipping_path = os.path.join(image_folder_path, clipping_file)
                    clipping_label = f"Paper Clipping-{clipping_file.split('_')[-1][0]}:"
                    c.drawString(120, y_position, clipping_label)
                    c.drawInlineImage(clipping_path, 200, y_position - 35, width=100, height=100)
                    y_position -= 120

            c.save()
            messagebox.showinfo("PDF Created", f"PDF created successfully at {pdf_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating PDF: {str(e)}")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = CombinedNSSApp()
    app.run()
