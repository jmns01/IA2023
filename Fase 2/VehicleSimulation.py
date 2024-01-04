from itertools import cycle
import tkinter as tk
from tkinter import ttk

class VehicleSimulation:
    def __init__(self, root, nodos, caminhos, vehicle_image_path):
        self.root = root
        self.canvas = tk.Canvas(root, width=4000, height=200)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.nodos = nodos
        self.caminhos = caminhos

        # Draw nodes and streets
        self.draw_nodes_and_streets()

        # vehicle initial position
        vehicle_size = 10
        self.vehicle_image = tk.PhotoImage(file=vehicle_image_path).subsample(int(100/vehicle_size), int(100/vehicle_size))
        self.car = self.canvas.create_image(0, 0, anchor=tk.CENTER, image=self.vehicle_image)

        self.current_path = self.create_path()
        self.current_path_iter = iter(self.current_path)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.root.after(1000, self.move_vehicle)  # Start moving after 1 second

    def create_path(self):
        path = []
        for i in range(len(self.nodos) - 1):
            path.append((self.nodos[i], self.nodos[i + 1], self.caminhos[i]))

        return path

    def draw_nodes_and_streets(self):
        for i, (node, street) in enumerate(zip(self.nodos, self.caminhos)):
            x = 400 + 400 * i
            y = 120
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="blue")
            self.canvas.create_text(x, y + 30, text=f"Nodo {node}", anchor=tk.CENTER, font=('Helvetica', 8), fill="red")

            if i > 0:
                x_prev = 400 + 400 * (i - 1)
                x_middle = (x + x_prev) / 2
                street_text = self.canvas.create_text(x_middle, y - 10, text=f"{street}", anchor=tk.CENTER, font=('Helvetica', 8), fill="green")
                self.canvas.create_line(x_prev, y, x, y, fill="gray", width=8)  # Linha contínua para representar a estrada

    def move_vehicle(self):
        try:
            i = next(self.current_path_iter)
            self.animate_vehicle(i)

        except StopIteration:
            print("Simulation completed!")

    def animate_vehicle(self, edge):
        start_node, end_node, street_name = edge

        start_pos = self.nodos.index(start_node)
        end_pos = self.nodos.index(end_node)

        x_start, y_start = 400 + 400 * start_pos, 120
        x_end, y_end = 400 + 400 * end_pos, 120

        # Update the position of the vehicle
        self.canvas.coords(self.car, x_start, y_start)

        # Animate the vehicle smoothly to the end position
        self.animate_smoothly(x_start, y_start, x_end, y_end, 0)

    def animate_smoothly(self, x_start, y_start, x_end, y_end, step):
        if step <= 1:
            x_car = x_start + (x_end - x_start) * step
            y_car = y_start + (y_end - y_start) * step
            self.canvas.coords(self.car, x_car, y_car)

            self.root.after(10, self.animate_smoothly, x_start, y_start, x_end, y_end, step + 0.005)
        else:
            try:
                next_edge = next(self.current_path_iter)
                self.move_vehicle_to_next_edge(next_edge)
            except StopIteration:
                print("Simulation completed!")

    def move_vehicle_to_next_edge(self, next_edge):
        # Move the vehicle to the next edge
        self.root.after(1000, self.animate_vehicle, next_edge)