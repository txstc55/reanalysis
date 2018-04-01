from django.shortcuts import render
from django.http import HttpResponse
from reanalysis.models import Sentence
# Create your views here.
import math
import ast
import json
# The first time a page is accessed, the following items will be created
# the index of the current word

# head ---->
# dependent <-----



def get_position(test_string):
	word_length=list(map(lambda x: len(x), test_string.split()))
	arrow_index=[]
	for count, length in enumerate(word_length):
		arrow_index.append(sum(word_length[0:count])+count+math.ceil(word_length[count]/2)-1)
	return arrow_index

def parse_representing_list(rep):
	arrow_pair_list = []
	arrow_id = 0
	for i in range(0, len(rep)):
		head_list = rep[i][0]
		dep_list = rep[i][1]
		for head in head_list:
			arrow_pair_list.append([str(i+2), head, "#"+"arrow"+str(arrow_id)])
			arrow_id = arrow_id + 1
		for dep in dep_list:
			arrow_pair_list.append([dep, str(i+2), "#"+"arrow"+str(arrow_id)])
			arrow_id = arrow_id + 1
	return(arrow_pair_list)







def index(request):
	# Every time you access the page, a random string will be assigned
	# the index of the random string will be passed
	random_record=Sentence.objects.order_by('?').first()
	random_sentence=random_record.sentence
	random_index=random_record.index
	word_list=random_sentence.split()
	current_word_index=1
	continue_test=True

	dependency_list=[]
	representing=[]
	arrow_list=[]

	re_index = 0

	for x in range(0, len(word_list)):
		dependency_list.append([])

	# print(dependency_list)
	if request.method == 'POST':
		if 'skip' in request.POST:
			random_record=Sentence.objects.order_by('?').first()
			random_sentence=random_record.sentence
			random_index=random_record.index
			word_list=random_sentence.split()
			current_word_index=1
			continue_test=True

			dependency_list=[]
			representing=[]
			for x in range(0, len(word_list)):
				dependency_list.append([])
		else:
			re_index = int(request.POST.getlist('reanalysis_index')[0])

			dependency_list=ast.literal_eval("".join(request.POST.getlist('dep_list')))
			# print(dependency_list)
			random_index=int(request.POST.getlist('sentence_index')[0])
			if 'reanalysis' in request.POST:
				re_index = re_index+1
				current_word_index = int(request.POST['re_list'])-1
			else:
				current_word_index = int(request.POST.getlist('count')[0])	
				head_list = request.POST.getlist('head')
				dependent_list = request.POST.getlist('dependent')	
				dependency_list[current_word_index].append([head_list, dependent_list, re_index])
				print("The index of the head of the current word is: "+str(head_list))
				print("The index of the dependent of the current word is: "+str(dependent_list))	

			
			# This part is to ensure if you are already doing a sentence
			# then you will not get another random string
			
			print("The sentence index is: "+str(random_index))
			print("Reanalysis index "+str(re_index))
			random_sentence=Sentence.objects.filter(index=random_index)[0].sentence
			word_list=random_sentence.split()



			# if we reach the end, we do not need to continue anymore
			if (current_word_index+1)>=len(word_list):
				current_word_index=len(word_list)-1
				continue_test=False
				print("Dependency List")
				
				for x in range(1, current_word_index+1):
					print(dependency_list[x])
					if len(dependency_list[x])>0:
						representing.append(dependency_list[x][-1][0:2])

			else:

				print("Dependency List")
				
				for x in range(1, current_word_index+1):
					print(dependency_list[x])
					if len(dependency_list[x])>0:
						representing.append(dependency_list[x][-1][0:2])
				current_word_index=current_word_index+1
				# print("Representing: ")
				# for x in representing:
				# 	print(x)
				# print("Arrow pairs")
				representing = parse_representing_list(representing)
				# print(representing)
				arrow_list = list(map(lambda x: x[2].strip('#'), representing))
				# print(arrow_list)




	print("Current word index is: "+str(current_word_index))
	# print(dependency_list)
	show_words=word_list[0:current_word_index]
	current_word=word_list[current_word_index]
	data_list = {"reanalysis_index":re_index, "before_words":show_words, "current_word":current_word,"if_continue":continue_test,"test_string":random_sentence, 'sentence_index':random_index, 'representing':json.dumps(representing), 'arrow_list':arrow_list,'select_list':show_words[1:], "dep_list":str(dependency_list)}
	response= render(request, 'reanalysis/index.html', data_list)
	return response
