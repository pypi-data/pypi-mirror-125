from typing import Tuple

from tensorflow.keras.models import Model

from leap_model_rebuilder.modelexpander import expand_model
from leap_model_rebuilder.utils import is_custom_layers, convert_subclassed_to_functional


def rebuild_model(model: Model, input_tensor_shape: Tuple[int, ...]) -> Model:
    """
        Rebuild keras models from Subclassed to Functional and Expands custom layers inside

        :param model: keras model to rebuild in Functional way
        :type model: tensorflow.keras.Model
        :param input_tensor_shape: shape of input tensor
        :type input_tensor_shape: Tuple[int, ...]gst
        :return: rebuilt Functional keras model
        :rtype: tensorflow.keras.Model
        """
    model = convert_subclassed_to_functional(model, input_tensor_shape)
    while is_custom_layers(model):
        model = expand_model(model)

    return model
