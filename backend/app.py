#!/usr/bin/env python3
"""Simple Flask API exposing an equation solver using SymPy."""

from __future__ import annotations

import os
from flask import Flask, jsonify, request
from sympy import symbols, solve, sympify, Eq
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.after_request
    def add_cors_headers(response):  # type: ignore[override]
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @app.get("/solve")
    def solve_equation():
        equation = (request.args.get("equation") or "").strip()
        variable = (request.args.get("variable") or "").strip()
        
        if not equation:
            return jsonify({"error": "Missing 'equation' query parameter"}), 400
        
        try:
            # Define transformations for parsing
            transformations = standard_transformations + (
                implicit_multiplication_application,
                convert_xor,  # Converts ^ to ** for exponentiation
            )
            
            # Check if it's an equation (contains '=')
            if '=' in equation:
                # Split by '=' and create an Eq object
                parts = equation.split('=')
                if len(parts) != 2:
                    return jsonify({"error": "Invalid equation format. Use single '=' sign."}), 400
                
                lhs = parse_expr(parts[0].strip(), transformations=transformations)
                rhs = parse_expr(parts[1].strip(), transformations=transformations)
                expr = Eq(lhs, rhs)
            else:
                # Treat as expression = 0
                expr = parse_expr(equation, transformations=transformations)
            
            # Get free symbols (variables) from the expression
            if isinstance(expr, Eq):
                free_syms = expr.free_symbols
            else:
                free_syms = expr.free_symbols
            
            # Determine which variable to solve for
            if variable:
                solve_var = symbols(variable)
            elif len(free_syms) == 1:
                solve_var = list(free_syms)[0]
            elif len(free_syms) == 0:
                # No variables - just evaluate
                if isinstance(expr, Eq):
                    result = expr.lhs.equals(expr.rhs)
                    return jsonify({"result": str(result)})
                else:
                    return jsonify({"result": str(expr)})
            else:
                # Multiple variables, default to x if present, else first alphabetically
                sym_names = sorted([str(s) for s in free_syms])
                if 'x' in sym_names:
                    solve_var = symbols('x')
                else:
                    solve_var = symbols(sym_names[0])
            
            # Solve the equation
            solutions = solve(expr, solve_var)
            
            if not solutions:
                return jsonify({"result": "No solution found"})
            
            # Format the result
            if len(solutions) == 1:
                result = f"{solve_var} = {solutions[0]}"
            else:
                result = f"{solve_var} = {', '.join(str(s) for s in solutions)}"
            
            return jsonify({"result": result})
            
        except Exception as e:
            return jsonify({"error": f"Failed to solve equation: {str(e)}"}), 400

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"message": "Equation API. Try /solve?equation=x^2+2x-10"})

    return app


def run() -> None:
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
