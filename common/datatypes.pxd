cdef class Frame:
    cdef public int pack
    cdef public dict message
    cdef public object hash
        
    cpdef serialize(self)
    cpdef pack_frame(Frame self, dict kwargs)
    cpdef digest(Frame self)

cdef class MetaFrame(Frame):

    cpdef gen_message(MetaFrame self)

cdef class DataFrame(Frame):

    cpdef gen_message(self)

cdef class TaskFrame(Frame):

    cpdef gen_message(self)