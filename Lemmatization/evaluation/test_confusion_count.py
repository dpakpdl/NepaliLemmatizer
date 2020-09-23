from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np

labels = ['cat', 'fish', 'hen']
actual = ["cat"] * 4 + ['fish'] * 2 + ['hen'] * 6
expected = ["cat"] * 4 + ['fish'] * 2 + ['hen'] * 6

expected += ['cat', 'cat']
expected += ['fish'] * 8
expected += ['hen'] * 3

actual += ['fish', 'hen']
actual += ['cat']*6
actual += ['hen']*2
actual += ['cat'] * 3

print(expected)
print(actual)
conf = confusion_matrix(expected, actual, labels=labels)
print(conf)


def counts_from_confusion(confusion):
    """
    Obtain TP, FN FP, and TN for each class in the confusion matrix
    """

    counts_list = []

    # Iterate through classes and store the counts
    for i in range(confusion.shape[0]):
        tp = confusion[i, i]

        fn_mask = np.zeros(confusion.shape)
        fn_mask[i, :] = 1
        fn_mask[i, i] = 0
        fn = np.sum(np.multiply(confusion, fn_mask))

        fp_mask = np.zeros(confusion.shape)
        fp_mask[:, i] = 1
        fp_mask[i, i] = 0
        fp = np.sum(np.multiply(confusion, fp_mask))

        tn_mask = 1 - (fn_mask + fp_mask)
        tn_mask[i, i] = 0
        tn = np.sum(np.multiply(confusion, tn_mask))

        counts_list.append({'Class': i,
                            'TP': tp,
                            'FN': fn,
                            'FP': fp,
                            'TN': tn})
    return counts_list


print(counts_from_confusion(conf))