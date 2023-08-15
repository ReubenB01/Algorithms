def lcs(s1, s2):
    s1_len = len(s1)
    s2_len = len(s2)
    table = [(s2_len + 1) * [0] for i in range(s1_len + 1)]
    string = ""

    for row in range(0, s1_len + 1):
        for col in range(0, s2_len + 1):
            if row == 0 or col == 0:
                table[row][col] = 0
            elif s1[row - 1] == s2[col - 1]:
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                table[row][col] = max(table[row - 1][col], table[row - 1][col - 1], table[row][col - 1])

    i = len(s1)
    j = len(s2)

    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            string = string + s1[i - 1]
            i -= 1
            j -= 1
        else:
            if table[i - 1][j] >= table[i][j - 1]:
                i -= 1
            else:
                j -= 1

    return string[::-1]


def line_edits(s1, s2):
    lines1 = s1.splitlines()
    lines2 = s2.splitlines()

    lines1_len = len(lines1)
    lines2_len = len(lines2)

    # Initialize table
    cost = [[0] * (lines2_len + 1) for _ in range(lines1_len + 1)]

    # Calculate table
    for i in range(1, lines1_len + 1):
        cost[i][0] = i

    for j in range(1, lines2_len + 1):
        cost[0][j] = j

    for i in range(1, lines1_len + 1):
        for j in range(1, lines2_len + 1):
            if lines1[i - 1] == lines2[j - 1]:
                cost[i][j] = cost[i - 1][j - 1]
            else:
                substitution_cost = cost[i - 1][j - 1] + 1
                deletion_cost = cost[i - 1][j] + 1
                insertion_cost = cost[i][j - 1] + 1
                cost[i][j] = min(substitution_cost, deletion_cost, insertion_cost)

    # Trace back through table
    i = lines1_len
    j = lines2_len
    operations = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines1[i - 1] == lines2[j - 1]:
            operations.append(('C', lines1[i - 1], lines2[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and cost[i][j] == cost[i - 1][j - 1] + 1:
            operations.append(('S', lines1[i - 1], lines2[j - 1]))
            i -= 1
            j -= 1
        elif i > 0 and cost[i][j] == cost[i - 1][j] + 1:
            operations.append(('D', lines1[i - 1], ''))
            i -= 1
        else:
            operations.append(('I', '', lines2[j - 1]))
            j -= 1

    # Highlight modified characters
    highlighted = []
    for op in operations[::-1]:
        if op[0] == 'S':
            lcs_result = lcs(op[1], op[2])
            left_string = ''
            right_string = ''
            for c in op[1]:
                if c not in lcs_result:
                    left_string += '[[' + c + ']]'
                else:
                    left_string += c
            for c in op[2]:
                if c not in lcs_result:
                    right_string += '[[' + c + ']]'
                else:
                    right_string += c
            highlighted_op = ('S', left_string, right_string)
            highlighted.append(highlighted_op)
        else:
            highlighted.append(op)

    return highlighted


s1 = "Line1\nLine 2a\nLine3\nLine4\n"
s2 = "Line5\nline2\nLine3\n"
table = line_edits(s1, s2)
for row in table:
    print(row)