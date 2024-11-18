def recognize_previous_str(context) -> list:
    cache_lst = []
    for i in range(len(context)):
        cache_lst.append(context[i])
        if isinstance(i, str) and isinstance(context[i], str) and context[i] == 'self':
            return cache_lst