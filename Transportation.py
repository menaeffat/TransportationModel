import itertools

from fraction import Fraction

values = {"cost": 0, "qty": 1, "transformation_sign": 2, "cell_evaluation": 3}


def format_number(x, var=None) -> str:
    if var is None:
        var = ""
    number = ""
    if x is None:
        return ""
    if x not in [-1, 0, 1]:
        if int(x) == x:
            number = f"{int(x)}{var}"
        else:
            n = Fraction(x)
            if len(str(n.denominator)) < 3:
                number = f"{format_number(n.numerator, var)}/{n.denominator}"
            else:
                number = f"{x:.2f}{var}"
    elif x == 0:
        number = "0"
    elif x == 1:
        number = "1" if var == "" else f"{var}"
    elif x == -1:
        number = "-1" if var == "" else f"-{var}"
    return number


def create_initial(cost, supply, demand):
    sum_supply = sum(supply)
    sum_demand = sum(demand)
    balanced = sum_supply == sum_demand
    if not balanced:
        if sum_supply < sum_demand:
            cost.append([0] * len(cost[0]))
            supply.append(sum_demand - sum_supply)
        else:
            cost = [i + [0] for i in cost]
            demand.append(sum_supply - sum_demand)
    # construct empty table
    TM = [[[j, None, 0, None] for j in i] for i in cost]

    # fill with qty
    s_supply = supply[:]
    s_demand = demand[:]
    i, j = 0, 0
    while i < len(TM):
        while j < len(TM[0]):
            v = min(s_supply[i], s_demand[j])
            TM[i][j][values["qty"]] = v
            s_demand[j] -= v
            s_supply[i] -= v
            if j == len(s_demand) - 1 and i == len(s_supply) - 1:
                i += 1
                j += 1
            elif s_supply[i] > 0:
                j += 1
            elif s_demand[j] > 0:
                i += 1
            else:
                i += 1
    return TM, supply, demand


def evaluate_empty_cells(tm):
    stepping_stones = []
    for i in range(len(tm)):
        for j in range(len(tm[0])):
            if tm[i][j][values["qty"]] is None:
                step_stone = stepping_stone(tm, i, j)
                stepping_stones.append(step_stone)
                tm[i][j][values["cell_evaluation"]] = step_stone[0]
    return tm, stepping_stones


def determine_selected_cell(tm, stepping_stones):
    next_step = min(stepping_stones)
    for idx, loc in enumerate(next_step[1]):
        tm[loc[0]][loc[1]][values["transformation_sign"]] = (idx % 2) + 1
    sc = next_step[1][0]
    av = min(tm[next_step[1][1][0]][next_step[1][1][1]][values["qty"]], tm[next_step[1][-1][0]][next_step[1][-1][1]][values["qty"]])
    ntc = get_total_cost(tm) + tm[sc[0]][sc[1]][values["cell_evaluation"]] * av
    return tm, sc, av, ntc


def stepping_stone(tm, i, j):
    v = []
    for row_idx, row in enumerate(tm):
        for item_idx, item in enumerate(row):
            if item[values["qty"]] is not None:
                v.append((row_idx, item_idx))
    all_path = []
    found_path = False
    for length_of_path in range(3, len(tm) + len(tm[0])):
        for path in itertools.permutations(v, r=length_of_path):
            all_path = [[i, j]] + list(path)
            found_path = path_is_valid(all_path)
            if found_path:
                break
        if found_path:
            break
    cell_evaluation = 0
    for idx, vert in enumerate(all_path):
        cell_evaluation += (-1 if idx % 2 else 1) * tm[vert[0]][vert[1]][values["cost"]]
    return cell_evaluation, all_path


def path_is_valid(path):
    for i in range(len(path) - 1):
        if not link_is_valid(path[i:i + 2]):
            return False
    if not link_is_valid([path[0]] + [path[-1]]):
        return False
    return True


def link_is_valid(link):
    if link[0][0] == link[1][0] or link[0][1] == link[1][1]:
        return True
    else:
        return False


def get_print_table_text(tm, supply, demand, table_num = None):
    max_letters = 5
    # top row (column numbers)
    text = ("" if table_num is None else f"[{table_num}]").center(max_letters + 1) + "".join(
        [str(i + 1).center(max_letters * 2 + 2) for i in range(len(tm[0]))]) + "\n"
    total_cost = get_total_cost(tm)
    for idx, row in enumerate(tm):
        # row: top border
        text += "".center(max_letters) + "".join(
            ["|" + "=" * (max_letters * 2 + 1) for _ in range(len(tm[0]))]) + "|\n"
        # row: cost and transformation sign
        text += "".center(max_letters) + "".join(["|" + format_number(row[i][values["cost"]]).center(
            max_letters) + "|" + ("" if row[i][values["transformation_sign"]] == 0 else "+" if row[i][values[
            "transformation_sign"]] == 1 else "-").center(max_letters) for i in range(len(row))]) + "|\n"
        # row: internal border and supply
        text += "".center(max_letters) + "".join(
            ["|" + "-" * (max_letters + 1) + "".center(max_letters) for _ in range(len(tm[0]))]) + "|" + str(
            supply[idx]).center(max_letters * 2) + "\n"
        # row: row number and (quantity or cell evaluation)
        # #######format_number(row[i][values["qty" if row[i][values["qty"] is not None else ""]]).center(max_letters)
        text += f"{idx + 1}".center(max_letters) + "|" + "|".join([(quantity_or_cel_eval(row[i][values["qty"]], row[i][
            values["cell_evaluation"]])).center(max_letters * 2 + 1) for i in range(len(row))]) + "|\n"
    # table: row bottom border
    text += "".center(max_letters) + "".join(
        ["|" + "=" * (max_letters * 2 + 1) for _ in range(len(tm[0]))]) + "|" + "=" * (max_letters * 2) + "|\n"
    # table: demand and total cost
    text += "".center(max_letters + 1) + " ".join(
        [str(demand[i]).center(max_letters * 2 + 1) for i in range(len(demand))]) + "|" + str(total_cost).center(
        max_letters * 2) + "|\n"
    # table: bottom border for total cost
    text += "".center(max_letters + 1) + " ".join(
        [" ".center(max_letters * 2 + 1) for _ in range(len(demand))]) + "|" + "=" * (max_letters * 2) + "|\n"
    return text


def quantity_or_cel_eval(qty, c_e):
    if qty is not None:
        num = format_number(qty)
        return num if num != "0" else "ZERO"
    elif c_e is not None:
        return f"(+{format_number(c_e)})".replace("+-", "-")
    else:
        return ""


def get_total_cost(tm):
    total_cost = 0
    for i, row in enumerate(tm):
        for j, vs in enumerate(row):
            if vs[values["qty"]] is not None:
                total_cost += vs[values["qty"]] * vs[values["cost"]]
    return total_cost


def new_basic_feasible_solution(tm, sc, av, selected_path):
    tm[sc[0]][sc[1]][values["qty"]] = av
    tm[sc[0]][sc[1]][values["cell_evaluation"]] = None
    tm[sc[0]][sc[1]][values["transformation_sign"]] = 0

    v1 = tm[selected_path[1][1][0]][selected_path[1][1][1]]
    v1_Q = v1[values["qty"]]
    v1_NQ = v1_Q + (1 if v1[values["transformation_sign"]] == 1 else -1) * av

    v2 = tm[selected_path[1][-1][0]][selected_path[1][-1][1]]
    v2_Q = v2[values["qty"]]
    v2_NQ = v2_Q + (1 if v2[values["transformation_sign"]] == 1 else -1) * av

    tm[selected_path[1][-1][0]][selected_path[1][-1][1]][values["cell_evaluation"]] = None
    tm[selected_path[1][-1][0]][selected_path[1][-1][1]][values["transformation_sign"]] = 0
    tm[selected_path[1][1][0]][selected_path[1][1][1]][values["cell_evaluation"]] = None
    tm[selected_path[1][1][0]][selected_path[1][1][1]][values["transformation_sign"]] = 0
    tm[selected_path[1][1][0]][selected_path[1][1][1]][values["qty"]] = v1_NQ if v1_Q >= v2_Q else None
    tm[selected_path[1][-1][0]][selected_path[1][-1][1]][values["qty"]] = v2_NQ if not v1_Q >= v2_Q else None

    for cell in selected_path[1][2:-1]:
        sign = tm[cell[0]][cell[1]][values["transformation_sign"]]
        if sign > 0:
            new_qty = tm[cell[0]][cell[1]][values["qty"]] + (1 if sign == 1 else -1) * av
            tm[cell[0]][cell[1]][values["qty"]] = new_qty
            tm[cell[0]][cell[1]][values["cell_evaluation"]] = None
            tm[cell[0]][cell[1]][values["transformation_sign"]] = 0

    for i in range(len(tm)):
        for j in range(len(tm[0])):
            tm[i][j][values["cell_evaluation"]] = None

    return tm
    # first_zero_taken = av == 0
    # tm[sc[0]][sc[1]][values["qty"]] = av
    # tm[sc[0]][sc[1]][values["cell_evaluation"]] = None
    # tm[sc[0]][sc[1]][values["transformation_sign"]] = 0
    #
    # for i in range(len(tm)):
    #     for j in range(len(tm[0])):
    #         sign = tm[i][j][values["transformation_sign"]]
    #         if sign > 0:
    #             tm[i][j][values["transformation_sign"]] = 0
    #             # 1 -> + , 2 -> 2
    #             new_qty = tm[i][j][values["qty"]] + (1 if sign == 1 else -1) * av
    #             # if tm[i][j][values["qty"]] != 0 and new_qty == 0:
    #             #     if first_zero_taken:
    #             #         tm[i][j][values["qty"]] = None
    #             #     else:
    #             #         first_zero_taken = True
    #             #         tm[i][j][values["qty"]] = 0
    #             # else:
    #             #     tm[i][j][values["qty"]] = new_qty
    #             if new_qty == 0:
    #                 if first_zero_taken:
    #                     tm[i][j][values["qty"]] = None
    #                 else:
    #                     tm[i][j][values["qty"]] = 0
    #             else:
    #                 tm[i][j][values["qty"]] = new_qty
    #             first_zero_taken = (first_zero_taken or new_qty == 0)
    #
    #         else:
    #             tm[i][j][values["cell_evaluation"]] = None
    # return tm
