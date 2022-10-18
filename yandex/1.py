
def main():
    n = int(input())
    n = 2 * n + 1
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    white = 1
    black = -1
    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            if i == j:
                continue

            if i % 2 == 0 and j % 2 != 0 or j % 2 == 0 and i % 2 != 0:
                matrix[i][j] = white
                white += 1

    for j in range(len(matrix[0])):
        for i in range(n):

            if i == j:
                continue

            if i % 2 == 0 and j % 2 == 0 or i % 2 != 0 and j % 2 != 0:
                matrix[i][j] = black
                black -= 1

    for row in matrix:
        print(' '.join([str(i) for i in row]))


if __name__ == '__main__':
    main()
