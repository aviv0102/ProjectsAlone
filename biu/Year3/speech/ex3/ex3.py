'''
Itay Hassid 209127596  Aviv Shisman 206558157
'''

import numpy as np
import sys


# a ab -> 0.23
# b ab -> ?
# aa ab -> 0.14
# ab ab -> 0.03
# ba ab -> 0.36

blank = '_'

def main():

    # load info:
    #prob_mat = np.array([[0.4, 0.2, 0.4], [0.1, 0.5, 0.4], [0.9, 0.05, 0.05]])
    prob_mat = np.load(sys.argv[1])
    prob_mat = prob_mat.transpose()             # rows - possible phonemes +1, col - time frames
    transcription = sys.argv[2]
    possible_phonemes = list(sys.argv[3]) + [blank]
    z_vector = get_Z(transcription)

    # calc prob:
    ctc_mat, res = ctc_prob(prob_mat, possible_phonemes, z_vector)
    print(round(res, 2))


'''
get the Z vector from string
'''
def get_Z(string):
    start = string.split(blank)
    return blank + blank.join(list(''.join(start))) + blank


'''
calculate ctc probability table
'''
def ctc_prob(prob_mat, possible_phonemes, Z_string):


    # initallize
    ctc_mat = np.zeros((len(Z_string) + 1, prob_mat.shape[1] + 1))  # add zeros for padding
    Z = list(Z_string)
    ctc_mat[1][1] = prob_mat[-1][0]                                        # y[epslion,t=0]
    ctc_mat[2][1] = prob_mat[possible_phonemes.index(Z_string[1])][0]     # y[z1, t=0]

    # dynamic programming:
    for i in range(1, ctc_mat.shape[0]):
        for j in range(2, ctc_mat.shape[1]):
            a1 = ctc_mat[i - 1][j - 1]
            a2 = ctc_mat[i][j - 1]

            if Z[i - 1] == blank or (i>3 and Z[i - 1] == Z[i - 3]):     # first case
                res = a1 + a2            # a[s-1][t-1] + a[s][t-1]
            else:                                                       # second case
                a3 =0
                if i >2:
                    a3 = ctc_mat[i - 2][j - 1]
                res = a1 + a2 + a3      # a[s-1][t-1] + a[s][t-1] + a[s-2][t-1]

            prob = prob_mat[possible_phonemes.index(Z[i - 1])][j-1] # res = res * y[Z=s.T=t]
            ctc_mat[i][j] = res * prob


    # final result
    res = ctc_mat[-1][-1] + ctc_mat[-2][-1]

    return ctc_mat,res


if __name__ == "__main__":
    main()
