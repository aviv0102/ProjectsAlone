	#206558157 aviv shisman
	.data
	.align	4	# we want all data to be save in an address that divise with their size


	.section	.rodata
str1:       .string " %c %c"
str2:       .string " %d %d"
result:     .string "length: %d, string: %s\nlength: %d, string: %s\n"
replaceCh:  .string "old char: %c, new char: %c, first string: %s, second string: %s \n"
Error:      .string "invalid option!\n"
outprint:   .string "first pstring length: %d, second pstring length: %d \n"
	
.align	8	# we want all data to be save in an address that divise with their size.
  .My_Switch:
  .quad .My_Switch_A 	# Case 50
  .quad .My_Switch_B	# Case 51
  .quad .My_Switch_C	# Case 52
  .quad .My_Switch_D	# Case 53
  .quad .My_Switch_Def 	# Case defult
  
############################################################################################################

	.text	#the beginning of the code.
.globl	run_func
	.type	run_func, @function
run_func:
        pushq %rbp
        movq %rsp,%rbp

        
        # Set up the jump table access
        leaq -50(%rdi),%r9      # adjusting the number to the jump table
        cmpq $4,%r9             # Compare x:54
        jge .My_Switch_Def      # if >=, goto default-case
        cmpq $-1,%r9            # Compare x:49
        jle .My_Switch_Def      # if <=, goto default-case
        jmp *.My_Switch(,%r9,8) # Goto jt[xi]
         
        # Case 50
        .My_Switch_A:       
            movq   %rsi,%rdi          
            movq	$0,%rax
            call   pstrlen    #getting the length of %rsi=first sturct
            movb   %al,%r9b   #the result will be in temp(%r9)
            
            movq   %rdx,%rdi
            movq	$0,%rax
            call   pstrlen    #same as before the result will be in r10
            movb   %al,%r10b
            
            movq $outprint,%rdi
            movq $0,%rax      #moving the results from the temporary registers to printf parameters
            movq $0,%rdx
            movb %r9b,%sil
            movb %r10b,%dl
            call printf
            
            jmp .done         # Goto done
         
        
        # Case 51
        .My_Switch_B:    
            movq %rsi,%r12      #copy the structs to other registers 
            movq %rdx,%r13      #scanf wont overwrite them becuase they callee-save
            movq $0,%rsi
            movq $0,%rdx

            leaq -2(%rsp),%rsp # allocate 2 bytes from stack
            movq $0, %rax      # clear rax
            movq $str1, %rdi   # load format string
            
            leaq 1(%rsp),%r8   # set storage to local variable
            movq %r8,%rsi
            movq %rsp,%rdx
            call scanf         #getting 2 chars from user
            
            movq $0,%r8        #getting the chars from the stack
            movq $0,%r9
            movb 1(%rsp),%r8b
            movb (%rsp),%r9b
            
            movq $0,%rax       #calling replace char for first Pstring
            movq $0,%rdi
            movq $0,%rsi
            movq $0,%rdx
            pushq %r8          #saving registers in stack
            pushq %r9
            
            movq %r8,%rdi
            movq %r9,%rsi
            movq %r12,%rdx
            call replaceChar
            
            popq %r9
            popq %r8
            movq $0,%rax       #calling replace char for second Pstring
            movq $0,%rdi
            movq $0,%rsi
            movq $0,%rdx
                  
            movq %r8,%rdi
            movq %r9,%rsi
            movq %r13,%rdx
            pushq %r8          #saving registers
            pushq %r9
            call replaceChar
            
            movq $0,%rax       #calling replace char for second Pstring
            movq $0,%rdi
            movq $0,%rsi
            movq $0,%rdx
            popq %r9           #getting the values back
            popq %r8
            movq $replaceCh,%rdi
            movb %r8b,%sil     #printing the values we got
            movb %r9b,%dl
            leaq 1(%r12),%r12
            leaq 1(%r13),%r13
            movq %r12,%rcx
            movq %r13,%r8
            call printf
            jmp .done              # Goto done 
          
          
          
            
            
            # Case 52
        .My_Switch_C:
            movq %rsi,%r12      #copy the structs to other registers 
            movq %rdx,%r13      #scanf wont overwrite them becuase they callee-save
            movq $0,%rsi
            movq $0,%rdx

            leaq -16(%rsp),%rsp # allocate 16 bytes from stack
            movq $0, %rax      # clear rax
            movq $str2, %rdi   # load format string
            
            leaq 8(%rsp),%r8   # set storage to local variable
            movq %r8,%rsi
            movq %rsp,%rdx
            call scanf         #getting 2 chars from user
            
            movq $0,%r8        #getting the chars from the stack
            movq $0,%r9
            movb 8(%rsp),%r8b
            movb (%rsp),%r9b
            movq $0,%rax       #calling replace char for pstrijcpy
            movq %r12,%rdi
            movq %r13,%rsi                                      
            movq %r8,%rdx
            movq %r9,%rcx
            call  ‪pstrijcpy
            
            movq $0,%rax
            movq $0,%rdi
            movq $0,%rsi
            movq $0,%rdx
            movq $0,%rcx            
            movq $result,%rdi
            movb (%r12),%sil
            leaq 1(%r12),%rdx
            movb (%r13),%cl
            leaq 1(%r13),%r8
            call printf
            
            
            jmp .done              # Goto done 
            
            # Cases 53
        .My_Switch_D:            
            movq %rsi,%r12      #copy the structs to other registers 
            movq %rdx,%r13      #scanf wont overwrite them becuase they callee-save
            movq $0,%rsi
            movq $0,%rdx           
            movq %r12,%rdi
            movq $0,%rax
            call swapCase
            
            movq $0,%rax
            movq $0,%rsi
            movq $0,%rdi
            movq %r13,%rdi
            call swapCase
            
            movq $0,%rax
            movq $0,%rsi
            movq $0,%rdi
            movq $0,%rcx
            movq $result,%rdi
            movb (%r12),%sil
            leaq 1(%r12),%rdx
            movb (%r13),%cl
            leaq 1(%r13),%r8
            call printf
            
            jmp .done              # Goto done
            
            # Default case
        .My_Switch_Def:         
            movq	$Error,%rdi    #passing the string the first parameter for printf.
            movq	$0,%rax
            call	printf
            
        .done:                   # done:
            movq	$0,%rax
            movq %rbp,%rsp
            popq %rbp
            
            ret                    #return to caller function (main)
