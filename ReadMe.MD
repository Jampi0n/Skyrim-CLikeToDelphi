# CLike to Delphi transpiler

This transpiler translates CLike code to Delphi for xEdit scripts.

## Introduction

The source language is not c, but a independent function with syntax similar to c.

## Limitations

The target language is limited and these limitations also affect the source language:

* No arrays. Use the TList object instead.
* No return statement. Assign a value to Result (implicitly declared).
* No break statement.
* No ternary condition operator.
* All local variables have the entire functions as scope.
* The for statement is very basic. If complex logic is required, manually write it with while.

## Header

The script must start with the header.

### Description (Required)

The first multi line comment will be used as description.
The multi line comment is between `'/*'` and `'*/'`.

### Unit (Required)

A single line comment starting with `// unit name` specifies the delphi unit.

### Uses (Optional)

To import other delphi units, use `// uses name`.

### Imports (Optional)

Single line comments starting with `// import path` can be used to split your project into multiple files.
Relative paths to the main file can be used:
* `./` specifies the directory of the main file.
* `../` specifies the parent directory of the main file.

All paths that do not start with `./` or `../` are interpreted as absolute paths.
This can be useful for shared imports.

### Delphi Code (Optional)

If needed, delphi code can be written directly.
There are two options to write delphi code:
```
// delphi begin
...
// delphi end

/* delphi begin
...
delphi end */
```
When using an IDE, the body of the second option will be considered a comment and will prevent syntax warnings.

You cannot use this feature for inline comments and only for top level elements, like functions.
If you cannot implement a function with CLike, write the entire function in delphi instead.
You can write a small delphi function containing the problematic part in order to minimize the delphi code.

## Special functions

* `__initialize__()` This function is executed at the start of the script.
* `__process__(IInterface e)` This function is executed for every selected element.
* `__finalize__()` This function is executed at the end of the script.




  