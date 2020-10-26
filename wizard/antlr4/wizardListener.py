# Generated from .\wizard.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .wizardParser import wizardParser
else:
    from wizardParser import wizardParser

# This class defines a complete listener for a parse tree produced by wizardParser.
class wizardListener(ParseTreeListener):

    # Enter a parse tree produced by wizardParser#parseWizard.
    def enterParseWizard(self, ctx:wizardParser.ParseWizardContext):
        pass

    # Exit a parse tree produced by wizardParser#parseWizard.
    def exitParseWizard(self, ctx:wizardParser.ParseWizardContext):
        pass


    # Enter a parse tree produced by wizardParser#body.
    def enterBody(self, ctx:wizardParser.BodyContext):
        pass

    # Exit a parse tree produced by wizardParser#body.
    def exitBody(self, ctx:wizardParser.BodyContext):
        pass


    # Enter a parse tree produced by wizardParser#stmt.
    def enterStmt(self, ctx:wizardParser.StmtContext):
        pass

    # Exit a parse tree produced by wizardParser#stmt.
    def exitStmt(self, ctx:wizardParser.StmtContext):
        pass


    # Enter a parse tree produced by wizardParser#assignment.
    def enterAssignment(self, ctx:wizardParser.AssignmentContext):
        pass

    # Exit a parse tree produced by wizardParser#assignment.
    def exitAssignment(self, ctx:wizardParser.AssignmentContext):
        pass


    # Enter a parse tree produced by wizardParser#compoundAssignment.
    def enterCompoundAssignment(self, ctx:wizardParser.CompoundAssignmentContext):
        pass

    # Exit a parse tree produced by wizardParser#compoundAssignment.
    def exitCompoundAssignment(self, ctx:wizardParser.CompoundAssignmentContext):
        pass


    # Enter a parse tree produced by wizardParser#controlFlowStmt.
    def enterControlFlowStmt(self, ctx:wizardParser.ControlFlowStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#controlFlowStmt.
    def exitControlFlowStmt(self, ctx:wizardParser.ControlFlowStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#caseStmt.
    def enterCaseStmt(self, ctx:wizardParser.CaseStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#caseStmt.
    def exitCaseStmt(self, ctx:wizardParser.CaseStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#defaultStmt.
    def enterDefaultStmt(self, ctx:wizardParser.DefaultStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#defaultStmt.
    def exitDefaultStmt(self, ctx:wizardParser.DefaultStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#elifStmt.
    def enterElifStmt(self, ctx:wizardParser.ElifStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#elifStmt.
    def exitElifStmt(self, ctx:wizardParser.ElifStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#elseStmt.
    def enterElseStmt(self, ctx:wizardParser.ElseStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#elseStmt.
    def exitElseStmt(self, ctx:wizardParser.ElseStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#forStmt.
    def enterForStmt(self, ctx:wizardParser.ForStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#forStmt.
    def exitForStmt(self, ctx:wizardParser.ForStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#forRangeLoop.
    def enterForRangeLoop(self, ctx:wizardParser.ForRangeLoopContext):
        pass

    # Exit a parse tree produced by wizardParser#forRangeLoop.
    def exitForRangeLoop(self, ctx:wizardParser.ForRangeLoopContext):
        pass


    # Enter a parse tree produced by wizardParser#forInLoop.
    def enterForInLoop(self, ctx:wizardParser.ForInLoopContext):
        pass

    # Exit a parse tree produced by wizardParser#forInLoop.
    def exitForInLoop(self, ctx:wizardParser.ForInLoopContext):
        pass


    # Enter a parse tree produced by wizardParser#ifStmt.
    def enterIfStmt(self, ctx:wizardParser.IfStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#ifStmt.
    def exitIfStmt(self, ctx:wizardParser.IfStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#selectStmt.
    def enterSelectStmt(self, ctx:wizardParser.SelectStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#selectStmt.
    def exitSelectStmt(self, ctx:wizardParser.SelectStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#selectCaseList.
    def enterSelectCaseList(self, ctx:wizardParser.SelectCaseListContext):
        pass

    # Exit a parse tree produced by wizardParser#selectCaseList.
    def exitSelectCaseList(self, ctx:wizardParser.SelectCaseListContext):
        pass


    # Enter a parse tree produced by wizardParser#optionTuple.
    def enterOptionTuple(self, ctx:wizardParser.OptionTupleContext):
        pass

    # Exit a parse tree produced by wizardParser#optionTuple.
    def exitOptionTuple(self, ctx:wizardParser.OptionTupleContext):
        pass


    # Enter a parse tree produced by wizardParser#selectOne.
    def enterSelectOne(self, ctx:wizardParser.SelectOneContext):
        pass

    # Exit a parse tree produced by wizardParser#selectOne.
    def exitSelectOne(self, ctx:wizardParser.SelectOneContext):
        pass


    # Enter a parse tree produced by wizardParser#selectMany.
    def enterSelectMany(self, ctx:wizardParser.SelectManyContext):
        pass

    # Exit a parse tree produced by wizardParser#selectMany.
    def exitSelectMany(self, ctx:wizardParser.SelectManyContext):
        pass


    # Enter a parse tree produced by wizardParser#whileStmt.
    def enterWhileStmt(self, ctx:wizardParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#whileStmt.
    def exitWhileStmt(self, ctx:wizardParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#argList.
    def enterArgList(self, ctx:wizardParser.ArgListContext):
        pass

    # Exit a parse tree produced by wizardParser#argList.
    def exitArgList(self, ctx:wizardParser.ArgListContext):
        pass


    # Enter a parse tree produced by wizardParser#keywordStmt.
    def enterKeywordStmt(self, ctx:wizardParser.KeywordStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#keywordStmt.
    def exitKeywordStmt(self, ctx:wizardParser.KeywordStmtContext):
        pass


    # Enter a parse tree produced by wizardParser#TIMES_DIVIDE_MODULO.
    def enterTIMES_DIVIDE_MODULO(self, ctx:wizardParser.TIMES_DIVIDE_MODULOContext):
        pass

    # Exit a parse tree produced by wizardParser#TIMES_DIVIDE_MODULO.
    def exitTIMES_DIVIDE_MODULO(self, ctx:wizardParser.TIMES_DIVIDE_MODULOContext):
        pass


    # Enter a parse tree produced by wizardParser#PLUS_MINUS.
    def enterPLUS_MINUS(self, ctx:wizardParser.PLUS_MINUSContext):
        pass

    # Exit a parse tree produced by wizardParser#PLUS_MINUS.
    def exitPLUS_MINUS(self, ctx:wizardParser.PLUS_MINUSContext):
        pass


    # Enter a parse tree produced by wizardParser#CONSTANTS.
    def enterCONSTANTS(self, ctx:wizardParser.CONSTANTSContext):
        pass

    # Exit a parse tree produced by wizardParser#CONSTANTS.
    def exitCONSTANTS(self, ctx:wizardParser.CONSTANTSContext):
        pass


    # Enter a parse tree produced by wizardParser#OR.
    def enterOR(self, ctx:wizardParser.ORContext):
        pass

    # Exit a parse tree produced by wizardParser#OR.
    def exitOR(self, ctx:wizardParser.ORContext):
        pass


    # Enter a parse tree produced by wizardParser#FUNCTION_CALL.
    def enterFUNCTION_CALL(self, ctx:wizardParser.FUNCTION_CALLContext):
        pass

    # Exit a parse tree produced by wizardParser#FUNCTION_CALL.
    def exitFUNCTION_CALL(self, ctx:wizardParser.FUNCTION_CALLContext):
        pass


    # Enter a parse tree produced by wizardParser#LESSER.
    def enterLESSER(self, ctx:wizardParser.LESSERContext):
        pass

    # Exit a parse tree produced by wizardParser#LESSER.
    def exitLESSER(self, ctx:wizardParser.LESSERContext):
        pass


    # Enter a parse tree produced by wizardParser#IN.
    def enterIN(self, ctx:wizardParser.INContext):
        pass

    # Exit a parse tree produced by wizardParser#IN.
    def exitIN(self, ctx:wizardParser.INContext):
        pass


    # Enter a parse tree produced by wizardParser#EQUAL.
    def enterEQUAL(self, ctx:wizardParser.EQUALContext):
        pass

    # Exit a parse tree produced by wizardParser#EQUAL.
    def exitEQUAL(self, ctx:wizardParser.EQUALContext):
        pass


    # Enter a parse tree produced by wizardParser#GREATER.
    def enterGREATER(self, ctx:wizardParser.GREATERContext):
        pass

    # Exit a parse tree produced by wizardParser#GREATER.
    def exitGREATER(self, ctx:wizardParser.GREATERContext):
        pass


    # Enter a parse tree produced by wizardParser#POWER.
    def enterPOWER(self, ctx:wizardParser.POWERContext):
        pass

    # Exit a parse tree produced by wizardParser#POWER.
    def exitPOWER(self, ctx:wizardParser.POWERContext):
        pass


    # Enter a parse tree produced by wizardParser#INDEXING.
    def enterINDEXING(self, ctx:wizardParser.INDEXINGContext):
        pass

    # Exit a parse tree produced by wizardParser#INDEXING.
    def exitINDEXING(self, ctx:wizardParser.INDEXINGContext):
        pass


    # Enter a parse tree produced by wizardParser#PRE_DECREMENT.
    def enterPRE_DECREMENT(self, ctx:wizardParser.PRE_DECREMENTContext):
        pass

    # Exit a parse tree produced by wizardParser#PRE_DECREMENT.
    def exitPRE_DECREMENT(self, ctx:wizardParser.PRE_DECREMENTContext):
        pass


    # Enter a parse tree produced by wizardParser#PRE_INCREMENT.
    def enterPRE_INCREMENT(self, ctx:wizardParser.PRE_INCREMENTContext):
        pass

    # Exit a parse tree produced by wizardParser#PRE_INCREMENT.
    def exitPRE_INCREMENT(self, ctx:wizardParser.PRE_INCREMENTContext):
        pass


    # Enter a parse tree produced by wizardParser#MINUS.
    def enterMINUS(self, ctx:wizardParser.MINUSContext):
        pass

    # Exit a parse tree produced by wizardParser#MINUS.
    def exitMINUS(self, ctx:wizardParser.MINUSContext):
        pass


    # Enter a parse tree produced by wizardParser#POST_INCREMENT.
    def enterPOST_INCREMENT(self, ctx:wizardParser.POST_INCREMENTContext):
        pass

    # Exit a parse tree produced by wizardParser#POST_INCREMENT.
    def exitPOST_INCREMENT(self, ctx:wizardParser.POST_INCREMENTContext):
        pass


    # Enter a parse tree produced by wizardParser#NOT.
    def enterNOT(self, ctx:wizardParser.NOTContext):
        pass

    # Exit a parse tree produced by wizardParser#NOT.
    def exitNOT(self, ctx:wizardParser.NOTContext):
        pass


    # Enter a parse tree produced by wizardParser#METHOD_CALL.
    def enterMETHOD_CALL(self, ctx:wizardParser.METHOD_CALLContext):
        pass

    # Exit a parse tree produced by wizardParser#METHOD_CALL.
    def exitMETHOD_CALL(self, ctx:wizardParser.METHOD_CALLContext):
        pass


    # Enter a parse tree produced by wizardParser#PARENS.
    def enterPARENS(self, ctx:wizardParser.PARENSContext):
        pass

    # Exit a parse tree produced by wizardParser#PARENS.
    def exitPARENS(self, ctx:wizardParser.PARENSContext):
        pass


    # Enter a parse tree produced by wizardParser#POST_DECREMENT.
    def enterPOST_DECREMENT(self, ctx:wizardParser.POST_DECREMENTContext):
        pass

    # Exit a parse tree produced by wizardParser#POST_DECREMENT.
    def exitPOST_DECREMENT(self, ctx:wizardParser.POST_DECREMENTContext):
        pass


    # Enter a parse tree produced by wizardParser#VARIABLE.
    def enterVARIABLE(self, ctx:wizardParser.VARIABLEContext):
        pass

    # Exit a parse tree produced by wizardParser#VARIABLE.
    def exitVARIABLE(self, ctx:wizardParser.VARIABLEContext):
        pass


    # Enter a parse tree produced by wizardParser#SLICING.
    def enterSLICING(self, ctx:wizardParser.SLICINGContext):
        pass

    # Exit a parse tree produced by wizardParser#SLICING.
    def exitSLICING(self, ctx:wizardParser.SLICINGContext):
        pass


    # Enter a parse tree produced by wizardParser#AND.
    def enterAND(self, ctx:wizardParser.ANDContext):
        pass

    # Exit a parse tree produced by wizardParser#AND.
    def exitAND(self, ctx:wizardParser.ANDContext):
        pass


    # Enter a parse tree produced by wizardParser#constant.
    def enterConstant(self, ctx:wizardParser.ConstantContext):
        pass

    # Exit a parse tree produced by wizardParser#constant.
    def exitConstant(self, ctx:wizardParser.ConstantContext):
        pass


    # Enter a parse tree produced by wizardParser#integer.
    def enterInteger(self, ctx:wizardParser.IntegerContext):
        pass

    # Exit a parse tree produced by wizardParser#integer.
    def exitInteger(self, ctx:wizardParser.IntegerContext):
        pass


    # Enter a parse tree produced by wizardParser#decimal.
    def enterDecimal(self, ctx:wizardParser.DecimalContext):
        pass

    # Exit a parse tree produced by wizardParser#decimal.
    def exitDecimal(self, ctx:wizardParser.DecimalContext):
        pass


    # Enter a parse tree produced by wizardParser#string.
    def enterString(self, ctx:wizardParser.StringContext):
        pass

    # Exit a parse tree produced by wizardParser#string.
    def exitString(self, ctx:wizardParser.StringContext):
        pass



del wizardParser