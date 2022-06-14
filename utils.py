
def create_http_message_response(status: bool, message: str):
    return {
        'status': status,
        'message': message
    }