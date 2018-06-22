import os
from flask import Flask, request, render_template
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
import json
from textrnn.model import text_model
from textrnn.utils import *


# initialize our Flask application and Keras model
app = Flask(__name__, static_url_path='')
model = None


#  set current working directory for loading models
current_file = __file__
real_path = os.path.realpath(current_file)
dir_path = os.path.dirname(real_path)
os.chdir(dir_path)


class textrnn:
    meta_token = '<s>'
    #  Default Configuration of trained model
    config = {
        'rnn_layers': 4,
        'rnn_size': 128,
        'rnn_bidirectional': True,
        'input_length': 100,
        'max_words': 20000,
        'input_dim': 200,
    }
    default_config = config.copy()

    def __init__(self, vocab_file_path=None, weights_file_path=None, config_file_path=None):
        """Initializes configuration and vocabulary from JSON files and conducts text preprocessing"""
        #  Open Configuration file if present
        if config_file_path is not None:
            with open(config_file_path, 'r', encoding='utf8', errors='ignore') as json_file:
                self.config = json.load(json_file)

        #  Open vocabulary file if present
        if vocab_file_path is not None:
            with open(vocab_file_path, 'r', encoding='utf8', errors='ignore') as json_file:
                self.vocabulary = json.load(json_file)

            #  Text preprocessing
            self.tokenizer = Tokenizer(filters='', char_level=True)  # Vectorize text and treat each char as a token
            self.num_of_classes = len(self.vocabulary) + 1
            self.model = text_model(self.num_of_classes, cfg=self.config, weights_file_path=weights_file_path)
            self.char_indices = dict((self.vocabulary[c], c) for c in self.vocabulary)



    def generate(self, n=1, prefix=None, temperature=0.25, max_length_gen=500):
        """Calls generate function from textrnn.utils.py which generates and returns a single text."""

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

def load_model():
    """Loads pre-trained model weights, vocabulary file and configuration."""
    global model
    model = textrnn(weights_file_path='models/model_weights.hdf5',
                    vocab_file_path='models/model_vocab.json',
                    config_file_path='models/model_config.json')


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def get_index():
    """Takes input from user and returns generated text."""
    if request.method == 'POST':
        load_model()
        user_input = request.form['prefix']
        generated_string = model.generate(prefix=user_input)
        return render_template('/nazim.html', generated_string=generated_string)
    else:
        return render_template('/nazim.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)

