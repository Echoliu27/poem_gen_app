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
import os
import re
import random
import pandas as pd
import numpy as np

import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import logging
from tqdm import tqdm, trange
# import flask library
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

gpt2_type = 'gpt2'
PATH = 'checkpoint/poem_new-2.pt'
model = GPT2LMHeadModel.from_pretrained(gpt2_type)
model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))

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

	while(len(output[0]) <= len(final_text) + 30):
		output = generate(model.to('cpu'), 
									GPT2Tokenizer.from_pretrained(gpt2_type),
									final_text,
									entry_count=1)
	def clean_poem(raw):
		pre1 = re.sub(r'<\|poem\|>', '', raw)
		pre2 = re.sub(r'<\|endoftext\|>', '', pre1)
		return pre2

	# return render_template('home.html', prediction_poem = output[0].replace('<|startoftext|> ', ''), error = error)
	return redirect(url_for('result', prediction_poem = clean_poem(output[0]), error = error))
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
		final_text = '<|poem|> ' + int_text.lower()
		
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
		final_text = '<|poem|> ' + int_text[0]
	else:
		error = 'Empty input. You have not fed the hungry machine yet.'
	return final_text, error

# generate text using this function	
def generate(
    model,
    tokenizer,
    prompt,
    entry_count=10,
    entry_length=100,
    top_p=0.8,
    temperature=0.7,
):

    model.eval()

    generated_num = 0
    generated_list = []

    filter_value = -float("Inf")

    with torch.no_grad():

        for entry_idx in trange(entry_count):

            entry_finished = False

            generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)

            # Using top-p (nucleus sampling): https://github.com/huggingface/transformers/blob/master/examples/run_generation.py

            for i in range(entry_length):
                outputs = model(generated, labels=generated)
                loss, logits = outputs[:2]
                logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                cumulative_probs = torch.cumsum(
                    F.softmax(sorted_logits, dim=-1), dim=-1
                )

                sorted_indices_to_remove = cumulative_probs > top_p
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                    ..., :-1
                ].clone()
                sorted_indices_to_remove[..., 0] = 0

                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[:, indices_to_remove] = filter_value

                next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
                generated = torch.cat((generated, next_token), dim=1)

                if next_token in tokenizer.encode("<|endoftext|>"):
                    entry_finished = True

                if entry_finished:

                    generated_num = generated_num + 1

                    output_list = list(generated.squeeze().numpy())
                    output_text = tokenizer.decode(output_list)

                    generated_list.append(output_text)
                    break
            
            if not entry_finished:
                output_list = list(generated.squeeze().numpy())
                output_text = f"{tokenizer.decode(output_list)}<|endoftext|>" 
                generated_list.append(output_text)
                
    return generated_list


if __name__ == "__main__":
    app.run(debug=True)