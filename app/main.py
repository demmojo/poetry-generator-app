import os
from flask import Flask, request, render_template
from keras.preprocessing.text import Tokenizer
import json
from rnn.model import chargen_model
from rnn.utils import *


# initialize our Flask application and Keras model
app = Flask(__name__, static_url_path='')
model = None
app.config["SERVER_NAME"] = "mohamedabdulaziz.com"


#  set current working directory for loading models
current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
os.chdir(dir_path)


class textrnn:
    meta_token = '<s>'

    def __init__(self, vocab_filepath=None, weights_filepath=None, config_filepath=None):
        """Initializes configuration and vocabulary from JSON files and conducts text preprocessing"""
        #  Open Configuration file if present
        if config_filepath is not None:
            with open(config_filepath, 'r', encoding='utf8', errors='ignore') as json_file:
                self.config = json.load(json_file)

        #  Open vocabulary file if present
        if vocab_filepath is not None:
            with open(vocab_filepath, 'r', encoding='utf8', errors='ignore') as json_file:
                self.vocabulary = json.load(json_file)

            #  Text preprocessing
            self.tokenizer = Tokenizer(filters='', char_level=True)  # Vectorize text and treat each char as a token
            self.num_of_classes = len(self.vocabulary) + 1
            self.model = chargen_model(self.num_of_classes, cfg=self.config, weights_filepath=weights_filepath)
            self.char_indices = dict((self.vocabulary[c], c) for c in self.vocabulary)

    def generate(self, n=1, prefix=None, temperature=0.5, max_length_gen=1000):
        """Calls generate function from rnn.utils.py which generates and returns a single text."""

        for _ in range(n):
            gen_text = generate(self.model,
                                self.vocabulary,
                                self.char_indices,
                                prefix,
                                temperature,
                                self.config['input_length'],
                                self.meta_token,
                                max_length_gen)
            return "{}\n".format(gen_text)


def load_model(subdomain):
    print(subdomain)
    """Loads pre-trained model weights, vocabulary file and configuration."""
    global model
    model = textrnn(weights_filepath='models/{}_weights.hdf5'.format(subdomain),
                    vocab_filepath='models/{}_vocab.json'.format(subdomain),
                    config_filepath='models/{}_config.json'.format(subdomain))


@app.route("/", methods=["GET", "POST"], subdomain='<subdomain>')
def get_nazim(subdomain):
    """Takes input from user and returns generated text."""
    print(subdomain)
    if request.method == 'POST':
        load_model(subdomain)
        user_input = request.form['prefix']
        generated_string = model.generate(prefix=user_input)
        return render_template('{}.html'.format(subdomain), generated_string=generated_string)
    else:
        return render_template('{}.html'.format(subdomain))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True, threaded=False)
