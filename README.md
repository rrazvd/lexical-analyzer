# lexical-analyzer
A Lexical Analyzer developed for Problem Based Learning of Programming Language Processors discipline.

# Getting started
1. Clone the main branch
2. Create input ("/input") and output ("/output") folders on root
3. Create a input file (Ex.: "input1.txt") on input folder and write your code
4. Run python3 main.py to analyze your code
5. Check the output folder

# Lexical structure of language

| Description | Composition |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Reserved words  | `var` `const` `typeDef` `struct` `extends` `procedure` `function` `start` `return` `if` `else` `then` `while` `read` `print` `int` `real` `boolean` `string` `true` `false` `global` `local` |
| Identifiers (ID) | letter(letter \| digit \| `_` )\*|
| Numbers | Digit+( . Digit+)? |
| Digits | [0-9] |
| Letters | [a-z] \| [A-Z] |
| Arithmetic operators | `+` `-` `*` `/` `++` `--` |
| Relational operators | `==` `!=` `>` `>=` `<` `<=` `=` |
| Logical operators | `&&` `\|\|` `!` |
| Comments delimeters | `//` This is a line comment `/*` This is a block comment `*/`
| Delimiters | `;` `,` `()` `[]` `{}` `.` |
| String | "(letter \| digit \| symbol \| `\"`)* " |
| Symbol | ASCII 32 to 126 (except ASCII 34) |

# Tokens

| Type | Token |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Reserved word | PRE |
| Identifier | IDE |
| Number | NRO |
| Delimiter | DEL |
| Relational operator | REL |
| Logical operator | LOG |
| Arithmetic operator | ART |
| String | CAD |
| Invalid symbol | SIB |
| Malformed string | CMF |
| Malformed number | NMF |
| Malformed comment | CoMF |
| Malformed operator | OpMF |
