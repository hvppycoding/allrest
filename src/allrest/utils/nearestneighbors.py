import numpy as np
from typing import List


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


def get_nearest_neighbors(x: List[int], y: List[int]) -> List[List[int]]:
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    pts = [Point(_x, _y) for _x, _y in zip(x, y)]
    pt_count = len(pts)
    neighbors = [[] for _ in range(pt_count)]

    # Initialize arrays to track quadrant boundaries
    ur = [np.inf] * pt_count
    lr = [np.inf] * pt_count
    ul = [-np.inf] * pt_count
    ll = [-np.inf] * pt_count

    # Sort indices based on y (primary) and x (secondary) coordinates
    sorted_indices = sorted(range(pt_count), key=lambda i: (pts[i].getY(), pts[i].getX()))

    # Compute neighbors
    for idx, pt_idx in enumerate(sorted_indices):
        pt_x = pts[pt_idx].getX()
        for i in range(idx):
            below_idx = sorted_indices[i]
            below_x = pts[below_idx].getX()
            if below_x <= pt_x < ur[below_idx]:
                neighbors[below_idx].append(pt_idx)
                ur[below_idx] = pt_x
            elif ul[below_idx] < pt_x < below_x:
                neighbors[below_idx].append(pt_idx)
                ul[below_idx] = pt_x

        for i in range(idx - 1, -1, -1):
            below_idx = sorted_indices[i]
            below_x = pts[below_idx].getX()
            if pt_x <= below_x < lr[pt_idx]:
                neighbors[pt_idx].append(below_idx)
                lr[pt_idx] = below_x
            elif ll[pt_idx] < below_x < pt_x:
                neighbors[pt_idx].append(below_idx)
                ll[pt_idx] = below_x

    return neighbors


if __name__ == "__main__":
    x = np.random.randint(0, 100, 10).tolist()
    y = np.random.randint(0, 100, 10).tolist()
    
    # Run the test
    neighbors = get_nearest_neighbors(x, y)

    # Print the results
    for i, pts in enumerate(neighbors):
        neighbor_points = [f"Point {j}" for j in pts]
        print(f"Neighbors of Point {i}: {', '.join(neighbor_points)}")
        
    
    import matplotlib.pyplot as plt

    # Plot the points
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue')

    # Annotate points
    for i, (px, py) in enumerate(zip(x, y)):
        plt.text(px, py, f'P{i}', color='red', fontsize=12)

    # Draw lines between neighbors
    for i, neighbor_idxs in enumerate(neighbors):
        for ni in neighbor_idxs:
            plt.plot([x[i], x[ni]], [y[i], y[ni]], 'g--')

    plt.title('Nearest Neighbors Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.savefig('nearest_neighbors.png')