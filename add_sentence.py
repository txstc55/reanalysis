import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','David.settings')

import django
django.setup()

from reanalysis.models import Sentence

sentence_file=sys.argv[1]
f = open(sentence_file,'r')
print("Text file read")
if Sentence.objects.count()==0:
	sentence_index=0
else:
	sentence_index=int(Sentence.objects.latest('index'))+1
print("The last index in Sentence table is: "+str(sentence_index))
print("Start adding sentence")

for line in f:
	s=Sentence.objects.create(sentence=line.strip('\n'), index=sentence_index)
	sentence_index= sentence_index+1
f.close()
print("Finished adding sentence")