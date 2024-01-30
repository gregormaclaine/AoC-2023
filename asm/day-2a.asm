.data

input_file: .asciiz "/Users/gregormaclaine/Projects/AoC-2023/input/day-2.txt"

buffer: .space 12000  # 12KB

err_msg: .asciiz "There was an error"

.text

read_file:
	li $v0, 13          # Load the system call code for open file
	la $a0, input_file  # Load the address of the input file name
	li $a1, 0           # Flag for reading
	li $a2, 0           # Mode is ignored
	syscall

	move $s0, $v0  # Save the file descriptor returned by syscall

	li $v0, 14      # Load the system call code for reading from file
	move $a0, $s0   # Load the file descriptor to read
	la $a1, buffer  # Load the address of the buffer to write into
	li $a2, 12000   # Read the entire file into the buffer
	syscall

	li $v0, 16     # Load the system call for close file
	move $a0, $s0  # Load the file descriptor to close
	syscall

	la $s0, buffer  # Character index
	li $t1, 0       # Current game number
	li $t2, 0       # Sum of valid game numbers

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

	addi $s0, $s0, 1
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
