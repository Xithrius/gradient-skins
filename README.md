# Gradient skins

Generate gradient Minecraft skins with ease.

## Setup and run

Install [uv](https://docs.astral.sh/uv/), and make sure it is in your `PATH` environment variable.

Run `uv run gradient_skins.py --help` for argument help.

Example of creating a gradient skin at `test.png` of the RGB values from `(8, 159, 143)` to `(42, 72, 88)`:

```
uv run gradient_skins.py test.png 8,159,143 42,72,88
```
