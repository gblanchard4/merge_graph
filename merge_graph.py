#!/usr/bin/env python
import argparse
import matplotlib
import matplotlib.pyplot as plt
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
	return [average_list(position) for position in transpose(quality_to_2d(file))]

if __name__ == '__main__':
	#  Argument Parser
	parser = argparse.ArgumentParser(description='PCR Error Simulation')

	# Forward
	parser.add_argument('-f','--forward',dest='forward', required=True, help='forward read file')
	# Reverse
	parser.add_argument('-r','--reverse',dest='reverse', required=True, help='reverse read file')
	# Amplicon
	parser.add_argument('-a','--amplicon',dest='amplicon', required=True, help='The desired amplicon length')
	
	# Parse arguments
	args = parser.parse_args()
	forward = args.forward
	reverse = args.reverse
	amplicon = int(args.amplicon)


	forward_average = process_file(forward)
	reverse_average = process_file(reverse)
	reverse_average.reverse()

	# Make X,Y coords
	fx = list(xrange(1,len(forward_average)+1))
	fy = forward_average

	rx = list(xrange(amplicon-len(reverse_average)+1,amplicon+1))
	ry = reverse_average
	
	plt.plot(fx, fy)
	plt.plot(rx, ry)
	plt.savefig("merge.png")







