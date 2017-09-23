#!/usr/bin/env python

import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f

filepath = sys.argv[1]
with open(filepath) as f:
	data = f.readlines()
	for line in data:
		s = line.rstrip('\n')
		s1 = '<option value=\"'+s+'\">'+s+"</option>"
		print s1

sys.stdout = orig_stdout
f.close()