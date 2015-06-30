FUNCTION jplot, x, y, _REF_EXTRA=e
;example of an IDL 8 plot routine wrapper
;call the function with extra args, and have it go to the buffer rather than a window
p=plot(x,y,_STRICT_EXTRA=e,/BUFFER)
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

