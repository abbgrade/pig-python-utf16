#!/usr/bin/python

from StringIO import StringIO
import array

'''
align utf-16 bytestring
'''
def align_utf16(line):

    if len(line) % 2 == 1:
        
        if line[0] != chr(0): 
            line = chr(0) + line
            
        elif line[-1] == chr(0):
            line = line[:-1]

        else:
            line = line + chr(0)
    
    return line

'''
convert signed byte array to string of unsigned bytes
'''
def cast_signed_to_unsigned_byte(input):
    assert isinstance(input, array.array), 'unexpected input parameter'
    assert input.typecode == 'b', 'unexpected input type'

    buffer = StringIO()
    for byte in input:
        byte = (256 + byte) % 256
        buffer.write(chr(byte))
    buffer.seek(0)
    output = buffer.getvalue()

    assert isinstance(output, str)
    return output

'''
convert unsigned byte array to string of signed bytes
'''
def cast_unsigned_to_signed_byte(line):
    line_array = array.array('b', [])

    for byte in line:

        if byte > 127:
            byte = byte & 127
            byte = -128 + byte

        line_array.append(byte)
    
    return line_array

'''
convert array of singed byte to unsigned byte
'''
def decode_utf16(line):
    
    # precondition
    assert isinstance(line, array.array), 'unexpected format'
    assert line.typecode == 'b', 'unexpected type'
    
    # pig passes the byte arrays as singed bytes.
    # however they need to be casted to unsigned bytes.
    line = cast_signed_to_unsigned_byte(line)

    # the pig loader splits a UTF16 stream by an ASCII char, 
    # so the parts aren't valid UTF16 strings anymore.
    line = align_utf16(line)

    # postcondition
    assert len(line) % 2 == 0, 'invalid utf-16'
    
    # convert to string
    line = line.decode('utf-16')
    return line

@outputSchema("(Line:chararray)")
def decode(line):
    
    line = decode_utf16(line)
    return [line]
