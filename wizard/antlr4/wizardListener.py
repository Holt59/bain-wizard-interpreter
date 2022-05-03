# Generated from ./vendor/wizparse/wizards/wizard.g4 by ANTLR 4.10.1
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


    # Enter a parse tree produced by wizardParser#Break.
    def enterBreak(self, ctx:wizardParser.BreakContext):
        pass

    # Exit a parse tree produced by wizardParser#Break.
    def exitBreak(self, ctx:wizardParser.BreakContext):
        pass


    # Enter a parse tree produced by wizardParser#Cancel.
    def enterCancel(self, ctx:wizardParser.CancelContext):
        pass

    # Exit a parse tree produced by wizardParser#Cancel.
    def exitCancel(self, ctx:wizardParser.CancelContext):
        pass


    # Enter a parse tree produced by wizardParser#Continue.
    def enterContinue(self, ctx:wizardParser.ContinueContext):
        pass

    # Exit a parse tree produced by wizardParser#Continue.
    def exitContinue(self, ctx:wizardParser.ContinueContext):
        pass


    # Enter a parse tree produced by wizardParser#For.
    def enterFor(self, ctx:wizardParser.ForContext):
        pass

    # Exit a parse tree produced by wizardParser#For.
    def exitFor(self, ctx:wizardParser.ForContext):
        pass


    # Enter a parse tree produced by wizardParser#If.
    def enterIf(self, ctx:wizardParser.IfContext):
        pass

    # Exit a parse tree produced by wizardParser#If.
    def exitIf(self, ctx:wizardParser.IfContext):
        pass


    # Enter a parse tree produced by wizardParser#Return.
    def enterReturn(self, ctx:wizardParser.ReturnContext):
        pass

    # Exit a parse tree produced by wizardParser#Return.
    def exitReturn(self, ctx:wizardParser.ReturnContext):
        pass


    # Enter a parse tree produced by wizardParser#Select.
    def enterSelect(self, ctx:wizardParser.SelectContext):
        pass

    # Exit a parse tree produced by wizardParser#Select.
    def exitSelect(self, ctx:wizardParser.SelectContext):
        pass


    # Enter a parse tree produced by wizardParser#While.
    def enterWhile(self, ctx:wizardParser.WhileContext):
        pass

    # Exit a parse tree produced by wizardParser#While.
    def exitWhile(self, ctx:wizardParser.WhileContext):
        pass


    # Enter a parse tree produced by wizardParser#cancelStmt.
    def enterCancelStmt(self, ctx:wizardParser.CancelStmtContext):
        pass

    # Exit a parse tree produced by wizardParser#cancelStmt.
    def exitCancelStmt(self, ctx:wizardParser.CancelStmtContext):
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


    # Enter a parse tree produced by wizardParser#forRangeHeader.
    def enterForRangeHeader(self, ctx:wizardParser.ForRangeHeaderContext):
        pass

    # Exit a parse tree produced by wizardParser#forRangeHeader.
    def exitForRangeHeader(self, ctx:wizardParser.ForRangeHeaderContext):
        pass


    # Enter a parse tree produced by wizardParser#forInHeader.
    def enterForInHeader(self, ctx:wizardParser.ForInHeaderContext):
        pass

    # Exit a parse tree produced by wizardParser#forInHeader.
    def exitForInHeader(self, ctx:wizardParser.ForInHeaderContext):
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


    # Enter a parse tree produced by wizardParser#PreIncrement.
    def enterPreIncrement(self, ctx:wizardParser.PreIncrementContext):
        pass

    # Exit a parse tree produced by wizardParser#PreIncrement.
    def exitPreIncrement(self, ctx:wizardParser.PreIncrementContext):
        pass


    # Enter a parse tree produced by wizardParser#DotFunctionCall.
    def enterDotFunctionCall(self, ctx:wizardParser.DotFunctionCallContext):
        pass

    # Exit a parse tree produced by wizardParser#DotFunctionCall.
    def exitDotFunctionCall(self, ctx:wizardParser.DotFunctionCallContext):
        pass


    # Enter a parse tree produced by wizardParser#Or.
    def enterOr(self, ctx:wizardParser.OrContext):
        pass

    # Exit a parse tree produced by wizardParser#Or.
    def exitOr(self, ctx:wizardParser.OrContext):
        pass


    # Enter a parse tree produced by wizardParser#In.
    def enterIn(self, ctx:wizardParser.InContext):
        pass

    # Exit a parse tree produced by wizardParser#In.
    def exitIn(self, ctx:wizardParser.InContext):
        pass


    # Enter a parse tree produced by wizardParser#PostDecrement.
    def enterPostDecrement(self, ctx:wizardParser.PostDecrementContext):
        pass

    # Exit a parse tree produced by wizardParser#PostDecrement.
    def exitPostDecrement(self, ctx:wizardParser.PostDecrementContext):
        pass


    # Enter a parse tree produced by wizardParser#TimesDivideModulo.
    def enterTimesDivideModulo(self, ctx:wizardParser.TimesDivideModuloContext):
        pass

    # Exit a parse tree produced by wizardParser#TimesDivideModulo.
    def exitTimesDivideModulo(self, ctx:wizardParser.TimesDivideModuloContext):
        pass


    # Enter a parse tree produced by wizardParser#Index.
    def enterIndex(self, ctx:wizardParser.IndexContext):
        pass

    # Exit a parse tree produced by wizardParser#Index.
    def exitIndex(self, ctx:wizardParser.IndexContext):
        pass


    # Enter a parse tree produced by wizardParser#Exponentiation.
    def enterExponentiation(self, ctx:wizardParser.ExponentiationContext):
        pass

    # Exit a parse tree produced by wizardParser#Exponentiation.
    def exitExponentiation(self, ctx:wizardParser.ExponentiationContext):
        pass


    # Enter a parse tree produced by wizardParser#PlusMinus.
    def enterPlusMinus(self, ctx:wizardParser.PlusMinusContext):
        pass

    # Exit a parse tree produced by wizardParser#PlusMinus.
    def exitPlusMinus(self, ctx:wizardParser.PlusMinusContext):
        pass


    # Enter a parse tree produced by wizardParser#Not.
    def enterNot(self, ctx:wizardParser.NotContext):
        pass

    # Exit a parse tree produced by wizardParser#Not.
    def exitNot(self, ctx:wizardParser.NotContext):
        pass


    # Enter a parse tree produced by wizardParser#Lesser.
    def enterLesser(self, ctx:wizardParser.LesserContext):
        pass

    # Exit a parse tree produced by wizardParser#Lesser.
    def exitLesser(self, ctx:wizardParser.LesserContext):
        pass


    # Enter a parse tree produced by wizardParser#Negative.
    def enterNegative(self, ctx:wizardParser.NegativeContext):
        pass

    # Exit a parse tree produced by wizardParser#Negative.
    def exitNegative(self, ctx:wizardParser.NegativeContext):
        pass


    # Enter a parse tree produced by wizardParser#Equal.
    def enterEqual(self, ctx:wizardParser.EqualContext):
        pass

    # Exit a parse tree produced by wizardParser#Equal.
    def exitEqual(self, ctx:wizardParser.EqualContext):
        pass


    # Enter a parse tree produced by wizardParser#And.
    def enterAnd(self, ctx:wizardParser.AndContext):
        pass

    # Exit a parse tree produced by wizardParser#And.
    def exitAnd(self, ctx:wizardParser.AndContext):
        pass


    # Enter a parse tree produced by wizardParser#Slice.
    def enterSlice(self, ctx:wizardParser.SliceContext):
        pass

    # Exit a parse tree produced by wizardParser#Slice.
    def exitSlice(self, ctx:wizardParser.SliceContext):
        pass


    # Enter a parse tree produced by wizardParser#Value.
    def enterValue(self, ctx:wizardParser.ValueContext):
        pass

    # Exit a parse tree produced by wizardParser#Value.
    def exitValue(self, ctx:wizardParser.ValueContext):
        pass


    # Enter a parse tree produced by wizardParser#Greater.
    def enterGreater(self, ctx:wizardParser.GreaterContext):
        pass

    # Exit a parse tree produced by wizardParser#Greater.
    def exitGreater(self, ctx:wizardParser.GreaterContext):
        pass


    # Enter a parse tree produced by wizardParser#FunctionCall.
    def enterFunctionCall(self, ctx:wizardParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by wizardParser#FunctionCall.
    def exitFunctionCall(self, ctx:wizardParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by wizardParser#PostIncrement.
    def enterPostIncrement(self, ctx:wizardParser.PostIncrementContext):
        pass

    # Exit a parse tree produced by wizardParser#PostIncrement.
    def exitPostIncrement(self, ctx:wizardParser.PostIncrementContext):
        pass


    # Enter a parse tree produced by wizardParser#ParenExpr.
    def enterParenExpr(self, ctx:wizardParser.ParenExprContext):
        pass

    # Exit a parse tree produced by wizardParser#ParenExpr.
    def exitParenExpr(self, ctx:wizardParser.ParenExprContext):
        pass


    # Enter a parse tree produced by wizardParser#PreDecrement.
    def enterPreDecrement(self, ctx:wizardParser.PreDecrementContext):
        pass

    # Exit a parse tree produced by wizardParser#PreDecrement.
    def exitPreDecrement(self, ctx:wizardParser.PreDecrementContext):
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