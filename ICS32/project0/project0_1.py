def diagonal_block(n):
    """Print diagonal blocks of size n."""
    if n == 0:
        return ''
    result = '+-+\n'
    for i in range(n):
        result += (i * '  ' + '| |\n')
        if i < n - 1:
            result += (i * '  ' + '+-+-+\n')
        elif i == n - 1:
            result += (i * '  ' + '+-+')
    return result


if __name__ == "__main__":
    x = int(input())
    print(diagonal_block(x))