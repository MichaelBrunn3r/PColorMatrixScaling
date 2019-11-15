## ABOUT
This little tool is supposed to help when scaling color matrices by hand.<br>
Currently supported Interpolations:
- Nearest Neighbor
- Bilinear

## Usage
`python cm_scaling.py [-h] {scale}`<br>
Arguments:
- `scale`: The subcommand to run

### Subcommand Scale
Scales the input Color Matrix

Usage: `python cm_scaling.py scale [-h] [string] size [-i {nn,bilin}] [-p]`
Arguments:
- `string`: A square matrix containing color values. Values seperated by ';', rows by '\\n'
- `size`: The target size of the matrix
- `-i`: The type of interpolation to use
  - `nn`: Nearest-Neighbor Interpolation
  - `bilin`: Bilinear Interpolation
- `-p`: Pretty-print resulting matrix using pretty-table

## Examples
- Scale matrix of size 3 to matrix of size 4, using Nearest-Neighbor Interpolation:
  `python cm_scaling.py scale "1;2;3\n4;5;6\n7;8;9" 4 -i nn`
  ```
  1;2;2;3
  4;5;5;6
  4;5;5;6
  7;8;8;9
  ```
- Scale matrix of size 3 to size 4, Bilinear Interpolation, pretty-print:
  `python cm_scaling.py scale "1;2;3\n4;5;6\n7;8;9" 4 -i bilin -p`
  ```
  +---+---+---+---+
  | 1 | 2 | 3 | 3 |
  +---+---+---+---+
  | 3 | 4 | 5 | 5 |
  +---+---+---+---+
  | 5 | 6 | 7 | 7 |
  +---+---+---+---+
  | 7 | 8 | 9 | 9 |
  +---+---+---+---+
  ```
