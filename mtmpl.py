# mtmpl/mtmpl.py

import re
from typing import Any, Dict, List, Tuple


class AttrDict(dict):
    """A dictionary that supports attribute-style access."""

    def __getattr__(self, key):
        try:
            value = self[key]
            # Recursively convert nested dictionaries to AttrDict
            if isinstance(value, dict):
                return AttrDict(value)
            elif isinstance(value, list):
                return [
                    AttrDict(item) if isinstance(item, dict) else item for item in value
                ]
            return value
        except KeyError:
            raise AttributeError(f"No such attribute: {key}")

    def __setattr__(self, key, value):
        self[key] = value


class Mtmpl:
    # Regular expressions to identify variables and tags
    VARIABLE_PATTERN = re.compile(r"{{\s*(.*?)\s*}}")
    TAG_PATTERN = re.compile(r"{%\s*(\w+)(.*?)\s*%}")

    def render(self, template: str, context: Dict[str, Any]) -> str:
        """
        Renders the template using the provided context.
        """
        tokens = self._tokenize(template)
        # Convert context to AttrDict for attribute-style access
        context_copy = self._convert_to_attrdict(context)
        rendered = self._render_tokens(tokens, context_copy)
        return rendered

    def _convert_to_attrdict(self, obj: Any) -> Any:
        """
        Recursively converts dictionaries in the context to AttrDict instances.
        """
        if isinstance(obj, dict):
            return AttrDict({k: self._convert_to_attrdict(v) for k, v in obj.items()})
        elif isinstance(obj, list):
            return [self._convert_to_attrdict(item) for item in obj]
        else:
            return obj

    def _tokenize(self, template: str) -> List[Tuple]:
        """
        Splits the template into tokens: text, variables, and tags.
        """
        token_specification = [
            ("VAR", self.VARIABLE_PATTERN),
            ("TAG", self.TAG_PATTERN),
            ("TEXT", re.compile(r"(.+?)(?=(?:{{|{%))", re.DOTALL)),
            ("TEXT_REST", re.compile(r"(.+)", re.DOTALL)),
        ]

        pos = 0
        tokens = []
        while pos < len(template):
            for tok_type, pattern in token_specification:
                match = pattern.match(template, pos)
                if match:
                    if tok_type == "VAR":
                        tokens.append(("VAR", match.group(1).strip()))
                    elif tok_type == "TAG":
                        tag_name = match.group(1).strip()
                        tag_args = match.group(2).strip()
                        tokens.append(("TAG", tag_name, tag_args))
                    elif tok_type in ("TEXT", "TEXT_REST"):
                        tokens.append(("TEXT", match.group(1)))
                    pos = match.end()
                    break
            else:
                # If no pattern matches, add the remaining text as TEXT
                tokens.append(("TEXT", template[pos:]))
                break
        return tokens

    def _render_tokens(self, tokens: List[Tuple], context: Dict[str, Any]) -> str:
        """
        Processes the list of tokens and returns the rendered text.
        """
        output = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token[0] == "TEXT":
                output.append(token[1])
            elif token[0] == "VAR":
                value = self._evaluate_expression(token[1], context)
                output.append(str(value))
            elif token[0] == "TAG":
                tag_name = token[1]
                tag_args = token[2]
                if tag_name == "if":
                    # Handle if condition
                    condition = self._evaluate_expression(tag_args, context)
                    # Find the block for if, considering nested ifs and fors
                    end_if, blocks = self._find_block(tokens, i + 1, "if")
                    if condition:
                        # Render the if block
                        output.append(self._render_tokens(blocks["if"], context))
                    else:
                        handled = False
                        for elif_cond, elif_block in blocks.get("elif", []):
                            if self._evaluate_expression(elif_cond, context):
                                output.append(self._render_tokens(elif_block, context))
                                handled = True
                                break
                        if not handled and "else" in blocks:
                            output.append(self._render_tokens(blocks["else"], context))
                    i = end_if
                elif tag_name == "for":
                    # Handle for loop
                    var, iterable = self._parse_for_args(tag_args)
                    iterable_value = self._evaluate_expression(iterable, context)
                    if not isinstance(iterable_value, list):
                        iterable_value = list(iterable_value)
                    # Find the endfor, considering nested fors and ifs
                    end_for, loop_body = self._find_block(tokens, i + 1, "for")
                    for item in iterable_value:
                        # Update context with the loop variable
                        context[var] = item
                        # Render loop body
                        output.append(self._render_tokens(loop_body, context))
                    # Safely remove loop variable from context
                    context.pop(var, None)
                    i = end_for
                else:
                    raise SyntaxError(f"Unknown tag: {tag_name}")
            i += 1

        return "".join(output)

    def _find_block(
        self, tokens: List[Tuple], start: int, block_type: str
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Finds the end of a block (if or for) considering nested blocks.
        Returns the index after the closing tag and a dictionary of blocks.
        For 'if', it includes 'if', 'elif', and 'else' blocks.
        For 'for', it includes only the loop body.
        """
        end = start
        blocks = {}
        current = block_type
        nested = 0

        if block_type == "if":
            blocks["if"] = []
            blocks["elif"] = []
            blocks["else"] = []
        elif block_type == "for":
            blocks["for"] = []

        while end < len(tokens):
            token = tokens[end]
            if token[0] == "TAG":
                tag_name = token[1]
                tag_args = token[2]
                if tag_name == block_type:
                    nested += 1
                    if block_type == "if":
                        blocks["if"].append(token)
                    elif block_type == "for":
                        blocks["for"].append(token)
                elif tag_name == f"end{block_type}":
                    if nested == 0:
                        break
                    else:
                        nested -= 1
                        if block_type == "if":
                            blocks["if"].append(token)
                        elif block_type == "for":
                            blocks["for"].append(token)
                elif block_type == "if" and tag_name == "elif" and nested == 0:
                    # Start collecting elif blocks
                    elif_cond = tag_args
                    blocks["elif"].append((elif_cond, []))
                    current = "elif"
                elif block_type == "if" and tag_name == "else" and nested == 0:
                    # Start collecting else block
                    blocks["else"] = []
                    current = "else"
                else:
                    if block_type == "if":
                        if current == "if":
                            blocks["if"].append(token)
                        elif current == "elif":
                            blocks["elif"][-1][1].append(token)
                        elif current == "else":
                            blocks["else"].append(token)
                    elif block_type == "for":
                        blocks["for"].append(token)
            else:
                if block_type == "if":
                    if current == "if":
                        blocks["if"].append(token)
                    elif current == "elif":
                        blocks["elif"][-1][1].append(token)
                    elif current == "else":
                        blocks["else"].append(token)
                elif block_type == "for":
                    blocks["for"].append(token)
            end += 1

        if end >= len(tokens):
            raise SyntaxError(f"Missing {{% end{block_type} %}}")

        if block_type == "if":
            return end, blocks
        elif block_type == "for":
            return end, blocks["for"]

    def _parse_for_args(self, args: str) -> Tuple[str, str]:
        """
        Parses the arguments of a for tag.
        Example: "item in items" -> ("item", "items")
        """
        parts = args.split(" in ")
        if len(parts) != 2:
            raise SyntaxError("Invalid syntax in 'for' tag")
        var = parts[0].strip()
        iterable = parts[1].strip()
        return var, iterable

    def _evaluate_expression(self, expression: str, context: Dict[str, Any]) -> Any:
        """
        Evaluates an expression within the given context.
        """
        try:
            return eval(expression, {}, context)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expression}': {e}")
