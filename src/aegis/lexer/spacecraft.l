%{
/*
 * Spacecraft DSL Lexical Analyzer
 *
 * This file demonstrates how Flex/Lex can tokenize
 * spacecraft-specific commands.
 */

#include "spacecraft.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%

"POWER"             { return POWER; }
"CAMERA_ON"         { return CAMERA_ON; }
"CAMERA_OFF"        { return CAMERA_OFF; }
"CAPTURE_IMAGE"     { return CAPTURE_IMAGE; }
"TRANSMIT_IMAGE"    { return TRANSMIT_IMAGE; }
"END_MISSION"       { return END_MISSION; }

"BATTERY"           { return BATTERY; }
"SOLAR"             { return SOLAR; }
"THERMAL"           { return THERMAL; }
"FAULT"             { return FAULT; }
"RECOVER"           { return RECOVER; }

[0-9]+              {
                      yylval.number = atoi(yytext);
                      return NUMBER;
                    }

[0-9]+\.[0-9]+      {
                      yylval.decimal = atof(yytext);
                      return DECIMAL;
                    }

\"[^\"]*\"          {
                      yylval.text = strdup(yytext);
                      return STRING;
                    }

[ \t\r\n]+          {
                      /* Ignore whitespace */
                    }

"("                 { return '('; }
")"                 { return ')'; }
"{"                 { return '{'; }
"}"                 { return '}'; }
":"                 { return ':'; }
";"                 { return ';'; }
","                 { return ','; }
"="                 { return '='; }

.                   {
                      return yytext[0];
                    }

%%

int yywrap(void)
{
    return 1;
}