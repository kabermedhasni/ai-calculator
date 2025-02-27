from flask import Flask, request, jsonify, send_from_directory
from test import AdvancedCalculator
import os
import openai
from datetime import datetime
import re

app = Flask(__name__)
calculator = AdvancedCalculator()

# Set the API key
api_key = "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"
os.environ["OPENAI_API_KEY"] = api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

def get_ai_suggestion(expression):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mathematical assistant. Provide brief, direct responses."},
                {"role": "user", "content": f"For the calculation '{expression}', suggest a related or next possible calculation. Respond with ONLY the suggested calculation, no other text."}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Suggestion Error: {str(e)}")  # Add error logging
        return None

def process_natural_language(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Convert natural language math queries to mathematical expressions. Respond with ONLY the mathematical expression, no other text."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Natural Language Processing Error: {str(e)}")  # Add error logging
        return None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    data = request.json
    text = data.get('text', '')
    
    # Convert natural language to mathematical expression
    expression = process_natural_language(text)
    if expression:
        return jsonify({'expression': expression})
    return jsonify({'error': 'Could not process voice input'}), 400

@app.route('/get_suggestion', methods=['POST'])
def get_suggestion():
    data = request.json
    current_calc = data.get('calculation', '')
    
    suggestion = get_ai_suggestion(current_calc)
    if suggestion:
        return jsonify({'suggestion': suggestion})
    return jsonify({'suggestion': None})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    print(f"Received data: {data}")  # Add request logging
    
    try:
        if 'natural_language' in data:
            # Process natural language input
            expression = process_natural_language(data['natural_language'])
            if not expression:
                return jsonify({'error': 'Could not process natural language input'}), 400
            try:
                # Safely evaluate the expression
                result = eval(expression)
                calculator.add_to_history('natural', f"{data['natural_language']} → {expression}", result)
                return jsonify({
                    'result': result,
                    'expression': expression,
                    'history': calculator.history[-5:]
                })
            except Exception as e:
                print(f"Expression Evaluation Error: {str(e)}")  # Add error logging
                return jsonify({'error': f'Could not evaluate expression: {expression}'}), 400
            
        elif 'function' in data:
            # Handle single-operand functions
            value = float(data['value'])
            func = data['function']
            
            if func == 'sin':
                result = calculator.sin(value)
            elif func == 'cos':
                result = calculator.cos(value)
            elif func == 'tan':
                result = calculator.tan(value)
            elif func == '√':
                result = calculator.square_root(value)
            elif func == 'log':
                result = calculator.log(value)
            elif func == 'ln':
                result = calculator.ln(value)
            elif func == 'x!':
                result = calculator.factorial(value)
            else:
                return jsonify({'error': 'Invalid function'}), 400
                
            calculator.add_to_history(func, str(value), result)
            
        else:
            # Handle binary operations
            num1 = float(data['num1'])
            num2 = float(data['num2'])
            operation = data['operation']
            
            if operation == '+':
                result = calculator.add(num1, num2)
            elif operation == '-':
                result = calculator.subtract(num1, num2)
            elif operation == '*':
                result = calculator.multiply(num1, num2)
            elif operation == '/':
                result = calculator.divide(num1, num2)
            elif operation == '^':
                result = calculator.power(num1, num2)
            else:
                return jsonify({'error': 'Invalid operation'}), 400
                
            calculator.add_to_history(operation, f"{num1} {operation} {num2}", result)
        
        calculator.ans = result
        
        # Get AI suggestion for next calculation
        suggestion = get_ai_suggestion(f"{calculator.history[-1]['inputs']} = {result}")
        
        return jsonify({
            'result': result,
            'history': calculator.history[-5:],
            'suggestion': suggestion
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/memory', methods=['POST'])
def memory_operation():
    data = request.json
    action = data['action']
    
    try:
        if action == 'MR':
            result = calculator.recall_memory()
        elif action == 'MC':
            calculator.clear_memory()
            result = 0
        elif action == 'M+':
            calculator.add_to_memory()
            result = calculator.recall_memory()
        elif action == 'M-':
            calculator.subtract_from_memory()
            result = calculator.recall_memory()
        else:
            return jsonify({'error': 'Invalid memory operation'}), 400
            
        return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({'history': calculator.history[-5:]})

if __name__ == '__main__':
    app.run(debug=True) 