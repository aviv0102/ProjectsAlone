	#206558157 aviv shisman
	.section	.rodata
strF:       .string " %d"
strS:       .string " %s"
##########################################################################################################
	.text	#the beginning of the code.
.globl	main
	.type	main, @function
main:
    pushq %rbp
    movq %rsp,%rbp
    
    leaq -1(%rsp),%rsp # allocate 8 bytes from stack
    movq $0, %rax      # clear rax
    movq $strF, %rdi   # load format string
    movq %rsp,%rsi
    call scanf         #getting the size of str1 from user
    
    movq $0,%r12       #getting the size from the stack
    movb (%rsp),%r12b
    
    subq  %r12,%rsp
    leaq -1(%rsp),%rsp #1 more byte for ending of string  
    movq  $0,(%rsp)    #adding '\0' to the end of string 
    movq $0,%rax
    movq %rsp,%rsi
    movq $strS,%rdi
    call scanf         #getting str1 from user
    
    movq %rsp,%r13

    
    leaq -8(%rsp),%rsp # allocate 8 bytes from stack
    movq $0, %rax      # clear rax
    movq $strF, %rdi   # load format string
    movq %rsp,%rsi
    call scanf         #getting the size of str2 from user
        
    movq $0,%r14       #getting the size from the stack
    movb (%rsp),%r14b
    
        
    subq  %r14,%rsp
    leaq -1(%rsp),%rsp
    movq  $0,(%rsp)    #adding '\0' to the end of string     
    movq $0,%rax
    movq %rsp,%rsi
    movq $strS,%rdi
    call scanf         #getting str2 from user
    movq %rsp,%r15
        
    leaq -8(%rsp),%rsp # allocate 8 bytes from stack
    movq $0, %rax      # clear rax
    movq $strF, %rdi   # load format string
    movq %rsp,%rsi
    call scanf         #getting the operator
    
    movq $0,%r10       #getting the size from the stack
    movb (%rsp),%r10b
        
    movq $0,%rax       #preperations for run func 
    movq $0,%rsi
    movq $0,%rdx
    movq %r10,%rdi
    
    leaq -1(%r13),%rsi
    movb %r12b,(%rsi)
    
    leaq -1(%r15),%rdx
    movb %r14b,(%rdx)
    
    movq $0,%r12
    movq $0,%r13
    movq $0,%r14
    movq $0,%r15
    
    call run_func
    
    movq %rbp,%rsp
    popq %rbp
    
    ret #return to caller function (OS)

