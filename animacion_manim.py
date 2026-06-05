from manim import *
import math

class AproximacionPetróleo(Scene):

    def construct(self):

        self.camera.background_color = "#0f1115"

        title = Text(
            "Aproximación Lineal en Tanques de Petróleo",
            font_size=34,
            color=WHITE
        ).to_edge(UP)

        subtitle = Text(
            "Estimación del volumen en un tanque cilíndrico",
            font_size=24,
            color=GRAY_A
        ).next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        # Parámetros del tanque
        r = 6

        f = lambda h: h**2 + 2*h

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 400, 50],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(LEFT)

        self.play(Create(axes))

        graph = axes.plot(f, color=BLUE, stroke_width=4)
        self.play(Create(graph))

        # Punto base
        h0 = 2
        V0 = f(h0)

        dot = Dot(axes.c2p(h0, V0), color=RED)
        label = Text("h₀", font_size=24, color=RED).next_to(dot, UP)

        self.play(FadeIn(dot), Write(label))

        # Derivada (constante)
        slope = 2*h0 + 2
        tangent = axes.plot(
            lambda x: V0 + slope * (x - h0),
            color=YELLOW
        )

        self.play(Create(tangent))

        # Nuevo punto
        h1 = h0 + 2

        real = f(h1)
        aprox = V0 + slope * (h1 - h0)
        error = abs(real - aprox)

        self.play(
            FadeIn(Dot(axes.c2p(h1, real), color=GREEN)),
            FadeIn(Dot(axes.c2p(h1, aprox), color=ORANGE))
        )

        panel = VGroup(
            Text(f"h₀ = {h0}", font_size=22),
            Text(f"h₁ = {h1}", font_size=22),
            Text(f"Real = {real:.2f}", font_size=22, color=BLUE),
            Text(f"Aprox = {aprox:.2f}", font_size=22, color=YELLOW),
            Text(f"Error = {error:.2f}", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT)

        box = SurroundingRectangle(panel, buff=0.3)
        box.set_fill("#1c1f26", opacity=0.8)

        self.play(Create(box), FadeIn(panel))

        conclusion = Text(
            "La aproximación lineal es útil para estimar volumen rápidamente",
            font_size=22,
            color=GRAY_A
        ).to_edge(DOWN)

        self.play(Write(conclusion))

        self.wait(3)