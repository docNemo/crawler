from math import ceil, floor
from multiprocessing import cpu_count, Process


def __get_additional_number_of_files__(num_elem, num_proc):
    average = num_elem / num_proc
    max_num = int(ceil(average))
    min_num = int(floor(average))

    disadvantage_min_num = (min_num - num_elem % max_num) % max_num

    num_max_num = num_elem // max_num - disadvantage_min_num

    while num_max_num > 0:
        num_max_num -= 1
        yield 1
    while True:
        yield 0


def __prepare_multiprocessing__(navigation_pages, target_func, parse_func, write_func):
    num_cpu = cpu_count()
    print(f"cpu: {num_cpu}")

    num_navigation_pages = len(navigation_pages)
    num_pages_in_thread = int(num_navigation_pages / num_cpu)
    additional_number_of_files = __get_additional_number_of_files__(num_navigation_pages, num_cpu)

    last_ind = 0
    processes = []

    for _ in range(num_cpu):
        new_ind = last_ind + num_pages_in_thread + next(additional_number_of_files)
        processes.append(
            Process(
                target=target_func,
                args=(
                    navigation_pages[last_ind: new_ind],
                    parse_func,
                    write_func
                )
            )
        )
        last_ind = new_ind
    return processes


def start_multiprocessing(navigation_pages, target_func, parse_func, write_func):
    processes = __prepare_multiprocessing__(navigation_pages, target_func, parse_func, write_func)
    for process in processes:
        process.start()
    for process in processes:
        process.join()
