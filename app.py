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
# import flask library
from flask import Flask, request, render_template
app = Flask(__name__)

# sess = gpt2.start_tf_sess()
# gpt2.load_gpt2(sess, 
#                run_name="run1",
#                checkpoint_dir="checkpoint")


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	# input
	int_text = request.form['sentence']

	# preprocess input (what if input are not words at all?) Only deal with empty input for now
	# lowercase input
	if (len(int_text) != 0):
		final_text = '<|startoftext|> ' + int_text.lower()
		output = ['']
	else:
		error = "Empty input. You have not fed the hungry machine yet."


	# start the gpt2 session
	sess = gpt2.start_tf_sess()
	gpt2.load_gpt2(sess, 
	               run_name="run1",
	               checkpoint_dir="checkpoint")

	while(len(output[0]) <= len(final_text)):
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


	return render_template('home.html', prediction_poem = output[0].replace('<|startoftext|> ', ''))
	# HAN: if you want to generate a new page => redirect(url_for(...))

if __name__ == "__main__":
    app.run(debug=True)