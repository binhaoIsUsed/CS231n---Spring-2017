from __future__ import print_function
import numpy as np
from random import shuffle


def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    # compute the loss and the gradient
    num_classes = W.shape[1]
    num_train = X.shape[0]
    loss = 0.0
    for i in xrange(num_train):
        scores = X[i].dot(W)
        correct_class_score = scores[y[i]]
        for j in xrange(num_classes):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            if margin > 0:
                loss += margin
                dW[:, y[i]] -= X[i]
                dW[:, j] += X[i]

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)
    dW += reg * W

    ##########################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    ##########################################################################

    return loss, dW


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero
    delta = 1.0

    ##########################################################################
    # TODO:                                                                  #
    # Implement a vectorized version of the structured SVM loss, storing the #
    # result in loss.                                                        #
    ##########################################################################

    num_train = X.shape[0]

    scores = X.dot(W)
    correct_class_score = scores[[np.arange(num_train), y]]

    margins = np.maximum(
        0, scores - correct_class_score[:, np.newaxis] + delta)

    # the subtraction of delta is to correct for the contribution of the
    # correct class
    loss = np.sum(margins) / num_train - delta

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)

    ##########################################################################
    #                             END OF YOUR CODE                           #
    ##########################################################################

    ##########################################################################
    # TODO:                                                                  #
    # Implement a vectorized version of the gradient for the structured SVM  #
    # loss, storing the result in dW.                                        #
    #                                                                        #
    # Hint: Instead of computing the gradient from scratch, it may be easier #
    # to reuse some of the intermediate values that you used to compute the  #
    # loss.                                                                  #
    ##########################################################################

    # print("X ~", X.shape)
    # print("y ~", y.shape)
    # print("W ~", W.shape)
    # print("scores ~", scores.shape)
    # print("correct_class_score ~", correct_class_score.shape)
    # print("margins ~", margins.shape)
    # print("marginsGZ ~", marginsGZ.shape)
    # print("oneHotScores ~", oneHotScores.shape)

    num_train = X.shape[0]
    num_classes = W.shape[1]

    marginsGZ = margins > 0

    oneHotScores = np.zeros((num_classes, num_train))
    oneHotScores[y, range(num_train)] = 1

    # it only took me 3h to write the following line:
    dW = np.dot(X.T, marginsGZ - (oneHotScores * np.sum(marginsGZ, axis=1)).T)
    dW /= num_train

    dW += reg * W

    ##########################################################################
    #                             END OF YOUR CODE                           #
    ##########################################################################

    return loss, dW
