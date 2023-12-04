.data

buffer: .asciiz "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

err_msg: .asciiz "There was an error"

.text

la $s0, buffer  # Character index
li $t2, 0       # Sum of powers
# li $t3, 0     # Cube count
# li $t4, 0     # Min req red
# li $t5, 0     # Min req green
# li $t6, 0     # Min req blue


main:
    lb $t0, ($s0)

    beq $t0, 'G', game_init
    bge $t0, 48, handle_count  # If character is a digit

    j error  # Main should only be called before a 'Game' or before a number

# Begins when u hit 'G', saves game number and goes to first count
game_init:
    # Initialise min req colours
    li $t4, 0
    li $t5, 0
    li $t6, 0

    addi $s0, $s0, 6
    jal goto_colon
    addi $s0, $s0, 1
    j main

goto_colon:
    addi $s0, $s0, 1
    lb $t0, -1($s0)
    bne $t0, ':', goto_colon
    jr $ra

handle_count:
    jal read_count
    j handle_colour

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
    bge $t4, $t3, goto_next_count
    move $t4, $t3
    j goto_next_count

handle_colour_g:
    bge $t5, $t3, goto_next_count
    move $t5, $t3
    j goto_next_count

handle_colour_b:
    bge $t6, $t3, goto_next_count
    move $t6, $t3
    j goto_next_count

goto_next_count:
    addi $s0, $s0, 1
    lb $t0, -1($s0)
    beq $t0, ' ', main
    beq $t0, '\n', completed_line
    beqz $t0, completed_line
    j goto_next_count

completed_line:
    mul $t5, $t5, $t6
    mul $t4, $t4, $t5
    add $t2, $t2, $t4

    beqz $t0, end
    j main

end:
    li $v0, 1
    move $a0, $t2
    syscall

	li $v0, 10
	syscall

error:
    li $v0, 4
    la $a0, err_msg
    syscall

    li $v0, 10
	syscall
