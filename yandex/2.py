import math


def main():
    w = int(input())
    n, k = map(int, input().split())
    photos = [input().split("x") for _ in range(n)]

    heights = []
    for photo in photos:
        new_height = math.ceil((int(photo[1]) * w) / int(photo[0]))
        heights.append(new_height)

    heights = sorted(heights)
    maximum = sum(heights[:k])
    minimum = sum(heights[len(heights) - k:])
    print(maximum)
    print(minimum)


if __name__ == '__main__':
    main()
