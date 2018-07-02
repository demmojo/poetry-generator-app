from keras.preprocessing import sequence
from keras import backend as K
import numpy as np



def sample(predictions, temperature):

    """"Simulates creativity by sampling predicted probabilities of next character."""

    predictions = np.asarray(predictions).astype('float64')

    if temperature is None or temperature == 0.0:
        return np.argmax(predictions)

    predictions = np.log(predictions + K.epsilon()) / temperature
    exp_preds = np.exp(predictions)
    predictions = exp_preds / np.sum(exp_preds)
    probabilities = np.random.multinomial(1, predictions, 1)
    index = np.argmax(probabilities)

    if index == 0:
        index = np.argsort(predictions)[-2]  # choose 2nd best index from predictions when index is 0 (placeholder)

    return index


def generate(model, vocab, indices_char, prefix=None, temperature=0.3, input_len=50, meta_token='<s>',
             max_length_gen=500):
    """Generates and returns a single text."""

    text = list(prefix) if prefix else ['']
    max_length_gen += len(text)
    next_char = ''

    while next_char != meta_token and len(text) < max_length_gen:
        encoded_text = encode_sequence(text[-input_len:],
                                       vocab, input_len)
        next_index = sample(
            model.predict(encoded_text, batch_size=1)[0],
            temperature)
        next_char = indices_char[next_index]
        text += [next_char]

    collapse_char = ''

    text_joined = collapse_char.join(text)
    text_joined = text_joined[:text_joined.rfind('\n')]  # as text generated in last line might cut-off incorrectly
    return text_joined

def encode_sequence(text, vocab, input_len):
    """Encode text in preparation for prediction with model."""

    encoded = np.array([vocab.get(x, 0) for x in text])
    return sequence.pad_sequences([encoded], maxlen=input_len)
