from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/todos', methods=['POST'])
def create_todo():
    # Get the request data
    data = request.get_json()

    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        db='todo_list'
    )

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO todos (title, description) VALUES (%s, %s)"
            cursor.execute(sql, (data['title'], data['description']))

        # Commit the changes to the database
        connection.commit()
    finally:
        connection.close()

    # Return the created todo item
    return jsonify(data)

@app.route('/todos', methods=['GET'])
def read_todos():
    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        db='todo_list'
    )

    todos = []
    try:
        with connection.cursor() as cursor:
            # Read all todo items
            sql = "SELECT * FROM todos"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                todo = {'id': row[0], 'title': row[1], 'description': row[2]}
                todos.append(todo)
    finally:
        connection.close()

    # Return the list of todos
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    # Get the request data
    data = request.get_json()

    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        db='todo_list'
    )

    try:
        with connection.cursor() as cursor:
            # Update a record
            sql = "UPDATE todos SET title=%s, description=%s WHERE id=%s"
            cursor.execute(sql, (data['title'], data['description'], todo_id))

        # Commit the changes to the database
        connection.commit()
    finally:
        connection.close()

    # Return the updated todo item
    return jsonify(data)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='password',
        db='todo_list'
    )

    try:
        with connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM todos WHERE id=%s"
            cursor.execute(sql, (todo_id))

        # Commit the changes to the database
        connection.commit()
    finally:
        connection.close()

    # Return a success message
    return jsonify({'message': 'Todo item deleted successfully'})
