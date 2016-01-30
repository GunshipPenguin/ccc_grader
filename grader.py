# CCC grader

from os import listdir, devnull
from os.path import isfile, isdir, join
from subprocess import Popen, check_output, PIPE, CalledProcessError, STDOUT
from argparse import ArgumentParser

# Argument handling
parser = ArgumentParser(prog='grader.py')
parser.add_argument("source", action="store", help="Path to source file, eg. /home/user/solution.py")
parser.add_argument("year", action="store", help="Year of question, eg. 2010, 2012")
parser.add_argument("problem", action="store", help="Problem number, eg. j1, s1, j4, s4")
parser.add_argument("--data_path", action="store", help="Path to data files (defaults to ./data)")
parser.add_argument("--no_suppress_errors", action="store_true", help="Do not suppress error messages")
parser.add_argument("--no_timeout", action="store_true", help="Do not timeout after 5 seconds")
args = parser.parse_args()

# Exif if the source file does not exist
if not isfile(args.source):
	print "Source file " + args.source + " does not exist"
	exit(2)

# Set the data path
if args.data_path == None:
	data_path = join("data", args.year)
else:
	data_path = args.data_path

# Exit if the data path does not exist
if not isdir(data_path):
	print "Data path does not exist"
	exit(0)

# Exit if the data path does not contain the data for the requested problem
if not isdir(join(data_path, args.problem)):
	print "Could not find problem " + args.year + "/"+ args.problem
	exit(2)

# Create a list of input/output file pairs
data_path = join(data_path, args.problem)
files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
files.sort()
io_file_pairs = []
for f in files:
	if f.endswith(".in"):
		output_file = f.rsplit(".", 1)[0] + ".out"
		if output_file in files:
			io_file_pairs.append([f, output_file])
		else:
			print f + " - Warning input file with no corresponding output"

# Execute all tests
for i in io_file_pairs:
	input_info = Popen(("cat", join(data_path, i[0])), stdout=PIPE)
	
	if args.no_timeout:
		command = ["python", args.source]
	else:
		command = ["timeout", "5", "python", args.source]
	
	try:
		if args.no_suppress_errors:
			received_output = check_output(command, stdin=input_info.stdout)
		else:
			FNULL = open(devnull, 'w')
			received_output = check_output(command, stdin=input_info.stdout, stderr=FNULL)
	except CalledProcessError as err:
		if err.returncode == 124:
			print i[0] + " TIMEOUT"
		else:
			print i[0] + " ERROR"
		continue
	expected_output = check_output(("cat", join(data_path, i[1])))
	if received_output == expected_output:
		print i[0] + " PASS"
	else:
		print i[0] + " FAIL"
