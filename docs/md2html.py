#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
import glob
import os.path

head='''
<head>
<title>Like Silk: Just for me</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="icon" href="/favicon.ico" >
<link rel="Shortcut Icon" href="/favicon.ico" >
<meta name="keywords" content="like silk">

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-53229821-7', 'auto');
  ga('send', 'pageview');

</script>

<meta property="og:title" content="Like Silk"/>
<meta property="og:description" content="Masayuki Tanaka Personal Site: Fear is often worse than the danger itself. Go for it!"/>
<meta property="og:image" content="http://like.silk.to/banner.gif"/>
<meta property="og:url" content="http://like.silk.to/"/>
<meta property="og:type" content="university"/>
<meta property="fb:admins" content=""/>
<meta property="og:site_name" content="Like Silk"/>


<meta name="twitter:card" content="summary" />
<meta name="twitter:site" content="@likesilkto" />
<meta name="twitter:creator" content="@likesilkto" />
<meta name="twitter:title" content="Like Silk" />
<meta name="twitter:description" content="Masayuki Tanaka Personal Site: Fear is often worse than the danger itself. Go for it!" />
<meta name="twitter:image" content="http://like.silk.to/banner.gif" />
<meta name="twitter:url" content="http://like.silk.to/" />

<link rel="stylesheet" href="mgqueue.css" type="text/css" />

</head>
'''

body='''
<div id="wrapper">

<div id="header">
{header}
</div>

<div id="main">

<div id="menu">
{menu}
</div>

<div id="contents">
{contents}
</div>

</div>

<div id="footer">
{footer}
 </div>
  
</div>
</body>
'''

gfm = markdown.Markdown(output_format='html5', extensions=['gfm'])

with open('side/header.md', 'r') as fin:
	md = fin.read()
header = gfm.convert(md)

with open('side/menu.md', 'r') as fin:
	md = fin.read()
menu = gfm.convert(md)

with open('side/footer.md', 'r') as fin:
	md = fin.read()
footer = gfm.convert(md)


files = glob.glob('*.md')
for file in files:
	basename = os.path.basename(file)
	titlename = os.path.splitext(basename) [0]
	
	with open(file, 'r') as fin:
		md = fin.read()
		
	contents = gfm.convert(md)
	html = '<html>\n' + head + body.format(contents=contents, menu=menu, header=header, footer=footer) + '</html>\n'
	
	with open(titlename+'.html','w') as fout:
		fout.write(html)
	
	print( file + ' -> ' + titlename+'.html')
	
