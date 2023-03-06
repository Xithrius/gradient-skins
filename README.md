# Gradient skins

Generate gradient Minecraft skins with ease.

## Setup and run

Install [pdm](https://github.com/pdm-project/pdm), and make sure it is in your PATH environment variable.

Afterwards, run `pdm install` in the cloned github repository.

Run `pdm gen --help` for argument help. Here is an example of outputting a gradient skin to the file `test.png`, from the RGB value of `(8, 159, 143)` to `(42, 72, 88)`:

```
pdm run gen ./test.png "8,159,143" "42,72,88"
```
