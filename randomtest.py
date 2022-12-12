from time import time_ns

if __name__ == "__main__":
    start_1 = time_ns()
    container = []
    for i in range(100):
        container.append(i)
    end_1 = time_ns()

    start_2 = time_ns()
    container_2 = [i for i in range(100)]
    end_2 = time_ns()
    td_1 = end_1 - start_1
    td_2 = end_2 - start_2
    print(f"\
        The first method took {td_1}\n\
        The second method took {td_2}")
    print(f"\
        The second method is {td_1/td_2} times faster")
    