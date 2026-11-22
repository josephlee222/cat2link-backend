def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def generate_error_response(message, status_code=400, errors=None):
    response = {"status": "error", "message": message}
    if errors:
        response["errors"] = errors
    return response, status_code