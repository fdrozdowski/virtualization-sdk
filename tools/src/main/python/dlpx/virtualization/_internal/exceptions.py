#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import collections
import json


class UserError(Exception):
    """
    UserError is the main error that gets caught in cli.py. The message from
    this exception is posted to logger.error. message will be the first arg
    that is passed in (for any exception that is extending it).
    """

    @property
    def message(self):
        return self.args[0]

    def __init__(self, message):
        super(UserError, self).__init__(message)


class InvalidArtifactError(UserError):
    """
    InvalidArtifactError gets raised when the parsed engineApi is not
    in the correct format. the example field shows an example of what the
    engineApi should have been.
    """

    def __init__(self):
        example = collections.OrderedDict([('type', 'APIVersion'), ('major',
                                                                    1),
                                           ('minor', 7), ('micro', 0)])
        message = ('The engineApi field is either missing or malformed.'
                   ' The field must be of the form:\n{}\nVerify that the'
                   ' artifact passed in was generated by the build'
                   ' function.'.format(json.dumps(example, indent=2)))
        super(InvalidArtifactError, self).__init__(message)


class HttpPostError(UserError):
    """
    HttpPostError gets raised when the response's type is ErrorResult. Takes
    in the code and error message that gets returned.
    """

    def __init__(self, status_code, error):
        self.status_code = status_code
        self.error = error
        message = 'Plugin upload failed with HTTP Status {}\n{}'.format(
            str(self.status_code), self.parse_error(self.error))
        super(HttpPostError, self).__init__(message)

    @staticmethod
    def parse_error(error):
        """
        This function returns the parsed error from an HttpPostError. While
        the error is likely to have a details and action property, depending
        on where the error was originally generated from on the appliance, the
        format may be different so we want to try to print that nicely as well.
        """
        details = error.get('details')
        if details:
            details = 'Details: {}'.format(details)
        else:
            # If error details is None then just dump the full error.
            details = ('Unable to parse details of error. Dumping full'
                       ' response: {}'.format(json.dumps(error, indent=2)))

        action = error.get('action')
        if action:
            return '{}\nAction: {}'.format(details, action)

        return details


class UnexpectedError(UserError):
    """
    UnexpectedError gets raised when the resulting response was not expected.
    Takes in the response's content. if it was a json it gets printed as best
    as possible.
    """

    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response
        message = ('Received an unexpected error with HTTP Status {},'
                   '\nDumping full response:\n{}'.format(
                       str(self.status_code), self.response))
        super(UnexpectedError, self).__init__(message)
