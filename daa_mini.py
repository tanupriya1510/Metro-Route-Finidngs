import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Graph (Metro Map – 20 Stations) ----------------
graph = {
    "Station A": {"Station B": 4, "Station D": 7},
    "Station B": {"Station A": 4, "Station C": 3, "Station E": 6},
    "Station C": {"Station B": 3, "Station F": 5, "Station G": 4},
    "Station D": {"Station A": 7, "Station E": 2, "Station H": 5},
    "Station E": {"Station B": 6, "Station D": 2, "Station F": 4, "Station I": 6},
    "Station F": {"Station C": 5, "Station E": 4, "Station J": 7},
    "Station G": {"Station C": 4, "Station K": 6},
    "Station H": {"Station D": 5, "Station I": 3, "Station L": 4},
    "Station I": {"Station E": 6, "Station H": 3, "Station J": 5, "Station M": 6},
    "Station J": {"Station F": 7, "Station I": 5, "Station N": 4},

    # Newly added stations
    "Station K": {"Station G": 6, "Station O": 5},
    "Station L": {"Station H": 4, "Station P": 6},
    "Station M": {"Station I": 6, "Station Q": 5},
    "Station N": {"Station J": 4, "Station R": 3},
    "Station O": {"Station K": 5, "Station P": 4},
    "Station P": {"Station L": 6, "Station O": 4, "Station Q": 5},
    "Station Q": {"Station M": 5, "Station P": 5, "Station R": 6},
    "Station R": {"Station N": 3, "Station Q": 6, "Station S": 4},
    "Station S": {"Station R": 4, "Station T": 5},
    "Station T": {"Station S": 5}
}

# ---------------- Dijkstra Algorithm ----------------
def dijkstra(start, end):
    import heapq
    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        path = path + [node]
        if node == end:
            return cost, path

        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path))
    return None

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Metro Route Finder – 20 Station Network")
root.geometry("1300x800")
root.configure(bg="#000000")

# ---------------- Left Side (Map Canvas) ----------------
canvas = tk.Canvas(root, width=950, height=800, bg="#111111", highlightthickness=0)
canvas.pack(side="left", fill="both")

# --- Coordinates for 20 stations ---
pos = {
    "Station A": (100, 100),  "Station B": (230, 100),  "Station C": (360, 100),
    "Station D": (100, 230),  "Station E": (230, 230),  "Station F": (360, 230),
    "Station G": (500, 100),  "Station H": (100, 360),  "Station I": (230, 360),
    "Station J": (360, 360),  "Station K": (500, 230),  "Station L": (100, 500),
    "Station M": (230, 500),  "Station N": (360, 500),  "Station O": (500, 360),
    "Station P": (100, 630),  "Station Q": (230, 630),  "Station R": (360, 630),
    "Station S": (500, 500),  "Station T": (650, 500)
}

# Draw edges + distance labels
edge_ids = {}
for s in graph:
    for n, w in graph[s].items():
        if (n, s) in edge_ids:
            continue

        x1, y1 = pos[s]
        x2, y2 = pos[n]

        # Draw route line
        line = canvas.create_line(x1, y1, x2, y2, fill="#22ffff", width=3)
        edge_ids[(s, n)] = line

        # Midpoint for distance label
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        canvas.create_text(mx, my, text=str(w), fill="white", font=("Arial", 10, "bold"))

# Draw nodes
node_ids = {}
def draw_stations():
    for name, (x, y) in pos.items():
        oval = canvas.create_oval(x-18, y-18, x+18, y+18,
                                  fill="#ff00ff", outline="white", width=2)
        canvas.create_text(x, y+32, text=name, fill="white", font=("Arial", 10))
        node_ids[name] = oval

draw_stations()

# ---------------- Right Panel ----------------
panel = tk.Frame(root, bg="#000000")
panel.pack(side="right", fill="y", padx=15, pady=15)

label = tk.Label(panel, text="Metro Route Finder", fg="white", bg="black",
                 font=("Consolas", 16))
label.pack(pady=10)

stations = list(graph.keys())
start_var = tk.StringVar()
end_var = tk.StringVar()

tk.Label(panel, text="From:", fg="white", bg="black", font=("Arial", 12)).pack(anchor="w")
start_menu = ttk.Combobox(panel, textvariable=start_var, values=stations, state="readonly")
start_menu.pack(fill="x", pady=5)

tk.Label(panel, text="To:", fg="white", bg="black", font=("Arial", 12)).pack(anchor="w")
end_menu = ttk.Combobox(panel, textvariable=end_var, values=stations, state="readonly")
end_menu.pack(fill="x", pady=5)

result_box = tk.Text(panel, height=20, width=32, bg="#111111", fg="white",
                     font=("Consolas", 11))
result_box.pack(pady=10)

# ---------------- Highlighter ----------------
def highlight_path(path):
    # Reset everything
    for e in edge_ids:
        canvas.itemconfig(edge_ids[e], fill="#22ffff", width=3)
    for n in node_ids:
        canvas.itemconfig(node_ids[n], fill="#ff00ff")

    # Highlight nodes
    for station in path:
        canvas.itemconfig(node_ids[station], fill="red")

    # Highlight edges
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]

        if (a, b) in edge_ids:
            canvas.itemconfig(edge_ids[(a, b)], fill="yellow", width=5)
        elif (b, a) in edge_ids:
            canvas.itemconfig(edge_ids[(b, a)], fill="yellow", width=5)

# ---------------- Find Route Button ----------------
def find_route():
    start = start_var.get()
    end = end_var.get()

    if not start or not end:
        messagebox.showwarning("Missing Input", "Choose both start and end stations.")
        return
    if start == end:
        messagebox.showinfo("Same Station", "Both stations cannot be same.")
        return

    result_box.delete("1.0", tk.END)

    res = dijkstra(start, end)
    if res is None:
        result_box.insert(tk.END, "No route found.")
    else:
        dist, path = res
        result_box.insert(tk.END, f"Shortest Distance: {dist}\n\nRoute:\n")
        for p in path:
            result_box.insert(tk.END, f"→ {p}\n")
        highlight_path(path)

tk.Button(panel, text="Find Route", command=find_route, bg="#222222",
          fg="cyan", font=("Arial", 12)).pack(fill="x", pady=10)

root.mainloop()
