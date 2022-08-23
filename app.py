import os
import os.path
from distutils.dir_util import mkpath, copy_tree, remove_tree
from flask import Flask, render_template, url_for
from utils import load_tiles_config
from opencv_run import Grid

GRID_PX_SIZE = 500
TILE_PX_SIZE = 50
TILES_FOLDER = "tiles/circuit_board/"
OUTPUT_FOLDER = "output/"

# Reading config about tiles info
config_path = os.path.join(TILES_FOLDER, "tiles.json")
TILE_LIST = load_tiles_config(config_path, TILE_PX_SIZE, tiles_folder=TILES_FOLDER)

# Creating cache folder for users generation
WORKING_FOLDER = "./tmp/"
WORKING_TILES_FOLDER = os.path.join(WORKING_FOLDER, TILES_FOLDER)
WORKING_OUTPUT_FOLDER = os.path.join(WORKING_FOLDER, OUTPUT_FOLDER)

if os.path.exists(WORKING_FOLDER):
    remove_tree(WORKING_FOLDER)
mkpath(WORKING_FOLDER)
copy_tree(TILES_FOLDER, WORKING_TILES_FOLDER)
copy_tree(OUTPUT_FOLDER, WORKING_OUTPUT_FOLDER)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = WORKING_OUTPUT_FOLDER
grid = Grid(GRID_PX_SIZE, TILE_PX_SIZE, TILE_LIST)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def show_index():
    # Introduction + links to other endpoints
    return render_template("index.html")


@app.route('/grid', methods=['GET'])
def show_grid():
    # Showing current state of grid
    filename = "cur_grid.png"
    grid.save_png(filename, folder="static")
    return render_template("grid.html", grid_image=filename)


@app.route('/collapse', methods=['GET', 'POST'])
def collapse():
    global grid
    # Collapse one cell on the grid and show current state
    try:
        grid.collapse_next_cell()
    except ValueError:
        grid = Grid(GRID_PX_SIZE, TILE_PX_SIZE, TILE_LIST)
    return show_grid()


@app.route('/tiles', methods=['GET', 'POST'])
def show_tiles():
    # Create directory with tiles in 'static' folder
    static_tiles = os.path.join('static', 'tiles')
    if os.path.exists(static_tiles):
        remove_tree(static_tiles)
    mkpath(static_tiles)
    copy_tree(WORKING_TILES_FOLDER, static_tiles)

    # Showing tiles that are used for collapsing
    image_filenames = []
    for f in os.listdir(static_tiles):
        if ".png" in f or ".jpg" in f or ".jpeg" in f:
            image_filenames.append(os.path.join(TILES_FOLDER, f))

    return render_template("tiles.html", tile_images=image_filenames)
