def max2(iterable):
    """

    :param iterable: An iterable
    :return: A list with with the 2 largest elements in the iterable
    """
    first = None
    second = None
    for ele in iterable:
        if first is None or ele > first:
            second = first
            first = ele
        elif second is None or ele > second:
            second = ele
    return [first, second]