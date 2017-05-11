import tensorflow as tf

from .base import Layer

def default_prelu_initializer():
    return tf.zeros_initializer()

def prelu(f_in, channelwise_params):
    pos = tf.nn.relu(f_in)
    neg = channelwise_params * (f_in - tf.abs(f_in)) * 0.5
    return pos + neg

SUPPORTED_OP = {'relu': tf.nn.relu,
                'relu6': tf.nn.relu6,
                'elu': tf.nn.elu,
                'softplus': tf.nn.softplus,
                'softsign': tf.nn.softsign,
                'sigmoid': tf.nn.sigmoid,
                'tanh': tf.nn.tanh,
                'prelu': prelu,
                'dropout': tf.nn.dropout}


class ActiLayer(Layer):
    def __init__(self, func, regularizer=None, name='activation'):
        self.func = func.lower()
        assert self.func in SUPPORTED_OP
        self.layer_name = '{}_{}'.format(name, self.func)
        self.regularizer = regularizer

        super(ActiLayer, self).__init__(name=self.layer_name)


    def layer_op(self, input_tensor, keep_prob=None):
        if self.func == 'prelu':
            alphas = tf.get_variable(
                'alpha', input_tensor.get_shape()[-1],
                initializer=default_prelu_initializer(),
                regularizer=self.regularizer)
            output_tensor = SUPPORTED_OP['prelu'](input_tensor, alphas)
        elif self.func == 'dropout':
            assert keep_prob > 0.0
            assert keep_prob <= 1.0
            output_tensor = SUPPORTED_OP['dropout'](
                input_tensor, keep_prob=keep_prob, name='dropout')
        else:
            output_tensor = SUPPORTED_OP[self.func](input_tensor, name='acti')
        return output_tensor
