#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import ast, hashlib, random
from datetime import datetime, date

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='',
                       db='flight_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    if not session.get('username') is None:
        if session['username'][1] == True:
            return render_template('index.html', username = session['username'][0], isCustomer = True)
        else: 
            return render_template('index.html', username = session['username'][0], isStaff = True)
    return render_template('index.html')

#Define route for login
@app.route('/login', methods = ['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
@app.route('/showStaffLogin', methods = ['GET','POST'])
def showStaffLogin():
    return render_template('login.html', staff = True)
#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
#DONE
@app.route('/customerloginAuth', methods=['GET', 'POST'])
def customerloginAuth():
 
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode()).digest()
    password = str(password)
    print(password)
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
    #print(data)
    #print(type(data))
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        session['username'] = [username,True]
        return render_template('index.html', username = username, isCustomer = True)
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

@app.route('/staffLoginAuth', methods = ['GET','POST'])
#TODO
def staffLoginAuth():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode()).digest()
    password = str(password)
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
	#stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None    
    if(data):
		#creates a session for the the user
		#session is a built in
        session['username'] = [username,False]
        return render_template('index.html', username = username, isStaff = True)
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error, staff = True)

@app.route('/showStaffReg/', methods = ['POST'])
#DONE
def showStaffReg():
    return render_template('staffRegister.html')

#Authenticates the register
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
#DONE
def registerAuthCustomer():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode()).digest()
    password = str(password)
    print(password)
    print(type(password))
    name = request.form['name']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (username))
	#stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(ins,(username,
                            name,
                            password,
                            building_number,
                            street,
                            city,
                            state,
                            phone_number,
                            passport_expiration, 
                            passport_country, 
                            date_of_birth))
        conn.commit()
        cursor.close()
    return render_template('index.html')

@app.route('/registerAuthStaff', methods = ['GET','POST'])
#TODO
def registerAuthStaff():
    username = request.form['username']
    password = request.form['password']
    password = hashlib.md5(password.encode()).digest()
    password = str(password)
    print(password)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    phone_number = request.form['phone_number']
    print(phone_number)
    print(len(phone_number))
    phone_number_lst = [phone_number[i:i+12] for i in range(int(len(phone_number)//12))]
    
	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
	#stores the results in a variable
    data = cursor.fetchone()
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('staffRegister.html', error = error)
    else:
        airline_query = 'SELECT * FROM airline WHERE name = %s'
        cursor.execute(airline_query, (airline_name))
        airline_exists = cursor.fetchone()
        if airline_exists:
            ins = 'INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s)'
            cursor.execute(ins,(username,
                            password,
                            first_name,
                            last_name,
                            date_of_birth,
                            airline_name))
            for number in phone_number_lst:
                ins = 'INSERT INTO airline_staff_phone_number VALUES(%s,%s)'
                cursor.execute(ins,(username,number))
            conn.commit()
            cursor.close()
        else:
            error = "This airline does not exist. Please enter a valid airline"
            return render_template('staffRegister.html', error = error)
    return render_template('index.html')



@app.route('/searchFlightStatus', methods = ['GET', 'POST'])
#DONE
def searchFlightStatus():
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']
    print(arrival_date)
    query = '''SELECT * FROM flight where airline_name = %s and
    flight_number = %s and departure_date = %s and arrival_date = %s'''
    cursor = conn.cursor()
    cursor.execute(query, (airline_name, 
                            flight_number, 
                            departure_date,
                            arrival_date))
    flights = cursor.fetchall()
    
    if not session.get('username') is None:
        return render_template('flight_status.html', query = flights, 
        username = session['username'][0])
    return render_template('flight_status.html', query = flights)
                                                     
@app.route('/lookForFlights', methods = ['GET', 'POST'])
#Done!
def lookForFlights():
    #print('here')
    trip_type = request.form['trip_type']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    #print('here2')
    departure_date =request.form['departure_date']
    #print(trip_type)
    if trip_type == 'round_trip':
        #print('here3')
        arrival_date = request.form['return_date']
        cursor = conn.cursor()
        print(type(arrival_date))
        departure_flight_query = 'SELECT * FROM flight WHERE arrival_airport = %s and departure_airport = %s and departure_date = %s'
        cursor.execute(departure_flight_query, (arrival_airport, 
            departure_airport, departure_date))
        depart_data = cursor.fetchall()
        arrival_flight_query = 'SELECT * FROM flight WHERE arrival_airport = %s and departure_airport = %s and arrival_date = %s'
        cursor.execute(arrival_flight_query, (departure_airport, 
        arrival_airport, arrival_date))
        return_data = cursor.fetchall()
        #data = ({"data":"data1", "data2":"datA2"},{"dAta":"dAta"})
        #print(data)
        #print(type(data))
        return render_template('search_results.html', depart_query = depart_data, return_query = return_data)
        print(arrival_date)
    elif trip_type == 'one_way':
        cursor = conn.cursor()
        flight_query = 'SELECT * FROM flight WHERE arrival_airport = %s and departure_airport = %s and departure_date = %s'
        cursor.execute(flight_query, (arrival_airport, 
            departure_airport, departure_date))
        flights = cursor.fetchall()
        return render_template('search_results.html', depart_query = flights)
        
    return render_template('index.html')

@app.route('/purchaseTicket', methods = ['GET', 'POST'])
# DONE!!!
def purchaseTicket():
    print('here')
    #print(session['username'])
    if not session.get('username') is None:
        flight_search = request.form.getlist("flight")
        print(flight_search)
        query = '''select flight.flight_number,base_price, flight.airline_name, 
        IFNULL(seats_taken,0) as seats_taken, number_of_seats from flight left join
        (select flight_number, count(flight_number) as seats_taken from ticket) as ticket on flight.flight_number = ticket.flight_number, 
        airplane where airplane.id = flight.airplane_id and flight.flight_number = %s and 
        departure_date = %s and departure_time = %s and flight.airline_name = %s;'''
        #print(query)
        flight_list = []
        for flight in flight_search:
            flight = ast.literal_eval(flight)
            cursor = conn.cursor()
            cursor.execute(query, (flight[0], flight[1], flight[2], flight[3]))
            query_result = cursor.fetchone()
            print(query_result)
            if query_result['seats_taken'] > query_result['number_of_seats']*.75:
                query_result['base_price'] = query_result['base_price']*.75
            flight_list.append(query_result)
            total_flight_price = 0
            for i in flight_list:
                total_flight_price += i['base_price']
        return render_template("purchase_ticket.html", flights = flight_list, 
        username = session['username'][0], flight = flight_list, 
        price = total_flight_price)
    else:
        depart_query = request.form["depart_query"]
        return_query = requet.form.get('return_query')
        original_query = ast.literal_eval(original_query)
        flight_search = request.form.getlist("flight")
        
        error = 'Please Login before purchasing a ticket'
        return render_template("search_results.html",depart_query = depart_query, return_query = return_query, error = error)
  
@app.route('/confirmPurchase', methods = ['GET','POST'])
def confirmPurchase():
    print('here')
    card_type = request.form['card_type']
    card_number = request.form['card_number']
    card_expiration_date = request.form['card_expiration_date']
    flights = request.form['flights']
    email = request.form['email']
    name_on_card = request.form['name_on_card']
    now = datetime.now()
    currTime = now.strftime("%H:%M")
    currDate = str(date.today())
    flights = ast.literal_eval(flights)
    print(flights)
    for i in flights:
        foundID = True
        cursor = conn.cursor()
         #check to see if ticket ID is already in flight
        while foundID:
            ID =  str(random.random())
            query  = 'SELECT * from ticket where id = %s'
            cursor.execute(query, (ID))
            data = cursor.fetchone()
            if not (data):
                foundID = False
                insert = 'INSERT INTO ticket VALUES (%s, %s , %s, %s, %s, %s, %s, %s, %s, %s,%s)'
                cursor.execute(insert, (ID, 
                                       i['base_price'], 
                                       card_type, 
                                       card_number, 
                                       name_on_card,
                                       card_expiration_date, 
                                       currDate,
                                       currTime, 
                                       i['airline_name'], 
                                       i['flight_number'], 
                                       email))

                conn.commit()
                cursor.close()
    return render_template('index.html', username = email, isCustomer = True, message ="Purchase was successful!" )
         
       
@app.route('/view_flights_customer', methods = ['GET', 'POST'])
def view_flights_customer():
    username = session['username'][0]
    if verifyIfCustomer(username):
        query = '''SELECT * from flight where flight_number in 
        (SELECT flight_number from ticket where customer_email = %s)'''
        cursor = conn.cursor()
        print(username)
        print(type(username))
        cursor.execute(query, (username))
        data = cursor.fetchall()
        return render_template('view_flights.html', query = data, username = username)
    else: 
        return render_template('index.html', username = username, isStaff = True, message = 'User is not authorized')
     
@app.route('/rateFlight', methods = ['GET','POST'])  
def rateFlight():
    username = session['username'][0]
    flight = request.form['flight']
    original_query = request.form['original_query']
    flight = ast.literal_eval(flight)
    original_query = ast.literal_eval(original_query)
    currDate = str(date.today())
    print(currDate)
    print(flight['arrival_date'])
    query = '''SELECT * from rate where email = %s and flight_number = %s 
    and departure_date = %s and departure_time = %s'''
    cursor = conn.cursor()
    cursor.execute(query, (username,
                           flight['flight_number'], 
                           flight['departure_date'],
                           flight['departure_time']))
    data = cursor.fetchone()
    if data:
        error = "Flight has already been rated by you"
        return render_template('view_flights.html', 
                                query = original_query, username = username,
                                error = error)
    if flight['arrival_date'] < currDate:
        return render_template('rate_flight.html', username = username, flight = flight)
    error = "Cannot rate a future flight"
    return render_template('view_flights.html', query = original_query, username = username, error = error)
 
@app.route('/submitRating', methods = ['GET', 'POST'])
def submitRating():
    username = session['username'][0]
    flight = request.form['flight']
    flight = ast.literal_eval(flight)
    rating = request.form['rating']
    comment = request.form['comment']
    ins = 'insert into rate values(%s,%s,%s,%s,%s,%s)'
    cursor = conn.cursor()
    cursor.execute(query, (username,
                           flight['flight_number'],
                           flight['departure_date'],
                           flight['departure_time'],
                           flight['airline_name'],
                           rating,
                           comment))
    conn.commit()
    cursor.close()
    message = 'Submitted rating successfully.'
    return render('index.html', username = username, isCustomer = True,
                  message = message)
   
@app.route('/viewSpending', methods = ['GET', 'POST'])
def viewSpending(): 
    username = session['username'][0]
    if verifyIfCustomer(username):
        today =  date.today()
        past_six_month = (today.month - 6) % 12
        past_six_year = today.year - ((today.month - 6) // 12)
        six_months_before = date(past_six_year, past_six_month, today.day)
        six_months_before = str(six_months_before)
        one_year_ago = today.year - 1
        last_year = date(one_year_ago, today.month, today.day)
        last_year = str(last_year)
        today = str(today)
        query = 'SELECT sold_price,purchase_date from ticket where customer_email = %s and purchase_date >= %s'
        cursor = conn.cursor()
        cursor.execute(query, (username, six_months_before))
        data_six_months = cursor.fetchall()
        query = 'SELECT sold_price,purchase_date from ticket where customer_email = %s and purchase_date >= %s'
        cursor.execute(query, (username, last_year))
        data_last_year = cursor.fetchall()
        total_spendings = 0
        for i in data_last_year:
            total_spendings += i['sold_price']
        return render_template('viewSpending.html', username = username, 
                        data_six_months = data_six_months, data_last_year = data_last_year, total_spendings = total_spendings)
    else:
        return render_template('index.html', username = username, isStaff = True, message = 'User is not authorized')
    
@app.route('/selectRangeSpending', methods = ['GET', 'POST'])
def selectRangeSpending():
    username = session['username'][0]
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    data_six_months = request.form['six_months']
    data_last_year = request.form['one_year']
    total_spendings = request.form['total_spendings']
    
    data_six_months = ast.literal_eval(data_six_months)
    data_last_year = ast.literal_eval(data_last_year)
    today =  date.today()
    today = str(today)
    if end_date > today:
        error = 'Ending date cannot be in the future.'
        return render_template('viewSpending.html', username = username, 
                        data_six_months = data_six_months, data_last_year = data_last_year,
                        total_spendings = total_spendings, error = error )
    else:
        query = 'SELECT sold_price,purchase_date from ticket where customer_email = %s and purchase_date >= %s and purchase_date <= %s'
        cursor = conn.cursor()
        cursor.execute(query, (username, start_date, end_date))
        data_range = cursor.fetchall()
        return render_template('viewSpending.html', username = username, 
                        data_six_months = data_six_months, data_last_year = data_last_year,
                        total_spendings = total_spendings, data_range = data_range)
           
@app.route('/view_flights_staff', methods = ['GET', 'POST'])
def viewFlightsStaff():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        today = date.today()
        next_month = (today.month + 1) % 12
        next_month_year = today.year + ((today.month+1)//12)
        next_month_date = date(next_month_year, next_month, today.day)
        today = str(today)
        next_month_date = str(next_month_date)
        query = '''SELECT * FROM flight where airline_name in 
        (select airline_name from airline_staff where username = %s) and 
         departure_date >= %s and departure_date <= %s'''
        cursor = conn.cursor()
        cursor.execute(query, (username,today,next_month_date))
        data = cursor.fetchall()
        for flight in range(len(data)):
            customer_query = '''SELECT name from customer where email in 
                                (SELECT customer_email from ticket where flight_number = %s and airline_name = %s)'''
            cursor.execute(customer_query, (data[flight]['flight_number'], data[flight]['airline_name']))
            customers = cursor.fetchall()
            print(customers)
            for i in range(len(customers)):
                customers[i] = customers[i]['name']
            data[flight]['customers'] = customers
        return render_template('viewFlightsStaff.html', query = data, username = username, currDate = today)
    else: 
        return render_template('index.html', username = username, isCustomer = True, message = 'User is not authorized')
@app.route('/selectRangeFlightsStaff', methods = ['GET', 'POST'])
def selectRangeFlightsStaff():
    username = session['username'][0]
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    original_query = request.form['original_query']
    if start_date > end_date:
        error = 'Start date cannot be after the end date'
        return render_template('viewFlightsStaff', query = original_query, username = username,
                               error =  error) 
    query = '''SELECT * FROM `flight` WHERe airline_name in 
        (select airline_name from airline_staff where username = %s) and 
         departure_date > %s and departure_date < %s'''
    cursor = conn.cursor()
    cursor.execute(query, (username,start_date,end_date))
    data = cursor.fetchall()
    today = str(date.today())
    return render_template('viewFlightsStaff.html', query = data, username = username, currDate = today)

@app.route('/setStatus', methods = ['GET','POST'])
def setStatus():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        original_query = request.form['original_query']
        flight = request.form['flight']
        print('here')
        flight = ast.literal_eval(flight)
        original_query = ast.literal_eval(original_query)
        print(flight['status'])
        print(len(flight['status']))
        if flight['status'] == 'on time': status = 'delayed'
        elif flight['status'] == 'delayed': status = 'on time'
        update = ' Update flight set status = %s where flight_number = %s'
        cursor = conn.cursor()
        cursor.execute(update, (status, flight['flight_number']))
        conn.commit()
        for i in original_query:
            if i['flight_number'] == flight['flight_number']:
                if i['status'] == 'on time': i['status'] = 'delayed'
                elif i['status'] == 'delayed': i['status'] = 'on time'
        cursor.close()
        today = str(date.today())
        return render_template('viewFlightsStaff.html', query = original_query, username = username, 
                                currDate = today, message = 'updated status successfully')
    else: 
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
@app.route('/seeRatings', methods = ['GET','POST'])
def seeRatings():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False: 
        original_query = request.form['original_query']
        flight = request.form['flight']
        original_query = ast.literal_eval(original_query)
        flight = ast.literal_eval(flight)
        query = '''SELECT avg(ratings) from rate where flight_number = %s and 
                  departure_date = %s and airline_name = %s'''
        cursor = conn.cursor()
        cursor.execute(query, (flight['flight_number'], 
                               flight['departure_date'], 
                               flight['airline_name']))
        rate_data = cursor.fetchone()
        query = '''SELECT comment from rate where flight_number = %s and 
                  departure_date = %s and airline_name = %s'''
        cursor.execute(query, (flight['flight_number'], 
                               flight['departure_date'], 
                               flight['airline_name']))
        comment_data = cursor.fetchall()
        print(comment_data)
        print(rate_data)
        if comment_data:
            return render_template('seeRatings.html', username = username, comment_data = comment_data, rate_data = rate_data)
        else:
            return render_template('viewFlightsStaff.html', query = original_query, username = username, currDate = today)
    else: 
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')   
@app.route('/add_airplane_redirect', methods = ['GET', 'POST'])
def addAirplaneRedirect():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        return render_template('addAirplane.html', username= username)
    else: 
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')

@app.route('/addAirplane', methods = ['GET','POST'])
def addAirplane():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        #verify that airplane does not exist already
        airplane_id = request.form['ID']
        airline_name = request.form['airline_name']
        number_of_seats = request.form['number_of_seats']
        query = 'select * from airplane where id = %s and airline_name = %s'
        cursor = conn.cursor()
        cursor.execute(query, (airplane_id, airline_name))
        airplane_exists = cursor.fetchone()
        if airplane_exists:
            return render_template('addAirplane.html', username = username, error = 'airplane already exists')
        query = 'select * from airline where name = %s'
        cursor.execute(query, (airline_name))
        airline_exists = cursor.fetchone()
        if not airline_exists:
            return render_template('addAirplane.html',username = username, error = 'airline does not exists')
        ins = 'insert into airplane values( %s, %s, %s)'
        cursor.execute(ins, (airplane_id,airline_name,number_of_seats))
        conn.commit()
        query = 'select * from airplane where airline_name = %s'
        cursor.execute(query, (airline_name))
        data = cursor.fetchall()
        cursor.close()
        return render_template('showAirplanes.html', username = username, query = data)
    else:
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
        
@app.route('/create_flights_redirect',  methods = ['GET','POST'])
def createFlightsRedirect():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        return render_template('createFlight.html', username= username)
    else: 
        return render_template('index.html', username = username, 
                               isCustomer = True, message = 'User is not authorized')

@app.route('/createFlight', methods = ['GET','POST']) 
def createFlight():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        #verify that airplane does not exist already
        flight_number = request.form['flight_number']
        airline_name = request.form['airline_name']
        departure_date = request.form['departure_date']
        departure_time = request.form['departure_time']
        arrival_airport = request.form['arrival_airport']
        departure_airport = request.form['departure_airport']
        arrival_date = request.form['arrival_date']
        arrival_time = request.form['arrival_time']
        base_price = request.form['base_price']
        airplane_id = request.form['airplane_id']
        status = request.form['status']
        if departure_date > arrival_date:
            return render_template('createFlight.html', username = username, error = 'arrival date cannot be before the departure date')
        if departure_time > arrival_time:
            return render_template('createFlight.html', username = username, error = 'arrival time cannot be before the departure time')
        if departure_airport == arrival_airport:
            return render_template('createFlight.html', username = username, error = 'arrival and departure airports cannot be the same')
        print(arrival_time)
        query = '''SELECT * from flight where flight_number = %s and departure_date =%s and departure_time = %s and airline_name =%s 
                   or airline_name = %s and airplane_id = %s and (departure_date = %s and arrival_time > %s or departure_time < %s)  '''
                   
        cursor = conn.cursor()
        cursor.execute(query, (flight_number, departure_date, departure_time, airline_name, airline_name, airplane_id, departure_date, departure_time, arrival_time))
        data = cursor.fetchall()
        
        if data:
            return render_template('createFlight.html', username= username, error = 'flight is not valid because of overlaps')
        query = 'select * from airplane where id = %s and airline_name = %s'
        cursor = conn.cursor()
        cursor.execute(query, (airplane_id, airline_name))
        airplane_exists = cursor.fetchone()
        if not airplane_exists:
            return render_template('createFlight.html', username = username, error = 'airplane does not exists')
        query = 'select * from airline where name = %s'
        cursor.execute(query, (airline_name))
        airline_exists = cursor.fetchone()
        if not airline_exists:
            return render_template('createFlight.html',username = username, error = 'airline does not exists')
        query = 'select * from airport where name = %s or name = %s'
        cursor.execute(query, (departure_airport, arrival_airport))
        airport_exists = cursor.fetchall()
        if len(airport_exists) >= 2:
            return render_template('createFlight.html',username = username, error = 'airport does not exist')
        
        ins = 'insert into flight values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(ins, (flight_number, 
                            airline_name, 
                            departure_date, 
                            departure_time, 
                            arrival_airport, 
                            departure_airport, 
                            arrival_date, 
                            arrival_time, 
                            base_price, 
                            airplane_id, 
                            status))
        conn.commit()
        cursor.close()
        
        today = date.today()
        next_month = (today.month + 1) % 12
        next_month_year = today.year + ((today.month+1)//12)
        next_month_date = date(next_month_year, next_month, today.day)
        today = str(today)
        next_month_date = str(next_month_date)
        query = '''SELECT * FROM `flight` WHERe airline_name in 
        (select airline_name from airline_staff where username = %s) and 
         departure_date > %s and departure_date < %s'''
        cursor = conn.cursor()
        cursor.execute(query, (username,today,next_month_date))
        data = cursor.fetchall()
        return render_template('viewFlightsStaff.html', query = data, username = username, currDate = today, message = 'Added Flight successfully!')
    else:
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')

@app.route('/add_airport_redirect', methods = ['GET','POST'])
def addAirportRedirect():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        return render_template('addAirport.html', username= username)
    else: 
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')

@app.route('/addAirport', methods = ['GET','POST']) 
def addAirport():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        code = request.form['code']
        name = request.form['name']
        city = request.form['city']
        query = 'Select * from airport where code = %s or name = %s'
        cursor = conn.cursor()
        cursor.execute(query, (code, name))
        airport_exists = cursor.fetchall()
        if airport_exists:
            return render_template('addAirport.html', username = username, error= 'airport already exists')
        ins = 'Insert into airport values(%s,%s,%s)'
        cursor.execute(ins, (code,name,city))
        conn.commit()
        cursor.close()
        return render_template('index.html', username = username, isCustomer = False, 
                            message = 'Airport was added successfully')
    else: 
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')

@app.route('/customerLookUp', methods = ['GET','POST'])
def customerLookUp():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        customer_email = request.form['customer_email']
        query = '''SELECT * from flight where flight_number in 
                    (select flight_number from ticket where customer_email = %s) and 
                   airline_name in (select airline_name from airline_staff where username = %s)'''
        cursor = conn.cursor()
        cursor.execute(query, (customer_email, username))
        data = cursor.fetchall()
        return render_template('viewFlightsStaff.html', query = data, username = username)
    else: 
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
   
@app.route('/lookupFrequentCustomer', methods = ['GET','POST'])
def lookUpFrequentCustomer():
    username = session['username'][0]
    today = date.today()
    one_year_ago = today.year - 1
    last_year = date(one_year_ago, today.month, today.day)
    last_year = str(last_year)
    if verifyIfStaff(username) and session['username'][1] == False:
        query = '''SELECT customer_email, max(ticket_count) from(select customer_email, 
        count(customer_email) as ticket_count from ticket where airline_name in 
        (select airline_name from airline_staff where username = %s) 
        group by customer_email order by ticket_count desc) as customer_table '''
        cursor = conn.cursor()  
        cursor.execute(query, (username))
        data = cursor.fetchone()
        cursor.close()
        print(data)
        if data:
            return render_template('frequent_customer.html', username = username, data = data)
        else: return render_template('index.html', username = username, isCustomer = True, 
                        message = 'No customers have purchased tickets yet')
        
    else:
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
        
@app.route('/viewReport', methods = ['GET', 'POST'])
def viewReport():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        query = '''SELECT count(id) from ticket where airline_name in 
                (select airline_name from airline_staff where username = %s)  and 
                purchase_date > %s and purchase_date < %s'''
        cursor = conn.cursor()
        cursor.execute(query, (username, start_date, end_date))
        total_data = cursor.fetchone()
        # end_date = datetime.strptime(end_date, '%Y-%M-%d')
        # start_date = datetime.strptime(start_date, '%Y-%M-%d')
        # end_date = date(end_date.year, end_date.month, end_date.day)
        # start_date = date(start_date.year, start_date.month, start_date.day)
       
        # print(end_date)
        # print(start_date)
        # print(end_date.year)
        # print(start_date.year)
        # month_query_results = []
        # while ((end_date.year != start_date.year)):
            # temp_end_month = (start_date.month + 1)% 12
            # temp_end_year = start_date.year + ((start_date.month +1 )//12)
            # temp_end_date = date(temp_end_year, temp_end_month,start_date.day)
            # cursor.execute(query, (username, start_date, temp_end_date))
            # start_date = temp_end_date
            # query_result = cursor.fetchone()
            # month_query_results.append(query_result)
            # print('here')
        # print(month_query_results)
        
        return render_template('viewReport.html', username = username, query = total_data)                    
        
    else:
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
    
@app.route('/revenue', methods = ['GET', 'POST'])
def revenue():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        today =  date.today()
        past_six_month = (today.month - 6) % 12
        past_month = (today.month - 1) % 12
        past_six_year = today.year - ((today.month - 6) // 12)
        past_month_year = today.year - (( today.month - 1) // 12)
        past_year_date = date(today.year-1, today.month, today.day)
        past_month_date = date(past_month_year, past_month, today.day)
        past_month_date = str(past_month_date)
        past_year_date = str(past_year_date)
        today = str(today)
        query = '''SELECT sum(sold_price) from ticket where airline_name in 
                (select airline_name from airline_staff where username = %s) and 
                purchase_date > %s and purchase_date < %s'''
        cursor = conn.cursor()
        cursor.execute(query, (username, past_month_date, today))
        month_data = cursor.fetchone()
        cursor.execute(query, (username, past_year_date, today))
        year_data = cursor.fetchone()
        print(year_data)
        print(month_data)
        return render_template('revenue.html', username = username, 
                            month_data = month_data, year_data = year_data)
        
    else:
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
    
    
@app.route('/topDestination', methods = ['GET', 'POST'])
def topDestination():
    username = session['username'][0]
    if verifyIfStaff(username) and session['username'][1] == False:
        query = '''SELECT arrival_airport, ticket_count from(select arrival_airport, 
        count(arrival_airport) as ticket_count from flight where airline_name in 
        (select airline_name from airline_staff where username = %s) 
        group by arrival_airport order by ticket_count desc) as customer_table limit 3'''
        cursor = conn.cursor()
        cursor.execute(query, (username))
        data = cursor.fetchall()
        cursor.close()
        return render_template('topDestination.html',username = username, query = data)
    else:
        return render_template('index.html', username = username, 
                                isCustomer = True, message = 'User is not authorized')
def verifyIfCustomer(username):
    query = 'SELECT * from customer where email = %s'
    cursor = conn.cursor()
    cursor.execute(query, (username))
    customer_exists = cursor.fetchone()
    if(customer_exists):
        return True
    else: return False
    
def verifyIfStaff(username):
    query = 'SELECT * from airline_staff where username = %s'
    cursor = conn.cursor()
    cursor.execute(query, (username))
    staff_exists = cursor.fetchone()
    if (staff_exists):
        return True
    else: return False
      
    
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = False)
    