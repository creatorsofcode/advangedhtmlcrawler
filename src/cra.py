import tkinter as tk
from tkinter import ttk
from tkinter import  messagebox, scrolledtext, Menu
import requests
from bs4 import BeautifulSoup

def fetch_specific_data(url, tag, attr_type, attr_value):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = []
        if attr_type == 'id':
            element = soup.find(tag, id=attr_value)
            if element:
                elements.append(element.get_text(separator="\n", strip=True))
        elif attr_type == 'class':
            elements = soup.find_all(tag, class_=attr_value)
            elements = [element.get_text(separator="\n", strip=True) for element in elements[:5]]  # Limit to first 5 elements for simplicity
        else:
            elements = soup.find_all(tag)
            elements = [element.get_text(separator="\n", strip=True) for element in elements[:5]]  # Limit to first 5 elements for simplicity

        if not elements:
            return ["No elements found."]
        return elements
    except Exception as e:
        return [f"Error fetching data: {e}"]

def on_submit():
    url = url_entry.get()
    selected_tag = tag_combobox.get()
    attr_type = attr_type_combobox.get()
    attr_value = attr_value_entry.get()
    elements_text = fetch_specific_data(url, selected_tag, attr_type, attr_value)
    text = "\n\n".join(elements_text)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.INSERT, text)
    result_text.config(state=tk.DISABLED)

def show_about():
    messagebox.showinfo("About", "Advanced HTML Crawler v1.0\nDeveloped by: Martin-Mattias Tarkus & ChatGPT\nThis tool allows you to fetch specific HTML tag data.")

# Creating the main window
root = tk.Tk()
root.title("Advanced HTML Crawler")


# Setting up the layout and the rest of the GUI components
# Code for setting up the GUI components remains the same

# New - Creating a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Adding the "File" menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Adding the "Help" menu with an "About" item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)



# Setting up the layout
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# URL Entry
url_label = ttk.Label(frame, text="Enter URL:")
url_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

url_entry = ttk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)

# Tag Selection Combobox
tag_label = ttk.Label(frame, text="Select Tag:")
tag_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

tag_combobox = ttk.Combobox(frame, values=["p", "h1", "h2", "h3", "table", "a", "div", "span"])
tag_combobox.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)
tag_combobox.set("p")  # set the default value

# Attribute Type Selection Combobox
attr_type_label = ttk.Label(frame, text="Attribute Type:")
attr_type_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

attr_type_combobox = ttk.Combobox(frame, values=["None", "id", "class"])
attr_type_combobox.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
attr_type_combobox.set("None")  # set the default value

# Attribute Value Entry
attr_value_label = ttk.Label(frame, text="Attribute Value:")
attr_value_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

attr_value_entry = ttk.Entry(frame, width=50)
attr_value_entry.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)

# Submit Button
submit_button = ttk.Button(frame, text="Fetch Data", command=on_submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=5)

# Result ScrolledText
result_text = scrolledtext.ScrolledText(frame, width=60, height=15, state=tk.DISABLED)
result_text.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

# Running the application
root.mainloop()
