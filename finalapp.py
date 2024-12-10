from flask import Flask, request, render_template_string, redirect, url_for
import calendar
import datetime

app = Flask(__name__)

# In-memory storage for greeting cards and holidays (for simplicity)
greeting_cards = []
holidays = {
    "New Year's Day": datetime.date(2025, 1, 1),  # Next New Year's Day
    "Christmas Day": datetime.date(2024, 12, 25),  # Upcoming Christmas
    "Hanukkah": datetime.date(2024, 12, 28),  # Example date for Hanukkah
    "Chinese New Year": datetime.date(2025, 2, 10),  # Example date for Chinese New Year
    "Eid al-Fitr": datetime.date(2025, 4, 10)  # Example date for Eid al-Fitr
}

@app.route('/')
def home():
    return render_template_string('''
        <html>
            <body>
                <h1>Welcome to Our Service</h1>
                <form action="/response" method="post">
                    <input type="radio" name="answer" value="greeting_card"> Receive a greeting card<br>
                    <input type="radio" name="answer" value="calendar"> See a calendar view with holidays<br>
                    <input type="radio" name="answer" value="exit"> Exit<br>
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    ''')

@app.route('/response', methods=['POST'])
def response():
    answer = request.form.get('answer')
    if not answer:
        return render_template_string('''
            <html>
                <body>
                    <h1>Welcome to Our Service</h1>
                    <p style="color:red;">Please select an option before submitting the form.</p>
                    <form action="/response" method="post">
                        <input type="radio" name="answer" value="greeting_card"> Receive a greeting card<br>
                        <input type="radio" name="answer" value="calendar"> See a calendar view with holidays<br>
                        <input type="radio" name="answer" value="exit"> Exit<br>
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>
        ''')
    elif answer == 'greeting_card':
        return redirect(url_for('manage_greeting_cards'))
    elif answer == 'calendar':
        return redirect(url_for('view_calendar'))
    elif answer == 'exit':
        return "Thank you for using our service. Goodbye!"
    else:
        return "Invalid option selected."

@app.route('/greeting_cards', methods=['GET', 'POST'])
def manage_greeting_cards():
    if request.method == 'POST':
        confirm = request.form.get('confirm')
        if confirm == 'yes':
            return "Here's your greeting card: 🎉 Happy Day! 🎉"
        else:
            return "Thank you for using our service. Goodbye!"
    return render_template_string('''
        <html>
            <body>
                <h1>Greeting Card Option</h1>
                <p>Would you like to receive a greeting card?</p>
                <form action="/greeting_cards" method="post">
                    <input type="radio" name="confirm" value="yes"> Yes<br>
                    <input type="radio" name="confirm" value="no"> No<br>
                    <input type="submit" value="Submit">
                </form>
                <a href="/">Back to Home</a>
            </body>
        </html>
    ''')

@app.route('/view_calendar')
def view_calendar():
    today = datetime.date.today()
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    current_month = cal.formatmonth(today.year, today.month)
    holiday_list = ''.join(f'<li>{name}: {date}</li>' for name, date in holidays.items())
    return render_template_string(f'''
        <html>
            <body>
                <h1>Here is your calendar for {today.strftime("%B %Y")}:</h1>
                {current_month}
                <h2>Holidays:</h2>
                <ul>
                    {holiday_list}
                </ul>
                <a href="/">Back to Home</a>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
