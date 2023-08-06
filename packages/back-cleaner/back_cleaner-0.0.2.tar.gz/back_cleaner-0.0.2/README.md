# back-cleaner
Server-side Python tool for escaping script tags and converting characters into HTML entity equivalents (no regex).

## def escape_script_tags(input_str)

This function escapes script tags with backslashes.


### Sample

from back_cleaner.cleaner import escape_script_tags

source = "<script>Hey, how are you doing?</script>"
result = escape_script_tags(source)
print(result)


## def replace_with_ents(input_str)

This function converts the following characters into the HTML entity equivalents.

1. Ampersand (&)
2. Less than (<)
3. Greater than (>)
4. Double quote (")
5. Single quote (')


### Sample

from back_cleaner.cleaner import replace_with_ents

source = "<script>Hey, how are you doing?</script>"
result = replace_with_ents(source)
print(result)
