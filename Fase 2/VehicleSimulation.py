from itertools import cycle
import tkinter as tk
from tkinter import ttk, simpledialog

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.pack(side="left", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)


class VehicleSimulation:
    def __init__(self, root, nodos, caminhos, vehicle_image_path, location_title, index, canvas, grafoAtual, nodosO):
        self.root = root
        self.root.title(f"Entregas em cidades: Simulação - Localização: {location_title}")

        self.canvas = canvas
        self.text_widget = None  # Attribute to store the text widget0
        self.nodos = nodos
        self.caminhos = caminhos
        self.flag=0
        self.grafoAtual = grafoAtual
        # Draw nodes and streets
        self.draw_nodes_and_streets(index)
        self.ruas_cortadas = []
        self.nodosO = nodosO
        # vehicle initial position
        if vehicle_image_path == "imagens/carro_icon.png":
            vehicle_size = 25
        else:
            vehicle_size = 10
        self.vehicle_image = tk.PhotoImage(file=vehicle_image_path).subsample(int(100 / vehicle_size),
                                                                              int(100 / vehicle_size))
        self.car = self.canvas.create_image(0, 0, anchor=tk.CENTER, image=self.vehicle_image)

        self.current_path = self.create_path()
        self.current_path_iter = iter(self.current_path)

        # Add the warehouse image at the beginning
        armazem_image_path = "imagens/armazem.png"
        self.armazem_image = tk.PhotoImage(file=armazem_image_path).subsample(2, 2)
        self.canvas.create_image(400 - 80, 120 + 300 * index, anchor=tk.CENTER, image=self.armazem_image)

        # Add the house image at the end
        last_node_x = 50 + 400 * (len(self.nodos) - 1)
        casa_image_path = "imagens/casa1.png"
        self.casa_image = tk.PhotoImage(file=casa_image_path).subsample(2, 2)
        self.canvas.create_image(last_node_x + 500, 120 + 300 * index, anchor=tk.CENTER, image=self.casa_image)

        # Start moving after 5 seconds
        self.root.after(5000, lambda: self.move_vehicle(index,vehicle_image_path))

    def create_path(self):
        path = []
        for i in range(len(self.nodos) - 1):
            path.append((self.nodos[i], self.nodos[i + 1], self.caminhos[i]))

        return path

    def draw_nodes_and_streets(self, index):
        node_spacing = 400  # Adjust this value based on your preference for node spacing
        shift_amount = 800  # Amount to shift the simulation forward

        # Find the x-coordinate of the start of the first street
        first_street_start_x = 400 - node_spacing

        for i, (node, street) in enumerate(zip(self.nodos, self.caminhos)):
            x = first_street_start_x + i * node_spacing + shift_amount
            y = 120 + 300 * index
            g=x-400
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="blue")
            self.canvas.create_text(g, y + 30, text=f"Nodo {node}", anchor=tk.CENTER, font=('Helvetica', 16), fill="red")
            size = 10

            x_prev = first_street_start_x + (i - 1) * node_spacing + shift_amount if i > 0 else x - node_spacing
            x_middle = (x + x_prev) / 2
            y_middle = y  # Average y coordinate of the road (line)
            street_text = self.canvas.create_text(x_middle, y -30, text=f"{street}", anchor=tk.CENTER,
                                                  font=('Helvetica', 16), fill="green")
            self.canvas.create_line(x_prev, y_middle, x, y_middle, fill="gray", width=10)

        # Add a button to trigger street cutting
        self.cut_street_button = tk.Button(self.root, text="Cut Street",
                                           command=lambda: self.cut_street_dialog(index))
        self.cut_street_button.pack()

    def cut_street_dialog(self, index):
        # Open a dialog window to input the node number
        node_number = simpledialog.askinteger("Cut Street",
                                              f"Enter the node number to cut the street in simulation {index}:",
                                              minvalue=0, maxvalue=len(self.nodos) - 1)

        if node_number is not None:
            self.cut_street(index, node_number)

    def cut_street(self, index, cut_node):
        # Example: Cut the street at the specified node
        cut_street_node = self.nodos[cut_node]
        print(f"Street cut in simulation {index} at node {cut_street_node}")

        # Adiciona a rua cortada à lista correspondente à simulação
        self.ruas_cortadas.append(self.nodos[cut_node])



    def move_vehicle(self, index,vehicle_image_path):
        try:
            i = next(self.current_path_iter)
            self.animate_vehicle(i, index,vehicle_image_path)

        except StopIteration:
            print(f"Simulation {index} completed!")

    def animate_vehicle(self, edge, index,vehicle_image_path):
        start_node, end_node, street_name = edge
        if start_node in self.ruas_cortadas:
            self.stop_simulation(index, street_name,start_node)
            return
        start_pos = self.nodos.index(start_node)
        end_pos = self.nodos.index(end_node)

        x_start, y_start = 400 + 400 * start_pos, 120 + 300 * index
        x_end, y_end = 400 + 400 * end_pos, 120 + 300 * index

        # Update the position of the vehicle
        self.canvas.coords(self.car, x_start, y_start)


        # Verifica se a próxima rua está na lista de ruas cortadas
        next_edge = None

        next_edge = next(self.current_path_iter)

        if next_edge:
            # Anima o veículo suavemente para a posição final
            self.animate_smoothly(x_start, y_start, x_end, y_end, 0, index, next_edge,vehicle_image_path)
        else:
            print(f"Simulation {index} completed, Delivery delivered successfully!")

    def stop_simulation(self, index, street_name, start_node):

        message = f"Simulation {index} stopped due to a cut of the street {street_name}, Simulation Stopped, waiting for a new route...."
        print(message)
        self.show_popup(message)
        self.recalculate_route(index,start_node)
    def animate_smoothly(self, x_start, y_start, x_end, y_end, step, index, next_edge,vehicle_image_path):
        if step <= 1:
            x_car = x_start + (x_end - x_start) * step
            y_car = y_start + (y_end - y_start) * step
            self.canvas.coords(self.car, x_car, y_car)

            self.root.after(10, lambda: self.animate_smoothly(x_start, y_start, x_end, y_end, step + 0.005, index,
                                                              next_edge,vehicle_image_path))
        else:
            # Move o veículo para a próxima rua
            if vehicle_image_path=="imagens/carro_icon.png":
                self.root.after(1000, lambda: self.animate_vehicle(next_edge, index,vehicle_image_path))
            elif vehicle_image_path=="imagens/bicicleta_icon.png":
                self.root.after(3000, lambda: self.animate_vehicle(next_edge, index,vehicle_image_path))
            else:
                self.root.after(2000, lambda: self.animate_vehicle(next_edge, index,vehicle_image_path))

    def move_vehicle_to_next_edge(self, next_edge, index):
        # Move the vehicle to the next edge
        self.root.after(1000, lambda: self.animate_vehicle(next_edge, index))

    def get_cut_street_node(self, index):
        # Add logic to get the cut street node for the given simulation index
        # For demonstration purposes, return a hardcoded cut street node
        cut_street_node = None
        if index == 0:  # Replace with your condition to determine the cut street node for each simulation
            cut_street_node = self.nodos[len(self.nodos) // 2]
        return cut_street_node

    def show_popup(self, message):
        # Display a popup with the given message
        tk.messagebox.showinfo("Simulation Stopped", message)

    def recalculate_route(self, index, cut_node):
        # Implement your route recalculation logic here
        new_route = self.calculate_new_route(cut_node)

        # Update the current_path with the new route
        self.current_path = new_route
        self.current_path_iter = iter(self.current_path)

        # Continue the simulation with the new route
        self.move_vehicle(index)

    def calculate_new_route(self,cut_node):

        nodo_cortado = self.nodosO[cut_node]
        print(nodo_cortado)
        nodo_cortado_i = nodo_cortado.m_id
        self.grafoAtual.m_h[nodo_cortado_i]= float('inf')
        # self.grafoAtual.m_h[nodo_cortado_i][1] = float('inf')
        # self.grafoAtual.m_h[nodo_cortado_i][2] = float('inf')
        destino = self.nodosO[len(self.nodosO)-1]
        inicial=cut_node-1
        nodo_inicial=self.nodosO[inicial]

        caminho = self.grafoAtual.procura_aStar(nodo_inicial,destino,"car")
        print(caminho)

