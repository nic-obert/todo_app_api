from frontend import api
from backend.database import check_database


if __name__ == "__main__":

    check_database()
    api.app.run(debug=True, host='127.0.0.1', port=5000)

else:

    check_database()
