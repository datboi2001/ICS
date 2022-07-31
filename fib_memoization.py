def fib(n, cache):
    if n == 0:
        return 0
    elif n == 1 or n==2:
        return 1

    if n in cache:
        return cache[n]
    result = fib(n-1, cache) + fib(n-2, cache)
    cache[n] = result
    return result
