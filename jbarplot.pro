FUNCTION jbarplot, x, y, _REF_EXTRA=e
;call the function with extra args, and have it go to the buffer rather than a window
IF N_PARAMS() eq 2 THEN p=barplot(x,y,_STRICT_EXTRA=e,/BUFFER) ELSE p=barplot(x,_STRICT_EXTRA=e,/BUFFER)
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

