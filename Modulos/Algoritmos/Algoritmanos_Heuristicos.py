import sys, random, math
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QSpinBox, QGridLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Algoritmos_Heuristicos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heurísticos y Metaheurísticos - Mochila")
        self.setGeometry(100, 100, 950, 650)
        self.setStyleSheet("background-color:#101820; color:white;")
        self.items = [
            (4,15), (3,10), (1,2), (6,11), (16,22), (9,13), (14,12),
            (5,16), (12,18), (7,15), (8,12), (6,14), (10,20), (13,16), (2,10)
        ]
        self.capacidad = 50
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        title = QLabel("🎒 Problema de la Mochila")
        title.setFont(QFont("", 16, QFont.Bold))
        layout.addWidget(title)

        row1 = QHBoxLayout()
        self.peso_in = QSpinBox(); self.peso_in.setPrefix("Peso: "); self.peso_in.setMaximum(100)
        self.val_in = QSpinBox(); self.val_in.setPrefix("Valor: "); self.val_in.setMaximum(200)
        row1.addWidget(self.peso_in); row1.addWidget(self.val_in)
        btn_add = QPushButton("➕ Añadir ítem"); btn_add.clicked.connect(self.add_item)
        row1.addWidget(btn_add)
        row1.addWidget(QLabel("Capacidad:"))
        self.cap_spin = QSpinBox(); self.cap_spin.setValue(self.capacidad); self.cap_spin.setMaximum(500)
        self.cap_spin.valueChanged.connect(lambda v: setattr(self, "capacidad", v))
        row1.addWidget(self.cap_spin)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems(["Voraz", "Local", "Tabú", "Enfriamiento", "Gradiente", "Hormigas", "Genético"])
        row2.addWidget(self.combo)
        run = QPushButton("▶️ Ejecutar"); run.clicked.connect(self.run)
        clear = QPushButton("🧹 Limpiar"); clear.clicked.connect(self.clear)
        row2.addWidget(run); row2.addWidget(clear)
        layout.addLayout(row2)
        
        btn_volver = QPushButton("🔙 Volver")
        btn_volver.setStyleSheet("padding: 6px; font-weight: bold; background-color: #444; color: white; border-radius: 6px;")
        btn_volver.clicked.connect(self.volver)
        layout.addWidget(btn_volver, alignment=Qt.AlignRight)


        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.draw_items()
        layout.addLayout(self.grid)

        self.res = QTextEdit(); self.res.setReadOnly(True); layout.addWidget(self.res)
        self.setLayout(layout)

    def draw_items(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        for idx, (peso, valor) in enumerate(self.items):
            box = QFrame()
            box.setStyleSheet("border: 2px solid white; padding: 10px; border-radius: 10px;")
            label = QLabel(f"{chr(65+idx)}) {peso}kg - {valor}")
            label.setAlignment(Qt.AlignCenter)
            box_layout = QVBoxLayout()
            box_layout.addWidget(label)
            box.setLayout(box_layout)
            self.grid.addWidget(box, idx // 5, idx % 5)

    def add_item(self):
        p, v = self.peso_in.value(), self.val_in.value()
        self.items.append((p, v))
        self.draw_items()
        self.res.append(f"🆕 Ítem añadido ➜ Peso={p}, Valor={v}")

    def clear(self):
        self.items = []
        self.draw_items()
        self.res.clear()
        self.res.append("🚫 Lista de ítems reiniciada")

    def run(self):
        algo = self.combo.currentText()
        if not self.items:
            self.res.setText("⚠️ Añade al menos un ítem")
            return

        if algo == "Voraz": sol, val = self.greedy()
        elif algo == "Local": sol, val = self.local_search()
        elif algo == "Tabú": sol, val = self.taboo_search()
        elif algo == "Enfriamiento": sol, val = self.simulated_annealing()
        elif algo == "Gradiente": sol, val = self.gradient_descent()
        elif algo == "Hormigas": sol, val = self.ant_colony()
        elif algo == "Genético": sol, val = self.genetic_algorithm()
        else: sol, val = [], 0

        self.res.append(f"\n✅ Método: {algo}")
        self.res.append("🎯 Solución obtenida:")
        for peso, valor in sol:
            self.res.append(f"• Peso: {peso} - Valor: {valor}")
        self.res.append(f"💰 Valor total: {val}")

    def greedy(self):
        items = sorted(self.items, key=lambda iv: iv[1] / iv[0], reverse=True)
        sol = []; val = 0; cap = self.capacidad
        for p, v in items:
            if p <= cap: sol.append((p, v)); cap -= p; val += v
        return sol, val

    def fitness(self, sel):
        total = 0; cap = self.capacidad
        for i in range(len(self.items)):
            if sel[i] == 1:
                total += self.items[i][1]; cap -= self.items[i][0]
                if cap < 0: return -1
        return total

    def random_sol(self):
        n = len(self.items)
        return [random.choice([0, 1]) for _ in range(n)]

    def fix(self, sol):
        cap = self.capacidad
        for i in range(len(sol)):
            if sol[i] == 1:
                p = self.items[i][0]
                if p <= cap: cap -= p
                else: sol[i] = 0
        return sol

    def local_search(self):
        sol = self.fix(self.random_sol()); best = self.fitness(sol); improved = True
        while improved:
            improved = False
            for i in range(len(sol)):
                nsol = sol[:]; nsol[i] = 1 - nsol[i]
                nsol = self.fix(nsol); fv = self.fitness(nsol)
                if fv > best: sol, best, improved = nsol, fv, True; break
        return [self.items[i] for i in range(len(sol)) if sol[i]], best

    def taboo_search(self):
        sol = self.fix(self.random_sol()); best = sol[:]; best_val = self.fitness(sol)
        tabu = []; it = 0
        while it < 50:
            neighbors = []
            for i in range(len(sol)):
                ns = sol[:]; ns[i] = 1 - ns[i]; neighbors.append(ns)
            neighbors = [self.fix(n) for n in neighbors]
            neighbors = sorted(neighbors, key=lambda s: self.fitness(s), reverse=True)
            for cand in neighbors:
                if cand not in tabu:
                    sol = cand; break
            val = self.fitness(sol)
            if val > best_val: best, best_val = sol[:], val
            tabu.append(sol[:])
            if len(tabu) > 10: tabu.pop(0)
            it += 1
        return [self.items[i] for i in range(len(best)) if best[i]], best_val

    def simulated_annealing(self):
        sol = self.fix(self.random_sol()); best_sol = sol[:]; best_val = self.fitness(sol)
        T = 100.0; alpha = 0.95
        while T > 0.1:
            i = random.randrange(len(sol))
            ns = sol[:]; ns[i] = 1 - ns[i]; ns = self.fix(ns)
            f0 = self.fitness(sol); f1 = self.fitness(ns)
            if f1 > f0 or random.random() < math.exp((f1 - f0) / T): sol = ns
            if self.fitness(sol) > best_val: best_sol, best_val = sol[:], self.fitness(sol)
            T *= alpha
        return [self.items[i] for i in range(len(best_sol)) if best_sol[i]], best_val

    def gradient_descent(self):
        sol = self.fix(self.random_sol()); best_val = self.fitness(sol)
        improved = True
        while improved:
            improved = False
            for i in range(len(sol)):
                ns = sol[:]; ns[i] = 1 - ns[i]; ns = self.fix(ns)
                fv = self.fitness(ns)
                if fv > best_val: sol, best_val, improved = ns, fv, True; break
        return [self.items[i] for i in range(len(sol)) if sol[i]], best_val

    def ant_colony(self):
        n = len(self.items); pher = np.ones(n); best_val = -1
        for _ in range(30):
            sol = [0] * n; cap = self.capacidad
            probs = pher / pher.sum()
            for i in range(n):
                if random.random() < probs[i] and cap >= self.items[i][0]:
                    sol[i] = 1; cap -= self.items[i][0]
            fv = self.fitness(sol)
            if fv > best_val: best_val = fv; best_sol = sol[:]
            pher = pher * 0.9
            for i in range(n):
                if best_sol[i] == 1: pher[i] += 1
        return [self.items[i] for i in range(len(best_sol)) if best_sol[i]], best_val

    def genetic_algorithm(self):
        n = len(self.items)
        pop = [self.fix(self.random_sol()) for _ in range(20)]
        def select(): return sorted(pop, key=lambda s: self.fitness(s), reverse=True)[:2]
        for _ in range(50):
            a, b = select(); cut = random.randrange(n)
            child = self.fix(a[:cut] + b[cut:])
            if random.random() < 0.1:
                idx = random.randrange(n); child[idx] = 1 - child[idx]
            pop.append(child)
            pop = sorted(pop, key=lambda s: self.fitness(s), reverse=True)[:20]
        best = pop[0]
        return [self.items[i] for i in range(n) if best[i]], self.fitness(best)
    
    def volver(self):
        from Modulos.menu_general.menu_general import MenuGeneral
        self.menu = MenuGeneral()
        self.menu.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Algoritmos_Heuristicos()
    win.show()
    sys.exit(app.exec_())
