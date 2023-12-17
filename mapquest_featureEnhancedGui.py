import urllib.parse
import requests
from tkinter import *
from tkinter import ttk

MAIN_API = "https://www.mapquestapi.com/directions/v2/route?"
KEY = "B9IbHMwjBTjCEprFMqmz6qXLDeyeVBJu"

def convert_distance(distance, to_metric=True):
    if to_metric:
        return distance * 1.61 
    else:
        return distance

def calculate_route():
    orig = entry_start.get()
    dest = entry_dest.get()
    metric_option = check_var.get()

    url = MAIN_API + urllib.parse.urlencode({"key": KEY, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        tree_result = ttk.Treeview(root, columns=("Step", "Distance", "Directions"), show="headings")
        tree_result.heading("Step", text="Step")
        tree_result.heading("Distance", text="Distance")
        tree_result.heading("Directions", text="Directions")

        tree_result.column("Step", width=50)
        tree_result.column("Distance", width=100)
        tree_result.column("Directions", width=650)

        tree_result.grid(row=5, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        vscrollbar = ttk.Scrollbar(root, orient='vertical', command=tree_result.yview)
        vscrollbar.grid(row=5, column=3, sticky='ns')

        tree_result.configure(yscrollcommand=vscrollbar.set)

        tree_result.delete(*tree_result.get_children())

        for idx, each in enumerate(json_data["route"]["legs"][0]["maneuvers"], start=1):
            distance = convert_distance(each["distance"], metric_option)
            narrative = each["narrative"].replace('\n', ' ')
            
            tag = "green" if "turn left" in narrative.lower() else "purple"
            
            tree_result.insert("", "end", values=(idx, f"{distance:.2f} {'km' if metric_option else 'miles'}", narrative), tags=(tag))

            tree_result.tag_configure(tag, foreground=tag)

        total_distance = convert_distance(json_data["route"]["distance"], metric_option)
        total_time = json_data["route"]["time"] / 60 

        result_var.set(f"Total Distance -> {total_distance:.2f} {'km' if metric_option else 'miles'}\n"
                       f"Estimated Time -> {total_time:.2f} minutes")

        label_result.config(justify=LEFT, font=('Arial', 11, 'italic'), fg="#850065")

        root.geometry("850x550")  

        entry_start.delete(0, 'end')
        entry_dest.delete(0, 'end')
        entry_start.insert(0, orig)
        entry_dest.insert(0, dest)

    elif json_status == 402:
        result_var.set(f"Status Code: {json_status}; Invalid user inputs for one or both locations.")

        label_result.config(fg="red", font=('Arial', 10, 'bold'))
    elif json_status == 611:
        result_var.set(f"Status Code: {json_status}; Missing an entry for one or both locations.")

        label_result.config(fg="red", font=('Arial', 10, 'bold'))
    else:
        result_var.set(f"For Status Code: {json_status}; Refer to:\nhttps://developer.mapquest.com/documentation/directions-api/status-codes")

        label_result.config(fg="red", font=('Arial', 10, 'bold'))

root = Tk()
root.title("MapQuest Route Calculator")

bg_color = "#DEDEDE"
fg_color_start = "#7C176B"  
fg_color_dest = "#7C176B"
bg_color_button = "#BB7CB9"  
fg_color_metric = "#5629AE"  
bg_color_button_error = "red"  

root.configure(bg=bg_color)

label_start = Label(root, text="Starting Location:", fg=fg_color_start, bg=bg_color)
label_dest = Label(root, text="Destination:", fg=fg_color_dest, bg=bg_color)
entry_start = Entry(root)
entry_dest = Entry(root)
check_var = BooleanVar()
check_metric = Checkbutton(root, text="Use metric system", variable=check_var, bg=bg_color, fg=fg_color_metric)
button_calculate = Button(root, text="Calculate Route", command=calculate_route, fg=fg_color_metric, bg=bg_color_button)
result_var = StringVar()
label_result = Label(root, textvariable=result_var, justify=LEFT, bg=bg_color)

label_start.grid(row=0, column=0, pady=5, padx=10)
entry_start.grid(row=0, column=1, columnspan=2, pady=5, padx=10, sticky="ew")
label_dest.grid(row=1, column=0, pady=5, padx=10)
entry_dest.grid(row=1, column=1, columnspan=2, pady=5, padx=10, sticky="ew")
check_metric.grid(row=2, column=0, columnspan=3, pady=5, padx=10, sticky="w")
button_calculate.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
label_result.grid(row=4, column=0, columnspan=3, pady=5, padx=10, sticky="ew")

root.mainloop()