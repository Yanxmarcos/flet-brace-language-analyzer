%{
#include <stdio.h>
#include <stdlib.h>
#include "parser.h"

int error = 0; // Variable global para manejar errores
%}

%option noyywrap
%option yylineno

ignora     [ \t\n\r]
letra      [a-zA-Z]
digito     [0-9]
identificador "$"{letra}({letra}|{digito}|[_])*
numero     {digito}+ 
real       {digito}+\.{digito}+ 
cadena     \".*\" 
comentario_linea "//".* 
comentario_bloque "/*"([^*]|\*+[^*/])*\*+"/"

%%

{ignora}+       { /* Ignorar espacios, tabulaciones y saltos de línea */ }

"&&"       { return AND; }
"||"       { return OR; }
"!!"       { return NOT; }
"["       { return '['; }
"]"       { return ']'; }
"entero"        { return DEF_ENTERO; }
"real"          { return DEF_REAL; }
"cadena"         { return DEF_CADENA; }
"si"            { return SI; }
"sino"          { return SINO; }
"mientras"      { return MIENTRAS; }
"para"          { return PARA; }
"escribir"      { return ESCRIBIR; }
"leer"          { return LEER; }
"retornar"          { return RETORNAR; }
"romper"          { return ROMPER; }
"vacio"          { return VACIO; }
"main"   {  return MAIN;}
"="             { return '='; }
"+"             { return '+'; }
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }
">"             { return '>'; }
"<"             { return '<'; }
">="            { return MAYOR_IGUAL; }
"<="            { return MENOR_IGUAL; }
"=="            { return IGUALDAD; }
"!="            { return DESIGUALDAD; }
"("             { return '('; }
")"             { return ')'; }
"{"             { return '{'; }
"}"             { return '}'; }
";"             { return ';'; }
","             { return ','; }
"%"             { return '%'; }
{numero}        { return NUMERO_ENTERO; }
{real}          { return NUMERO_REAL; }
{cadena}        { return CADENA; }
{identificador} { return IDENTIFICADOR; }
{comentario_linea}  { /* Ignorar comentarios de línea */ }
{comentario_bloque} { /* Ignorar comentarios de bloque */ }
.               { printf(">|%d|%s\n", yylineno, yytext); }

%%

// Función para obtener el nombre del token
const char* obtener_nombre_token(int TOKEN) {
    switch (TOKEN) {
        case DEF_ENTERO: return "DEF_ENTERO";
        case DEF_REAL: return "DEF_REAL";
        case DEF_CADENA: return "DEF_CADENA";
        case SI: return "SI";
        case SINO: return "SINO";
        case MIENTRAS: return "MIENTRAS";
        case PARA: return "PARA";
        case ESCRIBIR: return "ESCRIBIR";
        case LEER: return "LEER";
        case '=': return "ASIGNACION";
        case '+': return "SUMA";
        case '-': return "RESTA";
        case '*': return "MULTIPLICACION";
        case '/': return "DIVISION";
        case '>': return "MAYOR_QUE";
        case '<': return "MENOR_QUE";
        case MAYOR_IGUAL: return "MAYOR_IGUAL";
        case MENOR_IGUAL: return "MENOR_IGUAL";
        case IGUALDAD: return "IGUALDAD";
        case DESIGUALDAD: return "DESIGUALDAD";
        case '(': return "PARENTESIS_ABIERTO";
        case ')': return "PARENTESIS_CERRADO";
        case '{': return "LLAVES_ABIERTA";
        case '}': return "LLAVES_CERRADA";
        case ';': return "PUNTO_COMA";
        case ',': return "COMA";
        case NUMERO_ENTERO: return "NUMERO_ENTERO";
        case NUMERO_REAL: return "NUMERO_REAL";
        case CADENA: return "CADENA";
        case IDENTIFICADOR: return "IDENTIFICADOR";
        case RETORNAR: return "RETORNAR";
        case VACIO: return "VACIO";
        case MAIN: return "MAIN";
        case AND: return "AND";
        case OR: return "OR";
        case NOT: return "NOT";
        case '[': return "CORCHETE_ABIERTO";
        case ']': return "CORCHETE_CERRADO";
        case '%': return "MODULO";
        case ROMPER: return "ROMPER";
        default: return "ERRONEO";
    }
}

// Función para manejar errores sintácticos
void yyerror(const char *msg) {
    error = 1;
    printf("<|m|%s|%d\n", msg, yylineno);
}

int main(int argc, char* argv[]) {
    // Verificar que se proporcionó un nombre de archivo
    if (argc < 2) {
        printf("Uso: %s <nombre_archivo>\n", argv[0]);
        return 1;
    }

    // Abrir el archivo
    yyin = fopen(argv[1], "rt");
    if (yyin == NULL) {
        printf("ERROR: Archivo no se encuentra!\n");
        return 1;
    }

    // Analizar los tokens
    int Token;
    while ((Token = yylex()) > 0) {
        printf("+|%d|%s|%s\n", Token, yytext, obtener_nombre_token(Token));
    }

    // Reiniciar el análisis para el parser
    fseek(yyin, 0, SEEK_SET);
    yyrestart(yyin);
    yylineno = 1;

    printf("=\n");

    // Ejecutar el parser
    yyparse();

    // Verificar si hubo errores
    if (error == 0) {
        printf("<|b|Programa OK|0\n");
    }

    // Cerrar el archivo
    fclose(yyin);
    return 0;
}