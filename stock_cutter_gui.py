import customtkinter as ctk
import numpy as np
import pulp as plp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.messagebox as messagebox  # Use standard messagebox instead of CTkMessageBox

class StockCutterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Cutting Optimizer")
        self.root.geometry("1400x800")
        
        # Language settings
        self.languages = {
            "English": {
                "title": "Stock Cutting Optimizer",
                "stock_label": "Available Stock Lengths",
                "stock_tooltip": "Enter lengths separated by commas (e.g., 13,10)",
                "required_label": "Required Piece Lengths",
                "required_tooltip": "Enter required lengths separated by commas (e.g., 5,2)",
                "quantity_label": "Minimum Quantities Needed",
                "quantity_tooltip": "Enter minimum quantities for each required length (e.g., 2,0)",
                "calculate": "Calculate",
                "results": "Results",
                "visualization": "Visualization",
                "error": "Error",
                "try_again": "Please check your inputs and try again.",
                "input_guide": "Input Guide",
                "step1": "Step 1: Enter available stock lengths",
                "step2": "Step 2: Enter required piece lengths",
                "step3": "Step 3: Enter minimum quantities needed",
                "example": "Example:",
                "stock_example": "Stock: 13,10",
                "required_example": "Pieces: 5,2",
                "quantity_example": "Quantities: 2,0"
            },
            "Español": {
                "title": "Optimizador de Corte de Material",
                "stock_label": "Longitudes de Material Disponible",
                "stock_tooltip": "Ingrese longitudes separadas por comas (ej., 13,10)",
                "required_label": "Longitudes de Piezas Requeridas",
                "required_tooltip": "Ingrese longitudes requeridas separadas por comas (ej., 5,2)",
                "quantity_label": "Cantidades Mínimas Necesarias",
                "quantity_tooltip": "Ingrese cantidades mínimas para cada longitud requerida (ej., 2,0)",
                "calculate": "Calcular",
                "results": "Resultados",
                "visualization": "Visualización",
                "error": "Error",
                "try_again": "Por favor verifique sus entradas e intente nuevamente.",
                "input_guide": "Guía de Entrada",
                "step1": "Paso 1: Ingrese las longitudes de material disponible",
                "step2": "Paso 2: Ingrese las longitudes de piezas requeridas",
                "step3": "Paso 3: Ingrese las cantidades mínimas necesarias",
                "example": "Ejemplo:",
                "stock_example": "Material: 13,10",
                "required_example": "Piezas: 5,2",
                "quantity_example": "Cantidades: 2,0"
            }
        }
        self.current_language = "English"
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top bar with language selector
        top_bar = ctk.CTkFrame(self.main_frame, height=40)
        top_bar.pack(fill="x", pady=(0, 20))
        
        # Language selector
        self.language_var = ctk.StringVar(value=self.current_language)
        language_menu = ctk.CTkOptionMenu(top_bar, 
                                        values=list(self.languages.keys()),
                                        variable=self.language_var,
                                        command=self.change_language)
        language_menu.pack(side="right", padx=10)
        
        # Left panel for inputs
        left_panel = ctk.CTkFrame(self.main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Header
        self.header_label = ctk.CTkLabel(left_panel, 
                                       text=self.languages[self.current_language]["title"],
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(0, 20))
        
        # Input guide frame
        guide_frame = ctk.CTkFrame(left_panel)
        guide_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        guide_label = ctk.CTkLabel(guide_frame,
                                  text=self.languages[self.current_language]["input_guide"],
                                  font=ctk.CTkFont(size=16, weight="bold"))
        guide_label.pack(pady=10)
        
        # Example section
        example_frame = ctk.CTkFrame(guide_frame, fg_color="transparent")
        example_frame.pack(fill="x", pady=5)
        
        example_label = ctk.CTkLabel(example_frame,
                                   text=self.languages[self.current_language]["example"],
                                   font=ctk.CTkFont(size=14, weight="bold"))
        example_label.pack(side="left", padx=5)
        
        example_text = ctk.CTkLabel(example_frame,
                                  text=f"{self.languages[self.current_language]['stock_example']} | "
                                       f"{self.languages[self.current_language]['required_example']} | "
                                       f"{self.languages[self.current_language]['quantity_example']}",
                                  font=ctk.CTkFont(size=12))
        example_text.pack(side="left", padx=5)
        
        # Input frame with modern styling
        input_frame = ctk.CTkFrame(left_panel)
        input_frame.pack(fill="x", pady=10, padx=10)
        
        # Step 1: Stock sizes
        step1_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        step1_frame.pack(fill="x", pady=5)
        
        step1_label = ctk.CTkLabel(step1_frame,
                                  text=self.languages[self.current_language]["step1"],
                                  font=ctk.CTkFont(size=14, weight="bold"))
        step1_label.pack(side="left", padx=5)
        
        self.stock_entry = ctk.CTkEntry(step1_frame,
                                      placeholder_text="e.g., 13,10",
                                      width=200)
        self.stock_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.stock_entry.insert(0, "13,10")
        
        # Step 2: Required sizes
        step2_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        step2_frame.pack(fill="x", pady=5)
        
        step2_label = ctk.CTkLabel(step2_frame,
                                  text=self.languages[self.current_language]["step2"],
                                  font=ctk.CTkFont(size=14, weight="bold"))
        step2_label.pack(side="left", padx=5)
        
        self.required_entry = ctk.CTkEntry(step2_frame,
                                         placeholder_text="e.g., 5,2",
                                         width=200)
        self.required_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.required_entry.insert(0, "5,2")
        
        # Step 3: Minimum quantities
        step3_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        step3_frame.pack(fill="x", pady=5)
        
        step3_label = ctk.CTkLabel(step3_frame,
                                  text=self.languages[self.current_language]["step3"],
                                  font=ctk.CTkFont(size=14, weight="bold"))
        step3_label.pack(side="left", padx=5)
        
        self.min_quantities_entry = ctk.CTkEntry(step3_frame,
                                               placeholder_text="e.g., 2,0",
                                               width=200)
        self.min_quantities_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.min_quantities_entry.insert(0, "2,0")
        
        # Add help buttons for each step
        for frame, field_type in [(step1_frame, "stock"), 
                                (step2_frame, "required"), 
                                (step3_frame, "quantity")]:
            help_btn = ctk.CTkButton(frame,
                                   text="?",
                                   width=30,
                                   fg_color="transparent",
                                   hover_color="#2b2b2b",
                                   command=lambda t=field_type: self.show_tooltip(t))
            help_btn.pack(side="right", padx=5)
            
            # Add tooltip functionality
            help_btn.bind("<Enter>", lambda e, t=field_type: self.show_tooltip(e, t))
            help_btn.bind("<Leave>", lambda e: self.hide_tooltip())
        
        # Tooltip window
        self.tooltip = None
        
        # Calculate button
        self.calculate_btn = ctk.CTkButton(left_panel,
                                         text=self.languages[self.current_language]["calculate"],
                                         command=self.calculate,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         height=40)
        self.calculate_btn.pack(pady=20)
        
        # Results text area
        results_frame = ctk.CTkFrame(left_panel)
        results_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        self.results_label = ctk.CTkLabel(results_frame,
                                        text=self.languages[self.current_language]["results"],
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.results_label.pack(pady=10)
        
        self.results_text = ctk.CTkTextbox(results_frame,
                                         font=ctk.CTkFont(size=12),
                                         wrap="word")
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Right panel for visualization
        right_panel = ctk.CTkFrame(self.main_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Create scrollable frame for visualization
        self.scrollable_frame = ctk.CTkScrollableFrame(right_panel)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame to hold the canvas
        self.canvas_frame = ctk.CTkFrame(self.scrollable_frame)
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Visualization title
        self.vis_label = ctk.CTkLabel(self.canvas_frame,
                                    text=self.languages[self.current_language]["visualization"],
                                    font=ctk.CTkFont(size=16, weight="bold"))
        self.vis_label.pack(pady=10)
        
        # Create matplotlib figure with dark theme
        plt.style.use('dark_background')
        self.fig = None
        self.canvas = None
        self.create_new_figure()
    
    def create_new_figure(self):
        """Create a new figure and canvas"""
        if self.canvas is not None:
            # Remove old canvas
            self.canvas.get_tk_widget().destroy()
        
        # Create new figure
        self.fig = Figure(facecolor='#2b2b2b')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_tooltip(self, event, field_type):
        if self.tooltip:
            self.tooltip.destroy()
        
        tooltip_text = self.languages[self.current_language][f"{field_type}_tooltip"]
        self.tooltip = ctk.CTkToplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        # Configure tooltip appearance
        self.tooltip.configure(fg_color="#2b2b2b")
        
        label = ctk.CTkLabel(self.tooltip, 
                           text=tooltip_text,
                           font=ctk.CTkFont(size=12),
                           wraplength=200)
        label.pack(padx=10, pady=5)
    
    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def change_language(self, language):
        self.current_language = language
        # Update all text elements
        self.header_label.configure(text=self.languages[language]["title"])
        self.stock_label.configure(text=self.languages[language]["stock_label"])
        self.required_label.configure(text=self.languages[language]["required_label"])
        self.min_label.configure(text=self.languages[language]["quantity_label"])
        self.calculate_btn.configure(text=self.languages[language]["calculate"])
        self.results_label.configure(text=self.languages[language]["results"])
        self.vis_label.configure(text=self.languages[language]["visualization"])
        
        # Update placeholders
        self.stock_entry.configure(placeholder_text="e.g., 13,10")
        self.required_entry.configure(placeholder_text="e.g., 5,2")
        self.min_quantities_entry.configure(placeholder_text="e.g., 2,0")
    
    def calculate(self):
        try:
            # Get and validate inputs
            try:
                stock_sizes = [float(x.strip()) for x in self.stock_entry.get().split(',')]
                required_sizes = [float(x.strip()) for x in self.required_entry.get().split(',')]
                min_quantities = [float(x.strip()) for x in self.min_quantities_entry.get().split(',')]
            except ValueError:
                raise ValueError("Please enter valid numbers separated by commas")
            
            if len(required_sizes) != len(min_quantities):
                raise ValueError("Number of required sizes must match number of minimum quantities")
            
            if not stock_sizes or not required_sizes or not min_quantities:
                raise ValueError("Please fill in all fields")
            
            # Check if any required size is larger than the largest stock
            max_stock = max(stock_sizes)
            for size in required_sizes:
                if size > max_stock:
                    raise ValueError(f"Required size {size} is larger than the largest stock size {max_stock}")
            
            # Convert to numpy arrays
            troncos = np.array(stock_sizes)
            piezas = np.array(required_sizes)
            lim_inf = np.array(min_quantities)
            
            # Calculate total required length
            total_required_length = sum(piezas[i] * lim_inf[i] for i in range(len(piezas)))
            total_stock = sum(troncos)
            
            if total_required_length > total_stock:
                raise ValueError(
                    f"Insufficient stock. Required length ({total_required_length}) exceeds available stock ({total_stock})")
            
            # Define problem
            iponch = plp.LpProblem("iponch_p", plp.LpMinimize)
            
            # Variables - one for each possible cutting pattern for each stock piece
            sol = {}
            for i in range(len(troncos)):
                for j in range(len(piezas)):
                    sol['{},{}'.format(i,j)] = plp.LpVariable(
                        'Tronco:{},pieza:{}'.format(troncos[i], piezas[j]),
                        lowBound=0,
                        cat='Integer'
                    )
            
            # Objective function - minimize waste
            waste = plp.lpSum(troncos[i] - plp.lpSum(sol['{},{}'.format(i,j)] * piezas[j] 
                                                    for j in range(len(piezas))) 
                            for i in range(len(troncos)))
            iponch += waste
            
            # Constraints
            # 1. Length constraint for each stock piece
            for i in range(len(troncos)):
                iponch += plp.lpSum(sol['{},{}'.format(i,j)] * piezas[j] 
                                  for j in range(len(piezas))) <= troncos[i]
            
            # 2. Minimum quantity constraints
            for j in range(len(piezas)):
                iponch += plp.lpSum(sol['{},{}'.format(i,j)] 
                                  for i in range(len(troncos))) >= lim_inf[j]
            
            # Solve with CBC solver
            solver = plp.PULP_CBC_CMD(msg=False, timeLimit=10)
            status = iponch.solve(solver)
            
            if status != 1:
                raise ValueError(
                    f"Could not find optimal solution. Status: {plp.LpStatus[iponch.status]}\n"
                    f"Try different input values or check if the problem is feasible."
                )
            
            # Verify solution
            solution_valid = True
            error_message = ""
            
            # Check if minimum quantities are met
            for j in range(len(piezas)):
                total_pieces = sum(sol['{},{}'.format(i,j)].varValue for i in range(len(troncos)))
                if total_pieces < lim_inf[j]:
                    solution_valid = False
                    error_message = f"Could not meet minimum quantity for piece size {piezas[j]}"
                    break
            
            # Check if stock lengths are not exceeded
            for i in range(len(troncos)):
                used_length = sum(sol['{},{}'.format(i,j)].varValue * piezas[j] 
                                for j in range(len(piezas)))
                if used_length > troncos[i]:
                    solution_valid = False
                    error_message = f"Solution exceeds stock length for piece {i+1}"
                    break
            
            if not solution_valid:
                raise ValueError(error_message)

            # Display results with better formatting
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "Optimization Results\n")
            self.results_text.insert("end", "="*50 + "\n\n")
            
            # Calculate and display waste
            total_waste = sum(troncos) - sum(sol['{},{}'.format(i,j)].varValue * piezas[j] 
                                            for i in range(len(troncos)) for j in range(len(piezas)))
            self.results_text.insert("end", f"Total Stock Length: {sum(troncos)}\n")
            self.results_text.insert("end", f"Total Used Length: {sum(sol['{},{}'.format(i,j)].varValue * piezas[j] 
                                                                 for i in range(len(troncos)) for j in range(len(piezas)))}\n")
            self.results_text.insert("end", f"Total Waste: {total_waste}\n")
            self.results_text.insert("end", f"Status: {plp.LpStatus[iponch.status]}\n\n")
            
            self.results_text.insert("end", "Cutting Patterns:\n")
            self.results_text.insert("end", "-"*50 + "\n")
            
            # Clear previous visualization
            self.create_new_figure()
            
            # Calculate number of logs and set figure size
            num_logs = len(troncos)
            fig_height = max(4 * num_logs, 8)  # Minimum height of 8 inches
            self.fig.set_size_inches(8, fig_height)
            
            # Create a subplot for each log
            axes = []
            for i in range(num_logs):
                if i == 0:
                    ax = self.fig.add_subplot(num_logs, 1, i+1)
                else:
                    ax = self.fig.add_subplot(num_logs, 1, i+1, sharex=axes[0])
                axes.append(ax)
            
            # Plot each log in its own subplot
            log_height = 0.6
            label_offset = 0.05
            
            # Define colors
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6']
            
            for i, (ax, tronco) in enumerate(zip(axes, troncos)):
                # Draw the log
                ax.barh(0, tronco, height=log_height, 
                       color=colors[i % len(colors)], alpha=0.7)
                
                # Add log label
                ax.text(tronco/2, 0, f'Log {i+1} ({tronco})', 
                       ha='center', va='center', color='white', 
                       fontweight='bold', fontsize=10)
                
                # Draw cuts and add piece labels
                cut_pos = 0
                for j, pieza in enumerate(piezas):
                    count = int(sol['{},{}'.format(i,j)].varValue)
                    for _ in range(count):
                        # Draw cut line - extend beyond log edges
                        ax.axvline(x=cut_pos, ymin=0.3, ymax=0.7,
                                 color='red', linestyle='-', 
                                 linewidth=1.5, alpha=0.8)
                        
                        # Add piece label above the log
                        ax.text(cut_pos + pieza/2, 0.4, 
                               f'{pieza}', 
                               ha='center', va='bottom', color='white', 
                               fontsize=10, fontweight='bold',
                               bbox=dict(facecolor='#1a1a1a', 
                                       alpha=0.9, 
                                       edgecolor='white',
                                       linewidth=0.5,
                                       boxstyle='round,pad=0.2'))
                        
                        cut_pos += pieza
                
                # Draw final cut line at the end of used length
                if cut_pos < tronco:
                    ax.axvline(x=cut_pos, ymin=0.3, ymax=0.7,
                             color='red', linestyle='-', 
                             linewidth=1.5, alpha=0.8)
                
                # Set subplot properties
                ax.set_ylim(-0.5, 0.5)
                ax.set_xlim(0, max(troncos) * 1.1)
                ax.grid(True, linestyle='--', alpha=0.3, color='white')
                
                # Remove y-axis ticks and labels
                ax.set_yticks([])
                
                # Only show x-axis labels for the bottom subplot
                if i < num_logs - 1:
                    ax.set_xticklabels([])
                
                # Set background color
                ax.set_facecolor('#2b2b2b')
                
                # Customize spines
                for spine in ax.spines.values():
                    spine.set_color('white')
                    spine.set_linewidth(0.5)
            
            # Add common x-label to bottom subplot
            axes[-1].set_xlabel('Length', color='white', fontsize=12)
            
            # Add title to top subplot
            axes[0].set_title('Cutting Patterns Visualization', 
                            color='white', fontsize=14, pad=20)
            
            # Adjust layout
            self.fig.tight_layout()
            
            # Redraw canvas
            self.canvas.draw()
            
            # Add cutting patterns to text area
            for variable in iponch.variables():
                if variable.varValue > 0:
                    self.results_text.insert("end", f"• {variable.name} = {variable.varValue}\n")
            
        except Exception as e:
            error_message = str(e)
            # Clear previous results
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "Error\n")
            self.results_text.insert("end", "="*50 + "\n\n")
            self.results_text.insert("end", f"Error: {error_message}\n\n")
            self.results_text.insert("end", "Please check your inputs and try again.")
            
            # Show error message box using standard messagebox
            messagebox.showerror("Error", error_message)
            
            # Clear visualization
            self.create_new_figure()
            self.canvas.draw()

if __name__ == "__main__":
    root = ctk.CTk()
    app = StockCutterGUI(root)
    root.mainloop() 