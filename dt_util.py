import webbrowser
import sys

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise Error('Boolean value expected.')

def ask_yes_no_question(question):
    answer = input('%s (y/n) ' %question)
    if str2bool(answer):
        return True
    return False

def check_if_json(str):
    if "<html>" in str:
        print(str)
        return False
    if "<title>" in str:
        print(str)
        return False
    return True

def logged_in(response, a_config):
    a_config.logger.info("Checking if you're logged into DT.")
    if "<title>DT - Login</title>" in response:
        strMessage = "You need to login into DzjinTonik first... Be sure to set the correct variables on top of this file!"
        print(strMessage)
        a_config.logger.error(strMessage)
        webbrowser.open(a_config.domain)
        sys.exit()
        return False
    elif "<title>" in response:
        print(response)
        print("An other error occured... Please read the lines above! SUGGESTION: Is your model correct? Are you sending an ID?")
        return False
    elif "<html>" in response:
        print(response)
        print("Your output is html, which is not nice!")
        return False
    return True
