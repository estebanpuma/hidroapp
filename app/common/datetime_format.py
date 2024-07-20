from datetime import datetime, timedelta

datetime_format = "%Y-%m-%d"

def format_datetime(date):
   
    return datetime.strptime(date,datetime_format).date()


def format_time(time_str):
    print("entra a forta time")
    try:
        # Intenta convertir con segundos
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        print("2pppppp")
    except ValueError:
        try:
            # Si falla, intenta convertir sin segundos
            time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
            print("2hhh")
        except ValueError:
            # Si ambos formatos fallan, levanta una excepción
            raise ValueError("Formato de tiempo no válido: {}".format(time_str))

    # Extrae solo las horas y minutos
    print(time_obj, type(time_obj))
    formatted_time = time_obj
    print(formatted_time, type(formatted_time))
    return formatted_time
    
    
def calculate_time_difference(start_time, end_time):
    # Combine date with time to create datetime objects
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    
    # Calculate difference
    if end_datetime < start_datetime:
        end_datetime += timedelta(days=1)  # handle overnight case
    
    time_diff = end_datetime - start_datetime
    return time_diff.total_seconds() / 3600  # Convert to hours

def this_year():
    return datetime.today().year


def get_today():
    return datetime.today().strftime(datetime_format)


def get_timestamp():
    return datetime.now().timestamp()