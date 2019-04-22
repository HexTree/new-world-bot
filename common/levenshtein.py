# levenshtein distance between two strings
# ref: https://www.python-course.eu/levenshtein_distance.php


def lev_biased(s, t):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t

        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
    """

    rows = len(s) + 1
    cols = len(t) + 1
    # biased costs, to heavily penalise deletion and substitution, and favour insertion
    # we favour insertion because we expect users to often shorthand (e.g. 'iron sword' -> 'iron straight sword')
    deletes, inserts, substitutes = (10, 1, 10)

    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row - 1][col] + deletes,   # deletion
                                 dist[row][col - 1] + inserts,   # insertion
                                 dist[row - 1][col - 1] + cost)  # substitution

    return dist[row][col]
