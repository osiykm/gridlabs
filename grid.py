import math

###
### Инициализация набора начальных констант
###
beta = 5.0
w0 = 316.23
e_max = 10.0
L = 1.0
wb = 316.0
R = 10.0
t_start = 0.0
t_end = 0.5
t_step = 0.00005
is_filling_files_enabled = False
is_console_output_enabled = True 

###
### Данная функция решает систему диф. уравнений первого порядка 
### вида y' = f(x, y) из использованием модифицированного метода Эйлера
### Возвращает массив ответов 
###
### f_arr   - массив лямбда функций вида f(x, y_arr), 
###           где y_arr = [y1, y2, ..., yn]
### x_nodes - массив узлов x
### y0_arr  - краевое условие для задачи Коши
###
def solve_equation_system(f_arr, x_nodes, y0_arr):
    y = []
    y.append(y0_arr)
    x = x_nodes

    if len(f_arr) != len(y0_arr):
        return 

    for i in range(1, len(x_nodes)):
        prognose = [y[i - 1][j] + (x[i] - x[i - 1]) *  \
                   f_arr[j](x[i - 1], y[i - 1])        \
                   for j in range(0, len(f_arr))]

        new_value = [y[i - 1][j] + (x[i] - x[i - 1]) * \
                    (f_arr[j](x[i - 1], y[i - 1]) +    \
                    f_arr[j](x[i], prognose)) / 2      \
                    for j in range(0, len(f_arr))]

        y.append(new_value)

    result = []
    for j in range(0, len(f_arr)):
        result.append([y[i][j] for i in range(0, len(x_nodes))])

    return result

###
### Возвращает коллекцию всех в указанной области чисел с некоторым шагом
###
### start - начало (включается в коллекцию)
### end   - конец (не включается в коллекцию)
### step  - шаг
###
def drange(start, end, step = 1):
    i = start
    coll = []
    while i < end:
        coll.append(i)
        i += step

    return coll


###
### Решение задачи первой лабораторной работы
###
def lab1_task(out_file_name):
    time_nodes = drange(t_start, t_end, t_step)
    equation_system = [                                  \
        lambda t, q: q[1],                               \
        lambda t, q: -2 * beta * q[1] - (w0 ** 2) *      \
                     q[0] + e_max * math.cos(wb * t) / L \
    ]

    result = solve_equation_system(equation_system, time_nodes, [0, 0])
    charge_nodes = result[0]
    amperage_nodes = result[1]
    voltage_nodes = [R * amperage_nodes[i] for i in range(0, len(amperage_nodes))]
    emf_nodes = [e_max * math.cos(wb * t) / L for t in time_nodes]

    if is_filling_files_enabled:
        file = open(out_file_name, "w")
        file.seek(0)
        file.truncate() 
        for i in range(0, len(time_nodes)):
            file.write("%s" % time_nodes[i])
            file.write("\t%s" % charge_nodes[i])
            file.write("\t%s" % amperage_nodes[i])
            file.write("\t%s" % voltage_nodes[i])
            file.write("\t%s\n" % emf_nodes[i])

        file.close()

    if is_console_output_enabled:
        print("################## LAB 1 ###################")
        for i in range(0, len(time_nodes)):
            print("%7s %24s %24s %24s %24s" % ( \
                  round(time_nodes[i], 6),      \
                  charge_nodes[i],              \
                  amperage_nodes[i],            \
                  voltage_nodes[i],             \
                  emf_nodes[i]))

###
### Решение задачи третьей лабораторной работы
###
def lab3_task(out_file_name):
    time_nodes = drange(t_start, t_end, t_step) 
    equation_system = [                                    \
        lambda t, q: q[1],                                 \
        lambda t, q: -2 * beta * q[1] - (w0 ** 2.0) * q[0] \
    ]

    result = solve_equation_system(equation_system, time_nodes, [2E-4, 0])
    charge_nodes = result[0]
    amperage_nodes = result[1]
    voltage_nodes = [R * amperage_nodes[i] for i in range(0, len(amperage_nodes))]

    if is_filling_files_enabled:
        file = open(out_file_name, "w")
        file.seek(0)
        file.truncate() 
        for i in range(0, len(time_nodes)):
            file.write("%s" % time_nodes[i])
            file.write("\t%s" % charge_nodes[i])
            file.write("\t%s" % amperage_nodes[i])
            file.write("\t%s\n" % voltage_nodes[i])

        file.close()

    if is_console_output_enabled:
        print("################## LAB 3 ###################")
        for i in range(0, len(time_nodes)):
            print("%7s %24s %24s %24s" % ( \
                  round(time_nodes[i], 6),          \
                  charge_nodes[i],         \
                  amperage_nodes[i],       \
                  voltage_nodes[i]))

###
### Решение задачи четвертой лабораторной работы
###
def lab4_task(out_file_name):
    w_array = drange(3.0, 2 * w0, 3.0)
    
    amplitudes = []
    for w in w_array:
        equation_system = [                                 \
            lambda t, q: q[1],                              \
            lambda t, q: -2 * beta * q[1] - (w0 ** 2) *     \
                         q[0] + e_max * math.cos(w * t) / L \
        ]

        time_nodes = drange(t_start, t_end, t_step) 
        result = solve_equation_system(equation_system, time_nodes, [0, 0])
        amperage_nodes = result[1]
        amplitudes.append(max(amperage_nodes))

    if is_filling_files_enabled:
        file = open(out_file_name, "w")
        file.seek(0)
        file.truncate() 
        for i in range(0, len(w_array)):
            file.write("%s" % w_array[i])
            file.write("\t%s\n" % amplitudes[i])

        file.close()

    if is_console_output_enabled:
        print("################## LAB 4 ###################")
        for i in range(0, len(w_array)):
            print ("%10s: %24s" % (w_array[i], amplitudes[i]))


###
### Точка входа в программу 
###
if __name__ == "__main__":
    lab1_task("lab1_out.txt")
    lab3_task("lab3_out.txt")
    lab4_task("lab4_out.txt")




