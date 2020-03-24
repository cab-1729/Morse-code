from win32api import GetKeyState
from win32con import VK_SCROLL,VK_CAPITAL,VK_NUMLOCK
from pyautogui import press
from sys import exit,argv
from subprocess import call
#setting key state to 0
if GetKeyState(VK_CAPITAL)==1:press('capslock')
if GetKeyState(VK_NUMLOCK)==1:press('numlock')
if GetKeyState(VK_SCROLL)==1:press('scrolllock')
#getting code
f=0
for i,h in enumerate(argv[0]):
	if h=='\\':f=i
wd=argv[0][:f+1]
if len(argv)==1:
	call('wscript.exe "'+wd+'compiled.vbs"', shell=False)
	exit(0)
fn=argv[1]
if fn[-4:]=='.vbs':
	call('wscript.exe '+fn,shell=True)
	exit(0)
elif fn[-4:]!='.kls':
	print('File must have .ls extension')
	exit(0)
with open(fn,'r') as a:program=a.read().replace('\n','').replace(' ','').replace('\t','')
#creating parse tree
levels=[]
class Node:
	def __init__(self,arg1,arg2):
		self.text=arg1
		self.level=arg2
		self.parent=None
		self.children=[]
		self.code=[]
		self.break_()
		self.register()
	def break_(self):
		c=0
		for i in self.text[::-1]:
			if i=='}':break
			c-=1
		self.iters=int(self.text[c:])
		self.content=self.text[1:c-1]
		self.pure=not('{' in self.content or '}' in self.content)
		if self.pure:
			self.ins=[]
			inds=[]
			for i,c in enumerate(self.content):
				if c=='(':
					inds.append(i)
			inds.append(len(self.content))
			for i in range(0,len(inds)-1):
				self.ins.append(self.content[inds[i]:inds[i+1]])
		else:
			self.ins=None
	def register(self):
		try:
			levels[self.level].append(self)
		except IndexError:
			levels.append([self])
	def get_children(self):
		if self.pure:
			return
		br=[]
		c=0
		for i,h in enumerate(self.content):
			if c==0 and h=='{':br.append(i);c+=1
			elif h=='{':c+=1
			elif h=='}':c-=1
		gene=self.level+1
		br.append(len(self.content))
		for i in range(0,len(br)-1):
			child=Node(self.content[br[i]:br[i+1]],gene)
			child.parent=self
	def send_up(self):
		if self.pure:
			en=self.ins*self.iters
		else:
			en=self.code
		part=en*self.iters
		if self.parent==None:
			global code
			code=part
		else:
			self.parent.code.extend(part)
	def __repr__(self):return self.content+' '+str(self.iters)+' times'#remove later , for debugging purposes
adam=Node(program,0)
gen=0
while True:
	try:
		generation=levels[gen]
	except IndexError:
		break
	gen+=1
	for i in generation:
		i.get_children()
#bottom-up parse
for level in levels[::-1]:
	for i in level:
		i.send_up()
#virtual machine
vb_code='''set t=CreateObject("wscript.shell")'''
caps_on,num_on,scroll_on=False,False,False
def caps_open():
	global caps_on,vb_code
	if not caps_on:
		vb_code+='\nt.sendkeys"{capslock}"'
		caps_on=True
def caps_close():
	global caps_on,vb_code
	if caps_on:
		vb_code+='\nt.sendkeys"{capslock}"'
		caps_on=False
def scroll_open():
	global scroll_on,vb_code
	if not scroll_on:
		vb_code+='\nt.sendkeys"{scrolllock}"'
		scroll_on=True
def scroll_close():
	global scroll_on,vb_code
	if scroll_on:
		vb_code+='\nt.sendkeys"{scrolllock}"'
		scroll_on=False
def num_open():
	global num_on,vb_code
	if not num_on:
		vb_code+='\nt.sendkeys"{numlock}"'
		num_on=True
def num_close():
	global num_on,vb_code
	if num_on:
		vb_code+='\nt.sendkeys"{numlock}"'
		num_on=False
for c in code:
	phase,pause=c.split(')')
	if '0' in phase:
		caps_close()
		num_close()
		scroll_close()
	else:
		if '1' in phase:num_open()
		else:num_close()
		if '2' in phase:caps_open()
		else:caps_close()
		if '3' in phase:scroll_open()
		else:scroll_close()
	vb_code+='\nwscript.sleep '+pause
#load
with open(wd+'compiled.vbs','w') as b:b.write(vb_code)
#run
call('wscript.exe "'+wd+'compiled.vbs"',shell=False)
