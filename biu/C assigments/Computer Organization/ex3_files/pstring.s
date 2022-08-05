	#206558157 aviv shisman

.section	.rodata
here:     .string "result dst %s src %s start %c end %c\n"
error:    .string "invalid input!\n"
.text
.globl	pstrlen
	.type	pstrlen, @function
pstrlen:    
          pushq %rbp
          movq %rsp,%rbp
        
          movq   $0,%rsi
          movb   (%rdi), %al     #take the number out of the struct
          


          leave

          ret   
  
  
.globl	replaceChar
	.type	replaceChar, @function
replaceChar:
        pushq %rbp
        movq %rsp,%rbp
        
        movq   $0, %r14     #counter for loop
        movb   (%rdx),%r15b #loop stop condition (size of string)
        movq   %rdx,%r10
        pushq  %r10         #saving values in stack
        pushq  %rdi
        pushq  %rsi
        .loop:
            popq  %rsi
            popq  %rdi
            popq %r10
           
            leaq 1(%r10),%r10
            incq  %r14
            movq $0,%rax
            cmpb (%r10),%dil    #compare current char with old char
            je .start           #if equal go to start
           
            .end:
            pushq  %r10
            pushq  %rdi
            pushq  %rsi
            cmpq  %r14,%r15     #if i>string.length go to done
            jne .loop
            jmp .done
            
             .start:
            movb %sil,(%r10)    #if current=old char -> current=new char
            jmp .end
            
          .done:
            popq  %rsi
            popq  %rdi
            popq %r10
            subq %r14,%r10
            movq %r10,%rax
            
            leave
            
            ret
            
 .globl	‪pstrijcpy
	.type	‪pstrijcpy, @function
‪pstrijcpy:           

        pushq %rbp
        movq %rsp,%rbp
        movb   (%rdi),%r14b     #dst.length
        movb   (%rsi),%r15b     #src.length
        cmpq   $-1,%rdx         #if index i<=-1
        jle .error
        cmpq   %rcx,%rdx        #if index i>index j
        jg  .error
        cmpq   %r15,%rcx        #if j>=dest or src
        jge  .error
        cmpq   %r14,%rcx        #if j>=dest or src
        jge  .error
        
        movq %rdx,%r14          #now they will have the i and j index's
        movq %rcx,%r15
        leaq 1(%rdi),%rdi       #the strings
        leaq 1(%rsi),%rsi
        movq $0,%rdx            #counter=0
        pushq %rdx
        pushq %rdi
        pushq %rsi
        .myloop:
            popq %rsi
            popq %rdi
            popq %rdx
            pushq %rdx
            pushq %rdi
            pushq %rsi
            cmpq %r15,%rdx      #if counter>=j done
            jg .done2
            cmpq %r14,%rdx      #if counter>=i start replacing
            jge .replace
            
            .endif:
            popq %rsi
            popq %rdi
            popq %rdx
            leaq 1(%rdi),%rdi       #dest.i++ and src.i++
            leaq 1(%rsi),%rsi
            incq %rdx
            pushq %rdx
            pushq %rdi
            pushq %rsi
            jmp .myloop
            
            .replace:
                movb (%rsi),%r9b
                movb %r9b,(%rdi)
                jmp .endif
            
            .error:
                movq $error,%rdi
                movq $0,%rax
                call printf
                jmp .done2
                
          .done2:
            popq %rsi
            popq %rdi
            popq %rdx
            leave
    
            ret  

.globl	swapCase
	.type	swapCase, @function
swapCase:    
          
          pushq %rbp
          movq %rsp,%rbp
          movb (%rdi),%r14b     #length
          movq $0,%r15
          pushq %rdi
          .aLoop:
            popq %rdi
            leaq 1(%rdi),%rdi   #getting the next character
            incq %r15
            pushq %rdi
            cmpq %r14,%r15      #check exit condition
            jg .done3
            movb $'A',%sil       #if char is lower than A(not the abc)
            cmpb %sil,(%rdi)
            jl   .endCheck
            movb $'z',%sil      #if char is higher than z (not abc)
            cmpb %sil,(%rdi)
            jg   .endCheck
            
            jmp  .swap
                                             
          .endCheck:
            jmp .aLoop
            
          .swap:
            popq %rdi
            movb $'Z',%sil       #if char is greater than Z-> not capital
            cmpb %sil,(%rdi)
            pushq %rdi
            jg .swap2
            popq %rdi
            movq (%rdi),%rdx    #adding 32=difference between capital and not
            leaq 32(%rdx),%rdx
            movq %rdx,(%rdi)
            pushq %rdi
            jmp .aLoop
            
           .swap2:
            popq %rdi           #in case char is lower case
            movb $'a',%sil       #if char is greater than Z-> not capital
            cmpb %sil,(%rdi)
            pushq %rdi
            jl .aLoop           #if char is between 91-96 ->not abc character
            popq %rdi
            movq (%rdi),%rdx
            leaq -32(%rdx),%rdx
            movq %rdx,(%rdi)
            pushq %rdi
            jmp .aLoop
            
          .done3:
            popq %rdi

            leave

             ret 















