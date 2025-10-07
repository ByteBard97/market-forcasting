#!/bin/bash
# Render manim animation using Docker

docker run --rm \
  -v "$(pwd)":/manim \
  manimcommunity/manim:stable \
  manim -qm --format=webm --transparent /manim/convolution_animation.py ConvolutionAnimation
