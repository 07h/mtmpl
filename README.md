
# Template Engine: `μtmpl` 

`μtmpl` is a simple template engine inspired by Jinja, supporting variable insertion, conditions, and loops.

## Key Features

1. **Variable Insertion**: `{{ variable }}`
2. **Conditional Statements**:
    ```jinja
    {% if condition %}
        ...
    {% elif other_condition %}
        ...
    {% else %}
        ...
    {% endif %}
    ```
3. **Loops**:
    ```jinja
    {% for item in iterable %}
        ...
    {% endfor %}
    ```

## Explanation of the Code

1. **Classes and Methods**:
    - **`Mtmpl`**: The main class of the templating engine.
    - **`render(template, context)`**: The primary method to render the template with the provided context.
    - **`_tokenize(template)`**: Breaks down the template into tokens (text, variables, and tags).
    - **`_render_tokens(tokens, context)`**: Processes the list of tokens and generates the rendered text.
    - **`_find_else_or_endif(tokens, start)`**: Finds the next `{% else %}` or `{% endif %}` tag.
    - **`_find_endif(tokens, start)`**: Finds the next `{% endif %}` tag.
    - **`_parse_for_args(args)`**: Parses the arguments of a `for` tag.
    - **`_evaluate_expression(expression, context)`**: Evaluates an expression within the given context.

2. **Regular Expressions**:
    - **`VARIABLE_PATTERN`**: Detects variables in the format `{{ variable }}`.
    - **`TAG_PATTERN`**: Detects tags in the format `{% tag_name args %}`.

3. **Handling Tags**:
    - **Conditions**: Supports `{% if %}`, `{% elif %}`, `{% else %}`, `{% endif %}`.
    - **Loops**: Supports `{% for var in iterable %}`, `{% endfor %}`.

4. **Variable Insertion**: Replaces `{{ variable }}` with the corresponding value from the context.

5. **Error Handling**: Raises exceptions for incorrect syntax or errors during expression evaluation.

## Example Usage

```python
if __name__ == "__main__":
    template = """
    <h1>{{ title }}</h1>

    {% if user %}
        <p>Hello, {{ user.name }}!</p>
    {% else %}
        <p>Hello, Guest!</p>
    {% endif %}

    <h2>Product List:</h2>
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
    """

    context = {
        'title': 'Welcome',
        'user': {
            'name': 'Alexey'
        },
        'items': ['Product 1', 'Product 2', 'Product 3']
    }

    template_engine = Mtmpl()
    rendered = template_engine.render(template, context)
    print(rendered)
```

## Output

```html
<h1>Welcome</h1>

    <p>Hello, Alexey!</p>

<h2>Product List:</h2>
<ul>

        <li>Product 1</li>

        <li>Product 2</li>

        <li>Product 3</li>

</ul>
```

## Additional Notes

- **Security Considerations**: This templating engine uses `eval` to evaluate expressions, which can be a security risk if templates or contexts come from untrusted sources. To enhance security, consider restricting the allowed expressions or using a safer evaluation method.

- **Extensibility**: While `Mtmpl` provides basic templating functionalities, it can be extended to support additional features like filters, custom tags, or more complex expressions as needed.

- **Performance**: For small to medium-sized projects, `Mtmpl` performs adequately. However, for larger projects with complex templating needs, established libraries like Jinja2 are recommended for better performance and feature sets.

## Conclusion

The `Mtmpl` class offers a straightforward and efficient way to perform templating in Python, supporting essential features like variable insertion, conditionals, and loops. Its simplicity makes it easy to integrate and use in various projects without the overhead of additional dependencies or complexities.

If you have any further questions or need assistance with extending the templating engine, feel free to ask!