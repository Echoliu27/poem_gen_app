'''
Things to do:
(separately fullfill those two features first)
1. Fullfill if user type in one sentence, render the output.
2. Fullfill if user choose one topic, render the output.
   - topic list randomly?
   - 

(combination)
1. combine two features into one -> redesign home.html
2. multiple page (linked together for better visuals)


'''
# import gpt2 library
import gpt_2_simple as gpt2
import os
import random
import pandas as pd
import numpy as np
# import flask library
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

# sess = gpt2.start_tf_sess()
# gpt2.load_gpt2(sess, 
#                run_name="run1",
#                checkpoint_dir="checkpoint")

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/sentence_input')
def sentence_input():

	return render_template('sentence_input.html')


@app.route('/topic_input')
def topic_input():
	# can automate this use POS tagging
	curated_topic_list = ['love','dog','cat','life','friend','school','spring','summer','basketball',
							'rain', 'mom', 'blue', 'snow', 'brother', 'sky', 'winter', 'family', 'football',
							'sister', 'bird', 'red', 'stork', 'baseball', 'dream', 'tree', 'crazy', 'soccer', 
							'flowers', 'christmas', 'wind', 'wish', 'fall', 'homework', 'puppy', 'bed', 'eyes',
							'fish', 'teacher', 'eat', 'baby', 'moon', 'green', 'shoes', 'beach', 'ice', 'mouse',
							'candy', 'monkey', 'stars', 'heart', 'bear', 'frog', 'hair', 'house', 'people', 'fly',
							'dad', 'food', 'game', 'pizza', 'nature', 'beautiful', 'roses', 'friendship', 'colors',
							'halloween', 'happy', 'animals', 'ocean', 'sports', 'hands', 'pig', 'pie', 'books', 'horse',
							'war', 'monster', 'forever', 'sweet', 'dark', 'ode', 'music', 'water', 'dragon', 'awoke',
							'feet', 'butterfly', 'white', 'hate', 'chicken', 'rat', 'bunny', 'sea', 'hockey', 
							'pencil', 'cheese', 'chocolate', 'write', 'car', 'fire', 'dance', 'feelings', 'bananas',
							'pickles', 'angel','kitty', 'weird', 'today', 'rainbow', 'seasons', 'leaves', 'lunch', 'bee',
							'snake', 'birthday', 'computer', 'hat', 'tiger', 'sad', 'earth', 'death', 'money', 'story', 'pink',
							'math', 'magic', 'lion', 'jelly', 'bike', 'america', 'turtle', 'frogs', 'darkness', 'teddy', 'tears',
							'thunder', 'scary']

	return render_template('topic_input.html', data = random.sample(curated_topic_list, 10))

@app.route('/predict',methods=['POST'])
def predict():
	
	final_text, error = get_input(request.form)
	output = ['']

	# start the gpt2 session
	sess = gpt2.start_tf_sess()
	gpt2.load_gpt2(sess, 
	               run_name="run1",
	               checkpoint_dir="checkpoint")

	while(len(output[0]) <= len(final_text) + 30):
		output = gpt2.generate(sess, 
	              run_name='run1',
	              checkpoint_dir='checkpoint',
	              model_dir='models',
	              sample_dir='samples',
	              return_as_list=True,
	              length=120,
	              temperature=0.7,
	              prefix = final_text,
	              truncate = "<|endoftext|>",
	              include_prefix = True,
	              )


	# return render_template('home.html', prediction_poem = output[0].replace('<|startoftext|> ', ''), error = error)
	return redirect(url_for('result', prediction_poem = output[0].replace('<|startoftext|> ', ''), error = error))
	# HAN: if you want to generate a new page => redirect(url_for(...))


@app.route('/result')
def result():

	return render_template('result.html', prediction_poem = request.args.get('prediction_poem'), error = request.args.get('error'))


def get_input(request_dict):

	# not very rigorious error logic yet
	error = ''
	if (request_dict.get('oneTopic') == None and request_dict.get('sentence') != None):
		'''
		1. User type in one sentence
		
		'''
		# user input (haven't limit number of characters for input)
		int_text = request.form['sentence']

		# preprocess input, only deal with empty input for now
		final_text = '<|startoftext|> ' + int_text.lower()
		
	elif (request_dict.get('oneTopic') != None):
		'''
		2. User choose one topic
		
		'''
		# title and first sentence csv file
		df = pd.read_csv('data/poem_title_sentence.csv')
		df = df.dropna()
	
		# user input
		topic = request.form['oneTopic']

		# search for the first sentence corresponding to the topic in csv
		int_text = random.sample(df[df['title_clean'].str.contains(topic)]['first_sentence'].to_list(), 1)
		final_text = '<|startoftext|> ' + int_text[0]
	else:
		error = 'Empty input. You have not fed the hungry machine yet.'
	return final_text, error


if __name__ == "__main__":
    app.run(debug=True)