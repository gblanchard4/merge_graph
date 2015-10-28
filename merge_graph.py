#!/usr/bin/env python
import argparse
import matplotlib
import matplotlib.pyplot as plt
import sys
import os
import numpy
matplotlib.use('Agg')

'''
Look at the quality of your merge

'''
def ascii_to_qscore(base):
	return ord(base)-32

def quality_to_2d(file):
	quality_list = []
	with open(file, 'r') as fastq:
		for qscore_line in fastq.readlines()[3::4]:
			quality_list.append(map(ascii_to_qscore, qscore_line.rstrip('\n')))
	return quality_list

def transpose(mylist):
	return list(map(list, zip(*mylist)))

def average_list(mylist):
	return sum(mylist) / float(len(mylist))

def process_file(file):
	avg_std = [(numpy.average(position),numpy.std(position)) for position in transpose(quality_to_2d(file))]
	return map(list, zip(*avg_std))

def process_files(file_list):
	position_list = []
	for file in file_list:
		for index,position in enumerate(transpose(quality_to_2d(file))):
			try:
				position_list[index].extend(position)
			except IndexError:
				position_list.append(position)
	avg_std = [(numpy.average(position),numpy.std(position)) for position in position_list]
	return map(list, zip(*avg_std))
	

if __name__ == '__main__':
	#  Argument Parser
	parser = argparse.ArgumentParser(description='Visualize your merges')

	# Forward
	parser.add_argument('-f','--forward',dest='forward', help='Forward read fastq file')
	# Reverse
	parser.add_argument('-r','--reverse',dest='reverse', help='Reverse read fastq file')
	# Run directory
	parser.add_argument('-i','--run', dest='run_folder', help='A directory of fastqs')
	# Amplicon
	parser.add_argument('-a','--amplicon',dest='amplicon', type=int, required=True, help='The desired amplicon length')
	# Outfile
	parser.add_argument('-o','--output',dest='outfile', required=True, help='The name of the output PNG')
	
	# Parse arguments
	args = parser.parse_args()
	forward = args.forward
	reverse = args.reverse
	amplicon = args.amplicon
	run_folder = args.run_folder
	png = args.outfile

	if forward and reverse:
		forward_average, forward_std = process_file(forward)
		reverse_average, reverse_std = process_file(reverse)
		reverse_average.reverse()
		reverse_std.reverse()
	elif run_folder:
		forward_fastqs = []
		reverse_fastqs = []
		for fastq in os.listdir(run_folder):
			# Get fastqs
			if fastq.endswith('_R1_001.fastq'):
				forward_fastqs.append(run_folder+'/'+fastq)
			if fastq.endswith('_R2_001.fastq'):
				reverse_fastqs.append(run_folder+'/'+fastq)
		forward_average, forward_std = process_files(forward_fastqs)
		reverse_average , reverse_std= process_files(reverse_fastqs)
		reverse_average.reverse()
		reverse_std.reverse()
	else:
		print """Check you arguments
You must enter: A Forward and Reverse file or a Run folder """
		sys.exit()

	# Make X,Y coords
	fx = list(xrange(1,len(forward_average)+1))
	fy = forward_average
	fe = forward_std

	rx = list(xrange(amplicon-len(reverse_average)+1,amplicon+1))
	ry = reverse_average
	re = reverse_std
	
	plt.plot(fx, fy)
	plt.plot(rx, ry)
	plt.errorbar(fx, fy, fe)
	plt.errorbar(rx, ry, re)
	plt.savefig(png)







