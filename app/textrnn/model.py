from keras.optimizers import RMSprop
from keras.layers import Input, Embedding, Dense, LSTM, Bidirectional
from keras.layers import CuDNNLSTM, concatenate, SpatialDropout1D
from keras.models import Model
from .AttentionLayer import WeightedAverageAttention


def text_model(num_of_classes, cfg, weights_file_path=None, dropout=0.0, optimizer=RMSprop(lr=4e-3, rho=0.99)):

    """Builds the model architecture and loads the weights of the pre-trained model."""

    data_input = Input(shape=(cfg['input_length'],), name='input')
    embedded = Embedding(num_of_classes, cfg['input_dim'], input_length=cfg['input_length'],
                         name='embedding')(data_input)

    if dropout > 0.0:
        embedded = SpatialDropout1D(dropout, name='dropout')(embedded)

    list_rnn_layers = []

    #  Build LSTM layers based on model configuration
    for i in range(cfg['rnn_layers']):

        if i == 0:
            prev_layer = embedded
        else:
            prev_layer = list_rnn_layers[-1]

        list_rnn_layers.append(Bidirectional(LSTM(cfg['rnn_size'], return_sequences=True,
                                             recurrent_activation='sigmoid'),
                                             name='rnn_{}'.format(i + 1))(prev_layer))

    concat_seq = concatenate([embedded] + list_rnn_layers, name='rnn_concat')
    attention = WeightedAverageAttention(name='attention')(concat_seq)
    output = Dense(num_of_classes, name='output', activation='softmax')(attention)

    model = Model(inputs=[data_input], outputs=[output])
    if weights_file_path is not None:
        model.load_weights(weights_file_path, by_name=True)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    return model
