.data

buffer: .asciiz "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

err_msg: .asciiz "There was an error"

.text

la $s0, buffer  # Character index
li $t1, 0  # Current game number
li $t2, 0  # Sum of valid game numbers

main:
    lb $t0, ($s0)

    beq $t0, 'G', game_init
    bge $t0, 48, handle_count  # If character is a digit

    j error  # Main should only be called before a 'Game' or before a number

# Begins when u hit 'G', saves game number and goes to first count
game_init:
    addi $s0, $s0, 5  # Start of game number
    lb $t0, ($s0)  

    subi $t1, $t0, 48

    addi $s0, $s0, 1
    lb $t0, ($s0)
    beq $t0, ':', end_game_init

    subi $t0, $t0, 48
    mul $t1, $t1, 10
    add $t1, $t1, $t0

    addi $s0, $s0, 1
    lb $t0, ($s0)
    beq $t0, ':', end_game_init

    subi $t0, $t0, 48
    mul $t1, $t1, 10
    add $t1, $t1, $t0
    j end_game_init

end_game_init:
    addi $s0, $s0, 2  # Go to start of count listing
    j main

handle_count:
    jal read_count
    jal handle_colour
    j goto_next_count

read_count:
    subi $t3, $t0, 48  # Cube count

    addi $s0, $s0, 1
    lb $t0, ($s0)
    beq $t0, ' ', end_read_count

    mul $t3, $t3, 10
    subi $t0, $t0, 48
    add $t3, $t3, $t0

    addi $s0, $s0, 1  # Gets to the ' '
    j end_read_count

end_read_count:
    addi $s0, $s0, 1
    jr $ra

handle_colour:
    lb $t0, ($s0)
    beq $t0, 'r', handle_colour_r
    beq $t0, 'g', handle_colour_g
    beq $t0, 'b', handle_colour_b
    j error

handle_colour_r:
    bgt $t3, 12, goto_next_game
    jr $ra

handle_colour_g:
    bgt $t3, 13, goto_next_game
    jr $ra

handle_colour_b:
    bgt $t3, 14, goto_next_game
    jr $ra

goto_next_game:
    addi $s0, $s0, 1
    lb $t0, -1($s0)
    beq $t0, '\n', main
    beqz $t0, end
    j goto_next_game

goto_next_count:
    addi $s0, $s0, 1
    lb $t0, -1($s0)
    beq $t0, ' ', main
    beq $t0, '\n', completed_line
    beqz $t0, completed_line
    j goto_next_count

completed_line:
    add $t2, $t2, $t1
    j main

end:
    li $v0, 1
    move $a0, $t2
    syscall

	li $v0, 10
	syscall

error:
    li $v0, 11
    la $a0, err_msg
    syscall

    li $v0, 10
	syscall