from flask import Flask, render_template, url_for, request, redirect
import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client=MongoClient(os.environ.get("MONGODB_URI")) #cluster
    app.db = client.PaginaKiwi

    def write_to_file(data):
        with open('database.txt', mode='a') as database:
            email = data["email"]
            subject = data["subject"]
            message = data["message"]
            file = database.write(f'\n{email},{subject},{message}')


    def write_to_csv(data):
        with open('database.csv', newline='', mode='a') as database2:
            email2 = data["email"]
            subject2 = data["subject"]
            message2 = data["message"]
            csv_writer = csv.writer(database2, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email2, subject2, message2])

    @app.route('/')
    def my_home():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/<string:page_name>')
    def html_page(page_name):
        return render_template(page_name)

    @app.route('/submit_form', methods=['POST', 'GET'])
    def submit_form():
        if request.method == 'POST':
            try:
                data = request.form.to_dict()
                write_to_file(data)
                write_to_csv(data)
                app.db.contact.insert(data)
                return redirect('/thankyou.html')
            except:
                return 'did not save to database'
        else:
            return 'Something went wrong. Try again.'
            
    return app
