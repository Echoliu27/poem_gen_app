from flask import Flask, request
from flask_cors import CORS
import gpt_2_simple as gpt2
import json

app = Flask(__name__)
CORS(app)

# generate api
@app.route("/generate", methods=['GET'])
def generate():
    first_line = request.args['firstLine']
    first_line = '<|startoftext|> ' + first_line.lower()

    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess,
                   run_name="run1",
                   checkpoint_dir="checkpoint")

    output = ['']
    while(len(output[0]) <= len(first_line) + 30):
        output = gpt2.generate(sess, run_name='run1', checkpoint_dir='checkpoint',
                               model_dir='models', sample_dir='samples', return_as_list=True,
                               length=120, temperature=0.7, prefix = first_line,
                               truncate = "<|endoftext|>", include_prefix = True)

    data = output[0].replace('<|startoftext|> ', '')
    return json.dumps({"data": data})

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(debug=True, port=5000)
