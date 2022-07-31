def diagonal(n: int) -> str:
    if n == 0:
        return ''
    result = '+-+\n'
    for x in range(n):
        result += (x * '  ' + '| |\n')
        if x != n - 1:
            result += (x * '  ' + '+-+-+\n')
        else:
            result += (x * '  ' + '+-+')
    return result
if __name__ == "__main__":
    n = int(input())
    print(diagonal(n))
