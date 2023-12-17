import urllib.parse
import requests
from tkinter import *
from tkinter import ttk

# Constants
MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
KEY = "B9IbHMwjBTjCEprFMqmz6qXLDeyeVBJu"

# Function to convert distance based on user preference
def convert_distance(distance, to_metric=True):
    if to_metric:
        return distance * 1.61  # Convert to kilometers
    else:
        return distance  # Keep in miles

# Function to handle button click
def calculate_route():
    orig = entry_start.get()
    dest = entry_dest.get()
    metric_option = check_var.get()

    url = MAIN_API + urllib.parse.urlencode({"key": KEY, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        # Create a Treeview widget for steps, distance, and directions
        tree_result = ttk.Treeview(root, columns=("Step", "Distance", "Directions"), show="headings")
        tree_result.heading("Step", text="Step")
        tree_result.heading("Distance", text="Distance")
        tree_result.heading("Directions", text="Directions")

        # Set column widths
        tree_result.column("Step", width=50)
        tree_result.column("Distance", width=100)
        tree_result.column("Directions", width=600)  # Adjusted width for Directions column

        # Place the Treeview widget on the grid
        tree_result.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Add vertical scrollbar to the Treeview widget
        vscrollbar = ttk.Scrollbar(root, orient='vertical', command=tree_result.yview)
        vscrollbar.grid(row=5, column=3, sticky='ns')

        # Configure scrollbar for the Treeview widget
        tree_result.configure(yscrollcommand=vscrollbar.set)

        # Clear previous content in the Treeview widget
        tree_result.delete(*tree_result.get_children())

        # Display Steps, Distance, and Directions in the Treeview widget
        for idx, each in enumerate(json_data["route"]["legs"][0]["maneuvers"], start=1):
            distance = convert_distance(each["distance"], metric_option)
            narrative = each["narrative"].replace('\n', ' ')
            
            # Tag for coloring based on content
            tag = "green" if "turn left" in narrative.lower() else "purple"
            
            # Insert the item with the specified tag
            tree_result.insert("", "end", values=(idx, f"{distance:.2f} {'km' if metric_option else 'miles'}", narrative), tags=(tag))

            # Configure the tag with the desired color
            tree_result.tag_configure(tag, foreground=tag)

        # Resize the window to fit the content
        root.geometry("850x450")  # Adjusted width and height

        # Center the input fields
        entry_start.delete(0, 'end')
        entry_dest.delete(0, 'end')
        entry_start.insert(0, orig)
        entry_dest.insert(0, dest)

    elif json_status == 402:
        result_var.set(f"Status Code: {json_status}; Invalid user inputs for one or both locations.")
        # Change the color of the status code text on error
        label_result.config(fg="red")
    elif json_status == 611:
        result_var.set(f"Status Code: {json_status}; Missing an entry for one or both locations.")
        # Change the color of the status code text on error
        label_result.config(fg="red")
    else:
        result_var.set(f"For Status Code: {json_status}; Refer to:\nhttps://developer.mapquest.com/documentation/directions-api/status-codes")
        # Change the color of the status code text on error
        label_result.config(fg="red")

# Create the main window
root = Tk()
root.title("MapQuest Route Calculator")

# Set colors
bg_color = "#DEDEDE"  # Background color
fg_color_start = "#7C176B"  # Foreground color for the starting location
fg_color_dest = "#7C176B"  # Foreground color for the destination
bg_color_button = "#BB7CB9"  # Background color for the "Calculate Route" button
fg_color_metric = "#5629AE"  # Foreground color for "Use metric system"
bg_color_button_error = "red"  # Background color for the status code on error

# Configure background color
root.configure(bg=bg_color)

# Create GUI components with specified colors
label_start = Label(root, text="Starting Location:", fg=fg_color_start, bg=bg_color)
label_dest = Label(root, text="Destination:", fg=fg_color_dest, bg=bg_color)
entry_start = Entry(root)
entry_dest = Entry(root)
check_var = BooleanVar()
check_metric = Checkbutton(root, text="Use metric system", variable=check_var, bg=bg_color, fg=fg_color_metric)
button_calculate = Button(root, text="Calculate Route", command=calculate_route, fg=fg_color_metric, bg=bg_color_button)
result_var = StringVar()
label_result = Label(root, textvariable=result_var, justify=LEFT, bg=bg_color)

# Place GUI components on the grid
label_start.grid(row=0, column=0, pady=5, padx=10)
entry_start.grid(row=0, column=1, columnspan=2, pady=5, padx=10, sticky="ew")
label_dest.grid(row=1, column=0, pady=5, padx=10)
entry_dest.grid(row=1, column=1, columnspan=2, pady=5, padx=10, sticky="ew")
check_metric.grid(row=2, column=0, columnspan=3, pady=5, padx=10, sticky="w")
button_calculate.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
label_result.grid(row=4, column=0, columnspan=3, pady=5, padx=10, sticky="ew")

# Run the Tkinter event loop
root.mainloop()
