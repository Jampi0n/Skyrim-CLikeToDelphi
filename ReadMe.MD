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

## Special functions

* \_\_initialize__()
* \_\_process__(IInterface e)
* \_\_finalize__()




  