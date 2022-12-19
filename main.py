from parse import parse

def main():
   while True:
      try:
         s = input('> ')
      except EOFError:
         break
      print(parse(s))

def test():
   text = """
      print := (x, y) => {
         echo 'x y \n'
      }
      a <- 1+2
      (1 + a) * -3 -> b
      if 1 {
         print(a, b + 6)
      }
      c <- 4
      print2 := (x, y) {code} => {
         echo 'x is y \n'
         if c > 0 {
            c <- c - 1
            echo "c = "
            echo c
            echo "\n"
            code
            print2(x, y) {code}
         }
      }
      z <- 50
      print2(a, b){
         z<-c * 2
         echo "z = "
         echo z
         echo "\n"
      }
      """
   parse(text)

if __name__ == '__main__':
   test()
   #main()