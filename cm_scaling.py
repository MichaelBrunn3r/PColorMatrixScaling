# -*- coding: UTF-8

from fractions import Fraction
import prettytable
from prettytable import PrettyTable
import math

INTERP_NEARES_NEIGHBOUR = 'nn'
INTERP_BILINEAR = 'bilin'
INTERPOLATIONS = [INTERP_NEARES_NEIGHBOUR, INTERP_BILINEAR]

#############
# CLI Utils #
#############

class SquareMatrix(list):
	def __init__(self, rows):
		for row in rows: self.append(row)

		for i,row in enumerate(self):
			if len(row) != len(self): raise Exception("Matrix is of size '{}', but row {} has '{}' entries".format(len(self), i, len(row)))

	def pretty_print(self):
		table = PrettyTable(None)
		for row in self: table.add_row(row)

		table.header = False
		table.hrules = prettytable.ALL
		print(table)

class Rectangle:
	def __init__(self, top, left, bottom, right):
		self.left = left
		self.right = right
		self.top = top 
		self.bottom = bottom

	def __str__(self): return "({},{}) -> ({},{})".format(self.left, self.top, self.right, self.bottom)

	@property
	def width(self): return abs(self.right-self.left)

	@property
	def height(self): return abs(self.top-self.bottom)

	def middle(self): return (self.left+0.5*self.width, self.top+0.5*self.height)

	@property
	def area(self): return self.width * self.height

	def scale(self, factor):
		self.left *= factor
		self.right *= factor
		self.top *= factor
		self.bottom *= factor

	@staticmethod
	def from_points(a, b):
		return Rectangle(min(a[1],b[1]), min(a[0], b[0]), max(a[1], b[1]), max(a[0], b[0]))

def nn_round(num):
	""" Nearest Neighbor rounding"""
	return max(0, num-1 if float(num).is_integer() else math.floor(num))

def scale_matrix_to_size(matrix, size, interpolation):
	rows = [list() for i in range(size)]
	scale = Fraction(len(matrix), size)

	current = Rectangle(0,0,0,0) # Position of the new pixel relative to the original matrix
	# Calculate value of each pixel in new matrix
	for y in range(size): 
		current.top = scale*y
		current.bottom = scale*(y+1)
		for x in range(size):
			current.left = scale*x
			current.right = scale*(x+1)

			if interpolation == INTERP_NEARES_NEIGHBOUR:
				rows[x].append(matrix[int(nn_round(current.middle()[0]))][int(nn_round(current.middle()[1]))])
			elif interpolation == INTERP_BILINEAR:
				val = Fraction(0) # The value of the current pixel in the scaled up matrix
				# Compose new value from overlaid pixels in original, weighted with their relative intersection area
				for y_original in range(math.floor(current.top), math.ceil(current.bottom)):
					for x_original in range(math.floor(current.left), math.ceil(current.right)):
						intersection = Rectangle.from_points([max(x_original,current.left),max(y_original,current.top)], [min(x_original+1,current.right),min(y_original+1,current.bottom)])
						intersection.scale(1/scale) # Scale pixel in original to relative size in new matrix
						val+= intersection.area * matrix[x_original][y_original]
				rows[x].append(math.ceil(val))
	return SquareMatrix(rows)

################
# CLI Commands #
################

def cmd_scale(argv):
	parser = argparse.ArgumentParser(description='Scale input Color Matrix', usage='%(prog)s {} [-h] [string] size [-i {{nn,bilin}}] [-p]'.format(CMD_SCALE))
	parser.add_argument('string', nargs='?', type=str, default=None, help="The color matrix. Values seperated by ';', rows by '\n'")
	parser.add_argument('size', type=int, help="The size to scale the matrix to")
	parser.add_argument('-i', '--interpolation', choices=INTERPOLATIONS, help="The type of interpolation to use")
	parser.add_argument('-p', '--pretty-print', action='store_true', help='Pretty-print resulting matrix')
	args = parser.parse_args(argv)

	# Defaults
	if not args.interpolation: args.interpolation = INTERP_NEARES_NEIGHBOUR

	# Create matrix
	if args.string: rows = bytes(args.string, "utf-8").decode("unicode_escape").split('\n')
	else: rows = sys.stdin.readlines()
	rows = list(map(lambda row: list(map(lambda val: Fraction(val), row.split(';'))), rows))
	matrix = SquareMatrix(rows)

	scaled = scale_matrix_to_size(matrix, args.size, args.interpolation)
	if args.pretty_print:
		scaled.pretty_print()
	else:
		for row in scaled: print(';'.join(map(lambda x:str(x), row)))

########
# Main #
########

CMD_SCALE = 'scale'
COMMANDS = [CMD_SCALE]

if __name__ == '__main__':
	import argparse, sys, re, ast
    
	parser = argparse.ArgumentParser(description='Utility for scaling color matrices')
	parser.add_argument('command', type=str, choices=COMMANDS, help='Subcommand to run')
	args = parser.parse_args(sys.argv[1:2])

	if args.command == CMD_SCALE:
		cmd_scale(sys.argv[2:])