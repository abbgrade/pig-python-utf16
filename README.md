# pig-python-utf16

Apache Pig does not support UTF-16 input so far out of the box, so it becomes tricky to load it anyway.
This solution loads the input as bytearray and provides a user defined python function to convert the bytearray into a pig readable chararray. It contains hacks for the issue of UTF-8 line splitting with an UTF-16 file and the bugs of the ancient Jython version of Pig.

## Example

Upload the decode_utf16.py to a location, where you can load it from your PIG script.
Replace <PATH> in the following example PIG script with a path to that location.

    -- load helper functions
    REGISTER '<PATH>/decode_utf16.py' using jython as udf_utf16;
    
    -- load raw data
    bytes = LOAD '<PATH>/utf16-input.txt' USING PigStorage('\n') AS (line:bytearray);
    DESCRIBE bytes;
    
    lines = FOREACH bytes GENERATE flatten(udf_utf16.decode(line)) AS (line:chararray);
    DESCRIBE lines;
    ranked_lines = RANK lines;
    DUMP ranked_lines;
