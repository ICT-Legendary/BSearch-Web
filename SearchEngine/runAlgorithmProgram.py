# -*- coding: utf-8 -*-
import multiprocessing
import subprocess
import time
import os
import json

# def func_A(no):
# 	print "func_A_{} start".format(no)
# 	time.sleep(3)
# 	print "func_A_{} ended".format(no)

# def func_B():
# 	print "func_B start"
# 	time.sleep(10)
# 	print "func_B ended"

def func_A(configFile):
	# cmd = "./mkindex configFiles/"+configFile
	cmd = "./mkindex ./"+configFile
	p = subprocess.Popen(cmd, shell=True, cwd="/home/polly/GitHub/libdivsufsort-hdfs/build/examples", stdout=subprocess.PIPE)
	result = json.loads(p.stdout.read())
	print result
	# if result["code"]==0:
	# 	#os.system('ls -l')
	# 	subprocess.Popen("ls -l", shell=True)

def main():
	#cmd = "/home/polly/GitHub/libdivsufsort/build/examples/mkindex"
	#cfg = "/home/polly/GitHub/libdivsufsort/build/examples/config.json"
	cfg_list = ["config.json", "config-2.json"]
	pool = multiprocessing.Pool(processes=24)
	start = time.time()
	for cfg in cfg_list:
		pool.apply_async(func_A, (cfg,))
	pool.close()
	pool.join()
	end = time.time()
	print "Total time cost: {} s".format(end-start)

if __name__ == '__main__':
	main()










	# pool = multiprocessing.Pool(processes=10)
	# for i in range(10):
	# 	pool.apply_async(func_A, (i,))
	# print "wait for processes run"
	# pool.close()
	# pool.join()
	# print "all processes over!!"
		#sp = subprocess.Popen('python process_A.py',shell=True, stdout=subprocess.PIPE)
		#sp.wait()
		#print sp.communicate()
	
