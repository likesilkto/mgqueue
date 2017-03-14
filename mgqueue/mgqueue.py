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

try:
	import cPickle as pickle
except:
	import pickle

########################################################
# global variables
title = 'mgqueue'
version = '0.1.0'
root = os.path.expanduser('~') + '/' # $HOME/
queue_dir = root + '.' + title + '/'

########################################################
# utilities
def get_runs():
	pids = glob.glob( queue_dir + '*.pid' )
	return [os.path.splitext(os.path.basename(f))[0] for f in pids]

def ls_queue():
	runs = get_runs()
	pkl = glob.glob( queue_dir + '*.pkl' )
	for file in pkl:
		with open(file, 'rb') as fin:
			queue, env = pickle.load( fin )
		queue_name = os.path.splitext(os.path.basename(file))[0] + ' '
		if( env != None ):
			queue_name = queue_name + '+'
		if( queue_name in runs ):
			queue_name = queue_name + '*'
		print( queue_name + ' : ' + str(len(queue)) )

########################################################
# class
class mgqueue(object):
########################################################
## directry setting
	def __init__( self, queue_name ):
		if( not os.access( queue_dir, os.F_OK ) ):
			os.mkdir( queue_dir )

		self.queue_name = queue_name
		self.cwd = os.getcwd() + '/'
		
		self.pid_file = queue_dir + queue_name + '.pid'
		self.log_file = queue_dir + queue_name + '.log'
		self.pkl_file = queue_dir + queue_name + '.pkl'
		self.lck_file = queue_dir + queue_name + '.lck'
		
		self.env = self.load_env()
		
########################################################
## class utilities
	def lock(self):
		fd = open(self.lck_file, 'w')
		fcntl.flock(fd,fcntl.LOCK_EX)
		return fd

	def unlock(self,fd):
		fcntl.flock(fd,fcntl.LOCK_UN)
		fd.close()
		os.remove(self.lck_file)

	def has_env(self):
		return self.env != None

	def is_run(self):
		return os.access( self.pid_file, os.F_OK )
	
	def load_queue_env(self):
		try:
			with open(self.pkl_file, 'rb') as fin:
				queue, env = pickle.load( fin )
		except:
			queue = []
			env = None
		return queue, env

	def load_queue(self):
		queue, env = self.load_queue_env()
		return queue

	def load_env(self):
		queue, env = self.load_queue_env()
		return env

	def save_queue(self, queue):
		with open(self.pkl_file, 'wb') as fout:
			pickle.dump( [queue, self.env], fout )
	
	def save_env(self, env):
		if( os.access( self.pkl_file, os.F_OK ) ):
			msg = 'Cannot save env for existing queue.'
			raise ValueError(msg)
		
		self.env = env
		self.save_queue( [] )
		msg = self.queue_name + ' is initialized with \n'
		for k, v in self.env.items():
			msg = msg + k + '=' + v + '\n'
		return msg

	def del_pkl_file(self):
		if( self.env == None ):
			os.remove( self.pkl_file )


########################################################
## -ls
	def ls_task(self):
		queue = self.load_queue()
		
		if( self.has_env() ):
			print( 'env: ' )
			for k, v in self.env.items():
				print(' ' + k + '=' + v )
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
	def add_cmd( self, cmd, stdout = '/dev/null', stderr = '/dev/null' ):
		cwd = self.cwd
		
		task = { 'cmd':cmd, 'cwd':cwd, 'stdout':stdout, 'stderr':stderr }
		self.add_task( task )

		return task, 'Added ' + ' '.join(cmd) + ' to ' + self.queue_name


########################################################
## -remove
	def remove_ind( self, ind ):
		
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
			os.remove(self.pkl_file)

########################################################
## move
	def move_ind( self, ind, n ):
		fd = self.lock()
		queue = self.load_queue()

		if( ind == 0 and self.is_run() ):
			msg = 'Cannot move current task'
			raise ValueError(msg)
			
		elif( ind < 0 or ind >= len(queue) ):
			msg = 'Cannot find index: ' + str(ind) + ' in ' + self.queue_name
			raise ValueError(msg)

		task = queue.pop(ind)
		ind = ind - n
		
		mn = ( 1 if self.is_run() else 0 )
		
		if( ind < mn ):
			ind = mn
		elif( ind > len(queue)-1 ):
			ind = len(queue)-1
		queue.insert( ind, task )

		self.save_queue(queue)
		self.unlock(fd)
		
		return task, ind, 'task ' + str(ind) + ' is moved to ' + str(ind)
		
########################################################
## -up
	def up_ind( self, ind, n ):
		task, newind, msg = self.move_ind( ind, n )
		return task, newind, 'task ' + str(ind) + ' is moved up to ' + str(newind)


########################################################
## -down
	def down_ind( self, ind, n ):
		task, newind, msg = self.move_ind( ind, -n )
		return task, newind, 'task ' + str(ind) + ' is moved down to ' + str(newind)

########################################################
## -clear
	def clear_file(self):
		if( self.is_run() ):
			msg =  'Cannot clear, because it is still running.'
			raise ValueError(msg)
			
		files = glob.glob( queue_dir + self.queue_name + '.*' )
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
				res = subprocess.run(args=cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, env=self.env )
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

				logger.debug( str(self.env) )
				
				try:
					res = subprocess.run(' '.join(cmd), cwd=cwd, check=True, stdout=stdout, stderr=stderr, env=self.env, shell=True)
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
		
		return 'Daemon for ' + self.queue_name + ' is stoped.'


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
