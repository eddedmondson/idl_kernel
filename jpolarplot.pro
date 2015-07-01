FUNCTION jpolarplot, r, theta, _REF_EXTRA=e
;call the function with extra args, and have it go to the buffer rather than a window
CASE N_PARAMS() OF
1: p=polarplot(r,_STRICT_EXTRA=e,/BUFFER)
2: p=polarplot(r,theta,_STRICT_EXTRA=e,/BUFFER) 
ENDCASE
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

