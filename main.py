import Transportation

# cost = [[8, 3, 1], [2, 4, 1], [3, 6, 2]]
# supply = [100, 100, 100]
# demand = [120, 80, 120]
#
# cost = [[5, 3, 1], [2, 3, 1], [4, 2, 6]]
# supply = [200, 100, 50]
# demand = [250, 50, 100]

# practice problem
# cost = [[6,1,4], [2,4,3], [3,1,2]]
# supply = [80, 100, 100]
# demand = [100, 100, 80]

# michael
# cost = [[7,3,1], [4,2,3], [1,8,2]]
# supply = [100, 30, 70]
# demand = [50, 100, 20]

# George
cost = [[9,2,4], [3,5,1], [2,3,8]]
supply = [120, 80, 40]
demand = [180, 80, 100]

# cost = [[8, 3, 2], [5, 1, 2], [4, 6, 1]]
# supply = [100, 100, 100]
# demand = [100, 100, 100]

if __name__ == '__main__':
    print("Hello")
    tm, supply, demand = Transportation.create_initial(cost, supply, demand)

    tm, stones = Transportation.evaluate_empty_cells(tm)
    selected_path = min(stones)
    optimal = selected_path[0] >= 0
    tm, sc, av, ntc = Transportation.determine_selected_cell(tm, stones)
    print(Transportation.get_print_table_text(tm, supply, demand, 0))
    print(f"\tOptimal: {optimal}\tSC = ({sc[0] + 1}, {sc[1] + 1})\tAV = {av}\tNTC = {ntc}")

    table_num = 1
    while not optimal:
    # while table_num < 3:
        tm = Transportation.new_basic_feasible_solution(tm, sc, av, selected_path)
        tm, stones = Transportation.evaluate_empty_cells(tm)
        selected_path = min(stones)
        optimal = selected_path[0] >= 0
        tm, sc, av, ntc = Transportation.determine_selected_cell(tm, stones)
        print(Transportation.get_print_table_text(tm, supply, demand, table_num))
        print(f"\tOptimal: {optimal}\tSC = ({sc[0] + 1}, {sc[1] + 1})\tAV = {av}\tNTC = {ntc}")
        table_num += 1
        