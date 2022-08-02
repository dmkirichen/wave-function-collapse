# Wave Function Collapse

This is my own implementation of procedural generation using wave function collapse and Python programming language.

### Requirements
You need to have Python 3.8+ for this project.
Also install the following libraries (e.g. pip install _library_name_):

- numpy
- opencv-contrib-python
- Flask


### Basic Usage

#### Web App

Run ```flask run``` in terminal to start server.

Then you can type ```http://localhost/grid``` in browser to see the current state of the grid.

If you want to update the grid, use ```http://localhost/collapse```.

#### Locally

Run ```python3 wave_function_processing.py```

Then you can press ```n``` to get the next step of generation. 

If you want to save the image and quit, press ```s```.

If you want to just quit, press any other key.
