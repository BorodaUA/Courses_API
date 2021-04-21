from course_crud import create_app

app = create_app("development")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=4000,
        debug=True,
        use_debugger=False,
        use_reloader=False,
        passthrough_errors=True,
    )
