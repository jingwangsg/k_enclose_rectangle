import numpy as np
import argparse
import matplotlib.pyplot as plt
import time

import numpy as np

def smallest_k_enclosing_rectangle_approx(points, k):
    N = len(points)
    ratio = k / N
    k1 = int(N * np.sqrt(ratio))

    # Sort points by x and y coordinates
    x_sorted = np.sort(points[:, 0])
    y_sorted = np.sort(points[:, 1])

    def sliding_window_min_range(arr, K):
        min_range = float("inf")
        best_pair = None

        for i in range(len(arr) - K + 1):
            range_size = arr[i + K - 1] - arr[i]
            if range_size < min_range:
                min_range = range_size
                best_pair = (arr[i], arr[i + K - 1])
        return best_pair

    # Find the optimal ranges for both axes
    x_min, x_max = sliding_window_min_range(x_sorted, k1)
    y_min, y_max = sliding_window_min_range(y_sorted, k1)

    # Compute the area of the bounding box
    area = (x_max - x_min) * (y_max - y_min)
    return (x_min, y_min, x_max, y_max), area

def smallest_k_enclosing_rectangle_exact(points, k):
    n = len(points)
    # Sort points by x-coordinate
    points = sorted(points, key=lambda p: p[0])
    min_area = float('inf')
    result_rectangle = None

    for i in range(n):
        # Initialize a list to store y-coordinates in the current strip
        y_coords = []
        # For efficient insertion and maintaining order
        from bisect import insort
        for j in range(i, n):
            # Insert y-coordinate of the new point in sorted order
            y = points[j][1]
            insort(y_coords, y)
            # Now, find the minimal height interval covering at least k points
            l = 0
            while l + k - 1 < len(y_coords):
                y_min = y_coords[l]
                y_max = y_coords[l + k - 1]
                area = (points[j][0] - points[i][0]) * (y_max - y_min)
                if area < min_area:
                    min_area = area
                    result_rectangle = (points[i][0], y_min, points[j][0], y_max)
                l += 1  # Move the window up
    return result_rectangle, min_area

def count_points_in_rectangle(points, rectangle):
    x_min, y_min, x_max, y_max = rectangle
    count = 0
    
    for x, y in points:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            count += 1
            
    return count


def plot_points_and_bounding_box(points, rectangle, filename):
    # clear plt
    plt.clf()

    points = np.array(points)
    x_min, y_min, x_max, y_max = rectangle

    plt.scatter(points[:, 0], points[:, 1], label="Points", s=10)

    # Draw bounding box
    rect = plt.Rectangle(
        (x_min, y_min), x_max - x_min, y_max - y_min,
        linewidth=2, edgecolor="r", facecolor="none", label="Bounding Box"
    )
    plt.gca().add_patch(rect)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.title("Points and Smallest K-Enclosing Rectangle")
    plt.savefig(filename)



def get_algo(impl="k_enclose_exact"):
    if impl == "k_enclose_rectangle_exact":
        return smallest_k_enclosing_rectangle_exact
    elif impl == "k_enclose_rectangle_approx":
        return smallest_k_enclosing_rectangle_approx
    else:
        raise ValueError("Invalid algorithm name")

def validate_algo(args, impl="k_enclose_exact"):
    print(f">>>>>>>>>>>>>>> {impl} >>>>>>>>>>>>>>>>")
    np.random.seed(args.seed)
    if args.distribution == "uniform":
        points = np.random.rand(args.num_points, 2)
    elif args.distribution == "normal":
        points = np.random.randn(args.num_points, 2) * args.std + args.mean
        points = np.clip(points, 0, 1)

    K = int(0.8 * len(points))

    algo = get_algo(impl)
    st = time.time()
    rectangle, area = algo(points, K)
    print("Time taken:", time.time() - st)

    print("Smallest rectangle covering at least {} points: {}".format(K, rectangle))
    print("Area:", area)

    num_points = count_points_in_rectangle(points, rectangle)
    print("Number of points in the rectangle:", num_points)

    plot_points_and_bounding_box(points, rectangle, filename=f"{impl}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the smallest rectangle covering at least K points")
    parser.add_argument("seed", type=int, help="Seed for random number generation")
    parser.add_argument("--num_points", type=int, default=1000, help="Number of points to generate")
    parser.add_argument("--distribution", type=str, default="uniform", choices=["uniform", "normal"],)
    # For normal distribution
    parser.add_argument("--std", type=float, default=0.1, help="Standard deviation for normal distribution")
    parser.add_argument("--mean", type=float, default=0.5, help="Mean for normal distribution")
    args = parser.parse_args()

    validate_algo(args, impl="k_enclose_rectangle_approx")
    validate_algo(args, impl="k_enclose_rectangle_exact")

