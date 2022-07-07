"""Utilities to convert integer vector to categorical."""

from taimatsu.utils.progressbar import *
from taimatsu.utils.metrics import *

# pylint: disable=C0301
# Please refer to Keras: https://github.com/keras-team/keras/blob/14f71177ad28a60a4ea41775b2ac159d3688c792/keras/utils/np_utils.py#L22-L74

#TODO: Have a separate dataloader module as this is duplicated in Adaswarm
def to_categorical(y_class_values, num_classes=None, dtype="float32"):
    """Converts a class vector (integers) to binary class matrix.

    E.g. for use with `categorical_crossentropy`.

    Args:
        y: Array-like with class values to be converted into a matrix
            (integers from 0 to `num_classes - 1`).
        num_classes: Total number of classes. If `None`, this would be inferred
            as `max(y) + 1`.
        dtype: The data type expected by the input. Default: `'float32'`.

    Returns:
        A binary matrix representation of the input. The class axis is placed
        last.

    Example:

    >>> a = tf.keras.utils.to_categorical([0, 1, 2, 3], num_classes=4)
    >>> a = tf.constant(a, shape=[4, 4])
    >>> print(a)
    tf.Tensor(
        [[1. 0. 0. 0.]
        [0. 1. 0. 0.]
        [0. 0. 1. 0.]
        [0. 0. 0. 1.]], shape=(4, 4), dtype=float32)

    >>> b = tf.constant([.9, .04, .03, .03,
    ...                  .3, .45, .15, .13,
    ...                  .04, .01, .94, .05,
    ...                  .12, .21, .5, .17],
    ...                 shape=[4, 4])
    >>> loss = tf.keras.backend.categorical_crossentropy(a, b)
    >>> print(np.around(loss, 5))
    [0.10536 0.82807 0.1011  1.77196]

    >>> loss = tf.keras.backend.categorical_crossentropy(a, a)
    >>> print(np.around(loss, 5))
    [0. 0. 0. 0.]
    """
    y_class_values = np.array(y_class_values, dtype="int")
    input_shape = y_class_values.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y_class_values = y_class_values.ravel()
    if not num_classes:
        num_classes = np.max(y_class_values) + 1
    num_columns_y = y_class_values.shape[0]
    categorical = np.zeros((num_columns_y, num_classes), dtype=dtype)
    categorical[np.arange(num_columns_y), y_class_values] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical
