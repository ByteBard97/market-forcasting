"""
Convolution animation showing impulse response sliding across marketing signal.
Based on 3Blue1Brown's convolution visualization style.
"""
from manim import *
import numpy as np


class ConvolutionAnimation(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = "#00000000"  # Transparent background
    def construct(self):
        # Define impulse response (build-up, peak, decay)
        ir_lags = np.array([0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0,
                            1.0, 0.9, 0.7, 0.5, 0.3, 0.2, 0.1])

        # Define marketing signal (flat baseline with a peak)
        days = 40
        marketing = np.ones(days)
        marketing[15:26] = 2.0  # Marketing campaign from day 15 to 25

        # Create axes
        axes = Axes(
            x_range=[0, days, 5],
            y_range=[0, 2.5, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"color": BLUE},
            tips=False,
        )

        # Labels
        x_label = axes.get_x_axis_label("Days", edge=DOWN, direction=DOWN)
        title = Text("Impulse Response Convolution", font_size=36).to_edge(UP)

        # Marketing signal plot
        marketing_graph = axes.plot_line_graph(
            x_values=list(range(days)),
            y_values=marketing,
            add_vertex_dots=False,
            line_color=BLUE_C,
        )

        marketing_label = Text("Marketing Spend", font_size=24, color=BLUE_C)
        marketing_label.next_to(axes, RIGHT, buff=0.5).shift(UP * 1.5)

        # Show initial setup
        self.play(Create(axes), Write(x_label), Write(title))
        self.play(Create(marketing_graph), Write(marketing_label))
        self.wait(0.5)

        # Create impulse response kernel
        ir_x = list(range(len(ir_lags)))

        # Create bars for impulse response
        bars = VGroup()
        for i, val in enumerate(ir_lags):
            bar = Rectangle(
                width=0.15,
                height=val * 1.5,
                fill_color=GREEN,
                fill_opacity=0.7,
                stroke_width=1,
                stroke_color=WHITE,
            )
            bar.move_to(axes.c2p(i, val * 0.75))
            bars.add(bar)

        ir_label = Text("Impulse Response", font_size=24, color=GREEN)
        ir_label.next_to(axes, RIGHT, buff=0.5).shift(UP * 0.5)

        # Show impulse response
        self.play(Create(bars), Write(ir_label))
        self.wait(0.5)

        # Create output curve that will be built up
        output = np.zeros(days)

        output_dots = VGroup()

        # Animate sliding window
        for t in range(0, days - len(ir_lags) + 1, 2):  # Step by 2 for speed
            # Calculate output value at this position
            for lag in range(len(ir_lags)):
                if t + lag < days:
                    output[t + lag] += marketing[t] * ir_lags[lag]

            # Move the impulse response bars
            new_bars = VGroup()
            for i, val in enumerate(ir_lags):
                bar = Rectangle(
                    width=0.15,
                    height=val * 1.5,
                    fill_color=GREEN,
                    fill_opacity=0.7,
                    stroke_width=1,
                    stroke_color=WHITE,
                )
                bar.move_to(axes.c2p(t + i, val * 0.75))
                new_bars.add(bar)

            # Create highlight window
            window = Rectangle(
                width=len(ir_lags) * 0.4,
                height=2.5,
                stroke_color=YELLOW,
                stroke_width=2,
                fill_opacity=0.1,
                fill_color=YELLOW,
            )
            window.move_to(axes.c2p(t + len(ir_lags) / 2, 1.25))

            # Add output dots for computed values
            for i in range(max(0, t - 5), min(days, t + len(ir_lags))):
                if output[i] > 0:
                    dot = Dot(
                        point=axes.c2p(i, output[i] + 0.5),
                        color=PURPLE,
                        radius=0.04,
                    )
                    output_dots.add(dot)

            # Animate the movement
            if t == 0:
                self.play(
                    Create(window),
                    run_time=0.3,
                )
            else:
                self.play(
                    Transform(bars, new_bars),
                    FadeOut(window),
                    run_time=0.2,
                )
                window = Rectangle(
                    width=len(ir_lags) * 0.4,
                    height=2.5,
                    stroke_color=YELLOW,
                    stroke_width=2,
                    fill_opacity=0.1,
                    fill_color=YELLOW,
                )
                window.move_to(axes.c2p(t + len(ir_lags) / 2, 1.25))
                self.play(Create(window), run_time=0.2)

            # Show output dots accumulating
            if len(output_dots) > 0:
                self.add(output_dots[-min(5, len(output_dots)):])

        # Clean up and show final output curve
        self.play(FadeOut(window), FadeOut(bars))

        # Create smooth output curve
        output_graph = axes.plot_line_graph(
            x_values=list(range(days)),
            y_values=[v + 0.5 for v in output],
            add_vertex_dots=False,
            line_color=PURPLE,
        )

        output_label = Text("Demand Response", font_size=24, color=PURPLE)
        output_label.next_to(axes, RIGHT, buff=0.5).shift(DOWN * 0.5)

        self.play(
            Create(output_graph),
            Write(output_label),
            FadeOut(output_dots),
        )

        # Highlight the temporal lag
        arrow = Arrow(
            start=axes.c2p(20, 2.2),
            end=axes.c2p(28, 2.2),
            color=YELLOW,
            buff=0.1,
            stroke_width=4,
        )
        lag_label = Text("~8 day lag", font_size=20, color=YELLOW)
        lag_label.next_to(arrow, UP, buff=0.1)

        self.play(Create(arrow), Write(lag_label))
        self.wait(2)


if __name__ == "__main__":
    # Render the scene
    # Run with: manim -pql convolution_animation.py ConvolutionAnimation
    pass
