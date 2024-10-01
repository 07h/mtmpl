# tests/test_mtmpl.py

import unittest
import textwrap
from mtmpl import Mtmpl


class TestMtmpl(unittest.TestCase):
    def setUp(self):
        self.template_engine = Mtmpl()

    def test_variable_insertion(self):
        template = "Hello, {{ name }}!"
        context = {"name": "Alice"}
        expected = "Hello, Alice!"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_if_condition_true(self):
        template = "{% if user %}Hello, {{ user }}!{% endif %}"
        context = {"user": "Bob"}
        expected = "Hello, Bob!"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_if_condition_false(self):
        template = "{% if user %}Hello, {{ user }}!{% endif %}"
        context = {"user": None}
        expected = ""
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_if_else_true(self):
        template = "{% if user %}Hello, {{ user }}!{% else %}Hello, Guest!{% endif %}"
        context = {"user": "Carol"}
        expected = "Hello, Carol!"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_if_else_false(self):
        template = "{% if user %}Hello, {{ user }}!{% else %}Hello, Guest!{% endif %}"
        context = {"user": None}
        expected = "Hello, Guest!"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_if_elif_else(self):
        template = "{% if score >= 90 %}A{% elif score >= 80 %}B{% else %}C{% endif %}"
        context = {"score": 85}
        expected = "B"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

        context = {"score": 75}
        expected = "C"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_for_loop(self):
        template = "<ul>{% for item in items %}<li>{{ item }}</li>{% endfor %}</ul>"
        context = {"items": ["Apple", "Banana", "Cherry"]}
        expected = "<ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_for_loop_empty(self):
        template = "<ul>{% for item in items %}<li>{{ item }}</li>{% endfor %}</ul>"
        context = {"items": []}
        expected = "<ul></ul>"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_nested_if_in_for(self):
        template = textwrap.dedent(
            """
            <ul>
            {% for user in users %}
                {% if user.active %}
                    <li>{{ user.name }} (Active)</li>
                {% else %}
                    <li>{{ user.name }} (Inactive)</li>
                {% endif %}
            {% endfor %}
            </ul>
        """
        )
        context = {
            "users": [
                {"name": "Alice", "active": True},
                {"name": "Bob", "active": False},
                {"name": "Charlie", "active": True},
            ]
        }
        expected = textwrap.dedent(
            """
            <ul>
        
                    <li>Alice (Active)</li>
        
                    <li>Bob (Inactive)</li>
        
                    <li>Charlie (Active)</li>
        
            </ul>
        """
        )
        result = self.template_engine.render(template, context)
        # Normalize whitespace for comparison
        self.assertEqual(result.strip(), expected.strip())

    def test_unmatched_if(self):
        template = "{% if user %}Hello, {{ user }}!"
        context = {"user": "Dave"}
        with self.assertRaises(SyntaxError):
            self.template_engine.render(template, context)

    def test_unmatched_for(self):
        template = "{% for item in items %}{{ item }}"
        context = {"items": ["A", "B"]}
        with self.assertRaises(SyntaxError):
            self.template_engine.render(template, context)

    def test_invalid_expression(self):
        template = "Result: {{ 1 / 0 }}"
        context = {}
        with self.assertRaises(ValueError):
            self.template_engine.render(template, context)

    def test_unknown_tag(self):
        template = "{% unknown_tag %}Content{% endunknown_tag %}"
        context = {}
        with self.assertRaises(SyntaxError):
            self.template_engine.render(template, context)

    def test_multiple_variables(self):
        template = "Name: {{ name }}, Age: {{ age }}"
        context = {"name": "Eve", "age": 30}
        expected = "Name: Eve, Age: 30"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_whitespace_handling(self):
        template = (
            "Start {{   var1   }} Middle {% if var2 %}Yes{% else %}No{% endif %} End"
        )
        context = {"var1": "Value1", "var2": True}
        expected = "Start Value1 Middle Yes End"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_complex_expression(self):
        template = "Total: {{ price * quantity }}"
        context = {"price": 19.99, "quantity": 3}
        expected = "Total: 59.97"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_for_loop_with_range(self):
        template = "{% for i in range(3) %}{{ i }} {% endfor %}"
        context = {}
        expected = "0 1 2 "
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_if_with_no_else(self):
        template = "{% if show %}Visible{% endif %}"
        context = {"show": True}
        expected = "Visible"
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

        context = {"show": False}
        expected = ""
        result = self.template_engine.render(template, context)
        self.assertEqual(result, expected)

    def test_deeply_nested_conditions(self):
        template = textwrap.dedent(
            """
            {% if outer %}
                {% for user in users %}
                    {% if user.active %}
                        <p>{{ user.name }} is active.</p>
                    {% else %}
                        <p>{{ user.name }} is inactive.</p>
                    {% endif %}
                {% endfor %}
            {% else %}
                <p>No outer condition.</p>
            {% endif %}
        """
        )
        context = {
            "outer": True,
            "users": [
                {"name": "Dave", "active": True},
                {"name": "Eve", "active": False},
            ],
        }
        expected = textwrap.dedent(
            """
            <p>Dave is active.</p>
        
            <p>Eve is inactive.</p>
        """
        )
        result = self.template_engine.render(template, context)
        self.assertEqual(result.strip(), expected.strip())


if __name__ == "__main__":
    unittest.main()
