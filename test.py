# -*- coding:gbk -*- 
import urllib.request
import json
import time
import sys

#��ά�ֵ����
def dict2d_construct(thedict, key_a, key_b, val):
  if key_a in thedict:
    thedict[key_a].update({key_b: val})
  else:
    thedict.update({key_a:{key_b: val}})
#������
def printex(strs):
	sys.stdout.write("                                                   \r")
	sys.stdout.flush()
	sys.stdout.write(strs+"\r")
	sys.stdout.flush()
	
def savefile(data,listhead,fw,fs):
	for index in data:
		for head in listhead:
			if head in data[index]:
				try:
					fw.write(str(data[index][head]).replace("\n","\\n")+"\t")
				except Exception as err:
					fw.write("�����ı���ʽ��Ϣ��\t")
			else:
				fw.write("\t")
		fw.write("\n")
	fs.write(json.dumps(data))

#��ʼ��
URL_LISTAPI = "http://www.pkuhelper.com/services/pkuhole/api.php?action=getlist&p="
URL_COMMENTAPI = "http://www.pkuhelper.com/services/pkuhole/api.php?action=getcomment&pid="
  #�ϴδ��󱣴�Ľ��
try:
	p = int(open("lasterr.tmp").read())
except:
	p = 0
data = {}
index = 0
listhead = ['cid','pid','text','timestamp','hidden','anonymous','islz','name','type','reply','likenum','extra','url','hot','self_recordtime']
fw = open("pkuhole.tab",'a',encoding='gbk')
fs = open("pkuhole.list",'a',encoding='gbk')


while(1):
	#���������
	
	try:
		response = urllib.request.urlopen(URL_LISTAPI + str(p))
		strjson = response.read().decode('utf-8')
		ljson = json.loads(strjson,strict = False)
	except Exception as err:
		print(err,p)
		savefile(data,listhead,fw,fs)
		open("lasterr.tmp",'w').write(str(p))
		raise NameError(err)
		
	#û�˵Ļ��չ�
	if ljson['data']==[]:
		break
	printex("Downloading the Page: "+ str(p))
	
	for post in ljson['data']:
		#�ȱ�������
		index += 1
		for key in post:
			dict2d_construct(data,index,key,post[key])
			dict2d_construct(data,index,'self_recordtime',time.ctime())
		#����лظ��Ļ�,��ץȡ�ظ�
		if int(post['reply'])!=0:
			try:
				resreply = urllib.request.urlopen(URL_COMMENTAPI + post['pid'])
				printex("Downloading the Page: "+ str(p) +" -> reply")
			except Exception as err:
				print(err,p)
				savefile(data,listhead,fw,fs)
				open("lasterr.tmp",'w').write(str(p))
				raise NameError(err)
				
			strjson = resreply.read().decode('utf-8')
			rjson = json.loads(strjson,strict = False)
			for reply in rjson['data']:
				index += 1
				for key in reply:
					dict2d_construct(data,index,key,reply[key])
					dict2d_construct(data,index,'self_recordtime',time.ctime())
	p += 1
	time.sleep(0.1)
#дtab�ļ�



#����ϴα���
open("lasterr.tmp",'w').write("0")