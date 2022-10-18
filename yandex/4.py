def main_1(n, area, points):
    sides = get_all_sides(area)

    orders = []
    for point in points:
        for side in sides:
            rectangle = (
                point[0] + side[0],
                point[0] + side[1],
                point[1] + side[0],
                point[1] + side[1]
            )
            result = points_in_rectangle(points, rectangle)
            orders.append(result)

    max_len = 0
    for order in orders:
        if len(order) > max_len:
            max_len = len(order)

    print(max_len)
    if orders:
        max_order = orders[0]
        for order in orders:
            if len(order) == max_len:
                max_order = order

        print(max_order)


def get_all_sides(area):
    sides = []
    first = 0
    last = area

    while first <= last:
        sum_f_l = first + last
        if sum_f_l == area:
            sides.append((first, last))
            if first != last:
                sides.append((last, first))

            first += 1
            last -= 1
        else:
            if sum_f_l < area:
                first += 1
            else:
                last -= 1

    return sides


def main(n, area, points):
    """
    .-------.
    |       |
    |       |
    .-------.
    """
    rectangle = get_rectangle(points)
    while True:
        s = (rectangle[2][0] - rectangle[0][0]) * (rectangle[2][1] - rectangle[0][1])
        if s == area:
            points = points_in_rectangle(points, rectangle)
            print(len(points))
            return

        rectangle = get_rectangle(points)


def get_rectangle(points):
    sorted_x = sorted(points, key=lambda x: x[0])
    sorted_y = sorted(points, key=lambda x: x[1])

    max_x_point = sorted_x[:-1]
    min_x_pont = sorted_x[0]

    max_y_point = sorted_y[:-1]
    min_y_point = sorted_y[0]

    min_x = min_x_pont[0]
    min_y = max_y_point[1]

    max_x = max_x_point[0]
    max_y = min_y_point[1]

    return (min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)


def points_in_rectangle(points, rectangle):
    result = []
    for point in points:
        if (
                point[0] >= rectangle[0] and point[0] >= rectangle[2]
                and point[1] <= rectangle[1] and point[1] <= rectangle[3]
        ):
            result.append(point)

    return result


if __name__ == '__main__':
    # n, s = map(float, input().split())
    # points = [tuple(map(float, input().split())) for _ in range(int(n))]
    # main(n, s, points)
    main(5, 2, [(0, 0), (0, 2), (2, 0), (1, 1), (2, 2)])

"""
5 1
0 0
0 2
2 0
1 1
2 2

2
1 4
"""

"""
5 2
0 0
0 2
2 0
1 1
2 2

3
1 3 4
"""
