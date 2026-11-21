%{
#include <stdio.h>
#include <stdlib.h>
int yystopparser=0;
%}

// Tokens definidos en el léxico
%token DEF_ENTERO DEF_REAL DEF_CADENA VACIO MAIN
%token SI SINO MIENTRAS PARA ESCRIBIR LEER RETORNAR
%token AND OR NOT
%token MAYOR_IGUAL MENOR_IGUAL IGUALDAD DESIGUALDAD
%token NUMERO_ENTERO NUMERO_REAL CADENA IDENTIFICADOR ROMPER

// Precedencia de operadores
%left OR
%left AND
%left NOT
%left '>' '<' MAYOR_IGUAL MENOR_IGUAL IGUALDAD DESIGUALDAD
%left '+' '-'
%left '*' '/'

// Inicio de la gramática
%start programa

%%

// Reglas de la gramática

// Programa principal
programa:
    lista_decl lista_funciones
    | lista_funciones
    ;

// Lista de declaraciones globales
lista_decl:
    lista_decl dec
    | dec
    ;

// Declaración global o local
dec: 
    declaracion_var ';'
    ;

// Lista de funciones
lista_funciones:
    lista_funciones funcion
    | funcion
    ;

// Definición de una función
funcion:
    tipo IDENTIFICADOR '(' lista_parametros ')' bloque
    | tipo MAIN '(' ')' bloque
    ;

// Lista de parámetros
lista_parametros:
    parametro
    | lista_parametros ',' parametro
    |
    ;

// Parámetro de una función
parametro:
    tipo IDENTIFICADOR
    ;

// Bloque de código
bloque:
    '{' lista_sentencias '}'
    ;

// Lista de sentencias
lista_sentencias:
    lista_sentencias sentencia
    | sentencia
    ;

// Sentencias
sentencia:
    declaracion_var ';'
    | asignacion ';'
    | sentencia_si
    | sentencia_mientras
    | sentencia_para
    | sentencia_escribir ';'
    | sentencia_leer ';'
    | sentencia_retornar ';'
    | llamada_funcion ';'
    | ROMPER ';'
    ;

// Declaración de variables
declaracion_var:
    tipo IDENTIFICADOR
    | tipo IDENTIFICADOR '=' expresion
    | tipo IDENTIFICADOR '[' factor ']' '=' '{' lista_factores '}'
    ;

// Lista de Factores
lista_factores: 
    lista_factores ',' factor
    | factor
    |
    ;

// Asignación
asignacion:
    IDENTIFICADOR '=' expresion
    | IDENTIFICADOR '[' factor ']' '=' expresion
    | IDENTIFICADOR '+' '+'
    ;

// Sentencia if
sentencia_si:
    SI '(' expresion ')' bloque opt_sino
    ;

// Opcional else
opt_sino:
    SINO bloque
    |
    ;

// Sentencia while
sentencia_mientras:
    MIENTRAS '(' expresion ')' bloque
    ;

// Sentencia for
sentencia_para:
    PARA '(' declaracion_var ';' expresion ';' asignacion ')' bloque
    ;

// Sentencia escribir
sentencia_escribir:
    ESCRIBIR '(' lista_expresiones ')'
    ;

// Sentencia leer
sentencia_leer:
    LEER '(' IDENTIFICADOR ')'
    ;

// Sentencia retornar
sentencia_retornar:
    RETORNAR expresion
    ;

// Llamada a función
llamada_funcion:
    IDENTIFICADOR '(' lista_argumentos ')'
    ;

// Lista de argumentos
lista_argumentos:
    lista_argumentos ',' expresion
    | expresion
    |
    ;

// Lista de expresiones
lista_expresiones:
    lista_expresiones ',' expresion
    | expresion
    ;

// Expresiones
expresion:
    expresion OR expresion_and
    | expresion_and
    ;

expresion_and:
    expresion_and AND expresion_not
    | expresion_not
    ;

expresion_not:
    NOT expresion_not
    | expresion_relacional
    ;

expresion_relacional:
    expresion_simple '>' expresion_simple
    | expresion_simple '<' expresion_simple
    | expresion_simple MAYOR_IGUAL expresion_simple
    | expresion_simple MENOR_IGUAL expresion_simple
    | expresion_simple IGUALDAD expresion_simple
    | expresion_simple DESIGUALDAD expresion_simple
    | expresion_simple
    ;

expresion_simple:
    expresion_simple '+' termino
    | expresion_simple '-' termino
    | expresion_simple '%' termino
    | termino
    ;

termino:
    termino '*' factor
    | termino '/' factor
    | factor
    ;

factor:
    NUMERO_ENTERO
    | NUMERO_REAL
    | CADENA
    | IDENTIFICADOR
    | '(' expresion ')'
    | llamada_funcion
    | IDENTIFICADOR '[' factor ']'
    ;

// Tipos de datos
tipo:
    DEF_ENTERO
    | DEF_REAL
    | DEF_CADENA
    | VACIO
    ;

%%