# there are many issue with ANLTR4 typing in this code, so this is in a dedicated file
#
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

from antlr4.error.Errors import RecognitionException
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.IntervalSet import IntervalSet
from antlr4.Token import Token

from ..antlr4.wizardLexer import wizardLexer
from ..antlr4.wizardParser import wizardParser


class WizardErrorStrategy(DefaultErrorStrategy):
    """
    Custom error strategy that tries to recover for broken Wizard scripts.

    This class is inspired by DefaultErrorStrategy but is really experimental.
    Basically, it should recover by broken scripts by closing enclosing control
    block, e.g. if the body of a If is broken, we try to look for a Elif, Else
    or EndIf and skip everything in-between.
    """

    # "Block" contexts are context for which we need to consume the last token when
    # recovering to move to the next rule. This is basically the contexts for all the
    # rules that contains a EndXXX token at the end.
    BlockContexts = {
        wizardParser.IfStmtContext: wizardLexer.EndIf,
        wizardParser.ForStmtContext: wizardLexer.EndFor,
        wizardParser.SelectStmtContext: wizardLexer.EndSelect,
        wizardParser.WhileStmtContext: wizardLexer.EndWhile,
    }

    def recover(self, recognizer: wizardParser, e: RecognitionException) -> Token:
        # Mark the context (and "some" parent contexts):
        recognizer._ctx.exception = e

        # Try to do custom recovery using control-flow:
        controlRecoverSet = self.getControlRecoverySet(recognizer)
        index = recognizer._input.index  # type: ignore
        state = recognizer.state

        if controlRecoverSet.intervals:
            self.consumeUntil(recognizer, controlRecoverSet)  # type: ignore

        # Same state, nothing was done, fallback to parent:
        if recognizer.state == state and recognizer._input.index == index:
            super().recover(recognizer, e)
        else:
            # Something was consumed, but do we have to consume the next token
            # to close the statement? Yes if the current context if a "block"
            # context and the next context its close token:
            for tctx, tok in self.BlockContexts.items():
                if (
                    isinstance(recognizer._ctx, tctx)
                    and recognizer.getTokenStream().LA(1) == tok
                ):
                    recognizer.consume()
                    break

        return recognizer.getTokenStream().LT(1)

    def getControlRecoverySet(self, recognizer: wizardParser):
        ctx = recognizer._ctx
        recoverSet = IntervalSet()

        while ctx is not None and ctx.invokingState >= 0:
            # If statement (for Else we only want EndIf):
            if isinstance(
                ctx, (wizardParser.IfStmtContext, wizardParser.ElifStmtContext)
            ):
                recoverSet.addOne(wizardLexer.Elif)
                recoverSet.addOne(wizardLexer.Else)
                recoverSet.addOne(wizardLexer.EndIf)
            elif isinstance(ctx, wizardParser.ElseStmtContext):
                recoverSet.addOne(wizardLexer.EndIf)

            # For/While statement:
            elif isinstance(ctx, wizardParser.ForStmtContext):
                recoverSet.addOne(wizardLexer.EndFor)
            elif isinstance(ctx, wizardParser.WhileStmtContext):
                recoverSet.addOne(wizardLexer.EndWhile)

            # Case/Default context:
            elif isinstance(
                ctx,
                (wizardParser.CaseStmtContext, wizardParser.DefaultStmtContext),
            ):
                recoverSet.addOne(wizardLexer.Break)

            # Select context:
            elif isinstance(ctx, wizardParser.SelectStmtContext):
                recoverSet.addOne(wizardLexer.EndSelect)

            ctx = ctx.parentCtx
        recoverSet.removeOne(Token.EPSILON)

        return recoverSet
