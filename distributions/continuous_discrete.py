import math
import numpy as np

# Continuous Distributions

def uniforme(a: float, b: float, r: list[float]):
    """Generates random numbers from a Uniform(a, b) distribution."""
    if a >= b:
        raise ValueError("Parameter 'a' must be less than 'b' for Uniform distribution.")
    return [a + (b - a) * ri for ri in r]

def exponencial(lmbda: float, r: list[float]):
    """Generates random numbers from an Exponential(lambda) distribution."""
    if lmbda <= 0:
        raise ValueError("Parameter 'lambda' must be greater than 0 for Exponential distribution.")
    return [-(1/lmbda) * math.log(1 - ri) for ri in r]

def erlang(k: int, lmbda: float, r: list[float]):
    """Generates random numbers from an Erlang(k, lambda) distribution."""
    if k <= 0 or not isinstance(k, int):
        raise ValueError("Parameter 'k' must be a positive integer for Erlang distribution.")
    if lmbda <= 0:
        raise ValueError("Parameter 'lambda' must be greater than 0 for Erlang distribution.")
    
    xs = []
    # Ensure enough random numbers for k groups
    num_groups = len(r) // k
    for i in range(num_groups):
        prod = 1.0
        for j in range(k):
            prod *= (1 - r[i * k + j]) # Using 1-ri to avoid log(0)
        xs.append(-(1/lmbda) * math.log(prod))
    return xs

def gamma(alpha: int, beta: float, r: list[float]):
    """Generates random numbers from a Gamma(alpha, beta) distribution (for integer alpha)."""
    if alpha <= 0 or not isinstance(alpha, int):
        raise ValueError("Parameter 'alpha' must be a positive integer for Gamma distribution (this implementation).")
    if beta <= 0:
        raise ValueError("Parameter 'beta' must be greater than 0 for Gamma distribution.")
    
    xs = []
    num_groups = len(r) // alpha
    for i in range(num_groups):
        sum_logs = 0.0
        for j in range(alpha):
            sum_logs += math.log(1 - r[i * alpha + j]) # Using 1-ri to avoid log(0)
        xs.append(-beta * sum_logs)
    return xs

def normal(mu: float, sigma: float, r: list[float]):
    """Generates random numbers from a Normal(mu, sigma) distribution using Box-Muller."""
    if sigma <= 0:
        raise ValueError("Parameter 'sigma' must be greater than 0 for Normal distribution.")
    
    xs = []
    # Box-Muller requires pairs of random numbers
    for i in range(0, len(r) - 1, 2):
        r1 = r[i]
        r2 = r[i+1]
        
        # Avoid log(0) by ensuring r1 is not 0
        if r1 == 0:
            r1 = 1e-10 # Small epsilon to prevent log(0)

        z1 = math.sqrt(-2 * math.log(r1)) * math.cos(2 * math.pi * r2)
        z2 = math.sqrt(-2 * math.log(r1)) * math.sin(2 * math.pi * r2)
        xs.extend([mu + sigma * z1, mu + sigma * z2])
    return xs

def weibull(gamma_: float, beta: float, alpha: float, r: list[float]):
    """Generates random numbers from a Weibull(gamma, beta, alpha) distribution."""
    if beta <= 0:
        raise ValueError("Parameter 'beta' must be greater than 0 for Weibull distribution.")
    if alpha <= 0:
        raise ValueError("Parameter 'alpha' must be greater than 0 for Weibull distribution.")
    
    return [gamma_ + beta * ((-math.log(1 - ri)) ** (1/alpha)) for ri in r]

# Discrete Distributions

def uniforme_discreta(a: int, b: int, r: list[float]):
    """Generates random integers from a Discrete Uniform(a, b) distribution."""
    if a >= b:
        raise ValueError("Parameter 'a' must be less than 'b' for Discrete Uniform distribution.")
    return [a + int((b - a + 1) * ri) for ri in r]

def bernoulli(p: float, r: list[float]):
    """Generates random numbers from a Bernoulli(p) distribution."""
    if not (0 <= p <= 1):
        raise ValueError("Parameter 'p' must be between 0 and 1 for Bernoulli distribution.")
    return [1 if ri < p else 0 for ri in r]

def binomial(n: int, p: float, r: list[float]):
    """Generates random numbers from a Binomial(n, p) distribution."""
    if n <= 0 or not isinstance(n, int):
        raise ValueError("Parameter 'n' must be a positive integer for Binomial distribution.")
    if not (0 <= p <= 1):
        raise ValueError("Parameter 'p' must be between 0 and 1 for Binomial distribution.")
    
    xs = []
    num_trials = len(r) // n
    for i in range(num_trials):
        suma = 0
        for j in range(n):
            if r[i * n + j] < p:
                suma += 1
        xs.append(suma)
    return xs

def poisson(lmbda: float, r: list[float]):
    """Generates random numbers from a Poisson(lambda) distribution using Knuth's algorithm."""
    if lmbda <= 0:
        raise ValueError("Parameter 'lambda' must be greater than 0 for Poisson distribution.")
    
    xs = []
    L = math.exp(-lmbda)
    k = 0
    p = 1.0
    r_idx = 0
    while r_idx < len(r):
        p *= r[r_idx]
        r_idx += 1
        if p <= L:
            xs.append(k)
            p = 1.0
            k = 0
        else:
            k += 1
    return xs
