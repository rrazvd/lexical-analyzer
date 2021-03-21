# lexical-analyzer
A Lexical Analyzer developed for Problem Based Learning of Programming Language Processors discipline.

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
