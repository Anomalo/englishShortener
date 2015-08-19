import en 
import string
import re#
import random


romanNumerals = ['I','II','III','IV','V','VI','VII','IIX','IX','X',
				 'XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIIX','XIX','XX']

def strip(n,torepalce =''):

	for c in string.punctuation:
		n= n.replace(c,'  ')
	n = n.replace('  ',torepalce)
	return n
def _stripBrackets(line,brackets=('(',')')):
	a,b=brackets
	result = "" 
	flag = True 
	for c in line: 
		if c == a: flag = False 
		if flag: result += c 
		if c == b: flag = True 
	return result
def stripBrackets(line):
	if line =='':return ''
	line = _stripBrackets(line,('(',')'))
	line = _stripBrackets(line,('[',']'))
	return line

def isCAPS(n):
	
	if n == '':return False
	n = strip(n)
	if n == '':return False

	return n==n.upper()
def startsWithNum(line):
	if not '.' in line:return False
	start = line.split('.')[0]
	try: 
		int(start)
		return True
	except:return False
	
def deconjugate(word):
	word = word.upper()
	if en.verb.infinitive(word) != '': 
		return en.verb.infinitive(word)
	return en.singular.singular(word).upper()
	
class dictionary:
	def __init__(self,fname,brackets=False):
		self.readFile(fname,brackets=brackets)
	def readFile(self,fname,brackets=False):
		f = open(fname)
		raw = f.read()
		self.raw=raw
		d = (raw.split('\n'*5))[2:-1][0]
		d = d.split('\n'*2)
		D = {}
		curr = ''
		definition = ''
		for block in d:

			if isCAPS(block.split('\n')[0]):
				#print curr
				definition='\n'.join(definition.split('\n')[1:])
				#print definition
				if not brackets: 
					definition = stripBrackets(definition)
				definition = definition.replace('\n',' ')
				if ';' in curr:
					currs=curr.split(';')
					for curr in currs:
						curr = curr.replace(' ','')
						if not curr in D:D[curr]=[]
						D[curr].append(definition)
				else:
					curr = curr.replace(' ','')
					if not curr in D:D[curr]=[]
					D[curr].append(definition)
				curr = block.split('\n')[0]
				definition=''
			definition+=block
				
		del D['']
		self.D = D
			
	def __getitem__(self,q):
		q=deconjugate(q)
		if q in self.D:
			return '\n\n'.join(self.D[q])
		return ''
	
	def words(self):
		return len(self.D)
		
	def getWordsFromDef(self):
		words = []
		for n, definition in enumerate(self.D.values()):
			if n%10000==1:print n,self.words(),(n*100)/self.words(),'%'
			definition='\n'.join(definition)
			definition = strip(definition)
			for word in definition.split():
				words.append(word.upper())
		words = list(set(words))
		words = map(deconjugate,words)
		words = list(set(words))
		return words
	
	def read(self):
		return self.raw
	
	def checkRedundant(self,word):
		'''
		checks is a word can be removed 
		'''
		word = deconjugate(word)
		if not word in self.D: return None
		definition = self.D[word]
		definition =  '\n'.join(definition)
		words = self.get_words(definition)
		words.discard(word)
		for w in word:
			if not word in self.D:
				return False
		return True
	
	def delRedundant(self,word=None,v=False):
		if word == None:
			word = random.choice(self.D.keys())
		else:
			word = deconjugate(word)
		if self.checkRedundant(word):
			del self.D[word]
			if v: print 'deleted',word
		else:
			if v: print 'can`t delete', word
	def redundantCycle(self,cycles=1000,v = True):
		
		for i in range(cycles):
			self.delRedundant(word = None, v = v)
	
	def isReduced(self):
		for word in self.D.keys():
			if self.checkRedundant(word):
				return False
		return False
	
	
	def get_words(self,definition):

		words = en.spelling.words(definition)
		words = list(set(words))
		words = ' '.join(words).upper()
		words = words.split()
		for i in words:
			if i in romanNumerals:
				words.remove(i)
		words = map(deconjugate,words)
		words = set(words)
		joined = ' '.join(words)
		for i in '0123456789':
			joined = joined.replace(i,'')
		words = joined.split()
		return set(words)
		