from manim import *
import math

class AproximacionPetroleo(Scene):

    def construct(self):
        self.camera.background_color = "#0f1115"

  
        
        # 1. LA FUNCIÓN DEL VOLUMEN (Forma de la curva)
        # Define cómo crece el volumen del tanque. 
        f = lambda h: h**2 + 5*h

        # 2. RANGO DE LOS EJES (El "zoom" de la cámara)
        # x_range = [inicio, fin, saltos en la cuadrícula]
        # y_range = [inicio, fin, saltos en la cuadrícula]
        rango_x = [0, 8, 1]
        rango_y = [0, 100, 10]

        # 3. PUNTOS DE APROXIMACIÓN (El origen y el destino)
        # h0 (Punto Base): Es donde la recta amarilla toca a la curva azul.
        # > EJEMPLOS PARA CAMBIAR: 1.0, 2.0, 3.0
        # > LÍMITE: No pongas más de 5, o la gráfica se saldrá de la pantalla hacia arriba.
        h0 = 2.0  
        
        # h1 (Nuevo Punto): Es el destino, hasta donde llega la línea roja (Delta x).
        # > EJEMPLO ALTA PRECISIÓN: Pon h1 = 2.2. Verás que el error es mínimo (casi 0).
        # > EJEMPLO BAJA PRECISIÓN: Pon h1 = 7.0. Verás que la separación (error) es enorme.
        # > LÍMITE: Debe ser mayor a h0, pero menor a 8 (que es el fin de tu rango_x).
        h1 = 7.0

        # ==========================================================
        # FIN DE ZONA DE EXPERIMENTACIÓN (El resto es lógica y diseño visual)
        # ==========================================================

        # --- TÍTULOS ---
        title = Text(
            "APROXIMACIÓN LINEAL EN TANQUES DE PETRÓLEO",
            font_size=28, weight=BOLD, color=WHITE
        ).to_edge(UP, buff=0.4)

        subtitle = Text(
            "Estimación del volumen en un tanque cilíndrico",
            font_size=20, color=GRAY_A
        ).next_to(title, DOWN, buff=0.15)

        self.play(Write(title), FadeIn(subtitle))
        self.wait(0.5)

        # --- EJES ---
        axes = Axes(
            x_range=rango_x, y_range=rango_y,
            x_length=6.5, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 16}
        ).to_corner(DL, buff=0.8)
        
        x_label = Text("Altura h", font_size=16).next_to(axes.x_axis, DOWN, buff=0.4)
        y_label = Text("Volumen V", font_size=16).next_to(axes.y_axis, LEFT, buff=0.4).rotate(PI/2)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        # --- FUNCIÓN Y TANGENTE ---
        # 1. Dibujamos la curva azul (Realidad)
        graph = axes.plot(f, color=BLUE, stroke_width=3)
        func_label = Tex("$f(h) = h^2 + 5h$", color=BLUE, font_size=20).next_to(axes.c2p(rango_x[1]-1, f(rango_x[1]-1)), UL, buff=0.2).add_background_rectangle(color="#0f1115", opacity=0.8)
        
        # 2. Calculamos la recta tangente (Aproximación)
        V0 = f(h0) # Volumen inicial exacto
        
        # CORRECCIÓN MATEMÁTICA: La derivada de h^2 + 5h es 2h + 5. 
        # Esto asegura que la recta amarilla se apoye perfectamente en la curva azul.
        slope = 2*h0 + 5 
        
        # Dibujamos la recta amarilla
        tangent = axes.plot(lambda x: V0 + slope * (x - h0), x_range=[0.5, rango_x[1]-0.5], color=YELLOW, stroke_width=2)
        
        self.play(Create(graph), FadeIn(func_label))
        self.play(Create(tangent))

        # --- CÁLCULOS DE LOS DELTAS (La matemática detrás de escena) ---
        real = f(h1)                         # Y real (en la curva)
        aprox = V0 + slope * (h1 - h0)       # Y aproximado (en la recta)
        error_val = abs(real - aprox)        # El error es la diferencia
        
        delta_h = h1 - h0                    # Delta X (Avance horizontal)
        dv_val = slope * delta_h             # dy (Subida de la recta amarilla)

        # Puntos de colores que marcan los destinos
        dot_base = Dot(axes.c2p(h0, V0), color=RED, radius=0.06)
        dot_aprox = Dot(axes.c2p(h1, aprox), color=ORANGE, radius=0.06)
        dot_real = Dot(axes.c2p(h1, real), color=GREEN, radius=0.06)

        lbl_base = Tex(f"$h_0 = {h0}$", font_size=18, color=RED).next_to(dot_base, UP+LEFT, buff=0.1).add_background_rectangle(color="#0f1115", opacity=0.8)
        
        self.play(FadeIn(dot_base), FadeIn(lbl_base))
        self.play(FadeIn(dot_aprox), FadeIn(dot_real))

        # --- TRIÁNGULO DE APROXIMACIÓN (Aquí se dibuja Delta x, dy y Delta y) ---
        
        # Coordenadas base para las líneas
        p_0 = axes.c2p(h0, V0)             # Esquina inicial (h0, V0)
        p_base_escalon = axes.c2p(h1, V0)  # Esquina inferior derecha (Avance horizontal)
        p_aprox_coord = axes.c2p(h1, aprox)# Esquina superior de la recta amarilla
        p_real_coord = axes.c2p(h1, real)  # Esquina superior de la curva azul

        # -> AQUÍ DIBUJAMOS DELTA X (Línea Roja Horizontal)
        # Va desde el inicio hasta el nuevo punto h1. Representa tu "Avance".
        line_dh = DashedLine(p_0, p_base_escalon, color=RED, stroke_width=2)
        lbl_dh = Tex(f"$\\Delta h = {delta_h:.2f}$", font_size=16, color=RED).next_to(line_dh, DOWN, buff=0.1).add_background_rectangle(color="#0f1115", opacity=0.8)

        # -> AQUÍ DIBUJAMOS "dy" (Línea Amarilla Vertical)
        # Sube desde el suelo del triángulo hasta la recta tangente. Representa tu "Estimación".
        line_dy = DashedLine(p_base_escalon, p_aprox_coord, color=YELLOW, stroke_width=2)
        lbl_dV = Tex(f"$dV = {dv_val:.2f}$", font_size=16, color=YELLOW).next_to(line_dy, RIGHT, buff=0.1).add_background_rectangle(color="#0f1115", opacity=0.8)

        # -> AQUÍ DIBUJAMOS "Delta y" REAL (Línea Verde Vertical y Llave)
        # Sube desde el suelo del triángulo hasta la curva azul. Representa la "Realidad".
        line_real = DashedLine(p_aprox_coord, p_real_coord, color=GREEN, stroke_width=2)
        brace_real = BraceBetweenPoints(p_real_coord, p_base_escalon, direction=LEFT, color=GREEN, buff=0.1)
        
        # Control de colisiones visuales: Si el error es muy pequeño, no dibujamos la llave verde para que no se vea amontonado.
        if real - V0 > 1:
            lbl_real = brace_real.get_tex(f"\\Delta V_{{real}} = {(real-V0):.2f}").scale(0.5).add_background_rectangle(color="#0f1115", opacity=0.8)
            self.play(Create(line_dh), FadeIn(lbl_dh))
            self.play(Create(line_dy), FadeIn(lbl_dV))
            self.play(Create(line_real), GrowFromCenter(brace_real), FadeIn(lbl_real))
        else:
            self.play(Create(line_dh), FadeIn(lbl_dh))
            self.play(Create(line_dy), FadeIn(lbl_dV))

        # --- TABLA DE DATOS (Muestra los números en un panel a la derecha) ---
        labels = [
            "Punto Base $h_0$", "Nuevo Punto $h_1$", "Incremento $\\Delta h$",
            "Diferencial $dV$", "Inc. Real $\\Delta V_{real}$",
            "Volumen Real $V(h_1)$", "Vol. Aprox $V_{aprox}$", "Error"
        ]
        values = [f"{h0:.2f}", f"{h1:.2f}", f"{delta_h:.2f}", f"{dv_val:.2f}", f"{(real-V0):.2f}", f"{real:.2f}", f"{aprox:.2f}", f"{error_val:.2f}"]
        colors = [RED, WHITE, RED, YELLOW, GREEN, GREEN, ORANGE, RED]

        col_labels = VGroup(*[Tex(l, font_size=18, color=GRAY_B) for l in labels]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        col_vals = VGroup(*[Text(v, font_size=16, color=c) for v, c in zip(values, colors)]).arrange(DOWN, aligned_edge=RIGHT, buff=0.2)

        for l, v in zip(col_labels, col_vals): v.set_y(l.get_y())
        col_vals.next_to(col_labels, RIGHT, buff=0.8)
        for l, v in zip(col_labels, col_vals): v.set_y(l.get_y())

        t_param = Text("PARÁMETRO", font_size=14, color=WHITE).next_to(col_labels, UP, buff=0.4, aligned_edge=LEFT)
        t_valor = Text("VALOR", font_size=14, color=WHITE).set_y(t_param.get_y()).align_to(col_vals, RIGHT)

        table = VGroup(t_param, t_valor, col_labels, col_vals).to_edge(RIGHT, buff=0.8).shift(DOWN*0.2)
        table_bg = SurroundingRectangle(table, color=DARK_GRAY, stroke_width=1, fill_color="#14161a", fill_opacity=1, buff=0.25)
        line_sep = Line(table_bg.get_left(), table_bg.get_right(), color=DARK_GRAY, stroke_width=1).set_y(t_param.get_bottom()[1] - 0.15)

        self.play(FadeIn(table_bg), Create(line_sep), FadeIn(table))

        # --- CONCLUSIÓN ---
        conclusion = Text(
            "Acercar h₁ a h₀ reduce drásticamente \nel error de aproximación." if error_val < 2 else "La aproximación lineal pierde precisión \nsi nos alejamos mucho del punto base.",
            font_size=16,
            color=GRAY_A
        ).next_to(table_bg, DOWN, buff=0.4)

        self.play(Write(conclusion))

        self.wait(4)