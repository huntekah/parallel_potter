def longest_increasing_subsequence(X):
    sequence_length = len(X)
    predecessor = [0] * sequence_length  # Stores the predecessor of each element
    min_index_seq = [-1] * (sequence_length + 1)  # Holds indices for the increasing subsequence
    subsequence_length = 0

    for i in range(sequence_length):
        left = 1
        right = subsequence_length + 1

        # Binary search for the appropriate index to update the subsequence
        while left < right:
            middle = left + ((right - left) // 2)

            if X[min_index_seq[middle]] < X[i]:
                left = middle + 1
            else:
                right = middle

        new_length = left
        predecessor[i] = min_index_seq[new_length - 1]
        min_index_seq[new_length] = i

        if new_length > subsequence_length:
            subsequence_length = new_length

    # Reconstruct the subsequence based on predecessors
    longest_subsequence = []
    k = min_index_seq[subsequence_length]
    while k >= 0:
        longest_subsequence.append(X[k])
        k = predecessor[k]

    longest_subsequence.reverse()
    return longest_subsequence

def prefect_match(increasing_subsequence_l, increasing_subsequence_k, best_l_matches, best_k_matches):
    perfect_l_matches = []
    # Here we should reverse the for, so that we add to perfect_l_matches only increasing subsequence...
    last_k = -1
    for l_filtered in increasing_subsequence_l:
        for k,l_match in enumerate(best_l_matches):
            if l_filtered == l_match and k >= last_k:
                perfect_l_matches.append((k,l_match))
                last_k = k
                break

    print(f"{perfect_l_matches=}")

    last_l = -1
    perfect_k_matches = []
    for k_filtered in increasing_subsequence_k:
        for l,k_match in enumerate(best_k_matches):
            if k_filtered == k_match and l >= last_l:
                perfect_k_matches.append((k_match,l))
                last_l = l
                break

    print(f"{perfect_k_matches=}")
    #intersection of perfect matches
    perfect_matches = sorted(list(set(perfect_l_matches) & set(perfect_k_matches)))
    return perfect_matches

def fill_in_gaps(perfect_matches, sims):
    #fill in gaps in perfect matches, we need t include each sentence when matching dual language chapters
    all_matches = []
    next_l = 0
    next_k = 0
    for k,l in perfect_matches:
        if k == next_k and l == next_l:
            all_matches.append((k,l))
            next_k += 1
            next_l += 1
        else:
            # for ech gap, like [(0, 0), (1, 1), (2, 2), (4, 5)] we need to decide
            # which is best (3,2) or (3,3) or (2,3), and then fill between best and (4,5)
            pass

# Example usage:
if __name__ == "__main__":
    sequence = [3, 4, -1, 5, 8, 2, 3, 12, 7, 9, 10]
    result = longest_increasing_subsequence(sequence)
    print(result)
