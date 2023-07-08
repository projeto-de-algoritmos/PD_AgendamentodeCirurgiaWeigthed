import tkinter as tk
from tkinter import messagebox, StringVar
import re

prioridades = {"Normal": 1, "Grave": 2, "Urgente": 3}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agendamento de Cirurgias")
        
        self.cirurgias = []
        self.possiveis_cirurgias = []
        
        self.create_widgets()
    
    def create_widgets(self):
        frame_cirurgia = tk.Frame(self)
        frame_cirurgia.pack(padx=10, pady=10)
        
        tk.Label(frame_cirurgia, text="Nome do paciente:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(frame_cirurgia)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(frame_cirurgia, text="Horário de Início (hh:mm):").grid(row=1, column=0)
        self.entry_inicio = tk.Entry(frame_cirurgia)
        self.entry_inicio.grid(row=1, column=1)

        tk.Label(frame_cirurgia, text="Horário de Término (hh:mm):").grid(row=2, column=0)
        self.entry_termino = tk.Entry(frame_cirurgia)
        self.entry_termino.grid(row=2, column=1)

        tk.Label(frame_cirurgia, text="Prioridade:").grid(row=3, column=0)
        self.entry_prioridade = StringVar()
        self.entry_prioridade.set("Normal") # default value
        w = tk.OptionMenu(frame_cirurgia, self.entry_prioridade, "Normal", "Grave", "Urgente")
        w.grid(row=3, column=1)
        
        tk.Button(frame_cirurgia, text="Agendar", command=self.agendar_cirurgia).grid(row=4, column=0, columnspan=2)

        frame_salas_cirurgias = tk.Frame(self)
        frame_salas_cirurgias.pack(padx=10, pady=10)

        self.text_agendadas = tk.Text(frame_salas_cirurgias, width=50, height=10)
        self.text_agendadas.pack(side=tk.LEFT)

        self.text_possiveis = tk.Text(frame_salas_cirurgias, width=50, height=10)
        self.text_possiveis.pack(side=tk.LEFT)
        
    def agendar_cirurgia(self):
        nome = self.entry_nome.get()
        inicio = self.entry_inicio.get()
        termino = self.entry_termino.get()
        prioridade = prioridades[self.entry_prioridade.get()]
        
        if self.verificar_horario(inicio) and self.verificar_horario(termino) and self.verificar_nome(nome):
            cirurgia = (inicio, termino, nome, prioridade)
            self.cirurgias.append(cirurgia)
            self.entry_nome.delete(0, tk.END)
            self.entry_inicio.delete(0, tk.END)
            self.entry_termino.delete(0, tk.END)
            self.entry_prioridade.set("Normal")
            self.atualizar_cirurgias()
        else:
            tk.messagebox.showerror("Erro", "Insira um nome válido e horários válidos (hh:mm).")
    
    def verificar_nome(self, nome):
        if re.match(r"^[a-zA-Z]+$", nome):
            return True
        return False
    
    def verificar_horario(self, horario):
        if re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', horario):
            return True
        return False

    def atualizar_cirurgias(self):
        self.text_agendadas.delete(1.0, tk.END)
        self.text_possiveis.delete(1.0, tk.END)

        self.possiveis_cirurgias = self.weighted_interval_scheduling(self.cirurgias)

        for i, cirurgia in enumerate(self.cirurgias):
            self.text_agendadas.insert(tk.END, f"Cirurgias Solicitadas {i+1}:\n")
            self.text_agendadas.insert(tk.END, f"\tPaciente: {cirurgia[2]} \n\tInício: {cirurgia[0]} - Término: {cirurgia[1]} \n\tPrioridade: {list(prioridades.keys())[list(prioridades.values()).index(cirurgia[3])]} \n\n")

        for i, cirurgia in enumerate(self.possiveis_cirurgias):
            self.text_possiveis.insert(tk.END, f"Cirurgia Agendadas {i+1}:\n")
            self.text_possiveis.insert(tk.END, f"\tPaciente: {cirurgia[2]} \n\tInício: {cirurgia[0]} - Término: {cirurgia[1]} \n\tPrioridade: {list(prioridades.keys())[list(prioridades.values()).index(cirurgia[3])]} \n\n")

    def weighted_interval_scheduling(self, cirurgias):
        cirurgias = [("-1:-1", "-1:-1", "", 0)] + sorted(cirurgias, key=lambda x: x[1]) 
        n = len(cirurgias)
        
        dp = [0 for _ in range(n)]
        p = [0 for _ in range(n)]
        
        for i in range(n-1, -1, -1):
            for j in range(i-1, -1, -1):
                if cirurgias[j][1] <= cirurgias[i][0]:
                    p[i] = j
                    break
        
        for i in range(1, n):
            dp[i] = max(cirurgias[i][3] + dp[p[i]], dp[i-1])

        i = n - 1
        optimal_cirurgias = []
        while i > 0:
            if cirurgias[i][3] + dp[p[i]] >= dp[i-1]:
                optimal_cirurgias.append(cirurgias[i])
                i = p[i]
            else:
                i -= 1
        return optimal_cirurgias

if __name__ == "__main__":
    app = Application()
    app.mainloop()
