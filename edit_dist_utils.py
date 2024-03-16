'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.
[!] Feel free to use any of these methods as needed in your DistlePlayer.
[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''
def get_edit_dist_table(row_str: str, col_str: str) -> list[list[int]]:
    '''
    Returns the completed Edit Distance memoization structure: a 2D list
    of ints representing the number of string manupulations required to
    minimally turn each subproblem's string into the other.
    Parameters:
    row_str (str):
    The string located along the table's rows
    col_str (col):
    The string located along the table's columns
    Returns:
    list[list[int]]:
    Completed memoization table for the computation of the
    edit_distance(row_str, col_str)
    '''
    # [!] TODO
    memo = [[0] * (len(col_str) + 1) for _ in range(len(row_str) + 1)]
    for i in range(len(row_str) + 1):
        memo[i][0] = i
    for j in range(len(col_str) + 1):
        memo[0][j] = j
    for i in range(1, len(row_str) + 1):
        for j in range(1, len(col_str) + 1):
            # If the characters are equal, no operation is needed
            if row_str[i - 1] == col_str[j - 1]:
                memo[i][j] = memo[i - 1][j - 1]
            else:
                # Choose the minimum of three possible operations: insert, delete, or replace
                memo[i][j] = min(memo[i - 1][j] + 1,  # Insertion
                                 memo[i][j - 1] + 1,  # Deletion
                                 memo[i - 1][j - 1] + 1)  # Replacement

    return memo

def edit_distance(s0: str, s1: str) -> int:
    '''
    Returns the edit distance between two given strings, defined as an
    int that counts the number of primitive string manipulations (i.e.,
    Insertions, Deletions, Replacements, and Transpositions) minimally
    required to turn one string into the other.
    [!] Given as part of the skeleton, no need to modify
    Parameters:
    s0, s1 (str):
    The strings to compute the edit distance between
    Returns:
    int:
    The minimal number of string manipulations
    '''
    if s0 == s1: return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]
def get_transformation_list(s0: str, s1: str) -> list[str]:
    '''
    Returns one possible sequence of transformations that turns String s0
    into s1. The list is in top-down order (i.e., starting from the largest
    subproblem in the memoization structure) and consists of Strings representing
    the String manipulations of:
    1. "R" = Replacement
    2. "T" = Transposition
    3. "I" = Insertion
    4. "D" = Deletion
    In case of multiple minimal edit distance sequences, returns a list with
    ties in manipulations broken by the order listed above (i.e., replacements
    preferred over transpositions, which in turn are preferred over insertions, etc.)
    [!] Given as part of the skeleton, no need to modify
    Example:
    s0 = "hack"
    s1 = "fkc"
    get_transformation_list(s0, s1) => ["T", "R", "D"]
    get_transformation_list(s1, s0) => ["T", "R", "I"]
    Parameters:
    s0, s1 (str):
    Start and destination strings for the transformation
    Returns:
    list[str]:
    The sequence of top-down manipulations required to turn s0 into s1
    '''
    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))
def get_transformation_list_with_table(s0: str, s1: str, table: list[list[int]]) -> list[str]:
    '''
    See get_transformation_list documentation.
    This method does exactly the same thing as get_transformation_list, except that
    the memoization table is input as a parameter. This version of the method can be
    used to save computational efficiency if the memoization table was pre-computed
    and is being used by multiple methods.
    [!] MUST use the already-solved memoization table and must NOT recompute it.
    [!] MUST be implemented recursively (i.e., in top-down fashion)
    '''
    # [!] TODO
    def backtrack_transformations(i: int, j: int) -> list[str]:
        if i == 0 and j == 0:
            return []
        elif i == 0:
            return ["INSERT " + s1[j - 1]] + backtrack_transformations(i, j - 1)
        elif j == 0:
            return ["DELETE " + s0[i - 1]] + backtrack_transformations(i - 1, j)
        else:
            if s0[i - 1] == s1[j - 1]:
                return backtrack_transformations(i - 1, j - 1)
            else:
                min_dist = min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
                if min_dist == table[i - 1][j]:
                    return ["DELETE " + s0[i - 1]] + backtrack_transformations(i - 1, j)
                elif min_dist == table[i][j - 1]:
                    return ["INSERT " + s1[j - 1]] + backtrack_transformations(i, j - 1)
                else:
                    return ["REPLACE " + s0[i - 1] + " WITH " + s1[j - 1]] + backtrack_transformations(i - 1, j - 1)

    # Call the backtrack function starting from the end of both strings
    return backtrack_transformations(len(s0), len(s1))