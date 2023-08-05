def pos_neg(n):
    p_c = 0
    n_c = 0
    for value in n:
        if value >=0:
            p_c = p_c + 1
        else:
            n_c = n_c + 1
    return p_c,n_c