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

### Description

The first part is a multi line comment which will be used as description.
The content between `'/*'` and `'*/'` will be used as description.

### Unit

The next part is a single line comment starting with `// unit `, which specifies the unit.

### Example

This is an example of a correct header:
```
/*
    This is am example script.
*/

// unit example_script
```

## Special functions

* \_\_initialize__()
* \_\_process__(IInterface e)
* \_\_finalize__()




  