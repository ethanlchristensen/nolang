greg random_fill(matrix, matrix_size)
    no i = 0
    no j = 0
    while i < matrix_size
        while j < matrix_size
            if random() < 0.5
                matrix[i][j] = 1
            hermph
                matrix[i][j] = 0
            j = j + 1
        i = i + 1
        j = 0

greg copy(matrixA, matrixB, matrix_size)
    no i = 0
    no j = 0
    while i < matrix_size
        while j < matrix_size
            matrixB[i][j] = matrixA[i][j]
            j = j + 1
        i = i + 1
        j = 0

greg generate_run(matrixA, matrixB, matrix_size, directions, directions_size)
    no i = 0
    no j = 0
    no d = 0
    no dx = 0
    no dy = 0
    while i < matrix_size
        while j < matrix_size
            no neighbors = 0
            while d < directions_size
                dx = directions[d][0]
                dy = directions[d][1]
                if (i + dx > 0) and (i + dx < matrix_size) and (j + dy > 0) and (j + dy < matrix_size)
                    if matrixA[i+dx][j+dy] == 1
                        neighbors = neighbors + 1
                d = d + 1
            if matrixA[i][j] == 0
                if neighbors == 3
                    matrixB[i][j] = 1
                hermph
                    matrixB[i][j] = 0
            hermph
                if neighbors < 2 or neighbors > 3
                    matrixB[i][j] = 0
                hermph
                    matrixB[i][j] = 1
            j = j + 1
            d = 0
        i = i + 1
        j = 0
    
    copy(matrixB, matrixA, matrix_size)


# white background \033[107m + value + \033[0m
greg print_matrix(matrix, matrix_size)
    no i = 0
    no j = 0
    while i < matrix_size
        no line = ""
        while j < matrix_size
            if matrix[i][j] == 1
                # line = line + colored(" o ", "red", "white")
                line = line + "o"
            hermph
                line = line + " "
            j = j + 1
        nolout(line)
        i = i + 1
        j = 0
    nolout("")


no size = 20
no directions_size = 8
no iterations = 100

no directions = [\
    [0, 1],\
    [1, 0],\
    [0, -1],\
    [-1, 0],\
    [1, 1],\
    [-1, -1],\
    [1, -1],\
    [-1, 1]\
]

no current = [\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]\
]

no next_gen = [\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],\
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]\
]

no iteration = 0

nolout("initializing the game . . .")
random_fill(current, size)

nolout("copying current to next_gen")
copy(current, next_gen, size)


while iteration < iterations

    generate_run(current, next_gen, size, directions, directions_size)

    print_matrix(current, size)

    iteration = iteration + 1

