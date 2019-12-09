def encrypt_credential():
    pass

def decrypt_credential():
    pass

def validate_app_type():
    pass

def main():
    app_type = None
    name = None 
    version = None
    key = None
    region = None
    host = None
    app_id = None

    print('Create new credential: ')
    print('Application type: ')
    app_type = input()

    print('{} Name: '.format(app_type.upper()))
    name = input()

    if app_type.lower().strip() == 'luis':
        print('{} Version: '.format(app_type.upper()))
        version = input()

    print('{} Key: '.format(app_type.upper()))
    key = input()

    if app_type.lower().strip() == 'luis':
        print('{} Region: '.format(app_type.upper()))
        region = input()
    else:
        print('{} Host: '.format(app_type.upper()))
        host = input()

    print('{} ID: '.format(app_type.upper()))
    app_id = input()

    print('Encryption secret key: ')
    secret_key = input()

main()
