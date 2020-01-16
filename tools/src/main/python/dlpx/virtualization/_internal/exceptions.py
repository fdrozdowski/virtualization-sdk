#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import collections
import json
import re


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


class PathIsAbsoluteError(UserError):
    def __init__(self, path):
        self.path = path
        message = "The path '{}' should be a relative path, but is not."\
            .format(path)
        super(PathIsAbsoluteError, self).__init__(message)


class PathDoesNotExistError(UserError):
    def __init__(self, path):
        self.path = path
        message = "The path '{}' does not exist.".format(path)
        super(PathDoesNotExistError, self).__init__(message)


class PathExistsError(UserError):
    def __init__(self, path):
        self.path = path
        message = "The path '{}' already exists.".format(path)
        super(PathExistsError, self).__init__(message)


class PathTypeError(UserError):
    def __init__(self, path, path_type):
        self.path = path
        self.path_type = path_type
        message = "The path '{}' should be a {} but is not.".format(
            path, path_type)
        super(PathTypeError, self).__init__(message)


class SchemaMissingRequiredFieldError(UserError):
    """
    SchemaMissingRequiredFieldError gets raised when a specific schema is
    missing required fields.
    """
    def __init__(self, definition_type, missing_fields):
        self.definition_type = definition_type
        self.missing_fields = missing_fields
        message = ('The provided schema for {} is missing required fields.'
                   ' Verify that the field(s) {} are there.'.format(
                       self.definition_type, self.missing_fields))
        super(SchemaMissingRequiredFieldError, self).__init__(message)


class InvalidArtifactError(UserError):
    """
    InvalidArtifactError gets raised when the parsed engineApi is not
    in the correct format. the example field shows an example of what the
    engineApi should have been.
    """
    def __init__(self):
        example = collections.OrderedDict([('type', 'APIVersion'),
                                           ('major', 1), ('minor', 7),
                                           ('micro', 0)])
        message = ('The engineApi field is either missing or malformed.'
                   ' The field must be of the form:\n{}\nVerify that the'
                   ' artifact passed in was generated by the build'
                   ' function.'.format(json.dumps(example, indent=2)))
        super(InvalidArtifactError, self).__init__(message)


class MissingPluginError(UserError):
    """
    MissingPluginError is raised when the plugin name specified by the
    user does not exist on the Delphix Engine that is provided.
    """
    def __init__(self, plugin_name, delphix_engine):
        message = (
            'Cannot find plugin {} on Delphix Engine {}.'
            ' Upload your plugin with "dvp upload" and try again.'.format(
                plugin_name, delphix_engine))
        super(MissingPluginError, self).__init__(message)


class HttpError(UserError):
    """
    HttpError gets raised when the response's type is ErrorResult. Takes
    in the code and error message that gets returned.
    """
    def __init__(self, status_code, error):
        self.status_code = status_code
        self.error = error
        message = 'API request failed with HTTP Status {}\n{}'.format(
            str(self.status_code), self.parse_error(self.error))
        super(HttpError, self).__init__(message)

    @staticmethod
    def parse_error(error):
        """
        This function returns the parsed error from an HttpError. While
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


class SchemaValidationError(UserError):
    """
    SchemaValidationError gets raised when the validation on plugin config
    or plugin schema fails. Takes in the validation errors and formats
    the error attributes into a message string.
    """
    def __init__(self, schema_file, validation_errors):
        self.schema_file = schema_file
        self.validation_errors = validation_errors

        formatted_errors = self.__format_errors(validation_errors)
        error_msg = "\n".join(formatted_errors)

        message = (
            '{}\n\nValidation failed on {}. \n{} Warning(s). {} Error(s)'.
            format(error_msg, self.schema_file, 0, len(formatted_errors)))
        super(SchemaValidationError, self).__init__(message)

    @staticmethod
    def __format_errors(validation_errors):
        """
        Formats the validation errors by extracting out relevant parts of the
        object and also check for errros on nested schemas, if any.
        """
        all_errors = []
        for err in validation_errors:
            all_errors.append(SchemaValidationError.__format_error(err))

            #
            # Check if sub/nested schema errors are reported as well. If so,
            # get the error string based on those errors.
            #
            if err.context:
                nested_errors = SchemaValidationError.__format_errors(
                    err.context)
                all_errors.extend(nested_errors)

        return all_errors

    @staticmethod
    def __format_error(err):
        """
        Formats the error message by extracting out required ValidationError
        information. jsonschema.ValidationError has several attributes. Below
        are the 3 required to form the error message string. This could be
        modified in future to add more info in the validation error message.
        message - error message from validation failure
        path - path of the schema that failed validation
        instance - instance on which validation failed
        context - if there are errors on nested/sub-schemas, context object
                  contains validations errors from those schemas.
        e.g.
        Validation Error:
            'identityFields' is a required property

            Failed validating 'required' in
            schema['properties']['repositoryDefinition']['allOf'][1]:
                {'identityFields': {'items': {'type': 'string'},
                                     'minItems': 1,
                                     'type': 'array'},
                 'nameField': {'type': 'string'},
                 'required': ['nameField', 'identityFields'],
                 'type': 'object'}

            On instance['repositoryDefinition']:
                {'nameField': 'name',
                 'properties': {'name': {'type': 'string'}},
                 'type': 'object'}
        """
        #
        # Validation error message could be unicode encoded string. Strip out
        # any leading unicode characters for proper display and logging.
        #
        err_msg = re.compile(r'\bu\b', re.IGNORECASE)
        err_msg = err_msg.sub("", err.message)

        error_string = 'Error: {} on {}'.format(
            err_msg, map(str, list(err.schema_path)))

        return error_string


class BuildFailedError(UserError):
    """
    BuildFailedError gets raised when there is an error(s) validating any of
    plugin files - plugin config, plugin schema and the errors found importing
    the plugin module itself.
    Takes in the exception/error message generated by the validator(s) and
    constructs a user consumable build failure message.
    """
    def __init__(self, exception):
        message = ('{} \n\nBUILD FAILED.'.format(exception.message))
        super(BuildFailedError, self).__init__(message)


class SubprocessFailedError(UserError):
    """
    SubprocessFailedError gets raised when a command executing in a subprocess
    fails.
    """
    def __init__(self, command, exit_code, output):
        self.command = command
        self.exit_code = exit_code
        self.output = output
        message = ("{}\n"
                   "{} failed with exit code {}.").format(
                       output, command, exit_code)
        super(SubprocessFailedError, self).__init__(message)


class ValidationFailedError(UserError):
    """
    ValidationFailedError gets raised when validation fails on plugin config
    and its contents.
    Defines helpers methods to format warning and exception messages.
    """
    def __init__(self, warnings):
        message = self.__report_warnings_and_exceptions(warnings)
        super(ValidationFailedError, self).__init__(message)

    @classmethod
    def __report_warnings_and_exceptions(cls, warnings):
        """
        Prints the warnings and errors that were found in the plugin code, if
        the warnings dictionary contains the 'exception' key.
        """
        exception_msg = cls.exception_msg(warnings)
        exception_msg += '\n{}'.format(cls.warning_msg(warnings))
        return '{}\n{} Warning(s). {} Error(s).'.format(
            exception_msg, len(warnings['warning']),
            len(warnings['exception']))

    @classmethod
    def exception_msg(cls, exceptions):
        exception_msg = '\n'.join(
            cls.__format_msg('Error', ex) for ex in exceptions['exception'])
        return exception_msg

    @classmethod
    def warning_msg(cls, warnings):
        warning_msg = '\n'.join(
            cls.__format_msg('Warning', warning)
            for warning in warnings['warning'])
        return warning_msg

    @staticmethod
    def __format_msg(msg_type, msg):
        msg_str = "{}: {}".format(msg_type, msg)
        return msg_str
