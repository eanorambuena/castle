from lark import Lark, Transformer, Token, v_args 

from grammar import GRAMMAR


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
   from operator import add, sub, mul, truediv as div, neg, eq, ne, lt, gt, le, ge
   number = float

   def __init__(self):
      self.vars = {}
      self.functions = {}

   def assign_var(self, name, value):
      self.vars[name] = value
      return value

   def assign_to_var(self, value, name):
      return self.assign_var(name, value)

   def call(self, name, tuple):
      try:
         result = self.functions[name]
         for index in range(len(tuple)):
            result = result.replace(f"a{index}", repr(tuple[index]))
         return parse(result)
      except KeyError:
         return print("Callable not found: %s" % name)
      except RecursionError:
         return print(f"RecursionError: maximum recursion depth exceeded while calling {name}")

   def callable(self, args, *expressions):
      expression = expressions[-1]
      args_list = []
      expression_args_list = []
      for arg in args:
         args_list.append(arg)
      if len(expressions) > 1:
         expression_args = expressions[:-1]
         for arg in expression_args:
            expression_args_list.append(arg.value)
      return (args_list, expression_args_list, expression)

   def codeblock(self, *code):
      parsed_code = ""
      for item in code:
         if type(item) == Token:
            parsed_code += item.value
         elif type(item) == str:
            parsed_code += "{" + item + "}"
      return parsed_code

   def definition(self, name, constant):
      args, expression_args, expression = constant
      for index in range(len(args)):
         expression = expression.replace(args[index], f"a{index}")
      for index in range(len(expression_args)):
         expression = expression.replace(expression_args[index], f"e{index}")
      self.functions[name.value] = expression

   def echo(self, value):
      return print(str(value).replace("\\n", "\n"), end = "")

   def string(self, value):
      return value[1:-1]

   def tuple(self, *values):
      return values

   def conditional(self, number, code):
      if number != 0:
         return parse(code)

   def named_tuple(self, *values):
      if len(values) == 1:
         return values[0]
      return values

   def children_block(self, name):
      return name.value

   def var(self, name):
      try:
         return self.vars[name]
      except KeyError:
         return print("Variable not found: %s" % name)

parser = Lark(GRAMMAR, parser='lalr', transformer=CalculateTree())
parse = parser.parse