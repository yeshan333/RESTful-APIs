from flask import Flask, jsonify, request

from middleApplication.model.expense import Expense, ExpenseSchema
from middleApplication.model.income import Income, IncomeSchema
from middleApplication.model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
  Income('Salary', 5000),
  Income('Dividends', 200),
  Expense('pizza', 50),
  Expense('Rock Concert', 100)
]


@app.route('/incomes')
def get_incomes():
  # https://github.com/marshmallow-code/marshmallow/issues/1358
  schema = IncomeSchema(many=True)
  incomes = schema.dump(
    filter(lambda t: t.type == TransactionType.INCOME, transactions)
  )
  return jsonify(incomes) # incomes.data problem：already not support


@app.route('/incomes', methods=['POST'])
def add_income():
  income = IncomeSchema()
  result = income.load(request.get_json())
  transactions.append(result)
  return "", 204


@app.route('/expenses')
def get_expenses():
  schema = ExpenseSchema(many=True)
  expenses = schema.dump(
      filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
  )
  return jsonify(expenses)


@app.route('/expenses', methods=['POST'])
def add_expense():
  expense = ExpenseSchema().load(request.get_json())
  transactions.append(expense.data)
  return "", 204