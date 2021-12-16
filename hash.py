#!/usr/bin/python
#coding=utf-8

"""
created by Ahmed Al-Nassif
site: anhhacker.blogspot.com
fb: fb.com/ahmed.hackerone
"""

import hashlib,json,argparse,time,re,requests,random
from os.path import exists
from threading import Thread
from bs4 import BeautifulSoup as Html

parser = argparse.ArgumentParser()
parser.add_argument(
		"-x", "--hash", help="hash"
)
parser.add_argument(
		"-n", "--tims", help="tims word", type=int, default=False
)
parser.add_argument(
		"-t", "--thread", help="thread default 1", type=int, default=False
)
parser.add_argument(
		"-T", "--type", help="Type hash",
)
parser.add_argument("-v", "--view", help="show counter", action="store_true",)
parser.add_argument(
		"-f", "--file", help="wordlist",default=False
)
arg=parser.parse_args()

def logo():print('\x1b[H\x1b[2J\x1b[3J\n\x1b[38;5;203m \x1b[38;5;203m▄\x1b[38;5;203m \x1b[38;5;203m \x1b[38;5;203m \x1b[38;5;204m \x1b[38;5;198m▄\x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m█\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;163m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;128m▄\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m▄\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m▀\x1b[38;5;129m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m▀\x1b[38;5;93m▀\x1b[38;5;93m█\x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;99m \x1b[38;5;63m▀\x1b[38;5;63m▀\x1b[38;5;63m█\n\x1b[38;5;203m \x1b[38;5;203m█\x1b[38;5;204m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m█\x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m▄\x1b[38;5;198m▄\x1b[38;5;198m▄\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m▄\x1b[38;5;199m▄\x1b[38;5;199m▄\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;163m█\x1b[38;5;164m \x1b[38;5;164m▄\x1b[38;5;164m▄\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;128m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m█\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m▄\x1b[38;5;129m▀\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m▄\x1b[38;5;93m▄\x1b[38;5;93m▄\x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m█\x1b[38;5;99m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m█\n\x1b[38;5;198m \x1b[38;5;198m█\x1b[38;5;198m▄\x1b[38;5;198m▄\x1b[38;5;198m▄\x1b[38;5;198m▄\x1b[38;5;198m█\x1b[38;5;198m \x1b[38;5;198m▀\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m█\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m█\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;163m▀\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m█\x1b[38;5;164m▀\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m█\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;128m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m█\x1b[38;5;129m▄\x1b[38;5;129m█\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m█\x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;99m \x1b[38;5;63m \x1b[38;5;63m█\x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m█\n\x1b[38;5;198m \x1b[38;5;198m█\x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;198m \x1b[38;5;199m█\x1b[38;5;199m \x1b[38;5;199m▄\x1b[38;5;199m▀\x1b[38;5;199m▀\x1b[38;5;199m▀\x1b[38;5;199m█\x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;163m▀\x1b[38;5;164m▀\x1b[38;5;164m▀\x1b[38;5;164m▄\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m█\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m█\x1b[38;5;128m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m▀\x1b[38;5;129m▀\x1b[38;5;129m▀\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m█\x1b[38;5;129m \x1b[38;5;93m \x1b[38;5;93m█\x1b[38;5;93m▄\x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m█\x1b[38;5;93m \x1b[38;5;99m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m█\x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;69m█\n\x1b[38;5;198m \x1b[38;5;198m█\x1b[38;5;198m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m \x1b[38;5;199m█\x1b[38;5;199m \x1b[38;5;199m▀\x1b[38;5;199m▄\x1b[38;5;199m▄\x1b[38;5;199m▀\x1b[38;5;199m█\x1b[38;5;163m \x1b[38;5;164m \x1b[38;5;164m▀\x1b[38;5;164m▄\x1b[38;5;164m▄\x1b[38;5;164m▄\x1b[38;5;164m▀\x1b[38;5;164m \x1b[38;5;164m \x1b[38;5;164m█\x1b[38;5;164m \x1b[38;5;128m \x1b[38;5;129m \x1b[38;5;129m█\x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;129m \x1b[38;5;93m \x1b[38;5;93m█\x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m \x1b[38;5;93m▀\x1b[38;5;93m▄\x1b[38;5;93m \x1b[38;5;93m▄\x1b[38;5;99m▄\x1b[38;5;63m█\x1b[38;5;63m▄\x1b[38;5;63m▄\x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m \x1b[38;5;63m▀\x1b[38;5;63m▄\x1b[38;5;63m▄\x1b[38;5;63m \x1b[38;5;69m \x1b[38;5;33m \x1b[38;5;33m \x1b[38;5;33m▀\x1b[38;5;33m▄\x1b[38;5;33m▄\n\x1b[0m\x1b[1;36mCreated by\x1b[1;37m:\x1b[1;32m Ahmed Al-Nassif\x1b[0m\n\x1b[1;34mFB: \033[4;1;37mfb.com/ahmed.hackerone\033[0m\n\n ')
class Hash(object):
	user_agents = [
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
		"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
		"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
		"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
		"Mozilla/5.0 (Linux; Android 8.1.0; CPH1803 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Mobile Safari/537.36 OPR/44.6.2246.127414"
	]
	headers={'User-Agent': random.choice(user_agents)}
	name=['lib/db.json', 'lib/db.zip', 'lib/raw.zip']
	c=[0,arg.thread,False,0]
	hash=['md4', 'md5', 'sha1', 'sha256', 'sha384', 'sha512']
	length=[32, 40, 64, 96, 128]
	tims=arg.tims
	
	def printf(self,value,type=1):
		if type==0:value='.bld.grn[+] .nil'+value
		elif type==1:value='.bld.blu[*] .nil'+value
		elif type==2:value='.bld.red[-] .nil'+value
		color={
		'.bld': '\033[1m',
		'.nil': '\033[0m',
		'.blk': '\033[30m',
		'.red': '\033[31m',
		'.grn': '\033[32m',
		'.yll': '\033[33m',
		'.blu': '\033[34m',
		'.bka': '\033[35m',
		'.cya': '\033[36m',
		'.whi': '\033[37m',
		}
		for k,v in color.items():value=value.replace(k,v)
		print(value if len(value) < 30 else value+' '*20)
	
	def spanner(self):
		import sys
		n=0
		while True:
			for c in ['/','-','|','-','\\']:
				sys.stderr.write('\033[?25l')
				if self.c[2]:sys.stderr.write('\033[?12l\033[?25h');return
				w=list("Count words tested: ")
				if len(w) <= n:n=0
				if w[n]==w[n].upper():w[n]=w[n].lower()
				else:w[n]=w[n].upper()
				sys.stderr.write('\033[1;34m[*]\033[1;37m {}\033[32m{}\033[0;1m...\033[1;31m{}\033[0m\r'.format(str().join(w),self.c[3],c));sys.stderr.flush();n+=1
				time.sleep(0.4)
	
	###Websites###:
	def beta(self,hash,type):
		raw=requests.get('https://hashtoolkit.com/decrypt-hash/?hash='+hash,headers=self.headers).text
		x=re.search('Hashes for: <code>(.*?)</code>', raw)
		if x:return x.group(1)
	
	def theta(self,hash,type):
		raw=requests.get('https://md5.gromweb.com/?md5='+hash,headers=self.headers).text
		x=re.search('<em class="long-content string">(.*?)</em>', raw)
		if x:return x.group(1)
	
	def delta(self,hash,type):
		raw=requests.get('https://sha1.gromweb.com/?hash='+hash,headers=self.headers).text
		x=re.search('<em class="long-content string">(.*?)</em>', raw)
		if x:return x.group(1)
	
	def gamma(self,hash, type):
		x= requests.get('http://www.nitrxgen.net/md5db/' + hash, headers=self.headers).text
		if x:return x
	
	def alpha(self,hash, type):
		try:x= requests.get('https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728' % (hash, type),headers=self.headers).text
		except requests.exceptions.ConnectionError:return False
		if x:return x
	
	def marta(self,hash,type):
		raw=requests.get("https://hashdecryption.com/decrypt.php?send=Submit&str="+hash, headers=self.headers).text
		x=re.search("</b> is <b>(.*?)</b><br>", raw)
		if x:return x.group(1)
	
	def meta(self,hash,type):
		raw = requests.post("http://md5.my-addr.com:80/md5_decrypt-md5_cracker_online/md5_decoder_tool.php", headers=self.headers, cookies={"PHPSESSID": "aki2l78uvb3hk5n1uvuhefut17"}, data={"md5": hash, "x": "13", "y": "10"}).text
		x=re.search("Hashed string</span>: (.*?)</",raw)
		if x:return x.group(1)
	
	def search(self,hash,types):
		try:requests.get("http://188.160.0.104:80")
		except requests.exceptions.ConnectionError:return
		self.c+=[time.time()]
		H=self.hash
		self.printf('.bldUse Online:')
		self.printf('.bldUse Websites.nil')
		dict={
		H[1]: [self.beta, self.theta, self.meta, self.gamma, self.marta, self.alpha],
		H[0]: [self.beta, self.marta, self.alpha],
		H[2]: [self.beta, self.alpha, self.delta],
		H[3]: [self.beta, self.marta, self.alpha],
		H[4]: [self.beta, self.alpha],
		H[5]: [self.beta, self.alpha],
		};key=None
		for type in types:
			if self.c[2]:break
			for function in dict[type]:
				if self.c[2]:break
				try:key=function(hash,type)
				except KeyboardInterrupt:self.c[2]=True;return False
				except requests.exceptions.ConnectionError:return
				except:pass
				if key and self.brute(key,hash,type):return True
		self.printf('.bldUse Search Engine.nil')
		urls=['https://www.google.com/search?q=', 'https://duckduckgo.com/?q=', 'https://www.bing.com/?q=', 'https://yandex.com/search/touch/?text=']
		for url in urls:
			if self.c[2]:break
			try:raw=requests.get(url+hash,headers=self.headers).text
			except KeyboardInterrupt:self.c[2]=True;return False
			except requests.exceptions.ConnectionError:break
			except:pass
			soup=Html(raw, 'html.parser')
			for type in types:
				if self.c[2]:break
				for i in ["", ".", "\n", '"', "'"]:
					if self.c[2]:break
					for key in soup.get_text().split(" "):
						if self.c[2]:break
						if self.brute(key.replace(i, ""),hash,type):return True
					
	
	def brute(self,*args):
		self.c[3]+=1
		key,value,type=args
		x=hashlib.new(type)
		try:x.update(key.encode('utf-8'))
		except UnicodeDecodeError:x.update(key)
		if x.hexdigest()==value:
			self.c[2]=True
			name=self.name
			if not exists(name[0]):open(name[0],'w').write(json.dumps({value:key}))
			else:
				with open(name[0],'r') as R:
					db=json.loads(R.read())
					R.close()
				if not value in db:
					db.update({value:key})
					open(name[0],'w').write(json.dumps(db))
			self.printf('.bld.whi{.yllkey.whi:.grn %s .whi, .yllvalue.whi: .grn%s .whi, .ylltype.whi: .grn%s .whi}.nil'%(key, value, type),type=0)
			self.printf(".bldEnd in .grn%ss .whi%s brute.nil"%(int(time.time()-self.c[-1]),self.c[3]))
			return True
	
	def vetal(self,keys,value,type):
		self.c[0]+=1
		for i in keys:
			if self.c[2]:break
			key=i.strip()
			if self.tims:
				for n in range(1,self.tims+1):
					if self.brute(key*n,value,type):break
			else:
				if self.brute(key,value,type):break
		self.c[0]-=1
	
	def __init__(self,hash,file):
		self.file=file
		H=self.hash
		L=self.length
		name=self.name
		logo()
		if arg.type:
			if arg.type in H:types=[arg.type]
			else:self.printf('.bldType: .yll%s Not fuond in tool.nil'%repr(arg.type),type=2);return
		else:
			if len(hash) ==  L[0]:types=[H[1], H[0]];self.printf('.bldHash: .grn%s.whi type: .grnMD5.nil'%hash)
			elif len(hash)==L[1]:types=[H[2]];self.printf('.bldHash: .grn%s.whi type: .grnSHA-1.nil'%hash)
			elif len(hash)==L[2]:types=[H[3]];self.printf('.bldHash: .grn%s.whi type: .grnSHA-256.nil'%hash)
			elif len(hash)==L[3]:types=[H[4]];self.printf('.bldHash: .grn%s.whi type: .grnSHA-384.nil'%hash)
			elif len(hash)==L[4]:types=[H[5]];self.printf('.bldHash: .grn%s.whi type: .grnSHA-512.nil'%hash)
			else:self.printf('.bldHash: .red%s.whi type: .yllNot fuond.nil'%hash, type=2);return
			if arg.view:Thread(target=self.spanner).start()
		if exists(name[0]):
			with open(name[0]) as R:
				d=json.loads(R.read())
				try:self.printf('.bld.whi{.yllkey.whi:.grn %s .whi, .yllvalue.whi: .grn%s .whi}.nil'%(d[hash],hash),type=0);return
				except KeyError:pass
				for type in types:
					for n in range(1,self.tims+1 if self.tims else 2): 
						for key in d.values():
							if self.brute(key*n,hash,type):return
				R.close()
				del d,n
		if self.search(hash,types) or self.c[2]:return
		import zipfile
		self.printf('.bldUse Offline:')
		if types[0]=='md5':
			with zipfile.ZipFile(name[1]) as x:
				db=json.loads(x.open(types[0]).read())
				x.close()
				try:
					if self.brute(db[hash],hash,types[0]):del db;return
				except KeyError:pass
				del db
		self.printf('.bldUse BruteForce.nil')
		if self.file:
			if not exists(self.file):self.printf('.bldError in file: %s.nil'%self.file,type=2);return
			with open(self.file,'r') as f:
				data=list(set(f.readlines()))
				f.close()
		else:
			data=[]
			with zipfile.ZipFile(name[2]) as x:
				for _ in x.namelist():
					data+=x.open(_).read().split("\n")
				data=list(set(data))
				x.close()
				#open('raw.txt','w').write('\n'.join(sorted(data)))
		
		if self.c[1]:C=len(data)//self.c[1];cc=0
		self.c+=[time.time()]
		self.printf('.bldStart BruteForce in .grn%s.nil'%time.strftime('%y-%m-%d %I:%M:%S %p'))
		End=time.time();T=0
		for type in types:
			if self.c[2]:break
			if self.c[1]:
				for _ in range(self.c[1]):
					if self.c[2]:break
					cc+=C
					Thread(target=self.vetal,args=(data[cc-C:cc],hash,type)).start()
				if data[cc:]:Thread(target=self.vetal,args=(data[cc:],hash,type)).start()
				while True:
					Time=int(time.time()-End)
					if Time >= 60:
						T+=1
						End=time.time()
						self.printf(".bld.grn%s .whiword bruted at .cya%sm.nil"%(self.c[3],T))
					if self.c[2] or not self.c[0]:cc=0;break
			else:
				for _ in data:
					if self.brute(_.strip(), hash, type):return
					if int(time.time()-End) >= 60:
						T+=1
						End=time.time()
						self.printf(".bld.grn%s .whiword bruted at .cya%sm.nil"%(self.c[3],T))
		if not self.c[2]:self.printf(".bldI'm Sorry this Hash: .yll%s .whiis'nt in db.nil"%hash ,type=2)

if __name__ == '__main__':
	if not arg.hash:logo();parser.print_help();exit(0)
	Hash.c+=[time.time()]
	try:Hash(arg.hash,arg.file).printf('.bldEnd program in .grn%ss.whi bruted .grn%s.nil'%(int(time.time()-Hash.c[4]),Hash.c[3]))
	except KeyboardInterrupt:Hash.c[2]=True;print('\r\033[1;35m[>] \033[1;33mGood Luck :)\033[0m'+' '*20)