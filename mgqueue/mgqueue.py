#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import re

import glob
import fcntl

import subprocess
import signal
import logging

from daemonize import Daemonize
import psutil

try:
	import cPickle as pickle
except:
	import pickle

########################################################
# global variables
title = 'mgqueue'
version = '0.2.0'

########################################################
# utilities
def defulat_queue_dir():
	home = os.path.expanduser('~') # $HOME/
	return home + '/.' + title + '/'

def check_pid_file(pid_file):
	try:
		with open( pid_file, 'r' ) as fin:
			pid = int(fin.read())
	except:
		return False
	
	if( not psutil.pid_exists(pid) ):
		os.remove( pid_file )
		return False
	return True

def get_runs(queue_dir = None):
	if( queue_dir == None ):
		queue_dir = defulat_queue_dir()
	pids = glob.glob( queue_dir + '*.pid' )
	
	runs = []
	for pid in pids:
		if( check_pid_file(pid) ):
			runs.append(os.path.splitext(os.path.basename(pid))[0])
	return runs

def ls_queue(queue_dir = None):
	if( queue_dir == None ):
		queue_dir = defulat_queue_dir()
	runs = get_runs( queue_dir )
	pkl = glob.glob( queue_dir + '*.pkl' )
	pkl.sort()
	for file in pkl:
		with open(file, 'rb') as fin:
			queue, prefix = pickle.load( fin )
		queue_name = os.path.splitext(os.path.basename(file))[0]
		
		mark = ' '
		if( prefix != None ):
			mark += '+'
		else:
			mark += ' '

		if( queue_name in runs ):
			mark += '*'
		else:
			mark += ' '

		print( queue_name + mark + ' : ' + str(len(queue)) )


########################################################
# class
class mgqueue(object):
########################################################
## directry setting
	def __init__( self, queue_name, queue_dir = None ): #setUp
		if( queue_dir == None ):
			self.queue_dir = defulat_queue_dir()
		else:
			self.queue_dir = queue_dir
		
		if( not os.access( self.queue_dir, os.F_OK ) ):
			os.mkdir( self.queue_dir )

		self.queue_name = queue_name
		self.cwd = os.getcwd() + '/'
		
		if( self.queue_dir[-1] != '/' ):
			self.queue_dir = self.queue_dir + '/'
		
		self.pid_file = self.queue_dir + queue_name + '.pid'
		self.log_file = self.queue_dir + queue_name + '.log'
		self.pkl_file = self.queue_dir + queue_name + '.pkl'
		self.lck_file = self.queue_dir + queue_name + '.lck'
		
		self.prefix = self.load_prefix()
		
########################################################
## class utilities
	def lock(self): #test_lock_unlock
		fd = open(self.lck_file, 'w')
		fcntl.flock(fd,fcntl.LOCK_EX)
		return fd

	def unlock(self,fd): #test_lock_unlock
		fcntl.flock(fd,fcntl.LOCK_UN)
		fd.close()
		os.remove(self.lck_file)

	def has_prefix(self): #test_prefix
		return self.prefix != None

	def is_run(self): #test_is_run
		self.check_pid_file()
		return os.access( self.pid_file, os.F_OK )
	
	def _load_queue_prefix(self):
		try:
			with open(self.pkl_file, 'rb') as fin:
				queue, prefix = pickle.load( fin )
		except:
			queue = []
			prefix = None
		return queue, prefix

	def load_queue(self): #test_task, 
		queue, prefix = self._load_queue_prefix()
		return queue

	def load_prefix(self): #test_env
		queue, prefix = self._load_queue_prefix()
		return prefix

	def save_queue(self, queue):
		with open(self.pkl_file, 'wb') as fout:
			pickle.dump( [queue, self.prefix], fout )
	
	def save_prefix(self, prefix): #test_prefix
		if( os.access( self.pkl_file, os.F_OK ) ):
			msg = 'Cannot save prefix for existing queue.'
			raise ValueError(msg)
		
		self.prefix = prefix
		self.save_queue( [] )
		msg = self.queue_name + ' is initialized with : ' + self.prefix
		return msg

	def del_pkl_file(self): #test_env
		if( self.prefix == None ):
			os.remove( self.pkl_file )

	def check_pid_file(self):
		return check_pid_file(self.pid_file)


########################################################
## -ls
	def ls_task(self):
		self.check_pid_file()
		queue = self.load_queue()
		
		if( self.has_prefix() ):
			print( 'prefix: ' + self.prefix )
		if( len(queue) > 0 ):
			run_flg = ( self.queue_name in get_runs() )
			for i in range(len(queue)):
				if( i == 0 and run_flg ):
					line = ' * : '
				else:
					line = '{0:2d} : '.format(i)
				
				line = line + ' '.join(queue[i]['cmd'])
				
				try:
					if( os.path.dirname(queue[i]['stdout']) == os.path.dirname(queue[i]['cwd']) ):
						line = line + ' > ' + os.path.basename( queue[i]['stdout'] )
					else:
						line = line + ' > ' + queue[i]['stdout']
				except:
					pass

				try:
					if( os.path.dirname(queue[i]['stderr']) == os.path.dirname(queue[i]['cwd']) ):
						line = line + ' > ' + os.path.basename( queue[i]['stderr'] )
					else:
						line = line + ' 2> ' + queue[i]['stderr']
				except:
					pass

				print(line)
				print( '     ' + queue[i]['cwd'] )
				


########################################################
## 
	def add_task( self, task ):
		fd = self.lock()
		queue = self.load_queue()
		
		queue.append( task )

		self.save_queue( queue )
		self.unlock(fd)
	

########################################################
## -add
	def add_cmd( self, cmd, stdout = '/dev/null', stderr = '/dev/null' ): # test_prefix, test_task
		cwd = self.cwd
		
		task = { 'cmd':cmd, 'cwd':cwd, 'stdout':stdout, 'stderr':stderr }
		self.add_task( task )

		return task, 'Added ' + ' '.join(cmd) + ' to ' + self.queue_name


########################################################
## -remove
	def remove_ind( self, ind ): # test_task
		
		fd = self.lock()
		
		queue = self.load_queue()
		
		if( ind == 0 and self.is_run() ):
			self.unlock(fd)
			msg = 'Cannot remove current task.'
			raise ValueError(msg)
			
		if( ind < 0 or ind >= len(queue) ):
			self.unlock(fd)
			msg = 'Cannot find index: ' + str(ind)
			raise ValueError(msg)

		task = queue.pop(ind)

		self.save_queue(queue)
		self.unlock(fd)
		
		return task, 'Removed index: ' + str(ind) + ' from ' + self.queue_name

########################################################
## -rmall
	def remove_all(self):
		if( self.is_run() ):
			fd = self.lock()
			queue = self.load_queue()
			
			del queue[1:]
			
			self.save_queue(queue)
			self.unlock(fd)
		
		else:
			fd = self.lock()
			queue = self.load_queue()
			
			queue = []
			
			self.save_queue(queue)
			self.unlock(fd)

			self.del_pkl_file()

########################################################
## move
	def move_ind( self, ind, newind ): #test_task
		fd = self.lock()
		queue = self.load_queue()

		if( ind == 0 and self.is_run() ):
			msg = 'Cannot move current task'
			raise ValueError(msg)
			
		elif( ind < 0 or ind >= len(queue) ):
			msg = 'Cannot find index: ' + str(ind) + ' in ' + self.queue_name
			raise ValueError(msg)

		task = queue.pop(ind)
		
		mn = ( 1 if self.is_run() else 0 )
		
		if( newind < mn ):
			newind = mn
		elif( newind > len(queue) ):
			newind = len(queue)
		queue.insert( newind, task )

		self.save_queue(queue)
		self.unlock(fd)
		
		return task, newind, 'task ' + str(ind) + ' is moved to ' + str(ind)
		
########################################################
## -up
	def up_ind( self, ind, n ):
		task, newind, msg = self.move_ind( ind, ind-n )
		return task, newind, 'task ' + str(ind) + ' is moved up to ' + str(newind)


########################################################
## -down
	def down_ind( self, ind, n ): # test_task
		task, newind, msg = self.move_ind( ind, ind+n )
		return task, newind, 'task ' + str(ind) + ' is moved down to ' + str(newind)

########################################################
## -clear
	def clear_file(self): # tearDown
		if( self.is_run() ):
			msg =  'Cannot clear, because it is still running.'
			raise ValueError(msg)
			
		files = glob.glob( self.queue_dir + self.queue_name + '.*' )
		for file in files:
			os.remove(file)
		
		msg = 'Cleared files for ' + self.queue_name
		return msg

########################################################
## -check
	def check_queue(self):
		queue = self.load_queue()
		nerr = 0
		ind = 0
		for task in queue:
			print( str(ind) + ':' )
			if( os.access( task['cwd'], os.X_OK ) ):
				print( ' OK cwd: ' + task['cwd'] )
			else:
				print( '*NG*cwd: ' + task['cwd'] )
				nerr = nerr + 1
			
			cmd = [ 'which', task['cmd'][0] ]
			cwd = task['cwd']
			try:
				res = subprocess.run(args=cmd, cwd=cwd, check=True, stdout=subprocess.PIPE )
				realcmd = res.stdout.decode('utf8').rstrip()
				print( ' OK cmd: ' + task['cmd'][0] + ' -> ' + realcmd )
			except:
				print( '*NG*cmd: ' + task['cmd'][0] )
				nerr = nerr + 1
				
			stdout_file = task['stdout']
			if( stdout_file[0] != '/' ):
				stdout_file = cwd + stdout_file
			try:
				with open( stdout_file, 'w' ) as f:
					pass
				print( ' OK stdout: ' + task['stdout'] )
			except:
				print( '*NG*stdout: ' + task['stdout'] )
				nerr = nerr + 1

			stderr_file = task['stderr']
			if( stderr_file[0] != '/' ):
				stderr_file = cwd + stderr_file
			try:
				with open( stderr_file, 'w' ) as f:
					pass
				print( ' OK stderr: ' + task['stderr'] )
			except:
				print( '*NG*stderr: ' + task['stderr'] )
				nerr = nerr + 1
			
			print()
			
			ind = ind + 1
		
		print()
		if( nerr == 0 ):
			print( 'Passed with no error' )
		else:
			print( '***** ERROR ****' )
			print( str(nerr) + ' errors were found.' )

########################################################
## -start
	def daemon_start(self):
		if( not os.access( self.pkl_file, os.F_OK ) ):
			msg = 'Cannot find queue: ' + self.queue_name
			raise ValueError(msg)

		if( self.is_run() ):
			msg = 'Daemon for ' + self.queue_name + ' is already running.'
			raise ValueError(msg)


########################################################
### logger setting
		logger = logging.getLogger(title+'_'+self.queue_name)
		logger.propagate = False

		fh = logging.FileHandler(self.log_file, 'w')
		formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
		fh.setFormatter(formatter)
		fh.setLevel(logging.DEBUG)
		logger.addHandler(fh)
		keep_fds = [fh.stream.fileno()]


########################################################
#### daemon main
		def daemon_main():
			logger.info( 'Daemon for ' + self.queue_name + ' is stared.' )
			queue = self.load_queue()
			env = os.environ

			while( len(queue) > 0 ):
				cmd = queue[0]['cmd']
				cwd = queue[0]['cwd']
				
				stdout_file = queue[0]['stdout']
				if( stdout_file[0] != '/' ):
					stdout_file = cwd + stdout_file
					
				stderr_file = queue[0]['stderr']
				if( stderr_file[0] != '/' ):
					stderr_file = cwd + stderr_file
				
				try:
					stdout = open(stdout_file, 'w')
					log_stdout = ' > ' + stdout_file
				except:
					stdout = None
					log_stdout = ''
					logger.warning( 'No stdout information' )

				try:
					stderr = open(stderr_file, 'w')
					log_stderr = ' 2> ' + stderr_file
				except:
					stderr = None
					log_stderr = ''
					logger.warning( 'No stderr information' )

				logger.info( 'Start ' + ' '.join(cmd) + log_stdout + log_stderr + ' on ' + cwd )

				logger.debug( str(self.prefix) )
				
				if( self.has_prefix() ):
					cmd = [self.prefix] + cmd
				
				try:
					res = subprocess.run(' '.join(cmd), cwd=cwd, check=True, stdout=stdout, stderr=stderr, env=env, shell=True)
				except:
					logger.warning( 'Cannot run ' + ' '.join(cmd) + ' on ' + cwd )
					self.daemon_stop()
				
				if( stdout != None ):
					stdout.close()
				if( stderr != None ):
					stderr.close()
				
				fd = self.lock()
				queue = self.load_queue()
				
				del queue[0]
				
				self.save_queue(queue)
				self.unlock(fd)

				logger.info( 'Ended ' + ' '.join(cmd) + log_stdout + log_stderr + ' on ' + cwd )

			self.del_pkl_file()
			logger.info( 'Daemon for ' + self.queue_name + ' is ended.' )
		
########################################################
### daemon start
		app = title+'_'+self.queue_name
		daemon = Daemonize(app=app, pid=self.pid_file, action=daemon_main, keep_fds=keep_fds)
		daemon.start()


########################################################
## -stop
	def daemon_stop(self):
		try:
			with open( self.pid_file, 'r' ) as fin:
				pid = int(fin.read())
		except:
			msg = 'Cannot read pid file for ' + self.queue_name
			raise ValueError(msg)
		
		try:
			os.killpg(os.getpgid(pid), signal.SIGTERM)
		except:
			msg = 'Cannot kill process [' + str(pid) + '] for ' + self.queue_name
			raise ValueError(msg)
		
		
		if( os.path.exists(self.pid_file) ):
			os.remove( self.pid_file )
		
		return 'Daemon for ' + self.queue_name + ' is stopped.'


########################################################
## -log
	def cat_log(self, r=None):
		if( r == None ):
			pattern = None
		else:
			try:
				pattern = re.compile(r)
			except:
				msg = 'Regular expression error: ' + r
				raise ValueError(msg)
			
		if( os.access( self.log_file, os.F_OK ) ):
			try:
				with open( self.log_file, 'r' ) as fin:
					for line in fin:
						line = line.rstrip()
						if( pattern == None or pattern.search(line) != None ):
							print(line)
			except:
				msg = 'Cannot read ' + self.log_file
				raise ValueError(msg)
		

if( __name__ == '__main__' ):
	ls_queue()
	test = mgqueue('test')
