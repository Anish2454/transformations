from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix -
	 scale: create a scale matrix,
	    then multiply the transform matrix by the scale matrix -
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix,
	    then multiply the transform matrix by the translation matrix -
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 apply: apply the current transformation matrix to the
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""

def line_command(args, edge_matrix, transform_matrix, screen, color):
    args = [int(i) for i in args]
    return add_edge(edge_matrix, args[0], args[1], args[2], args[3], args[4], args[5])

def ident_command(args, edge_matrix, transform_matrix, screen, color):
    return ident(transform_matrix)

def scale_command(args, edge_matrix, transform_matrix, screen, color):
    args = [float(i) for i in args]
    scale_matrix = make_scale(args[0], args[1], args[2])
    #print_matrix(scale_matrix)
    matrix_mult(scale_matrix, transform_matrix)
    #print_matrix(transform_matrix)
    #print_matrix(edge_matrix)

def move_command(args, edge_matrix, transform_matrix, screen, color):
    args = [int(i) for i in args]
    #print args[0]
    #print args[1]
    #print args[2]
    move_matrix = make_translate(args[0], args[1], args[2])
    #print_matrix(move_matrix)
    return matrix_mult(move_matrix, transform_matrix)
    #print_matrix(transform_matrix)

def rotate_command(args, edge_matrix, transform_matrix, screen, color):
    rotate_funcs = {"x": make_rotX, "y": make_rotY, "z": make_rotZ}
    rotate_matrix = rotate_funcs[args[0]](float(args[1]))
    return matrix_mult(rotate_matrix, transform_matrix)

def apply_command(args, edge_matrix, transform_matrix, screen, color):
    matrix_mult(transform_matrix, edge_matrix)
    #print_matrix(edge_matrix)

def display_command(args, edge_matrix, transform_matrix, screen, color):
    #print_matrix(transform_matrix)
    draw_lines(edge_matrix, screen, color)
    display(screen)
    clear_screen(screen)

def save_command(args, edge_matrix, transform_matrix, screen, color):
    draw_lines(edge_matrix, screen, color)
    return save_extension(screen, args[0])


func_dict = {"line": line_command, "ident": ident_command, "scale": scale_command, "move": move_command, "rotate": rotate_command, "apply": apply_command, "display": display_command, "save": save_command}

def parse_file( fname, points, transform, screen, color ):
    with open(fname) as f:
        curr_command = ""
        need_commands = False
        for line in f:
            line = line.rstrip()
            args = line.split(" ")
            if need_commands:
                func_dict[curr_command](args, points, transform, screen, color)
                need_commands = False
            if line in func_dict:
                curr_command = line
                need_commands = True
            if line == "quit":
                return
        if need_commands:
            func_dict[curr_command](args, points, transform, screen, color)
