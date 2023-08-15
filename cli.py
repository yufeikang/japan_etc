import dotenv

dotenv.load_dotenv()

from etc.etc import main
from etc.db import close as close_db

if __name__ == "__main__":
    try:
        main()
    finally:
        close_db()
