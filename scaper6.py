import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from urllib.parse import urljoin
from prettytable import PrettyTable
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
import folium
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to extract emails
def extract_emails(soup):
    return set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))

# Function to extract telephone numbers
def extract_telephone_numbers(soup):
    return set(re.findall(r"\+?[0-9.\-\(\) ]{7,15}", soup.text))

# Function to categorize links
def categorize_links(soup, base_url):
    internal_links = set()
    external_links = set()
    for link in soup.find_all('a', href=True):
        url = urljoin(base_url, link['href'])
        if base_url in url:
            internal_links.add(url)
        else:
            external_links.add(url)
    return internal_links, external_links

# Function to write data to CSV
def write_to_csv(emails, telephone_numbers, internal_links, external_links, filepath):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Category', 'Data'])

        def write_category_data(category, data):
            if data:
                writer.writerow([category])
                for item in data:
                    writer.writerow([category[:-1], item])

        write_category_data('Emails', emails)
        write_category_data('Telephone Numbers', telephone_numbers)
        write_category_data('Internal Links', internal_links)
        write_category_data('External Links', external_links)

# Function to get the geographical location of a domain
def get_geolocation(domain):
    try:
        geolocator = Nominatim(user_agent="domain_locator")
        location = geolocator.geocode(domain)
        return (location.latitude, location.longitude) if location else None
    except GeopyError as e:
        messagebox.showerror("Geolocation Error", f"An error occurred: {e}")
        return None

# Function to create a map with the domain location
def create_map(latitude, longitude, domain):
    map_ = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup=domain).add_to(map_)
    map_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if map_path:
        map_.save(map_path)
        messagebox.showinfo("Success", f"Map has been saved to {map_path}")
    else:
        messagebox.showwarning("Cancelled", "Save operation was cancelled.")

# Function to visualize data
def visualize_data(emails, telephone_numbers, internal_links, external_links):
    categories = ['Emails', 'Telephone Numbers', 'Internal Links', 'External Links']
    counts = [len(emails), len(telephone_numbers), len(internal_links), len(external_links)]

    fig, ax = plt.subplots()
    ax.bar(categories, counts, color=['blue', 'green', 'red', 'purple'])
    ax.set_ylabel('Count')
    ax.set_title('Scraped Data Overview')

    return fig

# Function to scrape the website
def scrape_website(domain, scrape_options, progress_var, output_frame):
    try:
        base_url = f"http://{domain}"
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        progress_var.set(10)

        emails = extract_emails(soup) if scrape_options.get("Emails") else set()
        progress_var.set(25)
        
        telephone_numbers = extract_telephone_numbers(soup) if scrape_options.get("Telephone Numbers") else set()
        progress_var.set(50)
        
        internal_links, external_links = categorize_links(soup, base_url) if scrape_options.get("Links") else (set(), set())
        progress_var.set(75)

        table = PrettyTable()
        table.field_names = ["Category", "Data"]

        def add_to_table(category, data):
            if data:
                table.add_row([category, ""])
                for item in data:
                    table.add_row(["", item])

        add_to_table("Emails", emails)
        add_to_table("Telephone Numbers", telephone_numbers)
        add_to_table("Internal Links", internal_links)
        add_to_table("External Links", external_links)

        print(table)
        progress_var.set(100)

        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            write_to_csv(emails, telephone_numbers, internal_links, external_links, filepath)
            messagebox.showinfo("Success", "Data has been saved successfully.")
        else:
            messagebox.showwarning("Cancelled", "Save operation was cancelled.")

        location = get_geolocation(domain)
        if location:
            create_map(location[0], location[1], domain)

        fig = visualize_data(emails, telephone_numbers, internal_links, external_links)
        canvas = FigureCanvasTkAgg(fig, master=output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to start the scraping in a new thread
def start_scraping(domain_entry, scrape_options, progress_var, output_frame):
    domain = domain_entry.get()
    if domain:
        progress_var.set(0)
        for widget in output_frame.winfo_children():
            widget.destroy()
        threading.Thread(target=scrape_website, args=(domain, scrape_options, progress_var, output_frame)).start()
    else:
        messagebox.showwarning("Input Error", "Please enter a domain.")

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Website Scraper")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(main_frame, text="Enter the website domain (without http/https):").grid(row=0, column=0, pady=5)
    domain_entry = ttk.Entry(main_frame, width=40)
    domain_entry.grid(row=1, column=0, pady=5)

    scrape_options = {
        "Emails": tk.BooleanVar(value=True),
        "Telephone Numbers": tk.BooleanVar(value=True),
        "Links": tk.BooleanVar(value=True)
    }

    options_frame = ttk.LabelFrame(main_frame, text="Scrape Options")
    options_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
    ttk.Checkbutton(options_frame, text="Emails", variable=scrape_options["Emails"]).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
    ttk.Checkbutton(options_frame, text="Telephone Numbers", variable=scrape_options["Telephone Numbers"]).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
    ttk.Checkbutton(options_frame, text="Links", variable=scrape_options["Links"]).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100)
    progress_bar.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))

    start_button = ttk.Button(main_frame, text="Start Scraping", command=lambda: start_scraping(domain_entry, scrape_options, progress_var, output_frame))
    start_button.grid(row=4, column=0, pady=5)

    output_frame = ttk.Frame(main_frame)
    output_frame.grid(row=5, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    for child in main_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
