import json


def checkFormError(form=None):
    errors = []
    if form is not None:
        errors_asjson     = form.errors.as_json()
        errors_jsonloaded = json.loads(errors_asjson)
        for error in errors_jsonloaded:
            if len(errors_jsonloaded) > 1:
                print('plusieur erreur')
            else:
                error_msg = errors_jsonloaded[error][0]['message']
                errors.append(error_msg)
    
    return errors