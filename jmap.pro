FUNCTION jmap, m, _REF_EXTRA=e
;call the function with extra args, and have it go to the buffer rather than a window
p=map(m,_STRICT_EXTRA=e,/BUFFER) 
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

