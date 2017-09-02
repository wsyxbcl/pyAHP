import numpy as np
from fractions import Fraction

def load_units(file):
    units = []
    with open(file) as fp:
        for line in fp:
            units.append(line.split()[0]) # Used to deal with '\n'
        return units

def cross_compare(units):
    n = len(units)
    A = np.zeros((n, n))
    for i in range(0, n):
        for j in range(i, n):
            if i == j:
                scale = 1
            else:
                scale = float(Fraction(input(units[i]+' to '+units[j]+':')))
            A[i][j] = scale
            A[j][i] = float(1/scale)
    return A

def get_weight(A):
    n = A.shape[0]
    e_vals, e_vecs = np.linalg.eig(A)
    lamb = max(e_vals)
    w = e_vecs[:, e_vals.argmax()]
    w = w / np.sum(w) # Normalization
    # Consistency Checking
    ri = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51}
    ci = (lamb - n) / (n - 1)
    cr = ci / ri[n]
    print("The normalized eigen vector:")
    print(w)
    print('CR = %f'%cr)
    if cr >= 0.1:
        print("Failed in Consistency check.")
        exit = input("Enter 'q' to quit.")
        raise
    return w, cr

if __name__ == '__main__':
    goal = input("Your Goal: ")
    criterions = load_units('criterions.txt')
    alternatives = load_units('alternatives.txt')
    n2 = len(criterions)
    n3 = len(alternatives)
    A = cross_compare(criterions)
    print("The matrix A")
    print(A)
    print()
    W2, cr2 = get_weight(A)
    B = {}
    W3 = np.zeros((n2, n3))
    for i in range(n2):
        print("######################")
        print("Consider "+criterions[i])
        B[str(i)] = cross_compare(alternatives)
        w3, cr3 = get_weight(B[str(i)])
        W3[i] = w3
    W = np.dot(W2, W3)

    print("######################")
    print("The final Weight:")
    print(W)