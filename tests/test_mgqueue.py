#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os

import shutil

import sys
sys.path.append('../mgqueue')

from mgqueue import mgqueue

test_queue_dir = '__test_queue_dir__ '
test_queue_name = '__test__'
test_env_queue_name = '__test_env__'

test_stdout = test_queue_dir + '/test.stdout'
test_stderr = test_queue_dir + '/test.stdout'

class test_mgqueue( unittest.TestCase ):

	@classmethod
	def setUpClass(cls): # it is called before test starting
		pass

	@classmethod
	def tearDownClass(cls): # it is called before test ending
		shutil.rmtree( test_queue_dir )

	def setUp(self): # it is called before each test
		self.mgQueue = mgqueue.mgqueue( test_queue_name, test_queue_dir )
		self.assertTrue(os.access( test_queue_dir, os.X_OK) )

	def tearDown(self): # it is called after each test
		pass

###################################################################
	def test_lock_unlock(self): # lock, unlock
		fd = self.mgQueue.lock()
		self.assertTrue(os.access( self.mgQueue.lck_file, os.W_OK) )
		
		self.mgQueue.unlock(fd)
		self.assertFalse(os.access( self.mgQueue.lck_file, os.F_OK) )

	def test_env(self): # has_env, save_env, load_env, del_pkl_file, del_pkl_file, add_cmd
		self.assertFalse( self.mgQueue.has_env() )
		
		env = {}
		env['TEST'] = 'test'
		env['MGQ'] = 'mgq'
		
		self.mgQueue.add_cmd( ['echo', 'test'] )
		
		try:
			self.mgQueue.save_env( env )
			flg = True
		except:
			flg = False
		self.assertFalse( flg )
		
		mgQueueEnv = mgqueue.mgqueue( test_env_queue_name, test_queue_dir )
		mgQueueEnv.save_env( env )
		
		self.assertEqual( mgQueueEnv.load_env(), env )
		
		mgQueueEnv.del_pkl_file()
		self.assertTrue( os.access(mgQueueEnv.pkl_file, os.F_OK) )
		
		self.assertTrue( os.access(self.mgQueue.pkl_file, os.F_OK) )
		self.mgQueue.del_pkl_file()
		self.assertFalse( os.access(self.mgQueue.pkl_file, os.F_OK) )
		
		
	def test_is_run(self):# is_run
		self.assertFalse( self.mgQueue.is_run() )

	def test_task(self): # add_cmd, up_ind, down_ind
		cwd = os.getcwd() + '/'
		test_queue = []
		test_queue.append( 
		{ 'cmd':['echo', 'test0'], 'cwd':cwd, 'stdout':'/dev/null', 'stderr':'/dev/null' } )
		test_queue.append( 
		{ 'cmd':['echo', 'test1'], 'cwd':cwd, 'stdout':test_stdout, 'stderr':'/dev/null' } )
		test_queue.append( 
		{ 'cmd':['echo', 'test2'], 'cwd':cwd, 'stdout':test_stdout, 'stderr':test_stderr } )

		self.mgQueue.add_cmd(['echo', 'test0'])
		self.mgQueue.add_cmd(['echo', 'test1'], stdout=test_stdout)
		self.mgQueue.add_cmd(['echo', 'test2'], stdout=test_stdout, stderr=test_stderr)
		
		queue = self.mgQueue.load_queue()
		self.assertEqual( queue, test_queue )

		task, newid, msg = self.mgQueue.up_ind( 0, 1 );
		self.assertEqual( newid, 0 )
		
		task, newid, msg = self.mgQueue.down_ind( 2, 1 );
		self.assertEqual( newid, 2 )

		task, newid, msg = self.mgQueue.move_ind( 1, 0 );
		self.assertEqual( newid, 0 )

		task, newid, msg = self.mgQueue.down_ind( 0, 1 );
		self.assertEqual( newid, 1 )

		task, newid, msg = self.mgQueue.up_ind( 1, 1 );
		self.assertEqual( newid, 0 )

##

	def suite():
		suite = unittest.TestSuite()
		suite.addTests(unittest.makeSuite(test_mgqueue))
		return suite
  
if( __name__ == '__main__' ):
	print( os.getcwd() )
	unittest.main()
