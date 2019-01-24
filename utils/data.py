import tensorflow as tf
import numpy as np


def make_mnist_iter(batch_size, train=True, to32=True):
    pl_imgs = tf.placeholder(tf.float32, [None, 32*32 if to32 else 28*28])
    pl_lbls = tf.placeholder(tf.int32, [None])
    data = tf.data.Dataset.from_tensor_slices((pl_imgs, pl_lbls))
    if train:
        data = data.apply(tf.data.experimental.shuffle_and_repeat(60000))
    data = data.batch(batch_size)
    return data.make_initializable_iterator(), pl_imgs, pl_lbls


def init_mnist(base_path, sess, iterator, pl_imgs, pl_lbls, normalize=True,
               binarize=False, to32=True):
    imgs, lbls = preprocess_mnist(base_path, normalize, binarize, to32)
    sess.run(iterator.initializer, feed_dict={pl_imgs: imgs, pl_lbls: lbls})


def mnist_eager(base_path, batch_size, train=True, normalize=True,
                binarize=False, to32=True):
    imgs, lbls = preprocess_mnist(base_path, normalize, binarize, to32)
    data = tf.data.Dataset.from_tensor_slices((imgs, lbls))
    if train:
        data = data.apply(tf.data.experimental.shuffle_and_repeat(60000))
    data = data.batch(batch_size)
    return data


def preprocess_mnist(base_path, normalize=True, binarize=False, to32=True):
    imgs = np.load(base_path + "_imgs.npy")
    lbls = np.load(base_path + "_lbls.npy")
    lbls = lbls.astype(np.int32)
    if to32:
        imgs = imgs.reshape((-1, 28, 28))
        imgs = np.pad(imgs, ((0, 0), (2, 2), (2, 2)), "constant")
        imgs = imgs.reshape((-1, 32*32))
    if normalize:
        imgs = imgs.astype(np.float32) / 255
    if binarize:
        if not normalize:
            raise ValueError("Binarization not implemented for unnormalized "
                             "data.")
        imgs = np.around(imgs)
    return imgs, lbls
