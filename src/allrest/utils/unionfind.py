class UnionFind:
    def __init__(self, size):
        self.root = [i for i in range(size)]  # Each element is its own root initially
        self.rank = [1] * size  # Used to keep the tree flat
    
    def find(self, x):
        """Find the root of x"""
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])  # Path compression
        return self.root[x]
    
    def union(self, x, y):
        """Union the sets that x and y belong to"""
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
    
    def connected(self, x, y):
        """Check if x and y are in the same subset"""
        return self.find(x) == self.find(y)


if __name__ == "__main__":
    # Let's create a simple test case for our UnionFind class to demonstrate its functionality.

    # Initialize UnionFind with 10 elements (0 through 9)
    uf = UnionFind(10)

    # Create some unions
    uf.union(1, 2)
    uf.union(2, 3)
    uf.union(4, 5)
    uf.union(5, 6)
    uf.union(7, 8)

    # Now, let's check if certain elements are connected
    test_pairs = [(1, 3), (4, 6), (7, 8), (1, 4), (2, 8), (0, 9)]

    results = []
    for x, y in test_pairs:
        result = uf.connected(x, y)
        results.append((x, y, result))

    print(results)