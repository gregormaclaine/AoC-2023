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

	beq $t1, '\n', end_line
	beqz $t1, end

	bgt $t1, 64, hit_char  # If t1 is letter skip

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

# one
# two
# three
# four
# five
# six
# seven
# eight
# nine

hit_char:
	la $t9, buffer
	add $t9, $t9, $t0
	addi $t0, $t0, 1

	beq $t1, 111, hit_char_o
	beq $t1, 116, hit_char_t
	beq $t1, 102, hit_char_f
	beq $t1, 115, hit_char_s
	beq $t1, 101, hit_char_e
	beq $t1, 110, hit_char_n

	# Else not going to be a number
	j main

hit_char_o:
	lb $t1, 1($t9)
	bne $t1, 'n', main

	lb $t1, 2($t9)
	bne $t1, 'e', main

	li $t8, '1'
	sb $t8, buffer($t0)

	j main

hit_char_e:
	lb $t1, 1($t9)
	bne $t1, 'i', main

	lb $t1, 2($t9)
	bne $t1, 'g', main

	lb $t1, 3($t9)
	bne $t1, 'h', main

	lb $t1, 4($t9)
	bne $t1, 't', main

	li $t8, '8'
	sb $t8, buffer($t0)

	j main

hit_char_n:
	lb $t1, 1($t9)
	bne $t1, 'i', main

	lb $t1, 2($t9)
	bne $t1, 'n', main

	lb $t1, 3($t9)
	bne $t1, 'e', main

	li $t8, '9'
	sb $t8, buffer($t0)

	j main

hit_char_t:
	lb $t1, 1($t9)
	beq $t1, 'w', hit_char_t_0
	j hit_char_t_1

hit_char_f:
	lb $t1, 1($t9)
	beq $t1, 'o', hit_char_f_0
	j hit_char_f_1

hit_char_s:
	lb $t1, 1($t9)
	beq $t1, 'i', hit_char_s_0
	j hit_char_s_1

hit_char_t_0:
	lb $t1, 2($t9)
	bne $t1, 'o', main

	li $t8, '2'
	sb $t8, buffer($t0)

	j main

hit_char_t_1:
	lb $t1, 1($t9)
	bne $t1, 'h', main

	lb $t1, 2($t9)
	bne $t1, 'r', main

	lb $t1, 3($t9)
	bne $t1, 'e', main

	lb $t1, 4($t9)
	bne $t1, 'e', main

	li $t8, '3'
	sb $t8, buffer($t0)

	j main

hit_char_f_0:
	lb $t1, 2($t9)
	bne $t1, 'u', main

	lb $t1, 3($t9)
	bne $t1, 'r', main

	li $t8, '4'
	sb $t8, buffer($t0)

	j main

hit_char_f_1:
	lb $t1, 1($t9)
	bne $t1, 'i', main

	lb $t1, 2($t9)
	bne $t1, 'v', main

	lb $t1, 3($t9)
	bne $t1, 'e', main

	li $t8, '5'
	sb $t8, buffer($t0)

	j main

hit_char_s_0:
	lb $t1, 2($t9)
	bne $t1, 'x', main

	li $t8, '6'
	sb $t8, buffer($t0)

	j main

hit_char_s_1:
	lb $t1, 1($t9)
	bne $t1, 'e', main

	lb $t1, 2($t9)
	bne $t1, 'v', main

	lb $t1, 3($t9)
	bne $t1, 'e', main

	lb $t1, 4($t9)
	bne $t1, 'n', main

	li $t8, '7'
	sb $t8, buffer($t0)

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
