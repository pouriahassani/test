import numpy as np

def fem_1d_poisson(n):
    """
    Assemble the FEM system for -u'' = 1 on (0,1) with u(0)=u(1)=0
    using piecewise linear elements on an equispaced mesh.

    Parameters:
    - n: number of elements (=> n+1 nodes, n-1 interior nodes)

    Returns:
    - A: (n-1)x(n-1) stiffness matrix
    - b: (n-1) load vector
    - h: mesh size
    """
    # Mesh size
    h = 1.0 / n

    # Number of interior nodes
    N = n - 1

    # Stiffness matrix: tridiagonal with 2 on diagonal and -1 on off-diagonals
    A = (1.0 / h) * (2 * np.eye(N) - np.eye(N, k=1) - np.eye(N, k=-1))

    # right-hand side vector: f = 1, piecewise linear elements
    # For uniform f=1 and uniform mesh, each interior node gets 2*h/2 = h
    b = np.ones(N) * h

    return A, b, h

def dorr(alpha: float, n: int) -> np.ndarray:
    """
    Generate the Dorr matrix of order n with parameter alpha.

    Parameters
    ----------
    alpha : float
        Parameter controlling the strength of the perturbation. Smaller alpha leads to more ill-conditioning.
    n : int
        Size of the matrix.

    Returns
    -------
    A : ndarray of shape (n, n)
        The Dorr matrix.
    
    Reference
    ---------
    Fred Dorr, "An example of ill-conditioning in the numerical solution of singular perturbation problems",
    Mathematics of Computation, 25(114), 1971, pp. 271–283.
    """
    A = np.zeros((n, n), dtype=float)
    np1 = n + 1

    for i in range(n):
        row_idx = i + 1  # For 1-based indexing in formulas

        if row_idx <= (np1 // 2):
            # Upper half
            if i > 0:
                A[i, i - 1] = -alpha * np1**2
            A[i, i] = 2 * alpha * np1**2 + 0.5 * np1 - row_idx
            if i < n - 1:
                A[i, i + 1] = -alpha * np1**2 - 0.5 * np1 + row_idx
        else:
            # Lower half
            if i > 0:
                A[i, i - 1] = -alpha * np1**2 + 0.5 * np1 - row_idx
            A[i, i] = 2 * alpha * np1**2 - 0.5 * np1 + row_idx
            if i < n - 1:
                A[i, i + 1] = -alpha * np1**2

    return A

if __name__ == "__main__":

    n = 5  # number of elements (n+1 nodes)
    A, b, h = fem_1d_poisson(n)

    print("Stiffness matrix A:\n", A)
    print("\nVector b:\n", b)
