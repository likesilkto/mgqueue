#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse

from mgqueue import mgqueue

########################################################
def trans_env( src ):
	dst = {}
	for env in env_var.split(','):
		key, val = env.split('=')
		dst[key] = val


########################################################
# main
if( len(sys.argv) == 1 ):
	mgqueue.ls_queue()
	sys.exit()

parser = argparse.ArgumentParser(description=mgqueue.title+'-'+mgqueue.version)

parser.add_argument('queue', help='queue name')
parser.add_argument('-ls', '-l', action='store_true', help='show task list')

subparser = parser.add_subparsers(help='chose one command')


########################################################
## remove files
def clear(mgQueue, args):
	try:
		msg = mgQueue.clear_file()
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_clear = subparser.add_parser('clear', help='remove reated files')
parser_clear.set_defaults(func=clear)

########################################################
## initialize env
def env(mgQueue, args):
	
	env = {}
	for ev in args.env_val:
		key, val = ev.split('=')
		env[key] = val

	try:
		msg = mgQueue.save_env( env )
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_env = subparser.add_parser('env', help='initialize queue with env')
parser_env.set_defaults(func=env)
parser_env.add_argument('env_val', nargs='+', help='specify env: HOGE=hoge HAGE=hage')

########################################################
## check queue
def check(mgQueue, args):
	msg = mgQueue.check_queue()
parser_check = subparser.add_parser('check', help='check queue')
parser_check.set_defaults(func=check)

########################################################
## start daemon
def start(mgQueue, args):
	print( 'Daemon for ' + args.queue + ' is starting.' )
	try:
		mgQueue.daemon_start()
	except ValueError as msg:
		print('***** ERROR *****')
		print(msg)
parser_start = subparser.add_parser('start', help='start daemon for queue')
parser_start.set_defaults(func=start)

########################################################
## stop daemon
def stop(mgQueue, args):
	try:
		msg = mgQueue.daemon_stop()
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_stop = subparser.add_parser('stop', help='start stop for queue')
parser_stop.set_defaults(func=stop)

########################################################
## show log
def log(mgQueue, args):
	try:
		if( args.r == None ):
			mgQueue.cat_log()
		else:
			mgQueue.cat_log(args.r[0])
	except ValueError as err:
		print('***** ERROR *****')
		print(err)
parser_log = subparser.add_parser('log', help='show log of queue')
parser_log.set_defaults(func=log)
parser_log.add_argument('-r', nargs=1, help='regular expression')

########################################################
## add task
def ad(mgQueue, args):
	try:
		task, msg = mgQueue.add_cmd( args.command, stdout=args.stdout[0], stderr=args.stderr[0] )
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_ad = subparser.add_parser('ad', help='add task to queue')
parser_ad.set_defaults(func=ad)
parser_ad.add_argument('command', nargs='+', help='specify task')
parser_ad.add_argument('-stdout', nargs=1, default=['/dev/null'], help='specify stdout')
parser_ad.add_argument('-stderr', nargs=1, default=['/dev/null'], help='specify stderr')

########################################################
## remove task
def rm(mgQueue, args):
	try: 
		task, msg = mgQueue.remove_ind( args.index[0] )
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_rm = subparser.add_parser('rm', help='remove task from queue')
parser_rm.set_defaults(func=rm)
parser_rm.add_argument('index', nargs=1, type=int, help='task index')

########################################################
## remove all task
def rmall(mgQueue, args):
	mgQueue.remove_all()
parser_rmall = subparser.add_parser('rmall', help='remove all task from queue')
parser_rmall.set_defaults(func=rmall)

########################################################
## up task
def up(mgQueue, args):
	try:
		task, newind, msg = mgQueue.up_ind( args.index[0], args.c[0] )
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_up = subparser.add_parser('up', help='up task in queue' )
parser_up.set_defaults(func=up)
parser_up.add_argument('index', nargs=1, type=int, help='task index')
parser_up.add_argument('-c', nargs=1, type=int, default=[1], help='up count')

########################################################
## down task
def dn(mgQueue, args):
	try:
		task, newind, msg = mgQueue.down_ind( args.index[0], args.c[0] )
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_dn = subparser.add_parser('dn', help='down task in queue' )
parser_dn.set_defaults(func=dn)
parser_dn.add_argument('index', nargs=1, type=int, help='task index')
parser_dn.add_argument('-c', nargs=1, type=int, default=[1], help='down count')

########################################################
## move task
def mv(mgQueue, args):
	try:
		task, newind, msg = mgQueue.move_ind( args.index[0], args.c[0] )
	except ValueError as err:
		print('***** ERROR *****')
		msg = err
	print(msg)
parser_mv = subparser.add_parser('mv', help='move task in queue' )
parser_mv.set_defaults(func=mv)
parser_mv.add_argument('index', nargs=1, type=int, help='task index')
parser_mv.add_argument('-c', nargs=1, type=int, default=1, help='down count')


########################################################
# ls task
def ls(mgQueue, args):
	if( not args.ls ):
		mgQueue.ls_task()
parser.set_defaults(func=ls)


########################################################
# call subfunction
args = parser.parse_args()
mgQueue = mgqueue.mgqueue(args.queue)
args.func(mgQueue,args)


########################################################
# -ls
if( args.ls ):
	mgQueue.ls_task()

