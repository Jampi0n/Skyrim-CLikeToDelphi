# CLike to Delphi transpiler

This transpiler translates CLike code to Delphi for xEdit scripts.
If you prefer the standard c/Java syntax over Delphi syntax, you can use this transpiler to produce xEdit scripts without writing Delphi. 

## About CLike

CLike is the name of the input language and it uses a syntax very similar to c, hence the name.
The transpiler is mostly a syntax translator, since it only does basic transformations.
You need to understand Delphi, since you will need to call Delphi functions.

The main syntactical differences between CLike and Delphi are:
* Assignment with `=` instead of `:=`.
* Assignments with `+=`, `*=`, etc.
* Function definitions are like in c/Java: `ReturnType FunctionName(Type Parameter, ...) {...}` 
* Local variables can be declared (with optional initialization) inside functions.
* Global variables can be initialized when they are declared.
* Strings behave like in c/Java, use double quotes and support common special characters like `\n`

Statements work like in c/Java. The following statements are implemented:
* If, Else
* While
* Break
* Continue
* Return
* Try, Catch, Finally
* Throw

The `For` statement is only very basic. Use it for counting: `for(int i=0;i<10;i+=1){...}`. For more advanced loops, use While.

Syntax highlighting for c# fits well for CLike, because it supports exceptions, constants and global variables like they are implemented in CLike.

## Usage

Install python 3 and the required libraries from requirements.txt.
Run `CLikeToDelphi.py <Input Path> <Output Path>`. For more information, run `CLikeToDelphi.py --help`

## CLike Program Structure

The CLike script must start with the header.

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
You can write a small delphi function containing the problematic part in order to minimize the Delphi code.

## Special functions

* `__initialize__()` This function is executed at the start of the script.
* `__process__(IInterface e)` This function is executed for every selected element.
* `__finalize__()` This function is executed at the end of the script.




  