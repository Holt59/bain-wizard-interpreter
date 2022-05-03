# Generated from ./vendor/wizparse/wizards/wizard.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,66,323,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,1,0,1,0,1,0,1,1,1,1,5,1,62,8,1,10,1,12,1,65,9,1,1,2,1,
        2,1,2,1,2,3,2,71,8,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,5,1,5,1,5,
        1,5,1,5,1,5,1,5,1,5,3,5,89,8,5,1,6,1,6,3,6,93,8,6,1,7,1,7,1,7,1,
        7,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,11,1,11,1,11,1,11,
        3,11,113,8,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,3,12,
        124,8,12,1,13,1,13,1,13,1,14,1,14,1,14,1,14,5,14,133,8,14,10,14,
        12,14,136,9,14,1,14,3,14,139,8,14,1,14,1,14,1,15,1,15,3,15,145,8,
        15,1,15,1,15,1,16,5,16,150,8,16,10,16,12,16,153,9,16,1,16,3,16,156,
        8,16,1,17,1,17,1,17,1,17,1,17,1,17,1,18,1,18,1,18,1,18,5,18,168,
        8,18,10,18,12,18,171,9,18,1,18,3,18,174,8,18,1,18,1,18,1,19,1,19,
        1,19,1,19,5,19,182,8,19,10,19,12,19,185,9,19,1,19,3,19,188,8,19,
        1,19,1,19,1,20,1,20,1,20,1,20,1,20,1,21,1,21,1,21,5,21,200,8,21,
        10,21,12,21,203,9,21,3,21,205,8,21,1,22,1,22,1,22,1,23,1,23,1,23,
        1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,
        1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,3,23,237,
        8,23,3,23,239,8,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,
        1,23,1,23,1,23,3,23,253,8,23,1,23,1,23,1,23,1,23,3,23,259,8,23,1,
        23,1,23,1,23,1,23,3,23,265,8,23,1,23,1,23,1,23,1,23,1,23,1,23,1,
        23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,
        23,1,23,1,23,3,23,289,8,23,1,23,1,23,3,23,293,8,23,1,23,1,23,3,23,
        297,8,23,3,23,299,8,23,1,23,1,23,1,23,1,23,1,23,3,23,306,8,23,5,
        23,308,8,23,10,23,12,23,311,9,23,1,24,1,24,1,25,1,25,1,26,1,26,1,
        26,1,26,1,27,1,27,1,27,0,1,46,28,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,0,11,1,0,30,35,1,
        0,12,13,2,0,56,56,60,61,1,0,57,58,1,0,37,38,1,0,39,40,2,0,36,36,
        41,41,1,0,14,15,1,0,16,17,1,0,18,20,1,0,54,55,352,0,56,1,0,0,0,2,
        63,1,0,0,0,4,70,1,0,0,0,6,72,1,0,0,0,8,76,1,0,0,0,10,88,1,0,0,0,
        12,90,1,0,0,0,14,94,1,0,0,0,16,98,1,0,0,0,18,101,1,0,0,0,20,105,
        1,0,0,0,22,108,1,0,0,0,24,117,1,0,0,0,26,125,1,0,0,0,28,128,1,0,
        0,0,30,144,1,0,0,0,32,151,1,0,0,0,34,157,1,0,0,0,36,163,1,0,0,0,
        38,177,1,0,0,0,40,191,1,0,0,0,42,204,1,0,0,0,44,206,1,0,0,0,46,238,
        1,0,0,0,48,312,1,0,0,0,50,314,1,0,0,0,52,316,1,0,0,0,54,320,1,0,
        0,0,56,57,3,2,1,0,57,58,5,0,0,1,58,1,1,0,0,0,59,62,3,4,2,0,60,62,
        3,46,23,0,61,59,1,0,0,0,61,60,1,0,0,0,62,65,1,0,0,0,63,61,1,0,0,
        0,63,64,1,0,0,0,64,3,1,0,0,0,65,63,1,0,0,0,66,71,3,6,3,0,67,71,3,
        8,4,0,68,71,3,10,5,0,69,71,3,44,22,0,70,66,1,0,0,0,70,67,1,0,0,0,
        70,68,1,0,0,0,70,69,1,0,0,0,71,5,1,0,0,0,72,73,5,65,0,0,73,74,5,
        42,0,0,74,75,3,46,23,0,75,7,1,0,0,0,76,77,5,65,0,0,77,78,7,0,0,0,
        78,79,3,46,23,0,79,9,1,0,0,0,80,89,5,43,0,0,81,89,3,12,6,0,82,89,
        5,44,0,0,83,89,3,22,11,0,84,89,3,28,14,0,85,89,5,51,0,0,86,89,3,
        30,15,0,87,89,3,40,20,0,88,80,1,0,0,0,88,81,1,0,0,0,88,82,1,0,0,
        0,88,83,1,0,0,0,88,84,1,0,0,0,88,85,1,0,0,0,88,86,1,0,0,0,88,87,
        1,0,0,0,89,11,1,0,0,0,90,92,5,1,0,0,91,93,3,46,23,0,92,91,1,0,0,
        0,92,93,1,0,0,0,93,13,1,0,0,0,94,95,5,2,0,0,95,96,3,46,23,0,96,97,
        3,2,1,0,97,15,1,0,0,0,98,99,5,3,0,0,99,100,3,2,1,0,100,17,1,0,0,
        0,101,102,5,45,0,0,102,103,3,46,23,0,103,104,3,2,1,0,104,19,1,0,
        0,0,105,106,5,46,0,0,106,107,3,2,1,0,107,21,1,0,0,0,108,109,5,4,
        0,0,109,112,5,65,0,0,110,113,3,24,12,0,111,113,3,26,13,0,112,110,
        1,0,0,0,112,111,1,0,0,0,113,114,1,0,0,0,114,115,3,2,1,0,115,116,
        5,47,0,0,116,23,1,0,0,0,117,118,5,5,0,0,118,119,3,46,23,0,119,120,
        5,6,0,0,120,123,3,46,23,0,121,122,5,7,0,0,122,124,3,46,23,0,123,
        121,1,0,0,0,123,124,1,0,0,0,124,25,1,0,0,0,125,126,5,63,0,0,126,
        127,3,46,23,0,127,27,1,0,0,0,128,129,5,8,0,0,129,130,3,46,23,0,130,
        134,3,2,1,0,131,133,3,18,9,0,132,131,1,0,0,0,133,136,1,0,0,0,134,
        132,1,0,0,0,134,135,1,0,0,0,135,138,1,0,0,0,136,134,1,0,0,0,137,
        139,3,20,10,0,138,137,1,0,0,0,138,139,1,0,0,0,139,140,1,0,0,0,140,
        141,5,48,0,0,141,29,1,0,0,0,142,145,3,36,18,0,143,145,3,38,19,0,
        144,142,1,0,0,0,144,143,1,0,0,0,145,146,1,0,0,0,146,147,5,49,0,0,
        147,31,1,0,0,0,148,150,3,14,7,0,149,148,1,0,0,0,150,153,1,0,0,0,
        151,149,1,0,0,0,151,152,1,0,0,0,152,155,1,0,0,0,153,151,1,0,0,0,
        154,156,3,16,8,0,155,154,1,0,0,0,155,156,1,0,0,0,156,33,1,0,0,0,
        157,158,3,46,23,0,158,159,5,23,0,0,159,160,3,46,23,0,160,161,5,23,
        0,0,161,162,3,46,23,0,162,35,1,0,0,0,163,164,5,9,0,0,164,169,3,46,
        23,0,165,166,5,23,0,0,166,168,3,34,17,0,167,165,1,0,0,0,168,171,
        1,0,0,0,169,167,1,0,0,0,169,170,1,0,0,0,170,173,1,0,0,0,171,169,
        1,0,0,0,172,174,5,23,0,0,173,172,1,0,0,0,173,174,1,0,0,0,174,175,
        1,0,0,0,175,176,3,32,16,0,176,37,1,0,0,0,177,178,5,10,0,0,178,183,
        3,46,23,0,179,180,5,23,0,0,180,182,3,34,17,0,181,179,1,0,0,0,182,
        185,1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,187,1,0,0,0,185,
        183,1,0,0,0,186,188,5,23,0,0,187,186,1,0,0,0,187,188,1,0,0,0,188,
        189,1,0,0,0,189,190,3,32,16,0,190,39,1,0,0,0,191,192,5,11,0,0,192,
        193,3,46,23,0,193,194,3,2,1,0,194,195,5,50,0,0,195,41,1,0,0,0,196,
        201,3,46,23,0,197,198,5,23,0,0,198,200,3,46,23,0,199,197,1,0,0,0,
        200,203,1,0,0,0,201,199,1,0,0,0,201,202,1,0,0,0,202,205,1,0,0,0,
        203,201,1,0,0,0,204,196,1,0,0,0,204,205,1,0,0,0,205,43,1,0,0,0,206,
        207,5,52,0,0,207,208,3,42,21,0,208,45,1,0,0,0,209,210,6,23,-1,0,
        210,211,5,25,0,0,211,212,3,46,23,0,212,213,5,26,0,0,213,239,1,0,
        0,0,214,215,5,65,0,0,215,216,5,25,0,0,216,217,3,42,21,0,217,218,
        5,26,0,0,218,239,1,0,0,0,219,220,5,64,0,0,220,239,5,65,0,0,221,222,
        5,65,0,0,222,239,5,64,0,0,223,224,5,62,0,0,224,239,5,65,0,0,225,
        226,5,65,0,0,226,239,5,62,0,0,227,228,5,57,0,0,228,239,3,46,23,14,
        229,230,7,1,0,0,230,239,3,46,23,13,231,237,3,48,24,0,232,237,3,52,
        26,0,233,237,3,50,25,0,234,237,3,54,27,0,235,237,5,65,0,0,236,231,
        1,0,0,0,236,232,1,0,0,0,236,233,1,0,0,0,236,234,1,0,0,0,236,235,
        1,0,0,0,237,239,1,0,0,0,238,209,1,0,0,0,238,214,1,0,0,0,238,219,
        1,0,0,0,238,221,1,0,0,0,238,223,1,0,0,0,238,225,1,0,0,0,238,227,
        1,0,0,0,238,229,1,0,0,0,238,236,1,0,0,0,239,309,1,0,0,0,240,241,
        10,10,0,0,241,242,5,59,0,0,242,308,3,46,23,11,243,244,10,9,0,0,244,
        245,7,2,0,0,245,308,3,46,23,10,246,247,10,8,0,0,247,248,7,3,0,0,
        248,308,3,46,23,9,249,250,10,7,0,0,250,252,7,4,0,0,251,253,5,29,
        0,0,252,251,1,0,0,0,252,253,1,0,0,0,253,254,1,0,0,0,254,308,3,46,
        23,8,255,256,10,6,0,0,256,258,7,5,0,0,257,259,5,29,0,0,258,257,1,
        0,0,0,258,259,1,0,0,0,259,260,1,0,0,0,260,308,3,46,23,7,261,262,
        10,5,0,0,262,264,7,6,0,0,263,265,5,29,0,0,264,263,1,0,0,0,264,265,
        1,0,0,0,265,266,1,0,0,0,266,308,3,46,23,6,267,268,10,4,0,0,268,269,
        7,7,0,0,269,308,3,46,23,5,270,271,10,3,0,0,271,272,7,8,0,0,272,308,
        3,46,23,4,273,274,10,20,0,0,274,275,5,24,0,0,275,276,5,65,0,0,276,
        277,5,25,0,0,277,278,3,42,21,0,278,279,5,26,0,0,279,308,1,0,0,0,
        280,281,10,12,0,0,281,282,5,27,0,0,282,283,3,46,23,0,283,284,5,28,
        0,0,284,308,1,0,0,0,285,286,10,11,0,0,286,288,5,27,0,0,287,289,3,
        46,23,0,288,287,1,0,0,0,288,289,1,0,0,0,289,290,1,0,0,0,290,292,
        5,29,0,0,291,293,3,46,23,0,292,291,1,0,0,0,292,293,1,0,0,0,293,298,
        1,0,0,0,294,296,5,29,0,0,295,297,3,46,23,0,296,295,1,0,0,0,296,297,
        1,0,0,0,297,299,1,0,0,0,298,294,1,0,0,0,298,299,1,0,0,0,299,300,
        1,0,0,0,300,308,5,28,0,0,301,302,10,2,0,0,302,303,5,63,0,0,303,305,
        3,46,23,0,304,306,5,29,0,0,305,304,1,0,0,0,305,306,1,0,0,0,306,308,
        1,0,0,0,307,240,1,0,0,0,307,243,1,0,0,0,307,246,1,0,0,0,307,249,
        1,0,0,0,307,255,1,0,0,0,307,261,1,0,0,0,307,267,1,0,0,0,307,270,
        1,0,0,0,307,273,1,0,0,0,307,280,1,0,0,0,307,285,1,0,0,0,307,301,
        1,0,0,0,308,311,1,0,0,0,309,307,1,0,0,0,309,310,1,0,0,0,310,47,1,
        0,0,0,311,309,1,0,0,0,312,313,7,9,0,0,313,49,1,0,0,0,314,315,5,53,
        0,0,315,51,1,0,0,0,316,317,5,53,0,0,317,318,5,24,0,0,318,319,5,53,
        0,0,319,53,1,0,0,0,320,321,7,10,0,0,321,55,1,0,0,0,30,61,63,70,88,
        92,112,123,134,138,144,151,155,169,173,183,187,201,204,236,238,252,
        258,264,288,292,296,298,305,307,309
    ]

class wizardParser ( Parser ):

    grammarFileName = "wizard.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'Cancel'", "'Case'", "'Default'", "'For'", 
                     "'from'", "'to'", "'by'", "'If'", "'SelectOne'", "'SelectMany'", 
                     "'While'", "'!'", "'not'", "'|'", "'or'", "'&'", "'and'", 
                     "'False'", "'True'", "'SubPackages'", "<INVALID>", 
                     "<INVALID>", "','", "'.'", "'('", "')'", "'['", "']'", 
                     "':'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'Break'", "'Continue'", "'Elif'", "'Else'", 
                     "'EndFor'", "'EndIf'", "'EndSelect'", "'EndWhile'", 
                     "'Return'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'/'", "'-'", "'+'", "'^'", "'*'", "'%'", 
                     "<INVALID>", "'in'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "COMMENT", "CONTINUATION", "Comma", "Dot", 
                      "LeftParenthesis", "RightParenthesis", "LeftBracket", 
                      "RightBracket", "Colon", "CompoundAdd", "CompoundSub", 
                      "CompoundMul", "CompoundDiv", "CompoundExp", "CompoundMod", 
                      "Equal", "GreaterOrEqual", "Greater", "LesserOrEqual", 
                      "Lesser", "NotEqual", "Assign", "Break", "Continue", 
                      "Elif", "Else", "EndFor", "EndIf", "EndSelect", "EndWhile", 
                      "Return", "Keyword", "Number", "DoubleQuotedString", 
                      "SingleQuotedString", "Divide", "Minus", "Plus", "Raise", 
                      "Times", "Modulo", "Decrement", "In", "Increment", 
                      "Identifier", "WHITESPACE" ]

    RULE_parseWizard = 0
    RULE_body = 1
    RULE_stmt = 2
    RULE_assignment = 3
    RULE_compoundAssignment = 4
    RULE_controlFlowStmt = 5
    RULE_cancelStmt = 6
    RULE_caseStmt = 7
    RULE_defaultStmt = 8
    RULE_elifStmt = 9
    RULE_elseStmt = 10
    RULE_forStmt = 11
    RULE_forRangeHeader = 12
    RULE_forInHeader = 13
    RULE_ifStmt = 14
    RULE_selectStmt = 15
    RULE_selectCaseList = 16
    RULE_optionTuple = 17
    RULE_selectOne = 18
    RULE_selectMany = 19
    RULE_whileStmt = 20
    RULE_argList = 21
    RULE_keywordStmt = 22
    RULE_expr = 23
    RULE_constant = 24
    RULE_integer = 25
    RULE_decimal = 26
    RULE_string = 27

    ruleNames =  [ "parseWizard", "body", "stmt", "assignment", "compoundAssignment", 
                   "controlFlowStmt", "cancelStmt", "caseStmt", "defaultStmt", 
                   "elifStmt", "elseStmt", "forStmt", "forRangeHeader", 
                   "forInHeader", "ifStmt", "selectStmt", "selectCaseList", 
                   "optionTuple", "selectOne", "selectMany", "whileStmt", 
                   "argList", "keywordStmt", "expr", "constant", "integer", 
                   "decimal", "string" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    COMMENT=21
    CONTINUATION=22
    Comma=23
    Dot=24
    LeftParenthesis=25
    RightParenthesis=26
    LeftBracket=27
    RightBracket=28
    Colon=29
    CompoundAdd=30
    CompoundSub=31
    CompoundMul=32
    CompoundDiv=33
    CompoundExp=34
    CompoundMod=35
    Equal=36
    GreaterOrEqual=37
    Greater=38
    LesserOrEqual=39
    Lesser=40
    NotEqual=41
    Assign=42
    Break=43
    Continue=44
    Elif=45
    Else=46
    EndFor=47
    EndIf=48
    EndSelect=49
    EndWhile=50
    Return=51
    Keyword=52
    Number=53
    DoubleQuotedString=54
    SingleQuotedString=55
    Divide=56
    Minus=57
    Plus=58
    Raise=59
    Times=60
    Modulo=61
    Decrement=62
    In=63
    Increment=64
    Identifier=65
    WHITESPACE=66

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ParseWizardContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def EOF(self):
            return self.getToken(wizardParser.EOF, 0)

        def getRuleIndex(self):
            return wizardParser.RULE_parseWizard

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParseWizard" ):
                listener.enterParseWizard(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParseWizard" ):
                listener.exitParseWizard(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParseWizard" ):
                return visitor.visitParseWizard(self)
            else:
                return visitor.visitChildren(self)




    def parseWizard(self):

        localctx = wizardParser.ParseWizardContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_parseWizard)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56
            self.body()
            self.state = 57
            self.match(wizardParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.StmtContext)
            else:
                return self.getTypedRuleContext(wizardParser.StmtContext,i)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)


        def getRuleIndex(self):
            return wizardParser.RULE_body

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBody" ):
                listener.enterBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBody" ):
                listener.exitBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = wizardParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << wizardParser.T__0) | (1 << wizardParser.T__3) | (1 << wizardParser.T__7) | (1 << wizardParser.T__8) | (1 << wizardParser.T__9) | (1 << wizardParser.T__10) | (1 << wizardParser.T__11) | (1 << wizardParser.T__12) | (1 << wizardParser.T__17) | (1 << wizardParser.T__18) | (1 << wizardParser.T__19) | (1 << wizardParser.LeftParenthesis) | (1 << wizardParser.Break) | (1 << wizardParser.Continue) | (1 << wizardParser.Return) | (1 << wizardParser.Keyword) | (1 << wizardParser.Number) | (1 << wizardParser.DoubleQuotedString) | (1 << wizardParser.SingleQuotedString) | (1 << wizardParser.Minus) | (1 << wizardParser.Decrement))) != 0) or _la==wizardParser.Increment or _la==wizardParser.Identifier:
                self.state = 61
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 59
                    self.stmt()
                    pass

                elif la_ == 2:
                    self.state = 60
                    self.expr(0)
                    pass


                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(wizardParser.AssignmentContext,0)


        def compoundAssignment(self):
            return self.getTypedRuleContext(wizardParser.CompoundAssignmentContext,0)


        def controlFlowStmt(self):
            return self.getTypedRuleContext(wizardParser.ControlFlowStmtContext,0)


        def keywordStmt(self):
            return self.getTypedRuleContext(wizardParser.KeywordStmtContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = wizardParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 67
                self.compoundAssignment()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 68
                self.controlFlowStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 69
                self.keywordStmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)

        def Assign(self):
            return self.getToken(wizardParser.Assign, 0)

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = wizardParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(wizardParser.Identifier)
            self.state = 73
            self.match(wizardParser.Assign)
            self.state = 74
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompoundAssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def CompoundExp(self):
            return self.getToken(wizardParser.CompoundExp, 0)

        def CompoundMul(self):
            return self.getToken(wizardParser.CompoundMul, 0)

        def CompoundDiv(self):
            return self.getToken(wizardParser.CompoundDiv, 0)

        def CompoundMod(self):
            return self.getToken(wizardParser.CompoundMod, 0)

        def CompoundAdd(self):
            return self.getToken(wizardParser.CompoundAdd, 0)

        def CompoundSub(self):
            return self.getToken(wizardParser.CompoundSub, 0)

        def getRuleIndex(self):
            return wizardParser.RULE_compoundAssignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompoundAssignment" ):
                listener.enterCompoundAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompoundAssignment" ):
                listener.exitCompoundAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompoundAssignment" ):
                return visitor.visitCompoundAssignment(self)
            else:
                return visitor.visitChildren(self)




    def compoundAssignment(self):

        localctx = wizardParser.CompoundAssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_compoundAssignment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(wizardParser.Identifier)
            self.state = 77
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << wizardParser.CompoundAdd) | (1 << wizardParser.CompoundSub) | (1 << wizardParser.CompoundMul) | (1 << wizardParser.CompoundDiv) | (1 << wizardParser.CompoundExp) | (1 << wizardParser.CompoundMod))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 78
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ControlFlowStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return wizardParser.RULE_controlFlowStmt

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ReturnContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Return(self):
            return self.getToken(wizardParser.Return, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturn" ):
                listener.enterReturn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturn" ):
                listener.exitReturn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn" ):
                return visitor.visitReturn(self)
            else:
                return visitor.visitChildren(self)


    class CancelContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def cancelStmt(self):
            return self.getTypedRuleContext(wizardParser.CancelStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCancel" ):
                listener.enterCancel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCancel" ):
                listener.exitCancel(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCancel" ):
                return visitor.visitCancel(self)
            else:
                return visitor.visitChildren(self)


    class BreakContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Break(self):
            return self.getToken(wizardParser.Break, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreak" ):
                listener.enterBreak(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreak" ):
                listener.exitBreak(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak" ):
                return visitor.visitBreak(self)
            else:
                return visitor.visitChildren(self)


    class ForContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def forStmt(self):
            return self.getTypedRuleContext(wizardParser.ForStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFor" ):
                listener.enterFor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFor" ):
                listener.exitFor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFor" ):
                return visitor.visitFor(self)
            else:
                return visitor.visitChildren(self)


    class SelectContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def selectStmt(self):
            return self.getTypedRuleContext(wizardParser.SelectStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelect" ):
                listener.enterSelect(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelect" ):
                listener.exitSelect(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelect" ):
                return visitor.visitSelect(self)
            else:
                return visitor.visitChildren(self)


    class WhileContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def whileStmt(self):
            return self.getTypedRuleContext(wizardParser.WhileStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhile" ):
                listener.enterWhile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhile" ):
                listener.exitWhile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile" ):
                return visitor.visitWhile(self)
            else:
                return visitor.visitChildren(self)


    class ContinueContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Continue(self):
            return self.getToken(wizardParser.Continue, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinue" ):
                listener.enterContinue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinue" ):
                listener.exitContinue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue" ):
                return visitor.visitContinue(self)
            else:
                return visitor.visitChildren(self)


    class IfContext(ControlFlowStmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ControlFlowStmtContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ifStmt(self):
            return self.getTypedRuleContext(wizardParser.IfStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIf" ):
                listener.enterIf(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIf" ):
                listener.exitIf(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf" ):
                return visitor.visitIf(self)
            else:
                return visitor.visitChildren(self)



    def controlFlowStmt(self):

        localctx = wizardParser.ControlFlowStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_controlFlowStmt)
        try:
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [wizardParser.Break]:
                localctx = wizardParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 80
                self.match(wizardParser.Break)
                pass
            elif token in [wizardParser.T__0]:
                localctx = wizardParser.CancelContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 81
                self.cancelStmt()
                pass
            elif token in [wizardParser.Continue]:
                localctx = wizardParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 82
                self.match(wizardParser.Continue)
                pass
            elif token in [wizardParser.T__3]:
                localctx = wizardParser.ForContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 83
                self.forStmt()
                pass
            elif token in [wizardParser.T__7]:
                localctx = wizardParser.IfContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 84
                self.ifStmt()
                pass
            elif token in [wizardParser.Return]:
                localctx = wizardParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 85
                self.match(wizardParser.Return)
                pass
            elif token in [wizardParser.T__8, wizardParser.T__9]:
                localctx = wizardParser.SelectContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 86
                self.selectStmt()
                pass
            elif token in [wizardParser.T__10]:
                localctx = wizardParser.WhileContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 87
                self.whileStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CancelStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_cancelStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCancelStmt" ):
                listener.enterCancelStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCancelStmt" ):
                listener.exitCancelStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCancelStmt" ):
                return visitor.visitCancelStmt(self)
            else:
                return visitor.visitChildren(self)




    def cancelStmt(self):

        localctx = wizardParser.CancelStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_cancelStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(wizardParser.T__0)
            self.state = 92
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.state = 91
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CaseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_caseStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCaseStmt" ):
                listener.enterCaseStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCaseStmt" ):
                listener.exitCaseStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCaseStmt" ):
                return visitor.visitCaseStmt(self)
            else:
                return visitor.visitChildren(self)




    def caseStmt(self):

        localctx = wizardParser.CaseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_caseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(wizardParser.T__1)
            self.state = 95
            self.expr(0)
            self.state = 96
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefaultStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_defaultStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefaultStmt" ):
                listener.enterDefaultStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefaultStmt" ):
                listener.exitDefaultStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultStmt" ):
                return visitor.visitDefaultStmt(self)
            else:
                return visitor.visitChildren(self)




    def defaultStmt(self):

        localctx = wizardParser.DefaultStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_defaultStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.match(wizardParser.T__2)
            self.state = 99
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElifStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Elif(self):
            return self.getToken(wizardParser.Elif, 0)

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_elifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElifStmt" ):
                listener.enterElifStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElifStmt" ):
                listener.exitElifStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElifStmt" ):
                return visitor.visitElifStmt(self)
            else:
                return visitor.visitChildren(self)




    def elifStmt(self):

        localctx = wizardParser.ElifStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_elifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(wizardParser.Elif)
            self.state = 102
            self.expr(0)
            self.state = 103
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Else(self):
            return self.getToken(wizardParser.Else, 0)

        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_elseStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElseStmt" ):
                listener.enterElseStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElseStmt" ):
                listener.exitElseStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseStmt" ):
                return visitor.visitElseStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseStmt(self):

        localctx = wizardParser.ElseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_elseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(wizardParser.Else)
            self.state = 106
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)

        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def EndFor(self):
            return self.getToken(wizardParser.EndFor, 0)

        def forRangeHeader(self):
            return self.getTypedRuleContext(wizardParser.ForRangeHeaderContext,0)


        def forInHeader(self):
            return self.getTypedRuleContext(wizardParser.ForInHeaderContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStmt" ):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)




    def forStmt(self):

        localctx = wizardParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_forStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self.match(wizardParser.T__3)
            self.state = 109
            self.match(wizardParser.Identifier)
            self.state = 112
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [wizardParser.T__4]:
                self.state = 110
                self.forRangeHeader()
                pass
            elif token in [wizardParser.In]:
                self.state = 111
                self.forInHeader()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 114
            self.body()
            self.state = 115
            self.match(wizardParser.EndFor)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForRangeHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)


        def getRuleIndex(self):
            return wizardParser.RULE_forRangeHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForRangeHeader" ):
                listener.enterForRangeHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForRangeHeader" ):
                listener.exitForRangeHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForRangeHeader" ):
                return visitor.visitForRangeHeader(self)
            else:
                return visitor.visitChildren(self)




    def forRangeHeader(self):

        localctx = wizardParser.ForRangeHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_forRangeHeader)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.match(wizardParser.T__4)
            self.state = 118
            self.expr(0)
            self.state = 119
            self.match(wizardParser.T__5)
            self.state = 120
            self.expr(0)
            self.state = 123
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==wizardParser.T__6:
                self.state = 121
                self.match(wizardParser.T__6)
                self.state = 122
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForInHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def In(self):
            return self.getToken(wizardParser.In, 0)

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_forInHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForInHeader" ):
                listener.enterForInHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForInHeader" ):
                listener.exitForInHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForInHeader" ):
                return visitor.visitForInHeader(self)
            else:
                return visitor.visitChildren(self)




    def forInHeader(self):

        localctx = wizardParser.ForInHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_forInHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.match(wizardParser.In)
            self.state = 126
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def EndIf(self):
            return self.getToken(wizardParser.EndIf, 0)

        def elifStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ElifStmtContext)
            else:
                return self.getTypedRuleContext(wizardParser.ElifStmtContext,i)


        def elseStmt(self):
            return self.getTypedRuleContext(wizardParser.ElseStmtContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = wizardParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.match(wizardParser.T__7)
            self.state = 129
            self.expr(0)
            self.state = 130
            self.body()
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==wizardParser.Elif:
                self.state = 131
                self.elifStmt()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 138
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==wizardParser.Else:
                self.state = 137
                self.elseStmt()


            self.state = 140
            self.match(wizardParser.EndIf)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EndSelect(self):
            return self.getToken(wizardParser.EndSelect, 0)

        def selectOne(self):
            return self.getTypedRuleContext(wizardParser.SelectOneContext,0)


        def selectMany(self):
            return self.getTypedRuleContext(wizardParser.SelectManyContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_selectStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectStmt" ):
                listener.enterSelectStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectStmt" ):
                listener.exitSelectStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectStmt" ):
                return visitor.visitSelectStmt(self)
            else:
                return visitor.visitChildren(self)




    def selectStmt(self):

        localctx = wizardParser.SelectStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_selectStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [wizardParser.T__8]:
                self.state = 142
                self.selectOne()
                pass
            elif token in [wizardParser.T__9]:
                self.state = 143
                self.selectMany()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 146
            self.match(wizardParser.EndSelect)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectCaseListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def caseStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.CaseStmtContext)
            else:
                return self.getTypedRuleContext(wizardParser.CaseStmtContext,i)


        def defaultStmt(self):
            return self.getTypedRuleContext(wizardParser.DefaultStmtContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_selectCaseList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectCaseList" ):
                listener.enterSelectCaseList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectCaseList" ):
                listener.exitSelectCaseList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectCaseList" ):
                return visitor.visitSelectCaseList(self)
            else:
                return visitor.visitChildren(self)




    def selectCaseList(self):

        localctx = wizardParser.SelectCaseListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_selectCaseList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==wizardParser.T__1:
                self.state = 148
                self.caseStmt()
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 155
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==wizardParser.T__2:
                self.state = 154
                self.defaultStmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OptionTupleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(wizardParser.Comma)
            else:
                return self.getToken(wizardParser.Comma, i)

        def getRuleIndex(self):
            return wizardParser.RULE_optionTuple

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOptionTuple" ):
                listener.enterOptionTuple(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOptionTuple" ):
                listener.exitOptionTuple(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOptionTuple" ):
                return visitor.visitOptionTuple(self)
            else:
                return visitor.visitChildren(self)




    def optionTuple(self):

        localctx = wizardParser.OptionTupleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_optionTuple)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 157
            self.expr(0)
            self.state = 158
            self.match(wizardParser.Comma)
            self.state = 159
            self.expr(0)
            self.state = 160
            self.match(wizardParser.Comma)
            self.state = 161
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectOneContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def selectCaseList(self):
            return self.getTypedRuleContext(wizardParser.SelectCaseListContext,0)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(wizardParser.Comma)
            else:
                return self.getToken(wizardParser.Comma, i)

        def optionTuple(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.OptionTupleContext)
            else:
                return self.getTypedRuleContext(wizardParser.OptionTupleContext,i)


        def getRuleIndex(self):
            return wizardParser.RULE_selectOne

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectOne" ):
                listener.enterSelectOne(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectOne" ):
                listener.exitSelectOne(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectOne" ):
                return visitor.visitSelectOne(self)
            else:
                return visitor.visitChildren(self)




    def selectOne(self):

        localctx = wizardParser.SelectOneContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_selectOne)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self.match(wizardParser.T__8)
            self.state = 164
            self.expr(0)
            self.state = 169
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 165
                    self.match(wizardParser.Comma)
                    self.state = 166
                    self.optionTuple() 
                self.state = 171
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

            self.state = 173
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==wizardParser.Comma:
                self.state = 172
                self.match(wizardParser.Comma)


            self.state = 175
            self.selectCaseList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectManyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def selectCaseList(self):
            return self.getTypedRuleContext(wizardParser.SelectCaseListContext,0)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(wizardParser.Comma)
            else:
                return self.getToken(wizardParser.Comma, i)

        def optionTuple(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.OptionTupleContext)
            else:
                return self.getTypedRuleContext(wizardParser.OptionTupleContext,i)


        def getRuleIndex(self):
            return wizardParser.RULE_selectMany

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectMany" ):
                listener.enterSelectMany(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectMany" ):
                listener.exitSelectMany(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectMany" ):
                return visitor.visitSelectMany(self)
            else:
                return visitor.visitChildren(self)




    def selectMany(self):

        localctx = wizardParser.SelectManyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_selectMany)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.match(wizardParser.T__9)
            self.state = 178
            self.expr(0)
            self.state = 183
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 179
                    self.match(wizardParser.Comma)
                    self.state = 180
                    self.optionTuple() 
                self.state = 185
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==wizardParser.Comma:
                self.state = 186
                self.match(wizardParser.Comma)


            self.state = 189
            self.selectCaseList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(wizardParser.BodyContext,0)


        def EndWhile(self):
            return self.getToken(wizardParser.EndWhile, 0)

        def getRuleIndex(self):
            return wizardParser.RULE_whileStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStmt" ):
                listener.enterWhileStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStmt" ):
                listener.exitWhileStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = wizardParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            self.match(wizardParser.T__10)
            self.state = 192
            self.expr(0)
            self.state = 193
            self.body()
            self.state = 194
            self.match(wizardParser.EndWhile)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(wizardParser.Comma)
            else:
                return self.getToken(wizardParser.Comma, i)

        def getRuleIndex(self):
            return wizardParser.RULE_argList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgList" ):
                listener.enterArgList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgList" ):
                listener.exitArgList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgList" ):
                return visitor.visitArgList(self)
            else:
                return visitor.visitChildren(self)




    def argList(self):

        localctx = wizardParser.ArgListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_argList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 196
                self.expr(0)
                self.state = 201
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==wizardParser.Comma:
                    self.state = 197
                    self.match(wizardParser.Comma)
                    self.state = 198
                    self.expr(0)
                    self.state = 203
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeywordStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Keyword(self):
            return self.getToken(wizardParser.Keyword, 0)

        def argList(self):
            return self.getTypedRuleContext(wizardParser.ArgListContext,0)


        def getRuleIndex(self):
            return wizardParser.RULE_keywordStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeywordStmt" ):
                listener.enterKeywordStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeywordStmt" ):
                listener.exitKeywordStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeywordStmt" ):
                return visitor.visitKeywordStmt(self)
            else:
                return visitor.visitChildren(self)




    def keywordStmt(self):

        localctx = wizardParser.KeywordStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_keywordStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(wizardParser.Keyword)
            self.state = 207
            self.argList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return wizardParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class PreIncrementContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Increment(self):
            return self.getToken(wizardParser.Increment, 0)
        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreIncrement" ):
                listener.enterPreIncrement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreIncrement" ):
                listener.exitPreIncrement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPreIncrement" ):
                return visitor.visitPreIncrement(self)
            else:
                return visitor.visitChildren(self)


    class DotFunctionCallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)

        def Dot(self):
            return self.getToken(wizardParser.Dot, 0)
        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)
        def LeftParenthesis(self):
            return self.getToken(wizardParser.LeftParenthesis, 0)
        def argList(self):
            return self.getTypedRuleContext(wizardParser.ArgListContext,0)

        def RightParenthesis(self):
            return self.getToken(wizardParser.RightParenthesis, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDotFunctionCall" ):
                listener.enterDotFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDotFunctionCall" ):
                listener.exitDotFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDotFunctionCall" ):
                return visitor.visitDotFunctionCall(self)
            else:
                return visitor.visitChildren(self)


    class OrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOr" ):
                listener.enterOr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOr" ):
                listener.exitOr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOr" ):
                return visitor.visitOr(self)
            else:
                return visitor.visitChildren(self)


    class InContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def In(self):
            return self.getToken(wizardParser.In, 0)
        def Colon(self):
            return self.getToken(wizardParser.Colon, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIn" ):
                listener.enterIn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIn" ):
                listener.exitIn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIn" ):
                return visitor.visitIn(self)
            else:
                return visitor.visitChildren(self)


    class PostDecrementContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)
        def Decrement(self):
            return self.getToken(wizardParser.Decrement, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostDecrement" ):
                listener.enterPostDecrement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostDecrement" ):
                listener.exitPostDecrement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostDecrement" ):
                return visitor.visitPostDecrement(self)
            else:
                return visitor.visitChildren(self)


    class TimesDivideModuloContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def Times(self):
            return self.getToken(wizardParser.Times, 0)
        def Divide(self):
            return self.getToken(wizardParser.Divide, 0)
        def Modulo(self):
            return self.getToken(wizardParser.Modulo, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimesDivideModulo" ):
                listener.enterTimesDivideModulo(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimesDivideModulo" ):
                listener.exitTimesDivideModulo(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimesDivideModulo" ):
                return visitor.visitTimesDivideModulo(self)
            else:
                return visitor.visitChildren(self)


    class IndexContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def LeftBracket(self):
            return self.getToken(wizardParser.LeftBracket, 0)
        def RightBracket(self):
            return self.getToken(wizardParser.RightBracket, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndex" ):
                listener.enterIndex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndex" ):
                listener.exitIndex(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndex" ):
                return visitor.visitIndex(self)
            else:
                return visitor.visitChildren(self)


    class ExponentiationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def Raise(self):
            return self.getToken(wizardParser.Raise, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExponentiation" ):
                listener.enterExponentiation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExponentiation" ):
                listener.exitExponentiation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExponentiation" ):
                return visitor.visitExponentiation(self)
            else:
                return visitor.visitChildren(self)


    class PlusMinusContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def Plus(self):
            return self.getToken(wizardParser.Plus, 0)
        def Minus(self):
            return self.getToken(wizardParser.Minus, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlusMinus" ):
                listener.enterPlusMinus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlusMinus" ):
                listener.exitPlusMinus(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlusMinus" ):
                return visitor.visitPlusMinus(self)
            else:
                return visitor.visitChildren(self)


    class NotContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNot" ):
                listener.enterNot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNot" ):
                listener.exitNot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot" ):
                return visitor.visitNot(self)
            else:
                return visitor.visitChildren(self)


    class LesserContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def Lesser(self):
            return self.getToken(wizardParser.Lesser, 0)
        def LesserOrEqual(self):
            return self.getToken(wizardParser.LesserOrEqual, 0)
        def Colon(self):
            return self.getToken(wizardParser.Colon, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLesser" ):
                listener.enterLesser(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLesser" ):
                listener.exitLesser(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLesser" ):
                return visitor.visitLesser(self)
            else:
                return visitor.visitChildren(self)


    class NegativeContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Minus(self):
            return self.getToken(wizardParser.Minus, 0)
        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNegative" ):
                listener.enterNegative(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNegative" ):
                listener.exitNegative(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNegative" ):
                return visitor.visitNegative(self)
            else:
                return visitor.visitChildren(self)


    class EqualContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def Equal(self):
            return self.getToken(wizardParser.Equal, 0)
        def NotEqual(self):
            return self.getToken(wizardParser.NotEqual, 0)
        def Colon(self):
            return self.getToken(wizardParser.Colon, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqual" ):
                listener.enterEqual(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqual" ):
                listener.exitEqual(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqual" ):
                return visitor.visitEqual(self)
            else:
                return visitor.visitChildren(self)


    class AndContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd" ):
                listener.enterAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd" ):
                listener.exitAnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd" ):
                return visitor.visitAnd(self)
            else:
                return visitor.visitChildren(self)


    class SliceContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def LeftBracket(self):
            return self.getToken(wizardParser.LeftBracket, 0)
        def Colon(self, i:int=None):
            if i is None:
                return self.getTokens(wizardParser.Colon)
            else:
                return self.getToken(wizardParser.Colon, i)
        def RightBracket(self):
            return self.getToken(wizardParser.RightBracket, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSlice" ):
                listener.enterSlice(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSlice" ):
                listener.exitSlice(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSlice" ):
                return visitor.visitSlice(self)
            else:
                return visitor.visitChildren(self)


    class ValueContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def constant(self):
            return self.getTypedRuleContext(wizardParser.ConstantContext,0)

        def decimal(self):
            return self.getTypedRuleContext(wizardParser.DecimalContext,0)

        def integer(self):
            return self.getTypedRuleContext(wizardParser.IntegerContext,0)

        def string(self):
            return self.getTypedRuleContext(wizardParser.StringContext,0)

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)


    class GreaterContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(wizardParser.ExprContext)
            else:
                return self.getTypedRuleContext(wizardParser.ExprContext,i)

        def Greater(self):
            return self.getToken(wizardParser.Greater, 0)
        def GreaterOrEqual(self):
            return self.getToken(wizardParser.GreaterOrEqual, 0)
        def Colon(self):
            return self.getToken(wizardParser.Colon, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGreater" ):
                listener.enterGreater(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGreater" ):
                listener.exitGreater(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGreater" ):
                return visitor.visitGreater(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)
        def LeftParenthesis(self):
            return self.getToken(wizardParser.LeftParenthesis, 0)
        def argList(self):
            return self.getTypedRuleContext(wizardParser.ArgListContext,0)

        def RightParenthesis(self):
            return self.getToken(wizardParser.RightParenthesis, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)


    class PostIncrementContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)
        def Increment(self):
            return self.getToken(wizardParser.Increment, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostIncrement" ):
                listener.enterPostIncrement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostIncrement" ):
                listener.exitPostIncrement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostIncrement" ):
                return visitor.visitPostIncrement(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LeftParenthesis(self):
            return self.getToken(wizardParser.LeftParenthesis, 0)
        def expr(self):
            return self.getTypedRuleContext(wizardParser.ExprContext,0)

        def RightParenthesis(self):
            return self.getToken(wizardParser.RightParenthesis, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class PreDecrementContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a wizardParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def Decrement(self):
            return self.getToken(wizardParser.Decrement, 0)
        def Identifier(self):
            return self.getToken(wizardParser.Identifier, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreDecrement" ):
                listener.enterPreDecrement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreDecrement" ):
                listener.exitPreDecrement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPreDecrement" ):
                return visitor.visitPreDecrement(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = wizardParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 46
        self.enterRecursionRule(localctx, 46, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                localctx = wizardParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 210
                self.match(wizardParser.LeftParenthesis)
                self.state = 211
                self.expr(0)
                self.state = 212
                self.match(wizardParser.RightParenthesis)
                pass

            elif la_ == 2:
                localctx = wizardParser.FunctionCallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 214
                self.match(wizardParser.Identifier)
                self.state = 215
                self.match(wizardParser.LeftParenthesis)
                self.state = 216
                self.argList()
                self.state = 217
                self.match(wizardParser.RightParenthesis)
                pass

            elif la_ == 3:
                localctx = wizardParser.PreIncrementContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 219
                self.match(wizardParser.Increment)
                self.state = 220
                self.match(wizardParser.Identifier)
                pass

            elif la_ == 4:
                localctx = wizardParser.PostIncrementContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 221
                self.match(wizardParser.Identifier)
                self.state = 222
                self.match(wizardParser.Increment)
                pass

            elif la_ == 5:
                localctx = wizardParser.PreDecrementContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 223
                self.match(wizardParser.Decrement)
                self.state = 224
                self.match(wizardParser.Identifier)
                pass

            elif la_ == 6:
                localctx = wizardParser.PostDecrementContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 225
                self.match(wizardParser.Identifier)
                self.state = 226
                self.match(wizardParser.Decrement)
                pass

            elif la_ == 7:
                localctx = wizardParser.NegativeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 227
                self.match(wizardParser.Minus)
                self.state = 228
                self.expr(14)
                pass

            elif la_ == 8:
                localctx = wizardParser.NotContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 229
                _la = self._input.LA(1)
                if not(_la==wizardParser.T__11 or _la==wizardParser.T__12):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 230
                self.expr(13)
                pass

            elif la_ == 9:
                localctx = wizardParser.ValueContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 236
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
                if la_ == 1:
                    self.state = 231
                    self.constant()
                    pass

                elif la_ == 2:
                    self.state = 232
                    self.decimal()
                    pass

                elif la_ == 3:
                    self.state = 233
                    self.integer()
                    pass

                elif la_ == 4:
                    self.state = 234
                    self.string()
                    pass

                elif la_ == 5:
                    self.state = 235
                    self.match(wizardParser.Identifier)
                    pass


                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 309
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,29,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 307
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
                    if la_ == 1:
                        localctx = wizardParser.ExponentiationContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 240
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 241
                        self.match(wizardParser.Raise)
                        self.state = 242
                        self.expr(11)
                        pass

                    elif la_ == 2:
                        localctx = wizardParser.TimesDivideModuloContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 243
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 244
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << wizardParser.Divide) | (1 << wizardParser.Times) | (1 << wizardParser.Modulo))) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 245
                        self.expr(10)
                        pass

                    elif la_ == 3:
                        localctx = wizardParser.PlusMinusContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 246
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 247
                        _la = self._input.LA(1)
                        if not(_la==wizardParser.Minus or _la==wizardParser.Plus):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 248
                        self.expr(9)
                        pass

                    elif la_ == 4:
                        localctx = wizardParser.GreaterContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 249
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 250
                        _la = self._input.LA(1)
                        if not(_la==wizardParser.GreaterOrEqual or _la==wizardParser.Greater):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 252
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==wizardParser.Colon:
                            self.state = 251
                            self.match(wizardParser.Colon)


                        self.state = 254
                        self.expr(8)
                        pass

                    elif la_ == 5:
                        localctx = wizardParser.LesserContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 255
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 256
                        _la = self._input.LA(1)
                        if not(_la==wizardParser.LesserOrEqual or _la==wizardParser.Lesser):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 258
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==wizardParser.Colon:
                            self.state = 257
                            self.match(wizardParser.Colon)


                        self.state = 260
                        self.expr(7)
                        pass

                    elif la_ == 6:
                        localctx = wizardParser.EqualContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 261
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 262
                        _la = self._input.LA(1)
                        if not(_la==wizardParser.Equal or _la==wizardParser.NotEqual):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 264
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==wizardParser.Colon:
                            self.state = 263
                            self.match(wizardParser.Colon)


                        self.state = 266
                        self.expr(6)
                        pass

                    elif la_ == 7:
                        localctx = wizardParser.OrContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 267
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 268
                        _la = self._input.LA(1)
                        if not(_la==wizardParser.T__13 or _la==wizardParser.T__14):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 269
                        self.expr(5)
                        pass

                    elif la_ == 8:
                        localctx = wizardParser.AndContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 270
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 271
                        _la = self._input.LA(1)
                        if not(_la==wizardParser.T__15 or _la==wizardParser.T__16):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 272
                        self.expr(4)
                        pass

                    elif la_ == 9:
                        localctx = wizardParser.DotFunctionCallContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 273
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 274
                        self.match(wizardParser.Dot)
                        self.state = 275
                        self.match(wizardParser.Identifier)
                        self.state = 276
                        self.match(wizardParser.LeftParenthesis)
                        self.state = 277
                        self.argList()
                        self.state = 278
                        self.match(wizardParser.RightParenthesis)
                        pass

                    elif la_ == 10:
                        localctx = wizardParser.IndexContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 280
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 281
                        self.match(wizardParser.LeftBracket)
                        self.state = 282
                        self.expr(0)
                        self.state = 283
                        self.match(wizardParser.RightBracket)
                        pass

                    elif la_ == 11:
                        localctx = wizardParser.SliceContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 285
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 286
                        self.match(wizardParser.LeftBracket)
                        self.state = 288
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if ((((_la - 12)) & ~0x3f) == 0 and ((1 << (_la - 12)) & ((1 << (wizardParser.T__11 - 12)) | (1 << (wizardParser.T__12 - 12)) | (1 << (wizardParser.T__17 - 12)) | (1 << (wizardParser.T__18 - 12)) | (1 << (wizardParser.T__19 - 12)) | (1 << (wizardParser.LeftParenthesis - 12)) | (1 << (wizardParser.Number - 12)) | (1 << (wizardParser.DoubleQuotedString - 12)) | (1 << (wizardParser.SingleQuotedString - 12)) | (1 << (wizardParser.Minus - 12)) | (1 << (wizardParser.Decrement - 12)) | (1 << (wizardParser.Increment - 12)) | (1 << (wizardParser.Identifier - 12)))) != 0):
                            self.state = 287
                            self.expr(0)


                        self.state = 290
                        self.match(wizardParser.Colon)
                        self.state = 292
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if ((((_la - 12)) & ~0x3f) == 0 and ((1 << (_la - 12)) & ((1 << (wizardParser.T__11 - 12)) | (1 << (wizardParser.T__12 - 12)) | (1 << (wizardParser.T__17 - 12)) | (1 << (wizardParser.T__18 - 12)) | (1 << (wizardParser.T__19 - 12)) | (1 << (wizardParser.LeftParenthesis - 12)) | (1 << (wizardParser.Number - 12)) | (1 << (wizardParser.DoubleQuotedString - 12)) | (1 << (wizardParser.SingleQuotedString - 12)) | (1 << (wizardParser.Minus - 12)) | (1 << (wizardParser.Decrement - 12)) | (1 << (wizardParser.Increment - 12)) | (1 << (wizardParser.Identifier - 12)))) != 0):
                            self.state = 291
                            self.expr(0)


                        self.state = 298
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==wizardParser.Colon:
                            self.state = 294
                            self.match(wizardParser.Colon)
                            self.state = 296
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if ((((_la - 12)) & ~0x3f) == 0 and ((1 << (_la - 12)) & ((1 << (wizardParser.T__11 - 12)) | (1 << (wizardParser.T__12 - 12)) | (1 << (wizardParser.T__17 - 12)) | (1 << (wizardParser.T__18 - 12)) | (1 << (wizardParser.T__19 - 12)) | (1 << (wizardParser.LeftParenthesis - 12)) | (1 << (wizardParser.Number - 12)) | (1 << (wizardParser.DoubleQuotedString - 12)) | (1 << (wizardParser.SingleQuotedString - 12)) | (1 << (wizardParser.Minus - 12)) | (1 << (wizardParser.Decrement - 12)) | (1 << (wizardParser.Increment - 12)) | (1 << (wizardParser.Identifier - 12)))) != 0):
                                self.state = 295
                                self.expr(0)




                        self.state = 300
                        self.match(wizardParser.RightBracket)
                        pass

                    elif la_ == 12:
                        localctx = wizardParser.InContext(self, wizardParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 301
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 302
                        self.match(wizardParser.In)
                        self.state = 303
                        self.expr(0)
                        self.state = 305
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
                        if la_ == 1:
                            self.state = 304
                            self.match(wizardParser.Colon)


                        pass

             
                self.state = 311
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,29,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return wizardParser.RULE_constant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstant" ):
                listener.enterConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstant" ):
                listener.exitConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstant" ):
                return visitor.visitConstant(self)
            else:
                return visitor.visitChildren(self)




    def constant(self):

        localctx = wizardParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_constant)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 312
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << wizardParser.T__17) | (1 << wizardParser.T__18) | (1 << wizardParser.T__19))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self):
            return self.getToken(wizardParser.Number, 0)

        def getRuleIndex(self):
            return wizardParser.RULE_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger" ):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)




    def integer(self):

        localctx = wizardParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 314
            self.match(wizardParser.Number)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DecimalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self, i:int=None):
            if i is None:
                return self.getTokens(wizardParser.Number)
            else:
                return self.getToken(wizardParser.Number, i)

        def Dot(self):
            return self.getToken(wizardParser.Dot, 0)

        def getRuleIndex(self):
            return wizardParser.RULE_decimal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecimal" ):
                listener.enterDecimal(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecimal" ):
                listener.exitDecimal(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecimal" ):
                return visitor.visitDecimal(self)
            else:
                return visitor.visitChildren(self)




    def decimal(self):

        localctx = wizardParser.DecimalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_decimal)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self.match(wizardParser.Number)
            self.state = 317
            self.match(wizardParser.Dot)
            self.state = 318
            self.match(wizardParser.Number)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DoubleQuotedString(self):
            return self.getToken(wizardParser.DoubleQuotedString, 0)

        def SingleQuotedString(self):
            return self.getToken(wizardParser.SingleQuotedString, 0)

        def getRuleIndex(self):
            return wizardParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = wizardParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_string)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            _la = self._input.LA(1)
            if not(_la==wizardParser.DoubleQuotedString or _la==wizardParser.SingleQuotedString):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[23] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 2)
         




