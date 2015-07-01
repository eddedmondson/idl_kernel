FUNCTION jcontour, data,x, y, _REF_EXTRA=e
;call the function with extra args, and have it go to the buffer rather than a window
CASE N_PARAMS() OF
1: p=contour(data,_STRICT_EXTRA=e,/BUFFER) 
2: message, 'Cannot take only 2 arguments. 1 or 3 required.'
3: p=contour(data,x,y,_STRICT_EXTRA=e,/BUFFER) 
ENDCASE
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

