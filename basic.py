from resource import getrusage, RUSAGE_SELF
import sys
import time

GAP = 30
BASE_INDEX = {base: i for i, base in enumerate("ACGT")}
MISMATCH = ( # mismatch penalties for A, C, G, T
    (0, 110, 48, 94),
    (110, 0, 118, 48),
    (48, 118, 0, 110),
    (94, 48, 110, 0),
)

def read_input(path):
    """build the two strings from the input file"""
    with open(path) as file: # open file
        lines = [line.strip() for line in file if line.strip()] # remove whitsepace
    #init
    position = 0
    strings = []
    for _ in range(2): # for each of the two strings
        current = lines[position]
        position += 1
        while position < len(lines) and lines[position].isdigit(): # while we haven't reached end and current line contains digits 
            split = int(lines[position]) + 1 # split index is the number in the current line + 1
            current = current[:split] + current + current[split:] # insert current string into itself at the split index
            position += 1
        strings.append(current)
    return strings[0], strings[1]


def basic_alignment(x, y):
    """Full DP table and traceback"""
    m, n = len(x), len(y)
    dp = []  

    for i in range(m + 1):  # create table with m+1 rows and n+1 columns with all zeros
        row = []  
        for j in range(n + 1): 
            row.append(0)
        dp.append(row)  

    # initialize first row and column of DP table
    for i in range(m + 1):
        dp[i][0] = i * GAP
    for j in range(n + 1):
        dp[0][j] = j * GAP

    # min cost of aligning first i characters of x with first j characters of y
    for i in range(1, m + 1):  # Go through each character in x and y 
        for j in range(1, n + 1):  
            x_index = BASE_INDEX[x[i - 1]]  # Get the table index for x
            y_index = BASE_INDEX[y[j - 1]]  # Get the table index for y

            mismatch_cost = MISMATCH[x_index][y_index]  # Cost of pairing these characters

            pair = dp[i - 1][j - 1] + mismatch_cost  # pair
            gap_in_y = dp[i - 1][j] + GAP  # pair x with gap
            gap_in_x = dp[i][j - 1] + GAP  # Pair y with gap

            dp[i][j] = min(pair, gap_in_y, gap_in_x)  # Choose cheapest option

    # traceback 
    aligned_x, aligned_y = [], []
    i, j = m, n # start at bottom right 
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == ( # diagonal 
            dp[i - 1][j - 1] + MISMATCH[BASE_INDEX[x[i - 1]]][BASE_INDEX[y[j - 1]]]
        ):
            aligned_x.append(x[i - 1]) # add both chars and decrement i, j 
            aligned_y.append(y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + GAP: #upward 
            aligned_x.append(x[i - 1])
            aligned_y.append("_")
            i -= 1
        else: # leftward 
            aligned_x.append("_")
            aligned_y.append(y[j - 1])
            j -= 1
    return dp[m][n], "".join(reversed(aligned_x)), "".join(reversed(aligned_y))

# memory and time calculation
def process_memory():
    # using peak memory
    memory_consumed = getrusage(RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":  # mac in bytes
        memory_consumed = memory_consumed / 1024
    return float(memory_consumed)


def time_wrapper(x, y):
    start_time = time.time()
    cost, aligned_x, aligned_y = basic_alignment(x, y)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return cost, aligned_x, aligned_y, time_taken


def main():
    if len(sys.argv) != 3:
        raise SystemExit(2)
    x, y = read_input(sys.argv[1])  # Read input and generate strings.
    cost, aligned_x, aligned_y, time_taken = time_wrapper(x, y)
    memory_consumed = process_memory()  # measure memory
    with open(sys.argv[2], "w") as output:
        output.write(f"{cost}\n{aligned_x}\n{aligned_y}\n{time_taken:.6f}\n{memory_consumed:.6f}\n")


if __name__ == "__main__":
    main()
