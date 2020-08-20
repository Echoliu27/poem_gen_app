## incorporate into app.py already
# import gpt_2_simple as gpt2
# import os
# import requests

# sess = gpt2.start_tf_sess()
# gpt2.load_gpt2(sess, 
#                run_name="run1",
#                checkpoint_dir="checkpoint")

# text = gpt2.generate(sess, 
#               run_name='run1',
#               checkpoint_dir='checkpoint',
#               model_dir='models',
#               sample_dir='samples',
#               length=150,
#               temperature=0.7,
#               prefix ="<|startoftext|> i love my dad",
#               truncate = "<|endoftext|>",
#               include_prefix = True,
#               )
# print(text)