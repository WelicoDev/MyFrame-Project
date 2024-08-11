from myframeuz.app import MyFrameApp
from storage import BookStorage
from auth import STATIC_TOKEN, TokenMiddleware , login_required, on_exception

app = MyFrameApp()
book_storage = BookStorage()
book_storage.create(name="7 Habits of Highly Effective People", author="Steven Covey")
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)

@app.route("/", allowed_methods=["get"])
def index(request, response):
    books = book_storage.all()
    context = {
        "books": books
    }
    response.html = app.template("index.html", context=context)

@app.route('/login', allowed_methods=["post"])
def login(request, response):

    response.json = {"token": STATIC_TOKEN}

@app.route("/books", allowed_methods=["post"])
@login_required
def create_book(request, response):
    book = book_storage.create(**request.POST)

    response.status_code = 201
    response.json = book._asdict()

@app.route("/books/{id:d}", allowed_methods=["delete"])
@login_required
def delete(request, response, id):
    book_storage.delete(id)

    response.status_code = 204

