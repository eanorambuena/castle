GRAMMAR = r"""
   ?start: code+

   ?expression: sum
      | comparison

   ?assignation: NAME "<-" expression      -> assign_var
      | expression "->" NAME               -> assign_to_var

   ?definition: NAME ":=" constant -> definition

   ?constant: expression | callable | class | codeblock | use

   ?callable: named_tuple children_block* "=>" codeblock -> callable
   ?class: "class" named_tuple codeblock

   ?destructuring: "..." NAME

   ?use: (NAME ".")+ NAME
   ?call: (NAME ".")* NAME tuple codeblock* -> call

   ?codeblock: "{" /[^{^}]+/? codeblock* /[^{^}]+/? "}" -> codeblock
   ?children_block: "{" NAME "}" -> chlidren_block
   
   ?code: constant
      | assignation
      | definition
      | clause
      | conditional

   ?comparison: sum "<" sum    -> lt
      | sum ">" sum           -> gt
      | sum "<=" sum          -> le
      | sum ">=" sum          -> ge
      | sum "==" sum          -> eq
      | sum "!=" sum          -> ne

   ?sum: product
      | sum "+" product    -> add
      | sum "-" product    -> sub

   ?product: atom
      | product "*" atom   -> mul
      | product "/" atom   -> div

   ?conditional: "if" code codeblock    -> conditional

   ?atom: NUMBER           -> number
      | "-" atom           -> neg
      | NAME               -> var
      | singleton
      | call
      | string

   ?object: tuple
      | expression

   ?singleton: "(" expression ")"
   ?tuple: "(" ")" | "(" object ("," object)+ ","? ")" -> tuple
   ?named_tuple: "(" ")" | "(" NAME ("," NAME)* ","? ")" -> named_tuple

   ?clause: "echo" object     -> echo

   ?string: /\'[^\']*\'|\"[^\"]*\"/ -> string

   %import common.CNAME -> NAME
   %import common.NUMBER
   %import common.WS_INLINE
   %import common.WS

   %ignore WS_INLINE
   %ignore WS
"""