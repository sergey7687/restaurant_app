from restapp import app

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
