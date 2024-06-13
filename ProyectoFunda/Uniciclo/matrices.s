.data
# Matrices A, B y C
.align 4
matrix_A: .word 1, 2, 3, 4, 5, 6, 7, 8, 9
matrix_B: .word 9, 8, 7, 6, 5, 4, 3, 2, 1
matrix_C: .word 0, 0, 0, 0, 0, 0, 0, 0, 0

.text
.globl main

main:
    # Inicializa los índices
    li t0, 0   # Índice de fila de A
    li t1, 0   # Índice de columna de B
    li t2, 0   # Índice de columna de A y fila de B

outer_loop:
    # Reinicia el índice de la columna de B
    li t1, 0

    inner_loop:
        # Reinicia el acumulador para C[i][j]
        li t3, 0

        # Inicializa el índice de fila de B
        li t4, 0

        # Multiplica y acumula los elementos
        inner_product_loop:
            # Calcula la posición de los elementos en las matrices
            mul t5, t0, M       # t5 = i * M
            add t6, t5, t2      # t6 = (i * M) + j
            mul t7, t4, P       # t7 = k * P
            add t8, t7, t1      # t8 = (k * P) + j

            # Carga los elementos de las matrices A y B
            lw t9, matrix_A(t6) # t9 = A[i][k]
            lw t10, matrix_B(t8) # t10 = B[k][j]

            # Multiplica y acumula
            mul t9, t9, t10     # t9 = A[i][k] * B[k][j]
            add t3, t3, t9      # t3 += A[i][k] * B[k][j]

            # Actualiza el índice de fila de B
            addi t4, t4, 1

            # Comprueba si se ha completado la multiplicación de la fila de B
            bne t4, P, inner_product_loop

        # Guarda el resultado en C[i][j]
        mul t5, t0, P           # t5 = i * P
        add t6, t5, t1          # t6 = (i * P) + j
        sw t3, matrix_C(t6)     # C[i][j] = acumulador

        # Actualiza el índice de la columna de B
        addi t1, t1, 1

        # Comprueba si se ha completado la multiplicación de las columnas de B
        bne t1, P, inner_loop

    # Actualiza el índice de la fila de A
    addi t0, t0, 1

    # Comprueba si se ha completado la multiplicación de las filas de A
    bne t0, N, outer_loop

    # Fin del programa
    li a7, 10
    ecall