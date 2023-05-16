# TKOM_23L - dokmentacja wstępna

Imię i nazwisko     - Grzegorz Socha

Nr indeksu          - 310905

Prowadząca          - Agnieszka Malanowska


## Cel projektu
Projekt polega na realizacji interpretera pewnego języka. Każdy język powinien zawierać, oprócz elementów wymienionych w treści zadania, pewne standardowe elementy omówione na wykładzie (np. typy całkowitoliczbowe i zmiennoprzecinkowe, stałe znakowe, wyrażenia arytmetyczne i logiczne, instrukcję warunkową, pętlę, funkcje itd.)


## Temat projektu

Język umożliwiający opis punktów i odcinków w przestrzeni trójwymiarowej. Punkt i odcinek (zbudowany z punktów) są wbudowanymi typami języka. Z odcinków można budować bryły. Kolekcja brył tworzy scenę wyświetlaną na ekranie.


## Specyfikacja

- Realizacja w języku Python
- Statyczne oraz silne typowanie
- Zmienne mutowalne


## Typy wbudowane
### Typy proste
- `int`
- `float`
- `bool`
- `string`

### Typy złożone
- `List` - Lista pozwalająca na przechowywanie obiektów, zawiera następujące metody:
  - length() - zwraca ilość elementów w liście,
  - get(index) - zwraca element znajdujący się na pozycji index,
  - add(element) - dodaje element na koniec listy,
  - remove(index) - usuwa element znajdujący się na pozycji index,
- `Point` - Typ pozwalający na definiowanie punktu, posiada pola x(float), y(float), z(float) okreslające jego położenie, zawiera następujące metody:
  - set_x(x) - ustawia nową wartość x,
  - set_y(y) - ustawia nową wartość y,
  - set_z(z) - ustawia nową wartość z,
  - get_x() - zwraca wartość x,
  - get_y() - zwraca wartość y,
  - get_z() - zwraca wartość z,
- `Line` - Typ pozwalający na definiowanie odcinka składającego się z dwóch punktów - start(Point) oraz end(Point), zawiera następujące metody:
  - set_start(start) - ustawia nowy punkt start,
  - set_end(end) - ustawia nowy punkt end,
  - length() - zwraca długość odcinka,
  - get_start() - zwraca punkt start,
  - get_end() - zwraca punkt end,
- `Polyhedron` - Typ pozywalający na definiowanie bryły złożonej z n ilości odcinków, warunkiem koniecznym do stworzenia jest połączenie odcinków w jednolitą bryłę tj. każdy punkt składający się na daną bryłę ma min. 3 różnorodne wychodzące z niego odcinki, posiada następujące metody:
  - points() - zwraca listę punktów składających się na bryłę,
  - lines() - zwraca listę odcinków składających się na bryłę,
- `Collection` - Typ pozwalający na definiowanie zbioru brył, który jest wyświetlany na ekranie, zawiera następujące metody:
  - add(Polyhedron) - dodaje bryłę do zbioru,
  - remove(Polyhedron) - usuwa bryłę z zbioru,
  - display() - wyświetla na ekranie rzut 3d zbioru brył,
  - empty() - usuwa wszystkie bryły z zbioru.


## Operatory
- arytmetyczne `+, -, *, /`
- logiczne:
  - relacje `==, !=, >, <, >=, <=`
  - łączniki `or, and`
- przypisania `=`
- dostęp do obiektu `.`
- negacji `-, !`

Dla poszczególnych typów dostepne są następujące operatory:
| Typ          | Operator                              |
|--------------|---------------------------------------|
| int          | `=, +, -, *, /, ==, !=, >, <, >=, <=` |
| float        | `=, +, -, *, /, ==, !=, >, <, >=, <=` |
| bool         | `=, ==, !=, or, and, !`               |
| string       | `=, +, ==, !=`                        |
| List         | `=, +, ==, !=, .`                     |
| Point        | `=, ==, !=, .`                        |
| Line         | `=, ==, !=, .`                        |
| Polyhedron   | `=, ==, !=, .`                        |
| Collection   | `=, ==, !=, .`                        |


## Tworzenie zmiennych
Zmienne proste tworzone będą następująco:

`typ_zmiennej nazwa_zmiennej = wartość zmiennej;`

np.

```
int a = 0;
string temp = "smth";
```


## Komentarze
Komentarze będą tworzone poprzez dodanie # przed tekstem komentarza.


## Instrukcja warunkowe
Struktra instukcji wygląda następująco:

`if (warunek) {} else {}`

np.

```
if (a == 0)
{
    a = 0;
}
else
{
    a = 1;
}
```


## Pętla
Dostępna będzie jedna pętla wyglądająca nastepująco:

`while(warunek) {}`

np.

```
while(a != b)
{
    a = a + 1;
}
```


## Definiowanie funkcji
Każdy wczytany program musi zawierać funkcję `int main()`, która będzie wykonywana jako pierwsza.
Funkcje muszą być określone przed funkcją `main` oraz muszą mieć określony typ zwracanej wartości. Funkcje które nie będą zwracać żadnej wartości powinny być typu `void`.

Definiowanie funkcji będzie wyglądało następująco:

`typ_zwracanej_wartości nazwa_funkcji(przekazywane_argumenty) {}`

np.

```
int add(a, b)
{
    return a + b;
}
```


## Przykładowy kod programu

```
# przykładowa funkcja
bool is_vertex(Point a, Polyhedron p)
{
    bool vertex = false;
    int n = p.points().length();
    int i = 0;

    while(i < n)
    {
        if(p.points().get(i).x == a.x and p.points().get(i).y == a.y and p.points().get(i).z == a.z)
        {
            vertex = true;
        }
        i = i + 1;
    }

    return vertex;
}

int main()
{
  # definicja zmiennych
  Point a = Point(0, 0, 0);
  Point b = Point(2, 3, 0);
  Point c = Point(6, 1, 2);
  Point d = Point(4, 7, 5);

  Line ab = Line(a, b);
  Line ac = Line(a, c);
  Line ad = Line(a, d);
  Line bc = Line(b, c);
  Line bd = Line(b, d);
  Line cd = Line(c, d);

  Polyhedron p = Polyhedron(ab, ac, ad, bc, bd, cd);

  Collection scene = Collection();


  # dodanie wielokąta do sceny i wyświetlenie go
  scene.add(p);
  scene.display();


  # wywołanie funkcji oraz wypisanie wartości do konsoli
  bool result = is_vertex(c, p);
  print(result);
}
```


## Funkcje wbudowane
- print - wypisuje linię na wyjście standardowe.


## Gramatyka

```
program                     = {function_declaration} ;

block                       = "{", {statement}, "}" ;

statement                   = assigment | if_statement | while_statement | function_call, ";" | return, ";" ;

assignment                  = type, identifier, "=", expression, ";" ;

if_statement                = "if", "(", expression, ")", block, ["else", block] ;

while_statement             = "while", "(", expression, ")", block ;

function_call               = identifier, "(", [call_parameters_list], ")" ;

call_parameters_list        = expression, {",", expression} ;

function_declaration        = function_type, identifier, "(", [parameters_list], ")", block ;

parameters_list             = type, identifier, {",", type, identifier} ;

return                      = "return", [expression] ;

expression                  = or_expression ;

or_expression               = and_expression, {or_operator, and_expression} ;

and_expression              = comparative_expression, {and_operator, comparative_expression} ;

comparison_expression       = arithmetic_expression, [comparison_operator, arithmetic_expression] ;

arithmetic_expression       = multiplicative_expression, {arithmetic_operator, multiplicative_expression} ;

multiplicative_expression   = negation_expression, {multiplicative_operator, negation_expression} ;

negation_expression         = [negation_operator], object_access_expression ;

object_access_expression    = factor, {access_operator, identifier} ;

factor                      = literal | identifier | function_call | "(", expression, ")" ;

arithmetic_operator         = "+" | "-" ;

multiplicative_operator     = "*" | "/" ;

comparison_operator         = "==" | "!=" | ">" | "<" | ">=" | "<=" ;

or_operator                 = "or" ;

and_operator                = "and" ;

negation_operator           = "-" | "!" ;

access_operator             = "." ;

function_type               = "void" | type ;

type                        = "int" | "float" | "bool" | "string" | "Point" | "Line" | "Collection" | "List" ;

identifier                  = letter, {letter | digit } ;

literal                     = int | float | bool | string ;

int                         = "0" | (non_zero_digit, {digit}) ;

float                       = int, ".", digit, {digit} ;

bool                        = "true" | "false" ;

string                      = '"', {char}, '"' ;

char                        = ({letter} | {digit} | {other_symbols}), {char} ;

letter                      = #'[a-z]' | #'[A-Z]' ;

digit                       = "0" | non_zero_digit ;

non_zero_digit              = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

other_symbols               = " " | "." | "," | "!" | "?" | ":" | "/" | "@" | "$" | "%" | "^" | "*" | "-" | "+" | "_" ;
```


## Obsługiwanie błędów
W razie wystąpienia błędu zwracany będzie odpowiedni komunikat. Jeśli będzie to błąd krytyczny to program zostanie przerwany.

Przykładowe komunikaty błędu:

```
ComparissonError: Error occured in line 3, column 5:
cannot compare 'int' to 'string'.
```
```
InvalidTokenError: Error occured in line 2, column 3:
Invalid character '$'
```


## Analiza wymagań
- program interpretuje kod z pliku tekstowego,
- sprawdza poprawność leksykalną i składniową i zgłasza wykryte błędy,
- zapewnia unikalność nazw zmiennych i funkcji,
- sprawdza poprawność tworzonych zmiennych typów złożonych,
- umożliwia na wielokrotne tworzenie oraz wyświetlanie scen zawierających bryły.


## Podział na moduły
- Lekser - Moduł realizujacy analizę leksykalną. Z pobranych znaków tworzy tokeny.
- Parser - Moduł realizujący analizę składniową. Tworzy on drzewo obiektów do gotowych do interpretacji.
- Interpreter - Moduł realizujacy interpretację analizowanego kodu. Wykonuje on dostarczony kod i zwraca wynik.
- Obsługa błędów - Moduł realizujacy obsługę błędów zgłoszonych przez inne moduły.


## Testowanie

Każdy z poszczególnych modułów będzie posiadał testy jednostkowe zrealizowane za pomocą biblioteki `pytest`.


## Biblioteki

Na obecną chwilę, do wyświetlania scen na ekranie użyta będzie biblioteka `matplotlib`.
