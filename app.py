import os
import os.path
from distutils.dir_util import mkpath, copy_tree, remove_tree
from flask import Flask, render_template
from wave_function_processing import Grid, GRID_PX_SIZE, TILE_PX_SIZE, \
                                     IMAGE_DICT, NEIGHBOURS_DICT

TILES_FOLDER = "tiles/"
OUTPUT_FOLDER = "output/"

# Creating cache folder for users generation
WORKING_FOLDER = "tmp/"
WORKING_TILES_FOLDER = os.path.join(WORKING_FOLDER, TILES_FOLDER)
WORKING_OUTPUT_FOLDER = os.path.join(WORKING_FOLDER, OUTPUT_FOLDER)

remove_tree(WORKING_FOLDER)
mkpath(WORKING_FOLDER)
copy_tree(TILES_FOLDER, WORKING_TILES_FOLDER)
copy_tree(OUTPUT_FOLDER, WORKING_OUTPUT_FOLDER)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(WORKING_FOLDER, OUTPUT_FOLDER)
grid = Grid(GRID_PX_SIZE, TILE_PX_SIZE, IMAGE_DICT, NEIGHBOURS_DICT)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def show_index():
    # Introduction + links to other endpoints
    return render_template("index.html")


@app.route('grid', methods=['GET'])
def show_grid():
    # Showing current state of grid
    filename = "cur_grid.png"
    grid.save_png(filename, folder="WORKING_OUTPUT_FOLDER")
    return
