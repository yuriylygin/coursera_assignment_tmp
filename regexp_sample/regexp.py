def calculate(data, findall):
    matches = findall(r"([abc])(\+=|-=|=)([abc]?)([\+-]?[0-9]+)?")  # Если придумать хорошую регулярку, будет просто
    print(matches)
    for v1, s, v2, n in matches:
        if s == '=':
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s == '+=':
            data[v1] += data.get(v2, 0) + int(n or 0)
        elif s == '-=':
            data[v1] -= data.get(v2, 0) + int(n or 0)

    return data
