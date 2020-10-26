# Generated from .\wizard.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .wizardParser import wizardParser
else:
    from wizardParser import wizardParser

# This class defines a complete generic visitor for a parse tree produced by wizardParser.

class wizardVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by wizardParser#parseWizard.
    def visitParseWizard(self, ctx:wizardParser.ParseWizardContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#body.
    def visitBody(self, ctx:wizardParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#stmt.
    def visitStmt(self, ctx:wizardParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#assignment.
    def visitAssignment(self, ctx:wizardParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#compoundAssignment.
    def visitCompoundAssignment(self, ctx:wizardParser.CompoundAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#controlFlowStmt.
    def visitControlFlowStmt(self, ctx:wizardParser.ControlFlowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#caseStmt.
    def visitCaseStmt(self, ctx:wizardParser.CaseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#defaultStmt.
    def visitDefaultStmt(self, ctx:wizardParser.DefaultStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#elifStmt.
    def visitElifStmt(self, ctx:wizardParser.ElifStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#elseStmt.
    def visitElseStmt(self, ctx:wizardParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#forStmt.
    def visitForStmt(self, ctx:wizardParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#forRangeLoop.
    def visitForRangeLoop(self, ctx:wizardParser.ForRangeLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#forInLoop.
    def visitForInLoop(self, ctx:wizardParser.ForInLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#ifStmt.
    def visitIfStmt(self, ctx:wizardParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#selectStmt.
    def visitSelectStmt(self, ctx:wizardParser.SelectStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#selectCaseList.
    def visitSelectCaseList(self, ctx:wizardParser.SelectCaseListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#optionTuple.
    def visitOptionTuple(self, ctx:wizardParser.OptionTupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#selectOne.
    def visitSelectOne(self, ctx:wizardParser.SelectOneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#selectMany.
    def visitSelectMany(self, ctx:wizardParser.SelectManyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#whileStmt.
    def visitWhileStmt(self, ctx:wizardParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#argList.
    def visitArgList(self, ctx:wizardParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#keywordStmt.
    def visitKeywordStmt(self, ctx:wizardParser.KeywordStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#TIMES_DIVIDE_MODULO.
    def visitTIMES_DIVIDE_MODULO(self, ctx:wizardParser.TIMES_DIVIDE_MODULOContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PLUS_MINUS.
    def visitPLUS_MINUS(self, ctx:wizardParser.PLUS_MINUSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#CONSTANTS.
    def visitCONSTANTS(self, ctx:wizardParser.CONSTANTSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#OR.
    def visitOR(self, ctx:wizardParser.ORContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#FUNCTION_CALL.
    def visitFUNCTION_CALL(self, ctx:wizardParser.FUNCTION_CALLContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#LESSER.
    def visitLESSER(self, ctx:wizardParser.LESSERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#IN.
    def visitIN(self, ctx:wizardParser.INContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#EQUAL.
    def visitEQUAL(self, ctx:wizardParser.EQUALContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#GREATER.
    def visitGREATER(self, ctx:wizardParser.GREATERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#POWER.
    def visitPOWER(self, ctx:wizardParser.POWERContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#INDEXING.
    def visitINDEXING(self, ctx:wizardParser.INDEXINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PRE_DECREMENT.
    def visitPRE_DECREMENT(self, ctx:wizardParser.PRE_DECREMENTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PRE_INCREMENT.
    def visitPRE_INCREMENT(self, ctx:wizardParser.PRE_INCREMENTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#MINUS.
    def visitMINUS(self, ctx:wizardParser.MINUSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#POST_INCREMENT.
    def visitPOST_INCREMENT(self, ctx:wizardParser.POST_INCREMENTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#NOT.
    def visitNOT(self, ctx:wizardParser.NOTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#METHOD_CALL.
    def visitMETHOD_CALL(self, ctx:wizardParser.METHOD_CALLContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PARENS.
    def visitPARENS(self, ctx:wizardParser.PARENSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#POST_DECREMENT.
    def visitPOST_DECREMENT(self, ctx:wizardParser.POST_DECREMENTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#VARIABLE.
    def visitVARIABLE(self, ctx:wizardParser.VARIABLEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#SLICING.
    def visitSLICING(self, ctx:wizardParser.SLICINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#AND.
    def visitAND(self, ctx:wizardParser.ANDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#constant.
    def visitConstant(self, ctx:wizardParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#integer.
    def visitInteger(self, ctx:wizardParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#decimal.
    def visitDecimal(self, ctx:wizardParser.DecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#string.
    def visitString(self, ctx:wizardParser.StringContext):
        return self.visitChildren(ctx)



del wizardParser