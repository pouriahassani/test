# 🔍 Understanding Tridiagonal Matrices, Stability, and Conditioning

This document captures the discussion and explanations from a conversation focused on numerical linear algebra, specifically:

* Tridiagonal matrices
* Their real-world relevance
* Second derivative approximations
* Concepts of stability and conditioning
* Error bounds for solvers under floating-point arithmetic
* Metrics like 2-norm and MRED
* Toeplitz vs FEM tridiagonal matrices

---

## 📌 What is a Tridiagonal Matrix?

A **tridiagonal matrix** is a square matrix where only the main diagonal and the two diagonals directly adjacent to it (above and below) may contain non-zero entries.

### Example (5x5):

$$
\begin{bmatrix}
  b_1 & c_1 & 0   & 0   & 0 \\
  a_2 & b_2 & c_2 & 0   & 0 \\
  0   & a_3 & b_3 & c_3 & 0 \\
  0   & 0   & a_4 & b_4 & c_4 \\
  0   & 0   & 0   & a_5 & b_5
\end{bmatrix}
$$

Such matrices arise frequently when discretizing 1D differential equations.

---

## 🧮 Where Do Tridiagonal Matrices Appear?

| Domain               | Application Example                            |
| -------------------- | ---------------------------------------------- |
| Heat transfer        | 1D heat conduction in rods                     |
| Structural mechanics | Beam bending or deflection                     |
| Fluid flow           | 1D channel or pipe flow                        |
| Quantum mechanics    | 1D Schrödinger equation (tight-binding models) |
| Finance              | PDE-based option pricing models                |
| Interpolation        | Natural cubic splines                          |

In all these cases, only adjacent points interact, which is why the system matrix becomes tridiagonal.

---

## ✂️ How Does the Second Derivative Become a Tridiagonal Stencil?

We start from the 1D Poisson equation:

$$
-\frac{d^2 u}{dx^2} = f(x), \quad x \in (0,1), \quad u(0) = u(1) = 0
$$

### Discretize the interval:

Divide $[0,1]$ into $n$ equal segments (spacing $h = 1/n$). The grid points are:

$$
x_0 = 0,\ x_1 = h,\ \dots,\ x_n = 1
$$

We want to approximate $u''(x_i)$ using its neighbors.

### Taylor Expansion Derivation:

Use Taylor series around $x_i$:

$$
\begin{align*}
  u(x_{i+1}) &= u(x_i) + h u'(x_i) + \frac{h^2}{2} u''(x_i) + \dots \\
  u(x_{i-1}) &= u(x_i) - h u'(x_i) + \frac{h^2}{2} u''(x_i) - \dots
\end{align*}
$$

Add the two:

$$
u(x_{i+1}) + u(x_{i-1}) = 2u(x_i) + h^2 u''(x_i) + O(h^4)
$$

Solve for $u''(x_i)$:

$$
u''(x_i) \approx \frac{u_{i-1} - 2u_i + u_{i+1}}{h^2}
$$

This yields the tridiagonal stencil in matrix form.

---

## 🏗️ Uniform vs Non-Uniform Grid

A **uniform mesh** divides the domain into equal-sized segments:

$$
h = \frac{1}{n}, \quad x_i = ih, \quad h_i = x_{i+1} - x_i = h \quad \forall i
$$

In contrast, a **non-uniform mesh** has variable segment sizes:

$$
h_1 \neq h_2 \neq h_3 \neq \dots
$$

| Mesh Type   | Description                  | Implication on Matrix |
| ----------- | ---------------------------- | --------------------- |
| Uniform     | All elements have equal size | Often Toeplitz-like   |
| Non-uniform | Element sizes vary           | Non-Toeplitz          |

---

## 🔁 Tridiagonal Toeplitz vs FEM Matrix

### Tridiagonal Toeplitz

A matrix with **constant values on each diagonal**:

$$
T = \begin{bmatrix}
  b & c &   &        &   \\
  a & b & c &        &   \\
    & a & b & \ddots &   \\
    &   & \ddots & \ddots & c \\
    &   &        & a & b \\
\end{bmatrix}
$$

Used in: finite difference schemes, numerical linear algebra benchmarks.

### FEM Matrix for 1D Poisson

From piecewise linear basis functions:

* Still tridiagonal and symmetric
* Not necessarily Toeplitz unless mesh is uniform
* Values derived from integrals over elements

---

## 📐 Conditioning vs Stability

These concepts help us understand error amplification and solver behavior.

### 🎯 Conditioning (Problem-level)

Conditioning tells us how **sensitive the solution** of a problem is to changes in the input.

$$
\kappa(A) = \|A\| \cdot \|A^{-1}\|
$$

Or in 2-norm:

$$
\kappa_2(A) = \frac{\sigma_{\max}}{\sigma_{\min}}
$$

| $\kappa(A)$ | Meaning                     |
| ----------- | --------------------------- |
| \~1         | Well-conditioned            |
| 10^3 - 10^5 | Moderate risk of inaccuracy |
| > 10^6      | Ill-conditioned             |

### 🧠 Stability (Algorithm-level)

Stability refers to whether an **algorithm magnifies small errors** (like rounding or hardware approximation errors).

---

## 📏 Floating-Point Error Bound (Forward Error)

When solving $Ax = b$ using floating-point arithmetic, the computed solution $\hat{x}$ satisfies:

$$
\frac{\|x - \hat{x}\|}{\|x\|} \leq C \cdot \epsilon_{\text{mach}} \cdot \kappa(A)
$$

Where:

* $x$: exact solution
* $\hat{x}$: computed solution
* $C$: small constant ($1 \leq C \leq 10$ for stable methods)
* $\epsilon_{\text{mach}}$: machine epsilon (e.g. $\approx 10^{-7}$ for 32-bit float)

### Example:

If $\kappa(A) = 10^3$, $\epsilon = 1.2 \times 10^{-7}$, $C = 5$:

$$
\frac{\|x - \hat{x}\|}{\|x\|} \leq 6 \times 10^{-4} \Rightarrow 0.06\% \text{ relative error}
$$

---

## 🧮 Error Metrics

### 🔹 2-Norm of Vector Difference

$$
\|x - \hat{x}\|_2 = \sqrt{ \sum_{i=1}^n (x_i - \hat{x}_i)^2 }
$$

### 🔹 Relative Forward Error

$$
\text{RelErr} = \frac{ \|x - \hat{x}\|_2 }{ \|x\|_2 }
$$

### 🔹 Mean Relative Error of Differences (MRED)

$$
\text{MRED} = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{x_i - \hat{x}_i}{x_i} \right|
$$

To avoid division by zero:

$$
\text{MRED}_\varepsilon = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{x_i - \hat{x}_i}{x_i + \varepsilon} \right| \quad \text{for small } \varepsilon > 0
$$

---

## 📊 Summary Table

| Concept         | Refers To         | Measures                               |
| --------------- | ----------------- | -------------------------------------- |
| 🎯 Conditioning | The **problem**   | Output sensitivity to input            |
| 🧠 Stability    | The **algorithm** | Error amplification during computation |
| 🧮 Condition #  | $\kappa(A)$       | Degree of ill-conditioning             |

Use stable solvers on well-conditioned systems when possible. Measure errors numerically to evaluate robustness under hardware approximation.

---

## 🔬 Why This Matters for Approximate Multiplication

You're using a solver (like Thomas algorithm) on hardware with **approximate multiplication**. The impact of error depends on:

* ✅ Matrix is well-conditioned + algorithm is stable → **accurate result**
* ❌ Matrix is ill-conditioned → **hardware errors get amplified**

Use these to assess solver quality:

* **Relative Error**:

$$
\frac{\|x - \hat{x}\|}{\|x\|}
$$

* **Backward Error**:

$$
\frac{\|A \hat{x} - b\|}{\|b\|}
$$

---


