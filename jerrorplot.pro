FUNCTION jerrorplot, x, y, xe, ye, _REF_EXTRA=e
;call the function with extra args, and have it go to the buffer rather than a window
CASE N_PARAMS() OF
1: message, 'Insufficient arguments' 
2: p=errorplot(x,y,_STRICT_EXTRA=e,/BUFFER) 
3: p=errorplot(x,y,xe,_STRICT_EXTRA=e,/BUFFER) 
4: p=errorplot(x,y,xe,ye,_STRICT_EXTRA=e,/BUFFER) 
ENDCASE
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

