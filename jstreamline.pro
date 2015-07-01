FUNCTION jstreamline, u, v, x, y, _REF_EXTRA=e
;call the function with extra args, and have it go to the buffer rather than a window
CASE N_PARAMS() OF
1: message, 'Insufficient arguments' 
2: p=streamline(u,v,_STRICT_EXTRA=e,/BUFFER) 
3: message, 'Cannot take only 3 arguments. 2 or 4 required. 
4: p=streamline(u,v,x,y,_STRICT_EXTRA=e,/BUFFER) 
ENDCASE
;add to the stack for writing at the end
new_pointer=ptr_new([*!inline_8objs,ptr_new(p)])
ptr_free,!inline_8objs
!inline_8objs=new_pointer
RETURN, p
END

