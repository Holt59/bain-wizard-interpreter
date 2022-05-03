# Generated from ./vendor/wizparse/wizards/wizard.g4 by ANTLR 4.10.1
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


    # Visit a parse tree produced by wizardParser#Break.
    def visitBreak(self, ctx:wizardParser.BreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Cancel.
    def visitCancel(self, ctx:wizardParser.CancelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Continue.
    def visitContinue(self, ctx:wizardParser.ContinueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#For.
    def visitFor(self, ctx:wizardParser.ForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#If.
    def visitIf(self, ctx:wizardParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Return.
    def visitReturn(self, ctx:wizardParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Select.
    def visitSelect(self, ctx:wizardParser.SelectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#While.
    def visitWhile(self, ctx:wizardParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#cancelStmt.
    def visitCancelStmt(self, ctx:wizardParser.CancelStmtContext):
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


    # Visit a parse tree produced by wizardParser#forRangeHeader.
    def visitForRangeHeader(self, ctx:wizardParser.ForRangeHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#forInHeader.
    def visitForInHeader(self, ctx:wizardParser.ForInHeaderContext):
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


    # Visit a parse tree produced by wizardParser#PreIncrement.
    def visitPreIncrement(self, ctx:wizardParser.PreIncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#DotFunctionCall.
    def visitDotFunctionCall(self, ctx:wizardParser.DotFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Or.
    def visitOr(self, ctx:wizardParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#In.
    def visitIn(self, ctx:wizardParser.InContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PostDecrement.
    def visitPostDecrement(self, ctx:wizardParser.PostDecrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#TimesDivideModulo.
    def visitTimesDivideModulo(self, ctx:wizardParser.TimesDivideModuloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Index.
    def visitIndex(self, ctx:wizardParser.IndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Exponentiation.
    def visitExponentiation(self, ctx:wizardParser.ExponentiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PlusMinus.
    def visitPlusMinus(self, ctx:wizardParser.PlusMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Not.
    def visitNot(self, ctx:wizardParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Lesser.
    def visitLesser(self, ctx:wizardParser.LesserContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Negative.
    def visitNegative(self, ctx:wizardParser.NegativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Equal.
    def visitEqual(self, ctx:wizardParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#And.
    def visitAnd(self, ctx:wizardParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Slice.
    def visitSlice(self, ctx:wizardParser.SliceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Value.
    def visitValue(self, ctx:wizardParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#Greater.
    def visitGreater(self, ctx:wizardParser.GreaterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#FunctionCall.
    def visitFunctionCall(self, ctx:wizardParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PostIncrement.
    def visitPostIncrement(self, ctx:wizardParser.PostIncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#ParenExpr.
    def visitParenExpr(self, ctx:wizardParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wizardParser#PreDecrement.
    def visitPreDecrement(self, ctx:wizardParser.PreDecrementContext):
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