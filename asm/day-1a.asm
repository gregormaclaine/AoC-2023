.data

input_file: .asciiz "/Users/gregormaclaine/Projects/AoC-2023/input/day-1.txt"

buffer: .space 22000  # 22KB

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
	li $a2, 22000   # Read the entire file into the buffer
	syscall

	li $v0, 16     # Load the system call for close file
	move $a0, $s0  # Load the file descriptor to close
	syscall

	li $t0, 0   # Character index
	li $t2, 0   # Running sum
	li $t3, 10  # First digit (> 9 means not yet set for line)
	li $t4, 0   # Second digit

main:
	lb $t1, buffer($t0)

	bgt $t1, 64, next_char  # If t1 is letter skip

	beq $t1, '\n', end_line
	beqz $t1, end

	subi $t4, $t1, 48  # Set second digit to number in t1

	addi $t0, $t0, 1

	ble $t3, 9, main
	subi $t3, $t1, 48  # Set first digit to number in t1 if not set
	j main

end_line:
	add $t2, $t2, $t4
	mul $t3, $t3, 10
	add $t2, $t2, $t3

	li $t3, 10
	li $t4, 0

	addi $t0, $t0, 1
	j main

next_char:
	addi $t0, $t0, 1
	j main

end:
	add $t2, $t2, $t4
	mul $t3, $t3, 10
	add $t2, $t2, $t3

	li $v0, 1
	move $a0, $t2
	syscall

	li $v0, 10
	syscall
