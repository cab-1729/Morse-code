#rules
'''
The length of a dot is one unit
A dash is three units
The space between parts of the same letter is one unit
The space between letters is three units
The space between words is seven units
-wikipedia.org
'''
imc={
	'A':'.-',
	'B':'-...',
	'C':'-.-.',
	'D':'-..',
	'E':'.',
	'F':'..-.',
	'G':'--.',
	'H':'....',
	'I':'..',
	'J':'.---',
	'K':'-.-',
	'L':'.-..',
	'M':'--',
	'N':'-.',
	'O':'---',
	'P':'.--.',
	'Q':'--.-',
	'R':'.-.',
	'S':'...',
	'T':'-',
	'U':'..-',
	'V':'...-',
	'W':'.--',
	'X':'-..-',
	'Y':'-.--',
	'Z':'--..',
	'1':'.----',
	'2':'..---',
	'3':'...--',
	'4':'....-',
	'5':'.....',
	'6':'-....',
	'7':'--...',
	'8':'---..',
	'9':'----.',
	'0':'-----',
	'&':'.-...',
	'\'':'.----.',
	'@':'.--.-.',
	')':'-.--.-',
	'(':'-.--.',
	':':'---...',
	',':'--..--',
	'.':'.-.-.-',
	'=':'-...-',
	'!':'-.-.--',
	'-':'-....-',
	'+':'.-.-.',
	'"':'.-..-.',
	'?':'..--..',
	'/':'-..-.'
}
from sys import argv
from subprocess import call
#default args
kwargs=argv[1:]
phase='1'
unit='200'
repeat=False
file=None
text=''
for k in kwargs:#get changes
	arg_name,value=k.split('=')
	exec(arg_name+'='+value)
if file!=None:
	with open(file,'r') as f:text=f.read()
unit3=str(int(unit)*3)
unit7=str(int(unit)*7)
message=text.upper()
light='{ (0)2000'
m='('+phase+')'
for char in message:
	if char==' ':
		light+=' (0)'+unit7
	else:
		morse=imc[char]
		for o in morse:
			if o=='.':
				light+=' '+m+unit
			else:
				light+=' '+m+unit3
			light+=' (0)'+unit
		light+=' (0)'+unit3
light+='}1'
f=0
for i,h in enumerate(argv[0]):
	if h=='\\':
		f=i
c=argv[0][0:f+1]
with open(c+'morse.kls','w') as m:
	m.write(light)
try:
	call('"'+c+'lights.exe" "'+c+'morse.kls"')
except:
	call('"'+c+'lights.py" "'+c+'morse.kls"')
if isinstance(repeat,int):
	for _ in range(repeat-1):
		call('wscript.exe "' + c + 'compiled.vbs"')
else:
	while repeat:
		call('wscript.exe "' + c + 'compiled.vbs"')