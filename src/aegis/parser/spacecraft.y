%{
/*
 * Spacecraft DSL Syntax Parser
 *
 * This file demonstrates how Yacc/Bison can parse
 * spacecraft-specific commands using grammar rules.
 */

#include <stdio.h>
#include <stdlib.h>

int yylex(void);

void yyerror(const char *message)
{
    fprintf(stderr, "Syntax error: %s\n", message);
}
%}

/* Semantic value types */
%union
{
    int number;
    double decimal;
    char *text;
}

/* Tokens received from Lex/Flex */
%token POWER
%token CAMERA_ON
%token CAMERA_OFF
%token CAPTURE_IMAGE
%token TRANSMIT_IMAGE
%token END_MISSION

%token BATTERY
%token SOLAR
%token THERMAL
%token FAULT
%token RECOVER

%token <number> NUMBER
%token <decimal> DECIMAL
%token <text> STRING

%start mission

%%

mission:
      command_list END_MISSION
      {
          printf("Mission parsed successfully.\n");
      }
    ;

command_list:
      command_list command
    | command
    ;

command:
      power_command
    | camera_command
    | capture_command
    | transmit_command
    | telemetry_command
    | fault_command
    ;

power_command:
      POWER NUMBER ';'
      {
          printf("POWER command detected.\n");
      }
    ;

camera_command:
      CAMERA_ON ';'
      {
          printf("CAMERA_ON command detected.\n");
      }
    | CAMERA_OFF ';'
      {
          printf("CAMERA_OFF command detected.\n");
      }
    ;

capture_command:
      CAPTURE_IMAGE ';'
      {
          printf("CAPTURE_IMAGE command detected.\n");
      }
    ;

transmit_command:
      TRANSMIT_IMAGE ';'
      {
          printf("TRANSMIT_IMAGE command detected.\n");
      }
    ;

telemetry_command:
      BATTERY '=' NUMBER ';'
      {
          printf("BATTERY telemetry detected.\n");
      }
    | SOLAR '=' NUMBER ';'
      {
          printf("SOLAR telemetry detected.\n");
      }
    | THERMAL '=' NUMBER ';'
      {
          printf("THERMAL telemetry detected.\n");
      }
    ;

fault_command:
      FAULT STRING ';'
      {
          printf("FAULT command detected.\n");
      }
    | RECOVER STRING ';'
      {
          printf("RECOVER command detected.\n");
      }
    ;

%%